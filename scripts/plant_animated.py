#!/usr/bin/env python3
"""
Plant Monitor with Animated Display
Alternates between expressive face and sensor data
"""

import os
import fcntl
import time
import struct
import spidev
from emotion_faces_fixed import HAPPY_FACE, SAD_FACE, NEUTRAL_FACE
from oled_graphics import FONT_5x7
from sensor_icons import ICON_TEMP, ICON_HUMIDITY, ICON_LIGHT, ICON_SOIL

I2C_SLAVE = 0x0703
OLED_ADDR = 0x3C
BME280_ADDR = 0x76
BH1750_ADDR = 0x23

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# === OLED Functions ===
def oled_cmd(fd, cmd):
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    os.write(fd, bytes([0x00, cmd]))

def oled_data(fd, data):
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    os.write(fd, bytes([0x40, data]))

def init_oled(fd):
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    for cmd in [0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
                0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12,
                0x81, 0xCF, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6, 0xAF]:
        oled_cmd(fd, cmd)

def clear_oled(fd):
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    oled_cmd(fd, 0x21); oled_cmd(fd, 0); oled_cmd(fd, 127)
    oled_cmd(fd, 0x22); oled_cmd(fd, 0); oled_cmd(fd, 7)
    for _ in range(128 * 8):
        oled_data(fd, 0x00)

def display_bitmap(fd, bitmap):
    """Display full-screen bitmap"""
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    oled_cmd(fd, 0x21); oled_cmd(fd, 0); oled_cmd(fd, 127)
    oled_cmd(fd, 0x22); oled_cmd(fd, 0); oled_cmd(fd, 7)
    for byte in bitmap:
        oled_data(fd, byte)

def draw_text(fd, text, x, page):
    """Draw text at position"""
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    oled_cmd(fd, 0x21); oled_cmd(fd, x); oled_cmd(fd, 127)
    oled_cmd(fd, 0x22); oled_cmd(fd, page); oled_cmd(fd, page)
    
    for char in text:
        if char in FONT_5x7:
            for byte in FONT_5x7[char]:
                oled_data(fd, byte)
            oled_data(fd, 0x00)

def draw_icon(fd, icon, x, page):
    """Draw 16x16 icon"""
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    oled_cmd(fd, 0x21); oled_cmd(fd, x); oled_cmd(fd, x + 15)
    oled_cmd(fd, 0x22); oled_cmd(fd, page); oled_cmd(fd, page)
    for byte in icon:
        oled_data(fd, byte)

def display_sensors(fd, temp, humidity, light, soil):
    """Display sensor data with icons"""
    clear_oled(fd)
    
    # Temperature with icon
    draw_icon(fd, ICON_TEMP, 0, 1)
    draw_text(fd, f"{int(temp)}C", 20, 1)
    
    # Humidity with icon
    draw_icon(fd, ICON_HUMIDITY, 0, 3)
    draw_text(fd, f"{int(humidity)}%", 20, 3)
    
    # Light with icon  
    draw_icon(fd, ICON_LIGHT, 0, 5)
    draw_text(fd, f"{int(light)}", 20, 5)
    
    # Soil with icon (most important!)
    draw_icon(fd, ICON_SOIL, 70, 1)
    draw_text(fd, f"SOIL", 90, 1)
    draw_text(fd, f"{int(soil)}%", 90, 2)
    
    # Big progress bar for soil
    bar_len = int(soil * 1.1)
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    oled_cmd(fd, 0x21); oled_cmd(fd, 70); oled_cmd(fd, 127)
    oled_cmd(fd, 0x22); oled_cmd(fd, 4); oled_cmd(fd, 5)
    for _ in range(2):  # 2 pages tall
        for i in range(58):
            oled_data(fd, 0xFF if i < bar_len else 0x00)

# [Include all BME280, BH1750, soil sensor functions from previous script]
# (Copying them here for completeness)

def read_bme_byte(fd, reg):
    fcntl.ioctl(fd, I2C_SLAVE, BME280_ADDR)
    os.write(fd, bytes([reg]))
    time.sleep(0.01)
    return ord(os.read(fd, 1))

def read_bme_bytes(fd, reg, length):
    fcntl.ioctl(fd, I2C_SLAVE, BME280_ADDR)
    os.write(fd, bytes([reg]))
    time.sleep(0.01)
    return os.read(fd, length)

def write_bme_byte(fd, reg, value):
    fcntl.ioctl(fd, I2C_SLAVE, BME280_ADDR)
    os.write(fd, bytes([reg, value]))

