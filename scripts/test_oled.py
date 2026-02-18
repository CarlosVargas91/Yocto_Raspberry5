#!/usr/bin/env python3
"""
Full SSD1306 OLED initialization and test
128x64 display
"""

import os
import fcntl
import time

I2C_SLAVE = 0x0703
OLED_ADDR = 0x3C

def write_command(fd, cmd):
    """Write command to OLED"""
    os.write(fd, bytes([0x00, cmd]))

def write_data(fd, data):
    """Write data to OLED"""
    os.write(fd, bytes([0x40, data]))

def init_oled_full():
    """Complete SSD1306 initialization"""
    try:
        fd = os.open('/dev/i2c-1', os.O_RDWR)
        fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
        
        print("Initializing SSD1306 OLED (128x64)...")
        
        # Complete initialization sequence for SSD1306
        commands = [
            0xAE,       # Display OFF
            0xD5, 0x80, # Set display clock divide ratio/oscillator frequency
            0xA8, 0x3F, # Set multiplex ratio (1 to 64)
            0xD3, 0x00, # Set display offset (0)
            0x40,       # Set display start line to 0
            0x8D, 0x14, # Charge pump setting (enable)
            0x20, 0x00, # Memory addressing mode (horizontal)
            0xA1,       # Set segment re-map (A0/A1)
            0xC8,       # Set COM output scan direction
            0xDA, 0x12, # Set COM pins hardware configuration
            0x81, 0xCF, # Set contrast control
            0xD9, 0xF1, # Set pre-charge period
            0xDB, 0x40, # Set VCOMH deselect level
            0xA4,       # Resume to RAM content display
            0xA6,       # Set normal display (not inverted)
            0xAF,       # Display ON
        ]
        
        for cmd in commands:
            write_command(fd, cmd)
            time.sleep(0.001)
        
        print("✅ OLED fully initialized!")
        
        # Clear display (fill with black)
        print("Clearing display...")
        write_command(fd, 0x21)  # Set column address
        write_command(fd, 0)     # Column start
        write_command(fd, 127)   # Column end
        write_command(fd, 0x22)  # Set page address
        write_command(fd, 0)     # Page start
        write_command(fd, 7)     # Page end
        
        # Write 1024 bytes of 0x00 (clear screen)
        for i in range(128 * 8):  # 128 columns x 8 pages
            write_data(fd, 0x00)
        
        print("✅ Display cleared!")
        time.sleep(1)
        
        # Draw test pattern (fill screen with 0xFF)
        print("Drawing test pattern (all white)...")
        write_command(fd, 0x21)  # Set column address
        write_command(fd, 0)
        write_command(fd, 127)
        write_command(fd, 0x22)  # Set page address
        write_command(fd, 0)
        write_command(fd, 7)
        
        for i in range(128 * 8):
            write_data(fd, 0xFF)
        
        print("✅ You should see a FULLY WHITE screen now!")
        time.sleep(2)
        
        # Clear again
        print("Clearing display again...")
        write_command(fd, 0x21)
        write_command(fd, 0)
        write_command(fd, 127)
        write_command(fd, 0x22)
        write_command(fd, 0)
        write_command(fd, 7)
        
        for i in range(128 * 8):
            write_data(fd, 0x00)
        
        print("✅ Display should be black/off now")
        
        os.close(fd)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_oled_full()
