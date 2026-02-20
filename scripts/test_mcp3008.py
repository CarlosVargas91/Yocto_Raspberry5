#!/usr/bin/env python3
"""
Test MCP3008 ADC communication
Read all 8 channels
"""

import spidev
import time

# Open SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CE0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    """Read MCP3008 channel (0-7)"""
    if channel < 0 or channel > 7:
        return -1
    
    # MCP3008 protocol: send 3 bytes, get 3 back
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

print("=" * 50)
print("  MCP3008 Test - Reading All Channels")
print("=" * 50)

try:
    while True:
        print("\r", end='')
        for ch in range(8):
            value = read_adc(ch)
            voltage = (value / 1023.0) * 3.3
            print(f"CH{ch}:{value:4d}({voltage:.2f}V) ", end='')
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("\n\n✅ MCP3008 test complete!")
    spi.close()