def read_bme_calibration(fd):
    cal = {}
    data = read_bme_bytes(fd, 0x88, 6)
    cal['T1'] = struct.unpack('<H', data[0:2])[0]
    cal['T2'] = struct.unpack('<h', data[2:4])[0]
    cal['T3'] = struct.unpack('<h', data[4:6])[0]
    data = read_bme_bytes(fd, 0x8E, 18)
    cal['P1'] = struct.unpack('<H', data[0:2])[0]
    cal['P2'] = struct.unpack('<h', data[2:4])[0]
    cal['P3'] = struct.unpack('<h', data[4:6])[0]
    cal['P4'] = struct.unpack('<h', data[6:8])[0]
    cal['P5'] = struct.unpack('<h', data[8:10])[0]
    cal['P6'] = struct.unpack('<h', data[10:12])[0]
    cal['P7'] = struct.unpack('<h', data[12:14])[0]
    cal['P8'] = struct.unpack('<h', data[14:16])[0]
    cal['P9'] = struct.unpack('<h', data[16:18])[0]
    cal['H1'] = read_bme_byte(fd, 0xA1)
    data = read_bme_bytes(fd, 0xE1, 7)
    cal['H2'] = struct.unpack('<h', data[0:2])[0]
    cal['H3'] = data[2]
    cal['H4'] = (data[3] << 4) | (data[4] & 0x0F)
    cal['H5'] = (data[5] << 4) | (data[4] >> 4)
    cal['H6'] = struct.unpack('<b', bytes([data[6]]))[0]
    return cal

def compensate_temperature(adc_T, cal):
    var1 = ((adc_T >> 3) - (cal['T1'] << 1)) * cal['T2'] >> 11
    var2 = (((adc_T >> 4) - cal['T1']) * ((adc_T >> 4) - cal['T1']) >> 12) * cal['T3'] >> 14
    t_fine = var1 + var2
    temperature = (t_fine * 5 + 128) >> 8
    return temperature / 100.0, t_fine

def compensate_humidity(adc_H, t_fine, cal):
    v_x1_u32r = t_fine - 76800
    v_x1_u32r = (((((adc_H << 14) - (cal['H4'] << 20) - (cal['H5'] * v_x1_u32r)) + 
                   16384) >> 15) * (((((((v_x1_u32r * cal['H6']) >> 10) * 
                   (((v_x1_u32r * cal['H3']) >> 11) + 32768)) >> 10) + 2097152) * 
                   cal['H2'] + 8192) >> 14))
    v_x1_u32r = v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * 
                              cal['H1']) >> 4)
    v_x1_u32r = max(0, min(419430400, v_x1_u32r))
    return (v_x1_u32r >> 12) / 1024.0

def init_bme280(fd):
    write_bme_byte(fd, 0xF2, 0x01)
    write_bme_byte(fd, 0xF4, 0x27)
    time.sleep(0.1)
    return read_bme_calibration(fd)

def read_bme280_calibrated(fd, cal):
    data = read_bme_bytes(fd, 0xF7, 8)
    adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    adc_H = (data[6] << 8) | data[7]
    temperature, t_fine = compensate_temperature(adc_T, cal)
    humidity = compensate_humidity(adc_H, t_fine, cal)
    return temperature, humidity

def init_bh1750(fd):
    fcntl.ioctl(fd, I2C_SLAVE, BH1750_ADDR)
    os.write(fd, bytes([0x01]))
    time.sleep(0.01)
    os.write(fd, bytes([0x10]))
    time.sleep(0.2)

def read_bh1750(fd):
    fcntl.ioctl(fd, I2C_SLAVE, BH1750_ADDR)
    data = os.read(fd, 2)
    raw = struct.unpack('>H', data)[0]
    return raw / 1.2

def read_soil_moisture():
    adc = spi.xfer2([1, (8 + 0) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    moisture_percent = 100 - ((data / 1023.0) * 100)
    return moisture_percent

def evaluate_plant_health(temp, humidity, light, soil):
    issues = []
    if temp < 15:
        issues.append("too cold")
    elif temp > 28:
        issues.append("too hot")
    if humidity < 30:
        issues.append("air dry")
    elif humidity > 70:
        issues.append("air humid")
    if light < 100:
        issues.append("dark")
    if soil < 20:
        issues.append("needs water!")
    elif soil < 40:
        issues.append("soil dry")
    
    if len(issues) == 0:
        return "happy", "😊"
    elif len(issues) == 1 or (len(issues) == 2 and "soil dry" not in issues):
        return "neutral", "😐"
    else:
        return "sad", "😢"

def main():
    fd = os.open('/dev/i2c-1', os.O_RDWR)
    
    print("🌱" * 30)
    print("  ANIMATED PLANT MONITOR")
    print("🌱" * 30)
    
    init_oled(fd)
    bme_cal = init_bme280(fd)
    init_bh1750(fd)
    print("✅ All sensors initialized\n")
    
    show_face = True  # Alternate between face and data
    
    try:
        while True:
            # Read sensors
            temp, humidity = read_bme280_calibrated(fd, bme_cal)
            light = read_bh1750(fd)
            soil = read_soil_moisture()
            emotion, emoji = evaluate_plant_health(temp, humidity, light, soil)
            
            if show_face:
                # Show big expressive face
                if emotion == "happy":
                    display_bitmap(fd, HAPPY_FACE)
                elif emotion == "sad":
                    display_bitmap(fd, SAD_FACE)
                else:
                    display_bitmap(fd, NEUTRAL_FACE)
                print(f"{emoji} EMOTION FACE")
            else:
                # Show sensor data with icons
                display_sensors(fd, temp, humidity, light, soil)
                print(f"📊 DATA: T:{temp:.1f}°C H:{humidity:.0f}% L:{light:.0f}lux S:{soil:.0f}%")
            
            show_face = not show_face
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n✅ Monitor stopped")
        clear_oled(fd)
        spi.close()
    
    os.close(fd)

if __name__ == "__main__":
    main()
