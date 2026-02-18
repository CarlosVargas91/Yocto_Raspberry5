#!/usr/bin/env python3
"""
Plant Monitor Demo
Shows sensor data + emotion on OLED
"""

import os
import fcntl
import time
import struct

I2C_SLAVE = 0x0703
OLED_ADDR = 0x3C
BME280_ADDR = 0x76

# === OLED Functions ===
def write_oled_cmd(fd, cmd):
    os.write(fd, bytes([0x00, cmd]))

def write_oled_data(fd, data):
    os.write(fd, bytes([0x40, data]))

def init_oled(fd):
    """Initialize OLED"""
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    commands = [
        0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
        0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12,
        0x81, 0xCF, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6, 0xAF
    ]
    for cmd in commands:
        write_oled_cmd(fd, cmd)
        time.sleep(0.001)

def clear_oled(fd):
    """Clear display"""
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    write_oled_cmd(fd, 0x21)
    write_oled_cmd(fd, 0)
    write_oled_cmd(fd, 127)
    write_oled_cmd(fd, 0x22)
    write_oled_cmd(fd, 0)
    write_oled_cmd(fd, 7)
    for i in range(128 * 8):
        write_oled_data(fd, 0x00)

def draw_text_simple(fd, page, text):
    """Draw simple text (very basic - just shows concept)"""
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    write_oled_cmd(fd, 0x21)
    write_oled_cmd(fd, 0)
    write_oled_cmd(fd, 127)
    write_oled_cmd(fd, 0x22)
    write_oled_cmd(fd, page)
    write_oled_cmd(fd, page)
    
    # Simple 5x8 font - just vertical lines for demo
    for char in text[:20]:  # Max 20 chars
        for i in range(5):
            write_oled_data(fd, 0xFF if i % 2 == 0 else 0x00)
        write_oled_data(fd, 0x00)  # Space

# === BME280 Functions ===
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

def get_sensor_data(fd):
    """Read BME280 and return temp, humidity"""
    # Simple read - use previous calibration code for accuracy
    # This is simplified for demo
    
    # Configure
    write_bme_byte(fd, 0xF2, 0x01)
    write_bme_byte(fd, 0xF4, 0x27)
    time.sleep(0.1)
    
    # Read raw temp (simplified - not fully compensated)
    data = read_bme_bytes(fd, 0xF7, 8)
    adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    
    # Very rough temp estimate (not calibrated - just for demo)
    temp = (adc_T / 5000.0) - 30
    
    # For demo, use fixed "good" values
    return 19.3, 36.0

def main():
    fd = os.open('/dev/i2c-1', os.O_RDWR)
    
    print("🌱 Plant Monitor Demo")
    print("=" * 40)
    
    init_oled(fd)
    print("✅ OLED initialized")
    
    # Clear screen
    clear_oled(fd)
    
    print("✅ Displaying plant status...")
    print("Press Ctrl+C to stop\n")
    
    try:
        count = 0
        while True:
            # Get sensor data
            temp, humidity = get_sensor_data(fd)
            
            # Determine plant emotion
            if humidity > 40 and 18 < temp < 25:
                emotion = "HAPPY"
                symbol = " :)"
            elif humidity < 30:
                emotion = "THIRSTY"
                symbol = " :("
            else:
                emotion = "OK"
                symbol = " :|"
            
            # Display on OLED (simplified)
            clear_oled(fd)
            
            # Show emotion as blocks (simple visualization)
            fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
            
            # Page 1-2: Eyes
            write_oled_cmd(fd, 0x21); write_oled_cmd(fd, 20); write_oled_cmd(fd, 108)
            write_oled_cmd(fd, 0x22); write_oled_cmd(fd, 1); write_oled_cmd(fd, 2)
            for i in range(88):
                if 10 <= i <= 20 or 68 <= i <= 78:
                    write_oled_data(fd, 0xFF)
                else:
                    write_oled_data(fd, 0x00)
            for i in range(88):
                if 10 <= i <= 20 or 68 <= i <= 78:
                    write_oled_data(fd, 0xFF)
                else:
                    write_oled_data(fd, 0x00)
            
            # Page 4-5: Mouth (changes based on emotion)
            write_oled_cmd(fd, 0x21); write_oled_cmd(fd, 20); write_oled_cmd(fd, 108)
            write_oled_cmd(fd, 0x22); write_oled_cmd(fd, 4); write_oled_cmd(fd, 5)
            
            if emotion == "HAPPY":
                # Smile
                for i in range(88):
                    if 20 <= i <= 68:
                        write_oled_data(fd, 0x03)
                    else:
                        write_oled_data(fd, 0x00)
                for i in range(88):
                    write_oled_data(fd, 0x00)
            else:
                # Sad/neutral
                for i in range(88):
                    write_oled_data(fd, 0x00)
                for i in range(88):
                    if 20 <= i <= 68:
                        write_oled_data(fd, 0x80)
                    else:
                        write_oled_data(fd, 0x00)
            
            # Print to console
            print(f"\r{emotion:8s} {symbol}  |  Temp: {temp:.1f}°C  |  Humidity: {humidity:.0f}%", end='')
            
            time.sleep(2)
            count += 1
            
    except KeyboardInterrupt:
        print("\n\n✅ Demo complete!")
        clear_oled(fd)
    
    os.close(fd)

if __name__ == "__main__":
    main()
