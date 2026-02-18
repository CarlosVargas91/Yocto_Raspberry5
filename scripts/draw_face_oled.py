#!/usr/bin/env python3
"""
Draw emotion faces on SSD1306 OLED
128x64 display - Plant Monitor
"""

import os
import fcntl
import time

I2C_SLAVE = 0x0703
OLED_ADDR = 0x3C

def write_command(fd, cmd):
    os.write(fd, bytes([0x00, cmd]))

def write_data(fd, data):
    os.write(fd, bytes([0x40, data]))

def clear_display(fd):
    """Clear entire display"""
    write_command(fd, 0x21)  # Column address
    write_command(fd, 0)
    write_command(fd, 127)
    write_command(fd, 0x22)  # Page address
    write_command(fd, 0)
    write_command(fd, 7)
    
    for i in range(128 * 8):
        write_data(fd, 0x00)

def draw_happy_face(fd):
    """Draw a happy face 😊"""
    clear_display(fd)
    
    # Create a simple 8x8 bitmap for eyes and mouth
    # Each byte represents 8 vertical pixels
    
    # Happy face pattern (centered on 128x64 display)
    # We'll draw in pages (8 pixel rows each)
    
    print("Drawing HAPPY FACE 😊")
    
    # Set position to center area
    write_command(fd, 0x21)  # Column start/end
    write_command(fd, 30)    # Start column
    write_command(fd, 100)   # End column
    write_command(fd, 0x22)  # Page start/end
    write_command(fd, 2)     # Start page
    write_command(fd, 5)     # End page
    
    # Simple pattern: Draw rectangles for eyes and smile
    # Page 2: Eyes
    for col in range(71):
        if 10 <= col <= 20:  # Left eye
            write_data(fd, 0xFF)
        elif 50 <= col <= 60:  # Right eye
            write_data(fd, 0xFF)
        else:
            write_data(fd, 0x00)
    
    # Page 3: More eyes
    for col in range(71):
        if 10 <= col <= 20 or 50 <= col <= 60:
            write_data(fd, 0xFF)
        else:
            write_data(fd, 0x00)
    
    # Page 4: Smile curve (simplified)
    for col in range(71):
        if 15 <= col <= 55:  # Smile line
            write_data(fd, 0x01)  # Bottom pixel
        else:
            write_data(fd, 0x00)
    
    # Page 5: Bottom of smile
    for col in range(71):
        if col == 15 or col == 55:  # Smile edges curve up
            write_data(fd, 0x80)
        else:
            write_data(fd, 0x00)

def draw_sad_face(fd):
    """Draw a sad face 😢"""
    clear_display(fd)
    
    print("Drawing SAD FACE 😢")
    
    write_command(fd, 0x21)
    write_command(fd, 30)
    write_command(fd, 100)
    write_command(fd, 0x22)
    write_command(fd, 2)
    write_command(fd, 5)
    
    # Eyes (same as happy)
    for col in range(71):
        if 10 <= col <= 20 or 50 <= col <= 60:
            write_data(fd, 0xFF)
        else:
            write_data(fd, 0x00)
    
    for col in range(71):
        if 10 <= col <= 20 or 50 <= col <= 60:
            write_data(fd, 0xFF)
        else:
            write_data(fd, 0x00)
    
    # Sad mouth (inverted smile) - top part
    for col in range(71):
        if col == 15 or col == 55:
            write_data(fd, 0x01)
        else:
            write_data(fd, 0x00)
    
    # Sad mouth - bottom curve
    for col in range(71):
        if 15 <= col <= 55:
            write_data(fd, 0x80)
        else:
            write_data(fd, 0x00)

def init_oled():
    """Initialize OLED"""
    fd = os.open('/dev/i2c-1', os.O_RDWR)
    fcntl.ioctl(fd, I2C_SLAVE, OLED_ADDR)
    
    commands = [
        0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
        0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12,
        0x81, 0xCF, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6, 0xAF
    ]
    
    for cmd in commands:
        write_command(fd, cmd)
        time.sleep(0.001)
    
    return fd

def main():
    fd = init_oled()
    
    print("\n🌱 Plant Emotion Display Test")
    print("=" * 40)
    
    # Show happy face
    draw_happy_face(fd)
    print("Display shows: HAPPY 😊")
    time.sleep(3)
    
    # Show sad face
    draw_sad_face(fd)
    print("Display shows: SAD 😢")
    time.sleep(3)
    
    # Alternate between emotions
    print("\nAlternating emotions...")
    for i in range(3):
        draw_happy_face(fd)
        time.sleep(1.5)
        draw_sad_face(fd)
        time.sleep(1.5)
    
    # Clear and finish
    clear_display(fd)
    print("\n✅ Emotion display test complete!")
    
    os.close(fd)

if __name__ == "__main__":
    main()
