#!/usr/bin/env python3
"""
Read BME280 sensor data
Temperature, Humidity, Pressure
Pure Python I2C implementation
"""

import os
import fcntl
import time
import struct

I2C_SLAVE = 0x0703
BME280_ADDR = 0x76

# BME280 registers
REG_ID = 0xD0
REG_CTRL_HUM = 0xF2
REG_CTRL_MEAS = 0xF4
REG_CONFIG = 0xF5
REG_DATA = 0xF7

def read_byte(fd, reg):
    """Read single byte from register"""
    os.write(fd, bytes([reg]))
    return ord(os.read(fd, 1))

def read_bytes(fd, reg, length):
    """Read multiple bytes from register"""
    os.write(fd, bytes([reg]))
    return os.read(fd, length)

def write_byte(fd, reg, value):
    """Write byte to register"""
    os.write(fd, bytes([reg, value]))

def init_bme280(fd):
    """Initialize BME280 sensor"""
    # Check chip ID (should be 0x60)
    chip_id = read_byte(fd, REG_ID)
    print(f"BME280 Chip ID: 0x{chip_id:02X} (should be 0x60)")
    
    if chip_id != 0x60:
        print("⚠️  Warning: Unexpected chip ID")
        return False
    
    # Configure humidity oversampling (osrs_h = 1)
    write_byte(fd, REG_CTRL_HUM, 0x01)
    
    # Configure temp & pressure oversampling, normal mode
    # osrs_t=1, osrs_p=1, mode=11 (normal)
    write_byte(fd, REG_CTRL_MEAS, 0x27)
    
    # Configure standby time and filter
    write_byte(fd, REG_CONFIG, 0xA0)
    
    time.sleep(0.1)  # Wait for first measurement
    
    return True

def read_calibration(fd):
    """Read calibration parameters"""
    # Read temperature calibration
    cal = {}
    
    # Temp coefficients
    data = read_bytes(fd, 0x88, 6)
    cal['T1'] = struct.unpack('<H', data[0:2])[0]
    cal['T2'] = struct.unpack('<h', data[2:4])[0]
    cal['T3'] = struct.unpack('<h', data[4:6])[0]
    
    # Pressure coefficients
    data = read_bytes(fd, 0x8E, 18)
    cal['P1'] = struct.unpack('<H', data[0:2])[0]
    cal['P2'] = struct.unpack('<h', data[2:4])[0]
    cal['P3'] = struct.unpack('<h', data[4:6])[0]
    cal['P4'] = struct.unpack('<h', data[6:8])[0]
    cal['P5'] = struct.unpack('<h', data[8:10])[0]
    cal['P6'] = struct.unpack('<h', data[10:12])[0]
    cal['P7'] = struct.unpack('<h', data[12:14])[0]
    cal['P8'] = struct.unpack('<h', data[14:16])[0]
    cal['P9'] = struct.unpack('<h', data[16:18])[0]
    
    # Humidity coefficients
    cal['H1'] = read_byte(fd, 0xA1)
    data = read_bytes(fd, 0xE1, 7)
    cal['H2'] = struct.unpack('<h', data[0:2])[0]
    cal['H3'] = data[2]
    cal['H4'] = (data[3] << 4) | (data[4] & 0x0F)
    cal['H5'] = (data[5] << 4) | (data[4] >> 4)
    cal['H6'] = struct.unpack('<b', bytes([data[6]]))[0]
    
    return cal

def compensate_temperature(adc_T, cal):
    """Calculate temperature from raw ADC value"""
    var1 = ((adc_T >> 3) - (cal['T1'] << 1)) * cal['T2'] >> 11
    var2 = (((adc_T >> 4) - cal['T1']) * ((adc_T >> 4) - cal['T1']) >> 12) * cal['T3'] >> 14
    t_fine = var1 + var2
    temperature = (t_fine * 5 + 128) >> 8
    return temperature / 100.0, t_fine

def compensate_pressure(adc_P, t_fine, cal):
    """Calculate pressure from raw ADC value"""
    var1 = t_fine - 128000
    var2 = var1 * var1 * cal['P6']
    var2 = var2 + ((var1 * cal['P5']) << 17)
    var2 = var2 + (cal['P4'] << 35)
    var1 = ((var1 * var1 * cal['P3']) >> 8) + ((var1 * cal['P2']) << 12)
    var1 = ((1 << 47) + var1) * cal['P1'] >> 33
    
    if var1 == 0:
        return 0
    
    p = 1048576 - adc_P
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (cal['P9'] * (p >> 13) * (p >> 13)) >> 25
    var2 = (cal['P8'] * p) >> 19
    pressure = ((p + var1 + var2) >> 8) + (cal['P7'] << 4)
    
    return pressure / 256.0 / 100.0  # Convert to hPa

def compensate_humidity(adc_H, t_fine, cal):
    """Calculate humidity from raw ADC value"""
    v_x1_u32r = t_fine - 76800
    v_x1_u32r = (((((adc_H << 14) - (cal['H4'] << 20) - (cal['H5'] * v_x1_u32r)) + 
                   16384) >> 15) * (((((((v_x1_u32r * cal['H6']) >> 10) * 
                   (((v_x1_u32r * cal['H3']) >> 11) + 32768)) >> 10) + 2097152) * 
                   cal['H2'] + 8192) >> 14))
    
    v_x1_u32r = v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * 
                              cal['H1']) >> 4)
    v_x1_u32r = max(0, min(419430400, v_x1_u32r))
    
    return (v_x1_u32r >> 12) / 1024.0

def read_sensor_data(fd, cal):
    """Read and compensate all sensor data"""
    # Read all data registers (0xF7 to 0xFE)
    data = read_bytes(fd, REG_DATA, 8)
    
    # Extract raw ADC values
    adc_P = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    adc_H = (data[6] << 8) | data[7]
    
    # Compensate values
    temperature, t_fine = compensate_temperature(adc_T, cal)
    pressure = compensate_pressure(adc_P, t_fine, cal)
    humidity = compensate_humidity(adc_H, t_fine, cal)
    
    return temperature, pressure, humidity

def main():
    try:
        fd = os.open('/dev/i2c-1', os.O_RDWR)
        fcntl.ioctl(fd, I2C_SLAVE, BME280_ADDR)
        
        print("=" * 50)
        print("  BME280 Sensor Test")
        print("  Temperature, Humidity, Pressure")
        print("=" * 50)
        
        if not init_bme280(fd):
            print("Failed to initialize BME280")
            return
        
        print("✅ BME280 initialized successfully!\n")
        
        # Read calibration data
        print("Reading calibration data...")
        cal = read_calibration(fd)
        print("✅ Calibration loaded\n")
        
        # Read sensor data continuously
        print("Reading sensor data (Ctrl+C to stop)...\n")
        
        try:
            while True:
                temp, pressure, humidity = read_sensor_data(fd, cal)
                
                print(f"\r🌡️  Temp: {temp:6.2f}°C  |  "
                      f"💧 Humidity: {humidity:5.1f}%  |  "
                      f"🌍 Pressure: {pressure:7.2f} hPa", end='')
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n✅ Sensor test complete!")
        
        os.close(fd)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
