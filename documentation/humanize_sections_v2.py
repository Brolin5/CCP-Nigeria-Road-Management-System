import os
import time
import docx
import pyautogui
import pyperclip
import cv2
import numpy as np
from PIL import ImageGrab

INPUT_DOCX = r"C:\Users\ACER\Downloads\Nigeria_Road_Management_System_NJC_Polished (1).docx"
OUTPUT_DOCX = r"C:\Users\ACER\Downloads\Nigeria_Road_Management_System_NJC_Polished_DoubleHumanized.docx"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_HUMANIZE = os.path.join(SCRIPT_DIR, "tpl_humanize.png")
TPL_HUMANIZE_MORE = os.path.join(SCRIPT_DIR, "tpl_humanize_more.png")
TPL_REHUMANIZE = os.path.join(SCRIPT_DIR, "tpl_rehumanize.png")
TPL_COPY = os.path.join(SCRIPT_DIR, "tpl_copy.png")

def capture_screen():
    screenshot = ImageGrab.grab()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_button_on_screen(template_path, threshold=0.72, max_scrolls=6, scroll_step=-280):
    """
    Finds a template on screen with multi-scale matching.
    If not found, scrolls down and captures again.
    """
    if not os.path.exists(template_path):
        print(f"[-] Template missing: {template_path}")
        return None

    tpl = cv2.imread(template_path)
    th, tw = tpl.shape[:2]
    name = os.path.basename(template_path)

    for attempt in range(max_scrolls + 1):
        screen = capture_screen()
        sh, sw = screen.shape[:2]

        best_val = -1
        best_loc = None

        # Multi-scale search (covers 60% to 140% of template resolution)
        for s in np.linspace(0.6, 1.4, 12):
            nw, nh = int(tw * s), int(th * s)
            if nw >= sw or nh >= sh or nw < 10 or nh < 10:
                continue
            resized_tpl = cv2.resize(tpl, (nw, nh))
            res = cv2.matchTemplate(screen, resized_tpl, cv2.TM_CCOEFF_NORMED)
            _, max_v, _, max_l = cv2.minMaxLoc(res)
            if max_v > best_val:
                best_val = max_v
                best_loc = (max_l[0] + nw // 2, max_l[1] + nh // 2)

        if best_val >= threshold and best_loc:
            print(f"[+] Found {name} (confidence {best_val:.2f}) at screen coords {best_loc}")
            return best_loc

        if attempt < max_scrolls:
            print(f"[*] {name} not in view yet (best score {best_val:.2f}). Scrolling down...")
            pyautogui.scroll(scroll_step)
            time.sleep(0.7)

    print(f"[-] Could not find {name} after {max_scrolls} scrolls (best score {best_val:.2f}).")
    return None

def click_template(template_path, threshold=0.72, max_scrolls=6, scroll_step=-280):
    loc = find_button_on_screen(template_path, threshold, max_scrolls, scroll_step)
    if loc:
        pyautogui.moveTo(loc[0], loc[1], duration=0.6)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.5)
        return True
    return False

def scroll_to_top():
    print("[*] Scrolling to top of page...")
    for _ in range(5):
        pyautogui.scroll(600)
        time.sleep(0.1)
    pyautogui.press('home')
    time.sleep(0.8)

def countdown_wait(seconds, message="Waiting"):
    for s in range(seconds, 0, -1):
        print(f"    [{message}] {s}s remaining...", end="\r", flush=True)
        time.sleep(1)
    print(f"    [{message}] Done!                                    ")

