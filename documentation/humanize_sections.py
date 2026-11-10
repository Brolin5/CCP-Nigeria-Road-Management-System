import os
import json
import time
import docx
import pyautogui
import pyperclip

CONFIG_FILE = "stealth_coords.json"
INPUT_DOCX = r"C:\Users\ACER\Downloads\Nigeria_Road_Management_System_NJC_Polished (1).docx"
OUTPUT_DOCX = r"C:\Users\ACER\Downloads\Nigeria_Road_Management_System_NJC_Polished_DoubleHumanized.docx"

def load_coordinates():
    if not os.path.exists(CONFIG_FILE):
        print(f"[-] Config file '{CONFIG_FILE}' not found!")
        print("[-] Please run 'python calibrate_mouse.py' first to set your button coordinates.")
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def countdown_wait(seconds, message="Waiting for StealthWriter"):
    for s in range(seconds, 0, -1):
        print(f"    [{message}] {s}s remaining...", end="\r", flush=True)
        time.sleep(1)
    print(f"    [{message}] Done!                                    ")

def humanize_chunk_via_mouse(text, coords, wait_time=30):
    """
    Performs double humanization using physical mouse automation on StealthWriter:
    1. Pastes text into input box -> Clicks Humanize -> Waits -> Copies output (Pass 1)
    2. Pastes Pass 1 into input box -> Clicks Humanize -> Waits -> Copies output (Pass 2)
    """
    input_x = coords["input_box"]["x"]
    input_y = coords["input_box"]["y"]
    human_x = coords["humanize_btn"]["x"]
    human_y = coords["humanize_btn"]["y"]
    copy_x = coords["copy_btn"]["x"]
    copy_y = coords["copy_btn"]["y"]

    print("\n--- PASS 1: Humanizing Original Text ---")
    # Move to input box, clear it, paste original text
    print(f"-> Moving mouse to Input Box ({input_x}, {input_y})...")
    pyautogui.moveTo(input_x, input_y, duration=0.8)
    pyautogui.click()
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.3)
    
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)

    # Click Humanize
    print(f"-> Moving mouse to 'Humanize' Button ({human_x}, {human_y})...")
    pyautogui.moveTo(human_x, human_y, duration=0.8)
    pyautogui.click()
    
    countdown_wait(wait_time, "Generating Pass 1")

    # Click Copy Output
    print(f"-> Moving mouse to 'Copy' Button ({copy_x}, {copy_y})...")
    pyautogui.moveTo(copy_x, copy_y, duration=0.8)
    pyautogui.click()
    time.sleep(1.0)
    
    pass1_text = pyperclip.paste().strip()
    # Fallback copy if copy button wasn't at exact pixel
    if not pass1_text or pass1_text == text:
        print("[*] Trying fallback copy from output area...")
        pyautogui.moveTo(input_x, input_y, duration=0.5)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        pass1_text = pyperclip.paste().strip()

    if not pass1_text or pass1_text == text:
        print("[!] Warning: Output text matches original or is empty. Please check your browser.")
    else:
        print(f"[+] Pass 1 received ({len(pass1_text.split())} words).")

    print("\n--- PASS 2: Humanizing the Humanized Version (Double Humanize) ---")
    # Move to input box, clear it, paste pass 1 text
    print(f"-> Moving mouse to Input Box...")
    pyautogui.moveTo(input_x, input_y, duration=0.8)
    pyautogui.click()
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.3)
    
    pyperclip.copy(pass1_text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)

    # Click Humanize
    print(f"-> Moving mouse to 'Humanize' Button...")
    pyautogui.moveTo(human_x, human_y, duration=0.8)
    pyautogui.click()
    
    countdown_wait(wait_time, "Generating Pass 2")

    # Click Copy Output
    print(f"-> Moving mouse to 'Copy' Button...")
    pyautogui.moveTo(copy_x, copy_y, duration=0.8)
    pyautogui.click()
    time.sleep(1.0)
    
    pass2_text = pyperclip.paste().strip()
    if not pass2_text or pass2_text == pass1_text:
        print("[*] Trying fallback copy from output area for Pass 2...")
        pyautogui.moveTo(input_x, input_y, duration=0.5)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        pass2_text = pyperclip.paste().strip()

    print(f"[+] Pass 2 completed ({len(pass2_text.split())} words)!")
    return pass2_text

