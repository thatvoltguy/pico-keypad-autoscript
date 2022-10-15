"""
Stripped down and modified version of 
https://github.com/martinohanlon/pico-rgbkeypad/blob/main/rgbkeypad/rgbkeypad.py
for this project
"""

import board
import busio
import digitalio
import time

PIN_SDA = board.GP4
PIN_SCL = board.GP5
PIN_CS = board.GP17
PIN_SCK = board.GP18
PIN_MOSI = board.GP19

def colorwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

class RGBKeypad():
    
    KEYPAD_ADDRESS = 32
    def __init__(self, color=(0,0,0), brightness=0.05, auto_update=False):
        self._i2c = busio.I2C(scl=PIN_SCL, sda=PIN_SDA, frequency=400000)
        self._i2c.try_lock()
        self._spi = busio.SPI(clock=PIN_SCK, MOSI=PIN_MOSI)
        self._spi.try_lock()
        self._spi.configure(baudrate=4*1024*1024)
        self._cs = digitalio.DigitalInOut(PIN_CS)
        self._cs.direction = digitalio.Direction.OUTPUT
        self._cs.value = True
        self._color = color
        self._brightness = brightness
        self.last_led_data = bytearray((16*4) + 8)
    
    def read_keys(self):
        self._i2c.writeto(RGBKeypad.KEYPAD_ADDRESS, bytearray(1))
        data = bytearray(2)
        self._i2c.readfrom_into(RGBKeypad.KEYPAD_ADDRESS, data)
        return data

    def get_keys_pressed(self):
        data = self.read_keys()
        button_data = int.from_bytes(data, "little")
        button_states = []
        for button in range(16):
            button_states.append(0 == (button_data & (1<<button)))
        return button_states
    
    def is_pressed(self, pos):
        return self.get_keys_pressed()[pos]

    def write_leds(self, led_data):
        self._cs.value = False
        self.last_led_data
        self._spi.write(led_data)
        self._cs.value = True

    def color_keypad(self, r, g, b, brightness = 0.05):
        led_data = bytearray((16*4) + 8)
        data_pos = 4
        for key in range(16):
            led_data[data_pos] = int(255 - 31 + (31 * brightness))
            led_data[data_pos + 1] = b
            led_data[data_pos + 2] = g
            led_data[data_pos + 3] = r
            data_pos += 4
        self.last_led_data = led_data
        self.write_leds(led_data)
    
    def color_key(self, r, g, b, button = None, brightness = 0.05):
        led_data = bytearray((16*4) + 8)
        data_pos = 4
        for key in range(16):
            led_data[data_pos] = int(255 - 31 + (31 * brightness))
            led_data[data_pos + 1] = b if key == button else 0 
            led_data[data_pos + 2] = g if key == button else 0
            led_data[data_pos + 3] = r if key == button else 0
            data_pos += 4
        self.write_leds(led_data)
    
    def keypad_cycle(self, pos):
        color = colorwheel(pos)
        self.color_keypad(*color)
        time.sleep(0.1)