import rgb_keybad
import hardware_utils

pos = 0
k = rgb_keybad.RGBKeypad()
k.color_keypad(0,0,0)

while True:
    keys = k.get_keys_pressed()
    for button_pos in range(len(keys)):
        if k.is_pressed(button_pos):
            while k.is_pressed(button_pos):
                pass
            if  button_pos == 15:
                hardware_utils.jiggle_mouse(k, button_pos)
            if  button_pos < 15:
                hardware_utils.open_website(k, button_pos)
    k.keypad_cycle(pos)
    pos += 1
    pos = pos % 255