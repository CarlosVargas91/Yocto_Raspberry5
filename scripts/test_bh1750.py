#!/usr/bin/env python3
"""
Test BH1750 Light Sensor
Measures ambient light in lux
"""

import os
import fcntl
import time
import struct

I2C_SLAVE = 0x0703
BH1750_ADDR = 0x23

# BH1750 Commands
CMD_POWER_ON = 0x01
CMD_POWER_OFF = 0x00
CMD_RESET = 0x07
CMD_CONT_H_RES = 0x10  # Continuous High Resolution Mode (1 lux resolution)
CMD_CONT_H_RES2 = 0x11  # Continuous High Resolution Mode 2 (0.5 lux)
CMD_CONT_L_RES = 0x13  # Continuous Low Resolution Mode (4 lux)
CMD_ONE_H_RES = 0x20  # One Time High Resolution Mode
CMD_ONE_H_RES2 = 0x21  # One Time High Resolution Mode 2
CMD_ONE_L_RES = 0x23  # One Time Low Resolution Mode

def write_command(fd, cmd):
    """Send command to BH1750"""
    os.write(fd, bytes([cmd]))

def read_light(fd):
    """Read light level in lux"""
    # Read 2 bytes
    data = os.read(fd, 2)
    # Convert to lux (formula from datasheet)
    raw = struct.unpack('>H', data)[0]
    lux = raw / 1.2  # Default resolution
    return lux

def get_light_level_description(lux):
    """Human-readable light level"""
    if lux < 1:
        return "Very Dark 🌑", "Night"
    elif lux < 50:
        return "Dark 🌙", "Deep shade"
    elif lux < 200:
        return "Dim 💡", "Indoor evening"
    elif lux < 500:
        return "Indoor 🏠", "Normal room"
    elif lux < 1000:
        return "Bright 💡", "Well-lit office"
    elif lux < 10000:
        return "Very Bright ☀️", "Overcast day"
    elif lux < 30000:
        return "Daylight ☀️", "Full daylight"
    else:
        return "Brilliant ☀️☀️", "Direct sunlight"

def main():
    try:
        fd = os.open('/dev/i2c-1', os.O_RDWR)
        fcntl.ioctl(fd, I2C_SLAVE, BH1750_ADDR)
        
        print("=" * 60)
        print("  BH1750 Light Sensor Test")
        print("  Measuring Ambient Light")
        print("=" * 60)
        
        # Power on
        print("Powering on sensor...")
        write_command(fd, CMD_POWER_ON)
        time.sleep(0.01)
        
        # Reset
        print("Resetting sensor...")
        write_command(fd, CMD_RESET)
        time.sleep(0.01)
        
        # Start continuous high resolution measurement
        print("Starting continuous measurement (1 lux resolution)...")
        write_command(fd, CMD_CONT_H_RES)
        time.sleep(0.2)  # Wait for first measurement
        
        print("✅ BH1750 initialized!\n")
        print("Reading light levels (Ctrl+C to stop)...\n")
        
        try:
            while True:
                lux = read_light(fd)
                desc, situation = get_light_level_description(lux)
                
                # Create a simple bar graph
                bar_length = min(int(lux / 50), 50)
                bar = "█" * bar_length
                
                print(f"\r💡 {lux:8.1f} lux  |  {desc:20s} |  {situation:15s} | {bar:50s}", end='')
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n✅ Light sensor test complete!")
        
        # Power off
        write_command(fd, CMD_POWER_OFF)
        os.close(fd)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
