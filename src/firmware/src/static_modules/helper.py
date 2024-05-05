import time
import sys

def millis() -> int:
    return round(time.monotonic_ns() * 0.0000001)

def fmap(s, a1, a2, b1, b2) -> float:
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)

def imap(s, a1, a2, b1, b2) -> int:
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)

def has_wifi() -> bool:
    if 'Raspberry Pi Pico W' in str(sys.implementation._machine):
        return True
    return False


