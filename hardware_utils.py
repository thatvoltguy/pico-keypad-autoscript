import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode
import rgb_keybad
import random

DELAY = 0.25
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
web_site = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com", "https://www.hulu.com", "https://www.disneyplus.com", "https://www.netflix.com"]

def open_website(k, pos):
    k.color_keypad(0,0,0)
    k.color_key(0,255,0, button=pos)
    try:
        keyboard.press(Keycode.GUI, Keycode.SPACE)
        keyboard.release_all()
        time.sleep(0.5)
        keyboard_layout.write("terminal\n")
        time.sleep(0.5)
        keyboard_layout.write("open -a \"Google Chrome\" " + web_site[pos]+"\n")
    except Exception as e:
        k.color_key(255,0,0, button=pos)
        time.sleep(0.5)
    k.color_keypad(0,0,0)

def jiggle_mouse(k, button_pos):
    pos = 0
    timer_count = 0
    cont = True
    k.color_keypad(0,0,0)
    while cont:
        if k.is_pressed(button_pos):
            while k.is_pressed(button_pos):
                pass
            break
        curr_color = rgb_keybad.colorwheel(pos)
        k.color_key(*curr_color, button=button_pos)
        pos += 1
        pos = pos % 255
        
        #((60 min/sec * 4(0.25s) * 1) = 1 min
        if timer_count == ((60 * 4) * 10) or timer_count == 0:
            x_or_y = random.randint(0, 1)
            if x_or_y == 1:
                mouse.move(x=random.randint(-400, 400))
            else:
                mouse.move(y=random.randint(-400, 400))
            timer_count = 1
        timer_count += 1
        time.sleep(DELAY)
    k.color_keypad(0,0,0)


