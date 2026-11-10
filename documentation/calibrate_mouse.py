import pyautogui
import json
import time
import os

CONFIG_FILE = "stealth_coords.json"

print("=" * 60)
print("   STEALTHWRITER MOUSE COORDINATE CALIBRATION TOOL")
print("=" * 60)
print("Make sure your browser is open with:")
print("https://stealthwriter.ai/dashboard/humanizer visible on your screen.\n")

steps = [
    ("input_box", "Hover your mouse over the INPUT TEXT AREA (where you paste text)"),
    ("humanize_btn", "Hover your mouse over the 'HUMANIZE' BUTTON"),
    ("copy_btn", "Hover your mouse over the 'COPY' BUTTON (or result area)")
]

coords = {}

for key, prompt in steps:
    print(f"\n--> STEP: {prompt}")
    print("    You have 4 seconds to move your mouse there...")
    for sec in range(4, 0, -1):
        print(f"    Capturing in {sec}...", end="\r", flush=True)
        time.sleep(1)
    
    pos = pyautogui.position()
    coords[key] = {"x": pos.x, "y": pos.y}
    print(f"    [SAVED] {key} at X: {pos.x}, Y: {pos.y}              ")

with open(CONFIG_FILE, "w") as f:
    json.dump(coords, f, indent=4)

print("\n" + "=" * 60)
print(f"Calibration complete! Coordinates saved to '{CONFIG_FILE}'.")
print("Now you can run the automation script!")
print("=" * 60)