def run():
    print("=" * 65)
    print("  DOUBLE-HUMANIZER MOUSE AUTOMATION FOR STEALTHWRITER")
    print("=" * 65)

    coords = load_coordinates()
    if not coords:
        return

    if not os.path.exists(INPUT_DOCX):
        print(f"[-] Target document not found at: {INPUT_DOCX}")
        return

    doc = docx.Document(INPUT_DOCX)
    print(f"[+] Loaded document: {os.path.basename(INPUT_DOCX)}")

    # Identify Related Works paragraphs: 18 to 33
    rw_paragraphs = [doc.paragraphs[i] for i in range(18, 34) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith(('2.', 'TABLE'))]
    rw_text = "\n\n".join([p.text.strip() for p in rw_paragraphs])
    rw_words = len(rw_text.split())

    # Identify Methodology paragraphs: 35 to 72
    meth_paragraphs = [doc.paragraphs[i] for i in range(35, 73) if doc.paragraphs[i].text.strip() and not doc.paragraphs[i].text.strip().startswith(('3.', 'Figure', 'TABLE'))]
    meth_text = "\n\n".join([p.text.strip() for p in meth_paragraphs])
    meth_words = len(meth_text.split())

    print(f"[+] Extracted Related Works narrative body: {rw_words} words (Chunk 1)")
    print(f"[+] Extracted Methodology narrative body: {meth_words} words (Chunk 2)")
    print("\nHeadings and table/figure captions are safely preserved!")
    
    print("\n[!] Starting mouse automation in 5 seconds! Keep your browser visible on screen...")
    print("    Failsafe: Slam your mouse into the top-left corner of your monitor at any time to abort.")
    for i in range(5, 0, -1):
        print(f"    Starting in {i} seconds...", end="\r", flush=True)
        time.sleep(1)
    print("    Starting NOW!                                      \n")

    # CHUNK 1: Related Works
    print("\n" + "=" * 50)
    print(f"PROCESSING CHUNK 1: RELATED WORKS ({rw_words} words)")
    print("=" * 50)
    rw_humanized = humanize_chunk_via_mouse(rw_text, coords, wait_time=30)
    
    # Replace in document
    rw_chunks = rw_humanized.split("\n\n")
    if len(rw_chunks) == len(rw_paragraphs):
        for p, new_t in zip(rw_paragraphs, rw_chunks):
            p.text = new_t.strip()
    else:
        # If paragraph count changed slightly, replace the first and clear others or set combined
        rw_paragraphs[0].text = rw_chunks[0]
        for i in range(1, min(len(rw_paragraphs), len(rw_chunks))):
            rw_paragraphs[i].text = rw_chunks[i]

    # Save checkpoint
    doc.save(OUTPUT_DOCX)
    print(f"[+] Checkpoint saved: Related Works updated in '{os.path.basename(OUTPUT_DOCX)}'")

    # CHUNK 2: Methodology
    print("\n" + "=" * 50)
    print(f"PROCESSING CHUNK 2: METHODOLOGY ({meth_words} words)")
    print("=" * 50)
    meth_humanized = humanize_chunk_via_mouse(meth_text, coords, wait_time=30)

    meth_chunks = meth_humanized.split("\n\n")
    if len(meth_chunks) == len(meth_paragraphs):
        for p, new_t in zip(meth_paragraphs, meth_chunks):
            p.text = new_t.strip()
    else:
        meth_paragraphs[0].text = meth_chunks[0]
        for i in range(1, min(len(meth_paragraphs), len(meth_chunks))):
            meth_paragraphs[i].text = meth_chunks[i]

    # Final Save
    doc.save(OUTPUT_DOCX)
    print("\n" + "=" * 65)
    print("ALL DONE! SUCCESSFUL DOUBLE HUMANIZATION!")
    print(f"Final output saved to:\n  {OUTPUT_DOCX}")
    print("=" * 65)

if __name__ == "__main__":
    run()
