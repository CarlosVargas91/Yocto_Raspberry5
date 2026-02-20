#!/usr/bin/env python3
"""
Test Soil Moisture Sensor via MCP3008
Channel 0
"""

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_soil_moisture():
    """Read soil sensor on CH0, return percentage"""
    # Read MCP3008 channel 0
    adc = spi.xfer2([1, (8 + 0) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    
    # Convert to percentage (calibration needed!)
    # Typical: 0 = very wet, 1023 = very dry
    # We'll invert so 100% = wet, 0% = dry
    moisture_percent = 100 - ((data / 1023.0) * 100)
    
    return data, moisture_percent

print("=" * 60)
print("  Soil Moisture Sensor Test")
print("  Try touching sensor or putting in water/soil!")
print("=" * 60)

try:
    while True:
        raw, moisture = read_soil_moisture()
        
        # Determine status
        if moisture > 70:
            status = "💧 VERY WET"
        elif moisture > 50:
            status = "💦 WET"
        elif moisture > 30:
            status = "😐 MOIST"
        elif moisture > 15:
            status = "🌵 DRY"
        else:
            status = "🔥 VERY DRY"
        
        # Progress bar
        bar_length = int(moisture / 2)
        bar = "█" * bar_length
        
        print(f"\rRaw: {raw:4d} | Moisture: {moisture:5.1f}% | {status:15s} | {bar:50s}", end='')
        
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("\n\n✅ Soil sensor test complete!")
    spi.close()
