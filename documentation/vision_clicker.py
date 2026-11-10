import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import os

def capture_screen():
    screenshot = ImageGrab.grab()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_button_on_screen(template_path, threshold=0.75, max_attempts=15, scroll_step=-250):
    """
    Searches the live screen for a template image using multi-scale matching.
    If not found, scrolls down and retries.
    Returns (center_x, center_y) if found, else None.
    """
    if not os.path.exists(template_path):
        print(f"[-] Template not found: {template_path}")
        return None

    tpl = cv2.imread(template_path)
    th, tw = tpl.shape[:2]

    for attempt in range(max_attempts):
        screen = capture_screen()
        sh, sw = screen.shape[:2]

        best_val = -1
        best_loc = None

        # Multi-scale search (from 70% to 130% of template size)
        for s in np.linspace(0.7, 1.3, 10):
            nw, nh = int(tw * s), int(th * s)
            if nw >= sw or nh >= sh:
                continue
            resized_tpl = cv2.resize(tpl, (nw, nh))
            res = cv2.matchTemplate(screen, resized_tpl, cv2.TM_CCOEFF_NORMED)
            _, max_v, _, max_l = cv2.minMaxLoc(res)
            if max_v > best_val:
                best_val = max_v
                best_loc = (max_l[0] + nw // 2, max_l[1] + nh // 2)

        if best_val >= threshold and best_loc:
            print(f"[+] Found {os.path.basename(template_path)} (confidence {best_val:.2f}) at {best_loc}")
            return best_loc

        # Not found yet, scroll down slightly
        if scroll_step != 0:
            print(f"[*] Looking for {os.path.basename(template_path)} (attempt {attempt+1}/{max_attempts})... scrolling...")
            pyautogui.scroll(scroll_step)
            time.sleep(0.8)
        else:
            time.sleep(1.0)

    print(f"[-] Could not find {os.path.basename(template_path)} on screen (best confidence: {best_val:.2f})")
    return None

def click_template(template_path, threshold=0.75, max_attempts=12, scroll_step=-250):
    loc = find_button_on_screen(template_path, threshold, max_attempts, scroll_step)
    if loc:
        pyautogui.moveTo(loc[0], loc[1], duration=0.6)
        time.sleep(0.2)
        pyautogui.click()
        return True
    return False
