#!/usr/bin/env python3
"""
Scan I2C bus for connected devices
No external libraries needed - uses ioctl directly
"""

import os
import fcntl

I2C_SLAVE = 0x0703  # ioctl command

def scan_i2c_bus(bus=1):
    """Scan I2C bus for devices"""
    devices_found = []
    
    try:
        fd = os.open(f'/dev/i2c-{bus}', os.O_RDWR)
        
        print(f"Scanning I2C bus {bus}...")
        print("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")
        
        for addr in range(0x03, 0x78):
            try:
                fcntl.ioctl(fd, I2C_SLAVE, addr)
                # Try to read 1 byte
                os.read(fd, 1)
                devices_found.append(addr)
                print(f"{addr:02x} ", end='')
            except:
                print("-- ", end='')
            
            if (addr + 1) % 16 == 0:
                print()
        
        os.close(fd)
        
        print(f"\nDevices found at addresses: {[hex(d) for d in devices_found]}")
        return devices_found
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    scan_i2c_bus(1)
