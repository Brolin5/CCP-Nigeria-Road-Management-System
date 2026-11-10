import os
import sys
import time
import re
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

def disable_quickedit():
    """
    Prevents Windows Command Prompt from freezing when clicked (disables QuickEdit mode).
    """
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        hStdin = kernel32.GetStdHandle(-10) # STD_INPUT_HANDLE
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(hStdin, ctypes.byref(mode)):
            ENABLE_QUICK_EDIT = 0x0040
            ENABLE_EXTENDED_FLAGS = 0x0080
            new_mode = (mode.value & ~ENABLE_QUICK_EDIT) | ENABLE_EXTENDED_FLAGS
            kernel32.SetConsoleMode(hStdin, new_mode)
    except Exception:
        pass

def capture_screen():
    screenshot = ImageGrab.grab()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_button_on_screen(template_path, threshold=0.70, max_scrolls=7, scroll_step=-280):
    if not os.path.exists(template_path):
        print(f"[-] Missing template: {template_path}")
        return None

    tpl = cv2.imread(template_path)
    th, tw = tpl.shape[:2]
    name = os.path.basename(template_path)

    for attempt in range(max_scrolls + 1):
        screen = capture_screen()
        sh, sw = screen.shape[:2]

        best_val = -1
        best_loc = None

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
            print(f"[*] Scrolling down to look for {name} (attempt {attempt+1}/{max_scrolls})...")
            # Move mouse to center-right before scrolling so wheel reaches main container
            pyautogui.moveTo(900, 500, duration=0.2)
            pyautogui.scroll(scroll_step)
            time.sleep(0.7)

    print(f"[-] Could not find {name} (best confidence: {best_val:.2f})")
    return None

def click_template(template_path, threshold=0.70, max_scrolls=7, scroll_step=-280):
    loc = find_button_on_screen(template_path, threshold, max_scrolls, scroll_step)
    if loc:
        pyautogui.moveTo(loc[0], loc[1], duration=0.6)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.5)
        return True
    return False

def scroll_to_top_and_reset():
    print("[*] Scrolling to top of page (Ctrl + Home)...")
    pyautogui.moveTo(840, 200, duration=0.4)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'home')
    time.sleep(0.3)
    for _ in range(5):
        pyautogui.scroll(700)
        time.sleep(0.05)
    time.sleep(0.8)

def countdown_wait(seconds, message="Waiting"):
    for s in range(seconds, 0, -1):
        print(f"    [{message}] {s}s remaining...", end="\r", flush=True)
        time.sleep(1)
    print(f"    [{message}] Done!                                    ")

def sanitize_for_humanizer(text):
    """
    Completely removes ANY in-text citation containing a year (e.g., 2017, 2021)
    including those with '&', ';', 'et al.' so StealthWriter's in-text citation detector
    has 0 citations to flag.
    """
    pattern = r"\s*\([^\)]*?\b(?:19|20)\d{2}\b[^\)]*?\)"
    cleaned = re.sub(pattern, "", text)
    cleaned = re.sub(r"\s*\(\d{4}[a-z]?\)", "", cleaned)
    return cleaned

def process_single_batch(batch_name, text):
    print("\n" + "=" * 65)
    print(f"   STARTING {batch_name.upper()} ({len(text.split())} words)")
    print("=" * 65)

    # 1. Fresh URL navigation (Ctrl + L, Enter) to avoid Chrome's scroll restoration
    print("[1] Navigating fresh to https://stealthwriter.ai/dashboard/humanizer (Ctrl + L -> Enter)...")
    pyautogui.moveTo(840, 200, duration=0.2)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)
    pyautogui.press('enter')
    countdown_wait(4, "Loading fresh page")

    # 2. Focus the solid center of the text area (X: 850, Y: 650)
    print("[2] Focusing solid center of text box (X: 850, Y: 650)...")
    pyautogui.moveTo(850, 650, duration=0.5)
    pyautogui.click()
    time.sleep(0.5)

    # 3. Paste sanitized text directly (Strictly <= 950 words)
    clean_text = sanitize_for_humanizer(text)
    words_count = len(clean_text.split())
    if words_count > 950:
        raise ValueError(f"CRITICAL ERROR: {batch_name} has {words_count} words! Exceeds 950 words limit.")
    print(f"[3] Pasting {words_count} words into input box...")
    pyperclip.copy(clean_text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.0)

    # 4. Visually locate and click 'Humanize' button at its NEW position after paste
    print("[4] Visually locating 'Humanize' button after paste...")
    clicked_h = click_template(TPL_HUMANIZE, threshold=0.68, max_scrolls=7, scroll_step=-280)
    if not clicked_h:
        print("[!] Template search fell back. Clicking verified button coords (X: 594, Y: 988)...")
        pyautogui.moveTo(594, 988, duration=0.5)
        pyautogui.click()

    # 5. Wait for Pass 1
    print("\n[+] Humanize clicked! Generating Pass 1...")
    countdown_wait(32, "Pass 1 Generating")

    # 6. Scroll down and click Humanize More
    print("\n[4] Searching for 'Humanize More' button...")
    clicked_hm = click_template(TPL_HUMANIZE_MORE, threshold=0.70, max_scrolls=7, scroll_step=-280)
    if not clicked_hm:
        print("[*] Trying 'Rehumanize' button...")
        clicked_hm = click_template(TPL_REHUMANIZE, threshold=0.70, max_scrolls=4, scroll_step=-200)

    if not clicked_hm:
        print("[!] Trying fallback click at X: 436, Y: 492...")
        pyautogui.moveTo(436, 492, duration=0.5)
        pyautogui.click()

    # 7. Wait for Pass 2 (Humanize More)
    print("\n[+] Humanize More clicked! Generating Pass 2...")
    countdown_wait(32, "Pass 2 Generating")

    # 8. Click Copy button
    print("\n[5] Searching for 'Copy' button...")
    clicked_cp = click_template(TPL_COPY, threshold=0.75, max_scrolls=4, scroll_step=-150)
    if not clicked_cp:
        print("[!] Trying fallback click at X: 1017, Y: 492...")
        pyautogui.moveTo(1017, 492, duration=0.5)
        pyautogui.click()

    time.sleep(1.0)
    copied = pyperclip.paste().strip()
    if not copied or copied == clean_text:
        print("[*] Fallback copy hotkey...")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        copied = pyperclip.paste().strip()

    print(f"\n[SUCCESS] {batch_name} successfully double-humanized! ({len(copied.split())} words)")
    return copied