def humanize_chunk(text, chunk_name="Chunk"):
    print("\n" + "=" * 60)
    print(f"   STARTING HUMANIZATION FOR: {chunk_name} ({len(text.split())} words)")
    print("=" * 60)

    # 1. Scroll to top and click input area
    scroll_to_top()
    # Screen center of the dark textarea (between Y: 487 and Y: 825)
    pyautogui.moveTo(840, 620, duration=0.6)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.3)

    # 2. Paste text
    print(f"[*] Pasting {len(text.split())} words...")
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)

    # 3. Scroll down & Click 'Humanize'
    print("[*] Searching for 'Humanize' button...")
    clicked_humanize = click_template(TPL_HUMANIZE, threshold=0.70, max_scrolls=6, scroll_step=-280)
    if not clicked_humanize:
        print("[!] Trying fallback click near bottom left of card (X: 590, Y: 790)...")
        pyautogui.moveTo(590, 790, duration=0.5)
        pyautogui.click()

    # 4. Wait for Pass 1 generation
    print("\n[+] Humanize clicked! Waiting for generation to complete...")
    countdown_wait(32, "Pass 1 Generating")

    # 5. Scroll down & Click 'Humanize More' (or Rehumanize)
    print("\n[*] Searching for 'Humanize More' button...")
    clicked_hm = click_template(TPL_HUMANIZE_MORE, threshold=0.70, max_scrolls=6, scroll_step=-280)
    if not clicked_hm:
        print("[*] Trying 'Rehumanize' button...")
        clicked_hm = click_template(TPL_REHUMANIZE, threshold=0.70, max_scrolls=4, scroll_step=-200)

    if not clicked_hm:
        print("[!] Could not auto-detect Humanize More. Trying fallback coords (X: 436, Y: 492)...")
        pyautogui.moveTo(436, 492, duration=0.5)
        pyautogui.click()

    # 6. Wait for Pass 2 (Humanize More) generation
    print("\n[+] Humanize More clicked! Waiting for Pass 2 to complete...")
    countdown_wait(32, "Pass 2 Generating")

    # 7. Scroll down slightly if needed & Click 'Copy' button
    print("\n[*] Searching for 'Copy' button...")
    clicked_copy = click_template(TPL_COPY, threshold=0.75, max_scrolls=4, scroll_step=-150)
    if not clicked_copy:
        print("[!] Trying fallback Copy button coords (X: 1017, Y: 492)...")
        pyautogui.moveTo(1017, 492, duration=0.5)
        pyautogui.click()

    time.sleep(1.0)
    copied_text = pyperclip.paste().strip()

    if copied_text and copied_text != text:
        print(f"\n[SUCCESS] Successfully humanized and copied to clipboard! ({len(copied_text.split())} words)")
        return copied_text
    else:
        print("\n[!] Clipboard text was identical or empty. Checking fallback copy...")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        return pyperclip.paste().strip()

def run():
    print("=" * 65)
    print("  AUTONOMOUS VISION DOUBLE-HUMANIZER (STEALTHWRITER)")
    print("=" * 65)

    if not os.path.exists(INPUT_DOCX):
        print(f"[-] Document not found: {INPUT_DOCX}")
        return

    doc = docx.Document(INPUT_DOCX)
    print(f"[+] Loaded document: {os.path.basename(INPUT_DOCX)}")

    # Extract Related Works narrative paragraphs
    rw_paragraphs = [doc.paragraphs[i] for i in range(18, 34) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith(('2.', 'TABLE'))]
    rw_text = "\n\n".join([p.text.strip() for p in rw_paragraphs])
    rw_words = len(rw_text.split())

    # Extract Methodology narrative paragraphs
    meth_paragraphs = [doc.paragraphs[i] for i in range(35, 73) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith(('3.', 'Figure', 'TABLE'))]
    meth_text = "\n\n".join([p.text.strip() for p in meth_paragraphs])
    meth_words = len(meth_text.split())

    print(f"[1] Part 1: Related Works narrative ({rw_words} words)")
    print(f"[2] Part 2: Methodology narrative ({meth_words} words)")
    print("\n[!] The script will use visual recognition on your screen:")
    print("    1. Paste text at top of page")
    print("    2. Scroll & click 'Humanize'")
    print("    3. Scroll & click 'Humanize More'")
    print("    4. Click 'Copy' button and save to Word document")
    print("\nStarting in 5 seconds! Keep your Chrome window active...")
    print("Failsafe: Slam mouse into top-left corner to abort.")

    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds...", end="\r", flush=True)
        time.sleep(1)
    print("Starting NOW!                                          \n")

    # --- PART 1: RELATED WORKS ---
    rw_humanized = humanize_chunk(rw_text, "PART 1: RELATED WORKS")
    rw_chunks = [c.strip() for c in rw_humanized.split("\n\n") if c.strip()]
    
    # Replace in docx
    if len(rw_chunks) == len(rw_paragraphs):
        for p, new_t in zip(rw_paragraphs, rw_chunks):
            p.text = new_t
    else:
        rw_paragraphs[0].text = rw_chunks[0]
        for i in range(1, min(len(rw_paragraphs), len(rw_chunks))):
            rw_paragraphs[i].text = rw_chunks[i]

    doc.save(OUTPUT_DOCX)
    print(f"[+] Checkpoint saved: Related Works updated in '{os.path.basename(OUTPUT_DOCX)}'")

    # Brief pause before Part 2
    time.sleep(3.0)

    # --- PART 2: METHODOLOGY ---
    meth_humanized = humanize_chunk(meth_text, "PART 2: METHODOLOGY")
    meth_chunks = [c.strip() for c in meth_humanized.split("\n\n") if c.strip()]

    if len(meth_chunks) == len(meth_paragraphs):
        for p, new_t in zip(meth_paragraphs, meth_chunks):
            p.text = new_t
    else:
        meth_paragraphs[0].text = meth_chunks[0]
        for i in range(1, min(len(meth_paragraphs), len(meth_chunks))):
            meth_paragraphs[i].text = meth_chunks[i]

    doc.save(OUTPUT_DOCX)
    print("\n" + "=" * 65)
    print("ALL PARTS COMPLETED!")
    print(f"Double-humanized document saved to:\n  {OUTPUT_DOCX}")
    print("=" * 65)

if __name__ == "__main__":
    run()
