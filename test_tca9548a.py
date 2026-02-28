from machine import I2C, Pin
from time import sleep

# Initialize I2C (change pins if required)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

TCA_ADDR = 0x70   # Default TCA9548A address

def select_channel(channel):
    """
    Select TCA9548A channel (0-7)
    """
    if 0 <= channel <= 7:
        i2c.writeto(TCA_ADDR, bytes([1 << channel]))
    else:
        print("Invalid channel")

def disable_all_channels():
    """
    Disable all channels
    """
    i2c.writeto(TCA_ADDR, b'\x00')

print("\n--- Global I2C Scan (No Channel Selected) ---")
devices = i2c.scan()
print("Found:", devices)

if TCA_ADDR in devices:
    print("TCA9548A detected at 0x70\n")
else:
    print("TCA9548A NOT detected. Check wiring.")
    raise SystemExit

print("--- Scanning All TCA Channels ---")

for ch in range(8):
    select_channel(ch)
    sleep(0.1)   # Small delay for stability
    devices = i2c.scan()
    
    # Remove TCA address from result if present
    devices = [d for d in devices if d != TCA_ADDR]
    
    print("Channel", ch, ":", devices)

disable_all_channels()
print("\nScan Complete.")