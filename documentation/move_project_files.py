import os
import shutil

source_dir = r"c:\Users\ACER\Desktop\Report"
dest_dir = r"C:\Users\ACER\Desktop\CCP-Nigeria Road Management System"
downloads_dir = r"C:\Users\ACER\Downloads"

os.makedirs(dest_dir, exist_ok=True)
os.makedirs(os.path.join(dest_dir, "figures"), exist_ok=True)
os.makedirs(os.path.join(dest_dir, "figures", "extracted"), exist_ok=True)

# 1. Exact files to move from Report root
files_to_move = [
    # Documents
    "Nigeria_Road_Management_System_NJC.docx",
    "Nigeria_Road_Management_System_NJC.pdf",
    "Nigeria_Road_Management_System_NJC_Polished_Master.docx",
    "Nigeria_Road_Management_System_NJC_Final_FastAPI.docx",
    "Nigeria_Road_Management_System_NJC_Polished.docx",
    "Nigeria_Road_Management_System_NJC_Template.docx",
    "Nigeria_Road_Management_System_Chapters_1_and_2.docx",
    "CRIM_TVRS_Project_Documentation_Chapters_1_and_2.docx",
    
    # Presentations
    "Nigeria_Road_Management_System_Defense_Deck_Phone_Fixed.pptx",
    "Nigeria_Road_Management_System_Defense_Deck_Updated.pptx",
    "Nigeria_Road_Management_System_Defense_Deck.pptx",
    "test_tx.pptx",
    
    # Scripts
    "build_fixed_powerpoint.py",
    "build_full_document.py",
    "build_humanized_njc_document.py",
    "build_njc_template_document.py",
    "build_powerpoint.py",
    "generate_clean_diagram.py",
    "generate_nrms_diagram.py",
    "rebuild_perfect_document.py",
    "humanize_all_batches.py",
    "humanize_methodology_now.py",
    "humanize_sections.py",
    "humanize_sections_v2.py",
    "calibrate_mouse.py",
    "test_mouse_session.py",
    "vision_clicker.py",
    
    # Text, Batch, and Data files
    "Methodology_Cleaned_No_Citations.txt",
    "Methodology_To_Humanize.txt",
    "Related_Works_To_Humanize.txt",
    "sections_summary.txt",
    "START_HUMANIZER.bat",
    "stealth_coords.json",
    "mouse_result.txt",
    
    # Humanizer Automation Image Assets
    "btn_humanize_img1.png",
    "btn_row_img2.png",
    "crop_copy.png",
    "crop_hm.png",
    "crop_humanize.png",
    "crop_input.png",
    "tpl_copy.png",
    "tpl_humanize.png",
    "tpl_humanize_main.png",
    "tpl_humanize_more.png",
    "tpl_rehumanize.png",
    "verified_input_click.png"
]

moved_count = 0
failed_moves = []

print("--- Moving files from Report to CCP-Nigeria Road Management System ---")
for fname in files_to_move:
    src_path = os.path.join(source_dir, fname)
    dst_path = os.path.join(dest_dir, fname)
    if os.path.exists(src_path):
        try:
            shutil.move(src_path, dst_path)
            print(f"MOVED: {fname}")
            moved_count += 1
        except Exception as e:
            # If move fails (e.g. file lock), try copy
            try:
                shutil.copy2(src_path, dst_path)
                print(f"COPIED (locked for move): {fname}")
                moved_count += 1
            except Exception as e2:
                print(f"ERROR: {fname} -> {e2}")
                failed_moves.append(fname)
    else:
        print(f"NOT FOUND (already moved or missing): {fname}")

# 2. Figures specific to the group project
figures_to_move = [
    "nrms_clean_architecture.png",
    "nrms_system_architecture.png",
    "system_architecture.png"
]

print("\n--- Moving figures ---")
for f_name in figures_to_move:
    s_p = os.path.join(source_dir, "figures", f_name)
    d_p = os.path.join(dest_dir, "figures", f_name)
    if os.path.exists(s_p):
        try:
            shutil.move(s_p, d_p)
            print(f"MOVED FIGURE: {f_name}")
            moved_count += 1
        except Exception as e:
            print(f"ERROR FIGURE: {f_name} -> {e}")

# 3. figures/extracted directory
src_extracted = os.path.join(source_dir, "figures", "extracted")
dst_extracted = os.path.join(dest_dir, "figures", "extracted")
if os.path.exists(src_extracted):
    for f in os.listdir(src_extracted):
        s = os.path.join(src_extracted, f)
        d = os.path.join(dst_extracted, f)
        try:
            shutil.move(s, d)
            print(f"MOVED EXTRACTED FIGURE: {f}")
            moved_count += 1
        except Exception as e:
            print(f"ERROR EXTRACTED: {f} -> {e}")
    try:
        os.rmdir(src_extracted)
    except:
        pass

# 4. Copy Nile logo to destination (retain in source for SIWES)
logo_src = os.path.join(source_dir, "nile_logo.png")
logo_dst = os.path.join(dest_dir, "nile_logo.png")
if os.path.exists(logo_src):
    shutil.copy2(logo_src, logo_dst)
    # Also in figures
    shutil.copy2(logo_src, os.path.join(dest_dir, "figures", "nile_logo.png"))
    print("COPIED: nile_logo.png to destination and destination/figures")

# 5. Also copy relevant downloads if available
downloads_files = [
    "Nigeria_Road_Management_System_Defense_Deck_FastAPI (1).pptx",
    "Nigeria_Road_Management_System_NJC_Polished (1).docx"
]
print("\n--- Checking Downloads ---")
for df in downloads_files:
    df_src = os.path.join(downloads_dir, df)
    df_dst = os.path.join(dest_dir, df)
    if os.path.exists(df_src) and not os.path.exists(df_dst):
        try:
            shutil.copy2(df_src, df_dst)
            print(f"COPIED FROM DOWNLOADS: {df}")
        except Exception as e:
            print(f"ERROR FROM DOWNLOADS: {df} -> {e}")

print(f"\nCompleted! Total items moved/copied: {moved_count}")
if failed_moves:
    print(f"Failed items: {failed_moves}")