def run():
    disable_quickedit()
    print("=" * 65)
    print("   AUTONOMOUS MULTI-BATCH HUMANIZER (STEALTHWRITER)")
    print("=" * 65)

    # ALWAYS load clean original source text from INPUT_DOCX
    source_doc = docx.Document(INPUT_DOCX)
    # Target document where updates are saved
    doc = docx.Document(OUTPUT_DOCX if os.path.exists(OUTPUT_DOCX) else INPUT_DOCX)
    print(f"[+] Loaded original text from: {os.path.basename(INPUT_DOCX)}")

    # Extract all 3 batches strictly from clean original document
    # Batch 1: Related Works (paras 18 to 33)
    rw_text = "\n\n".join([source_doc.paragraphs[i].text.strip() for i in range(18, 34) if source_doc.paragraphs[i].text.strip() and not source_doc.paragraphs[i].text.strip().startswith(('2.', 'TABLE'))])
    rw_paragraphs = [doc.paragraphs[i] for i in range(18, 34) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith(('2.', 'TABLE'))]

    # Batch 2: Methodology (paras 35 to 72)
    meth_text = "\n\n".join([source_doc.paragraphs[i].text.strip() for i in range(35, 73) if source_doc.paragraphs[i].text.strip() and not source_doc.paragraphs[i].text.strip().startswith(('3.', 'Figure', 'TABLE'))])
    meth_paragraphs = [doc.paragraphs[i] for i in range(35, 73) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith(('3.', 'Figure', 'TABLE'))]

    # Batch 3: Introduction (paras 8 to 16)
    intro_text = "\n\n".join([source_doc.paragraphs[i].text.strip() for i in range(8, 17) if source_doc.paragraphs[i].text.strip() and not source_doc.paragraphs[i].text.strip().startswith('I.')])
    intro_paragraphs = [doc.paragraphs[i] for i in range(8, 17) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith('I.')]

    all_batches = [
        ("Batch 1: Related Works", rw_paragraphs, rw_text),
        ("Batch 2: Methodology", meth_paragraphs, meth_text),
        ("Batch 3: Introduction", intro_paragraphs, intro_text)
    ]

    print("\nDocument Batches:")
    for idx, (name, paras, text) in enumerate(all_batches, 1):
        print(f"  [{idx}] {name} ({len(text.split())} words)")

    print("\n-----------------------------------------------------------")
    print("STATUS: Batch 1 (Related Works) & Batch 2 (Methodology) are COMPLETE!")
    print("Defaulting to finalize the remaining batch: [3] Batch 3: Introduction")
    print("Press Enter to run Batch 3, or type 1 to rerun all batches: ", end="", flush=True)

    start_idx = 3
    user_choice = input().strip()
    if user_choice == '1':
        start_idx = 1
    elif user_choice == '2':
        start_idx = 2

    batches_to_run = all_batches[start_idx - 1:]

    print(f"\n[!] Will run {len(batches_to_run)} batches in continuous sequence:")
    for b_name, _, _ in batches_to_run:
        print(f"    -> {b_name}")

    print("\nStarting in 5 seconds! Keep your Chrome window active...")
    print("Failsafe: Slam mouse into top-left corner at any time to abort.")
    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds...", end="\r", flush=True)
        time.sleep(1)
    print("Starting NOW!                                          \n")

    for batch_name, paragraphs, text in batches_to_run:
        humanized_result = process_single_batch(batch_name, text)

        # Update document
        chunks = [c.strip() for c in humanized_result.split("\n\n") if c.strip()]
        if len(chunks) == len(paragraphs):
            for p, new_t in zip(paragraphs, chunks):
                p.text = new_t
        else:
            paragraphs[0].text = chunks[0]
            for i in range(1, min(len(paragraphs), len(chunks))):
                paragraphs[i].text = chunks[i]

        doc.save(OUTPUT_DOCX)
        print(f"[+] Checkpoint saved: {batch_name} updated in '{os.path.basename(OUTPUT_DOCX)}'")
        print("[*] Taking 3 seconds pause before next batch...")
        time.sleep(3.0)

    print("\n" + "=" * 65)
    print("ALL BATCHES COMPLETED SUCCESSFULLY!")
    print(f"Final double-humanized document is saved at:\n  {OUTPUT_DOCX}")
    print("=" * 65)

if __name__ == "__main__":
    run()
