import json
import time
from pynput import keyboard, mouse

FPS = 20
FRAME_TIME = 1.0 / FPS

# Frame counter
frame_id = 0

# Currently held keys/buttons
held_keys = set()
held_mouse = set()

# Keys pressed THIS frame only
new_keys = set()
new_mouse = set()

# Mouse motion per frame
mouse_dx = 0.0
mouse_dy = 0.0
last_mouse_pos = None


def format_key(key):
    if key == keyboard.Key.space:
        return "key.keyboard.space"
    if key == keyboard.Key.caps_lock:
        return "key.keyboard.caps.lock"
    try:
        return f"key.keyboard.{key.char}"
    except AttributeError:
        return None


def on_press(key):
    global new_keys
    formatted = format_key(key)
    if formatted:
        if formatted not in held_keys:
            new_keys.add(formatted)
        held_keys.add(formatted)


def on_release(key):
    formatted = format_key(key)
    if formatted and formatted in held_keys:
        held_keys.remove(formatted)


def on_click(x, y, button, pressed):
    global new_mouse
    name = f"key.mouse.{button.name}"
    if pressed:
        if name not in held_mouse:
            new_mouse.add(name)
        held_mouse.add(name)
    else:
        if name in held_mouse:
            held_mouse.remove(name)


def on_move(x, y):
    global last_mouse_pos, mouse_dx, mouse_dy
    if last_mouse_pos is not None:
        mouse_dx += x - last_mouse_pos[0]
        mouse_dy += y - last_mouse_pos[1]
    last_mouse_pos = (x, y)


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

keyboard_listener.start()
mouse_listener.start()

with open("vpt_actions.jsonl", "w") as f:
    print("Recording VPT actions... Ctrl+C to stop.")
    try:
        while True:
            start = time.time()

            frame_id += 1

            action = {
                "frame": frame_id,  # 🔥 Frame counter added here
                "keyboard": {
                    "keys": sorted(list(held_keys)),
                    "newKeys": sorted(list(new_keys)),
                },
                "mouse": {
                    "dx": mouse_dx,
                    "dy": mouse_dy,
                    "buttons": sorted(list(held_mouse)),
                    "newButtons": sorted(list(new_mouse)),
                },
                "isGuiOpen": False,
                "hotbar": 0
            }

            f.write(json.dumps(action) + "\n")

            # Reset per-frame values
            new_keys.clear()
            new_mouse.clear()
            mouse_dx = 0.0
            mouse_dy = 0.0

            elapsed = time.time() - start
            time.sleep(max(0, FRAME_TIME - elapsed))

    except KeyboardInterrupt:
        print("Stopped recording.")