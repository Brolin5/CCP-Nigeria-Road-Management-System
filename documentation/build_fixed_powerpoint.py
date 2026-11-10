import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 widescreen
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    
    # Explicit high-contrast colors
    c_white = RGBColor(255, 255, 255)
    c_navy = RGBColor(11, 83, 148)       # Deep NJC Blue
    c_dark = RGBColor(26, 32, 44)        # Deep Charcoal Black (100% visible on any screen)
    c_grey = RGBColor(80, 90, 105)       # Neutral slate for category subtitles
    c_light_bg = RGBColor(245, 247, 250) # Light neutral card bg
    c_blue_tint = RGBColor(235, 243, 252)# Soft blue card bg
    c_border = RGBColor(180, 205, 235)   # Crisp card border
    
    def set_white_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = c_white
        
    def add_slide_header(slide, title_text, category_text="NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)"):
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.73), Inches(1.15))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        r_cat = p_cat.add_run()
        r_cat.text = category_text.upper()
        r_cat.font.name = "Calibri"
        r_cat.font.size = Pt(11)
        r_cat.font.bold = True
        r_cat.font.color.rgb = c_grey
        
        p_title = tf.add_paragraph()
        p_title.space_before = Pt(3)
        r_title = p_title.add_run()
        r_title.text = title_text
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(24)
        r_title.font.bold = True
        r_title.font.color.rgb = c_navy

    def add_card_box(slide, left, top, width, height, title, body_bullets, bg_rgb, border_rgb):
        # 1. Background shape
        sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        sh.fill.solid()
        sh.fill.fore_color.rgb = bg_rgb
        sh.line.color.rgb = border_rgb
        sh.line.width = Pt(1.5)
        
        # 2. Textbox directly layered on top with explicit run colors (Guarantees dark text on phones/WPS)
        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.36))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(13)
        r_t.font.bold = True
        r_t.font.color.rgb = c_navy
        
        for bullet in body_bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(6)
            r_b = p_b.add_run()
            r_b.text = bullet
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(10.5)
            r_b.font.color.rgb = c_dark

    # ==================== SLIDE 1: Title & Members ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)
    
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(0.65), Inches(11.33), Inches(2.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "NILE UNIVERSITY OF NIGERIA | DEPARTMENT OF COMPUTER SCIENCE"
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    r0.font.bold = True
    r0.font.color.rgb = c_grey
    
    p1 = tf.add_paragraph()
    p1.space_before = Pt(6)
    r1 = p1.add_run()
    r1.text = "Nigeria Road Management System: A Citizen-Centric Platform for Road Monitoring, Reporting, and Progress Tracking"
    r1.font.name = "Calibri"
    r1.font.size = Pt(24)
    r1.font.bold = True
    r1.font.color.rgb = c_navy
    
    p2 = tf.add_paragraph()
    p2.space_before = Pt(5)
    r2 = p2.add_run()
    r2.text = "Undergraduate Software Engineering Project Defense | Academic Session 2025/2026"
    r2.font.name = "Calibri"
    r2.font.size = Pt(12)
    r2.font.color.rgb = c_grey
    
    table_shape = s1.shapes.add_table(7, 3, Inches(1.5), Inches(3.2), Inches(10.33), Inches(3.5))
    table = table_shape.table
    table.columns[0].width = Inches(1.0)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(6.33)
    
    headers = ["S/N", "Matriculation No.", "Full Student Name & Role"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = c_white
        
    members = [
        ("1", "241030116", "Chibuzor Clinton AGADA (Group Leader)"),
        ("2", "241030026", "Ephraim Ayokunle Tackie OFOLI (Member)"),
        ("3", "241030081", "Isaac Akorede-Abayomi ODUJOKO (Member)"),
        ("4", "241030123", "Aisha Mohammed RASHEED (Member)"),
        ("5", "241030021", "Prince Arinze Wenceslaus OBINABO (Member)"),
        ("6", "241030039", "Mubarak Ibrahim AUDU (Member)")
    ]
    for row_idx, (sn, mat, name) in enumerate(members, start=1):
        for col_idx, val in enumerate([sn, mat, name]):
            cell = table.cell(row_idx, col_idx)
            cell.text = ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_light_bg if row_idx % 2 == 1 else c_white
            p = cell.text_frame.paragraphs[0]
            if col_idx < 2:
                p.alignment = PP_ALIGN.CENTER
            else:
                p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = val
            r.font.name = "Calibri"
            r.font.size = Pt(11)
            r.font.color.rgb = c_dark
            if "Leader" in val:
                r.font.bold = True
                r.font.color.rgb = c_navy

    # ==================== SLIDE 2: Introduction & Background ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)
    add_slide_header(s2, "1. Introduction & Background")
    
    cards_s2 = [
        ("Nigeria Road Network", [
            "• Over 193,200 km of roads across Nigeria (largest network in West Africa).",
            "• Connects towns, cities, and rural agricultural zones.",
            "• Transports over 90% of national passenger and cargo traffic."
        ], Inches(0.8)),
        ("Current Road Conditions", [
            "• Widespread potholes, broken bridges, and washed-out shoulders.",
            "• Premature pavement damage from heavy trucks and poor drainage.",
            "• High cost of vehicle maintenance, long transit delays, and frequent accidents."
        ], Inches(4.7)),
        ("Management Inefficiencies", [
            "• Roads divided among federal (FERMA), state, and local councils.",
            "• Over-reliance on manual inspections and paper complaints.",
            "• Citizens have no direct digital platform to report bad roads with photo proof."
        ], Inches(8.6))
    ]
    for title, bullets, left in cards_s2:
        add_card_box(s2, left, Inches(1.8), Inches(3.9), Inches(5.1), title, bullets, c_blue_tint, c_navy)

    # ==================== SLIDE 3: Problem Statement ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_white_bg(s3)
    add_slide_header(s3, "2. Problem Statement: Key Flaws in the Current System")
    
    flaws = [
        ("1. Slow Defect Reporting", "Citizens have no direct digital platform to report potholes and road damage with photos and GPS. Complaints take months to reach maintenance teams (Farouq et al., 2017).", Inches(1.8)),
        ("2. Contractor Opacity", "Road construction progress is not documented in open digital records with photo proof, enabling substandard materials and delayed milestones (Adepoju, 2021).", Inches(3.1)),
        ("3. Unchecked Traffic Violations", "Violations like driving against traffic ('one-way'), illegal parking, and dumping dirt on roads frequently occur without penalty because officers cannot be everywhere (Umar et al., 2021).", Inches(4.4)),
        ("4. Missed Inspection Cycles", "Maintenance agencies lack an automated alert system when road inspections or contractor site checks are overdue, leading to forgotten maintenance schedules (Odinfono & Olawole, 2024).", Inches(5.7))
    ]
    for title, desc, top in flaws:
        # Background shape
        sh = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.73), Inches(1.12))
        sh.fill.solid()
        sh.fill.fore_color.rgb = c_light_bg
        sh.line.color.rgb = c_border
        sh.line.width = Pt(1.2)
        
        # Textbox on top with dark runs
        tx = s3.shapes.add_textbox(Inches(1.0), top + Inches(0.12), Inches(11.33), Inches(0.9))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        r_t = p.add_run()
        r_t.text = title + ": "
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(12.5)
        r_t.font.bold = True
        r_t.font.color.rgb = c_navy
        
        r_d = p.add_run()
        r_d.text = desc
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(11)
        r_d.font.color.rgb = c_dark

    # ==================== SLIDE 4: Literature Audit ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_white_bg(s4)
    add_slide_header(s4, "3. Literature Audit: Findings from Consensus AI")
    
    t_shape = s4.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    t = t_shape.table
    t.columns[0].width = Inches(1.8)
    t.columns[1].width = Inches(2.2)
    t.columns[2].width = Inches(2.4)
    t.columns[3].width = Inches(2.6)
    t.columns[4].width = Inches(2.73)
    
    headers_lit = ["Study & Year", "Architecture", "Core Features", "Problem Solved", "Unaddressed Gap"]
    for i, h in enumerate(headers_lit):
        c = t.cell(0, i)
        c.text = ""
        c.fill.solid()
        c.fill.fore_color.rgb = c_navy
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = c_white
        
    lit_rows = [
        ("Afieroho et al. (2023)", "Web E-Gov Survey", "Citizen adoption survey of public project tracking", "Showed public willingness to adopt digital monitoring", "Survey only; no working software tool with photo reporting."),
        ("Farouq et al. (2017)", "Database Audit", "Kano road defect logs & user satisfaction survey", "Demonstrated dissatisfaction with manual defect logging", "Paper-based; no citizen-facing web or mobile platform."),
        ("Sese (2020)", "Client-Server DB", "Centralized traffic offence database for FRSC", "Shared offence records across state commands", "Internal officers only; no citizen reporting or road defect logs."),
        ("Audu et al. (2021)", "Spatial GIS", "Crash hotspot map & shortest ambulance routes", "Improved post-crash ambulance response times", "Post-crash only; no defect prevention or public reporting.")
    ]
    for r_idx, row in enumerate(lit_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t.cell(r_idx, c_idx)
            c.text = ""
            c.fill.solid()
            c.fill.fore_color.rgb = c_light_bg if r_idx % 2 == 1 else c_white
            p = c.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            r.font.color.rgb = c_dark
            if c_idx == 0:
                r.font.bold = True

    # ==================== SLIDE 5: Value-Add Delta ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_white_bg(s5)
    add_slide_header(s5, "4. Proposed Improvement: The Value-Add Delta")
    
    t_shape = s5.shapes.add_table(5, 3, Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    t = t_shape.table
    t.columns[0].width = Inches(2.5)
    t.columns[1].width = Inches(4.5)
    t.columns[2].width = Inches(4.73)
    
    headers_val = ["Functional Area", "Standard / Existing Practice", "Proposed NRMS Contribution (Value-Add Delta)"]
    for i, h in enumerate(headers_val):
        c = t.cell(0, i)
        c.text = ""
        c.fill.solid()
        c.fill.fore_color.rgb = c_navy
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = c_white
        
    val_rows = [
        ("Citizen Defect Reporting", "Slow verbal complaints or unverified social media posts without location data.", "Simple web and mobile interface where citizens report potholes and violations with photos and GPS."),
        ("Contractor Progress Tracking", "Contractor-submitted paperwork with little or no public photo verification.", "Contractor portal requiring timestamped progress photos for each milestone before inspection sign-off."),
        ("Inspection Alerts", "Irregular manual visits with no automated reminder system when inspections are overdue.", "Automated background engine that checks the database daily and sends email/SMS alerts (> 30 days)."),
        ("Official Dashboard & Analytics", "Disorganized paper files and separate spreadsheets with no interactive map.", "Central dashboard showing monitored roads, critical road counts, and overdue inspections on a map.")
    ]
    for r_idx, row in enumerate(val_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t.cell(r_idx, c_idx)
            c.text = ""
            c.fill.solid()
            c.fill.fore_color.rgb = c_blue_tint if c_idx == 2 else (c_light_bg if r_idx % 2 == 1 else c_white)
            p = c.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            r.font.color.rgb = c_navy if c_idx == 2 else c_dark
            if c_idx == 0 or c_idx == 2:
                r.font.bold = True

    # ==================== SLIDE 6: One Project Aim ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_white_bg(s6)
    add_slide_header(s6, "5. One Overarching Project Aim (The Golden Rule)")
    
    # Background Box
    sh = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(10.33), Inches(3.0))
    sh.fill.solid()
    sh.fill.fore_color.rgb = c_blue_tint
    sh.line.color.rgb = c_navy
    sh.line.width = Pt(2)
    
    # Textbox layered on top
    tx = s6.shapes.add_textbox(Inches(1.8), Inches(2.5), Inches(9.73), Inches(2.4))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r_tag = p.add_run()
    r_tag.text = "THE OVERARCHING PROJECT AIM"
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(14)
    r_tag.font.bold = True
    r_tag.font.color.rgb = c_navy
    
    p2 = tf.add_paragraph()
    p2.space_before = Pt(14)
    p2.alignment = PP_ALIGN.CENTER
    r_aim = p2.add_run()
    r_aim.text = '"To design, implement, and test a web-based Nigeria Road Management System (NRMS) that enables citizen defect and violation reporting, tracks construction progress, and alerts officials to overdue inspections."'
    r_aim.font.name = "Calibri"
    r_aim.font.size = Pt(19)
    r_aim.font.bold = True
    r_aim.font.color.rgb = c_navy
    
    tx2 = s6.shapes.add_textbox(Inches(1.5), Inches(5.6), Inches(10.33), Inches(1.0))
    tf2 = tx2.text_frame
    p_note = tf2.paragraphs[0]
    p_note.alignment = PP_ALIGN.CENTER
    r_note = p_note.add_run()
    r_note.text = "Strict adherence to departmental guideline: Exactly ONE clear, overarching aim with no competing secondary aims."
    r_note.font.name = "Calibri"
    r_note.font.italic = True
    r_note.font.size = Pt(12)
    r_note.font.color.rgb = c_grey

    # ==================== SLIDE 7: Three Objectives ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_white_bg(s7)
    add_slide_header(s7, "6. Project Milestones: Exactly Three Objectives")
    
    objs = [
        ("OBJECTIVE 1: DESIGN", [
            "Architecture, Database & UI Wireframes",
            "",
            "• Multi-tier system architecture specification",
            "• PostgreSQL + PostGIS database schema",
            "• Responsive web wireframes for citizens, contractors, and road officials"
        ], Inches(0.8)),
        ("OBJECTIVE 2: IMPLEMENT", [
            "Core Software Modules",
            "",
            "• Citizen reporting portal with photo uploads & GPS",
            "• Contractor milestone progress tracker",
            "• Automated overdue inspection alert engine",
            "• Officials' spatial monitoring dashboard"
        ], Inches(4.7)),
        ("OBJECTIVE 3: TEST", [
            "System Testing & Validation",
            "",
            "• Functional testing across all modules",
            "• Verification of duplicate report detection",
            "• Testing alert dispatch under simulated delays",
            "• Usability testing across sample user roles"
        ], Inches(8.6))
    ]
    for tag, bullets, left in objs:
        add_card_box(s7, left, Inches(1.8), Inches(3.9), Inches(5.1), tag, bullets, c_light_bg, c_navy)

    # ==================== SLIDE 8: Proposed System Overview ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_white_bg(s8)
    add_slide_header(s8, "7. Proposed System Overview")
    
    mods = [
        ("Citizen Reporting Portal", "Citizens use a web or mobile browser to report potholes, erosion, or traffic violations, attaching a photo and submitting automatic GPS coordinates.", Inches(0.8), Inches(1.8)),
        ("Contractor Portal", "Road contractors log into their portal to view assigned road projects, upload on-site progress photos, and submit milestone completion updates.", Inches(6.8), Inches(1.8)),
        ("Inspection Alert Engine", "A background engine scans road records daily and automatically sends SMS/email alerts to engineers when an inspection is overdue (> 30 days).", Inches(0.8), Inches(4.3)),
        ("Officials Dashboard", "Officials monitor road conditions on an interactive map, view counts of critical roads and ongoing projects, and assign maintenance teams.", Inches(6.8), Inches(4.3))
    ]
    for title, desc, left, top in mods:
        sh = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        sh.fill.solid()
        sh.fill.fore_color.rgb = c_blue_tint
        sh.line.color.rgb = c_navy
        sh.line.width = Pt(1.4)
        
        tx = s8.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.2), Inches(1.8))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        r_t = p.add_run()
        r_t.text = title
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(14)
        r_t.font.bold = True
        r_t.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        r_d = p2.add_run()
        r_d.text = desc
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(11)
        r_d.font.color.rgb = c_dark

    # ==================== SLIDE 9: System Architecture Diagram ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_white_bg(s9)
    add_slide_header(s9, "8. Multi-Tier System Architecture Diagram")
    
    img_path = 'figures/extracted/img_2.png' if os.path.exists('figures/extracted/img_2.png') else 'figures/nrms_clean_architecture.png'
    if os.path.exists(img_path):
        s9.shapes.add_picture(img_path, Inches(1.8), Inches(1.6), width=Inches(9.73))

    # ==================== SLIDE 10: Component Breakdown ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_white_bg(s10)
    add_slide_header(s10, "9. Architecture Component Details")
    
    tiers_s10 = [
        ("Tier 1: Client Tier", [
            "• Citizen web & mobile reporting form",
            "• Contractor milestone progress portal",
            "• Officials' interactive map dashboard"
        ], Inches(0.8)),
        ("Tier 2: Logic Tier", [
            "• User authentication & role control",
            "• FastAPI application service endpoints",
            "• Report manager with duplicate checking",
            "• Inspection alert scheduler & map service"
        ], Inches(3.8)),
        ("Tier 3: Data Tier", [
            "• PostgreSQL + PostGIS (or MySQL)",
            "• Cloudinary / AWS S3 (photo storage)",
            "• Redis (caching and task queues)"
        ], Inches(6.8)),
        ("Tier 4: Output Tier", [
            "• Leaflet.js interactive road map",
            "• SMS & email notification gateways",
            "• PDF/CSV report generation for officials"
        ], Inches(9.8))
    ]
    for title, bullets, left in tiers_s10:
        add_card_box(s10, left, Inches(1.8), Inches(2.73), Inches(5.1), title, bullets, c_light_bg, c_navy)

    # ==================== SLIDE 11: Tech Stack ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_white_bg(s11)
    add_slide_header(s11, "10. Proposed Technology Stack")
    
    t_shape = s11.shapes.add_table(6, 3, Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    t = t_shape.table
    t.columns[0].width = Inches(2.5)
    t.columns[1].width = Inches(3.2)
    t.columns[2].width = Inches(6.03)
    
    headers_tech = ["Layer", "Technology Selected", "Practical Reason for Selection"]
    for i, h in enumerate(headers_tech):
        c = t.cell(0, i)
        c.text = ""
        c.fill.solid()
        c.fill.fore_color.rgb = c_navy
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = c_white
        
    stack_rows = [
        ("Frontend (Client)", "HTML, CSS, JavaScript (React)", "Responsive on mobile devices; fast loading and modular UI components."),
        ("Backend (Logic)", "Python (FastAPI Framework)", "Course-designated framework; high-throughput asynchronous API handling with migration path to Express."),
        ("Database (Data)", "PostgreSQL + PostGIS (or MySQL)", "Reliable relational database with spatial indexing for GPS coordinates and geographic clustering."),
        ("Media Storage", "Cloudinary (or AWS S3)", "Stores defect and progress photos safely without overloading the database."),
        ("Mapping & Alerts", "Leaflet.js + SMS / Email API", "Open-source map library without licensing fees; reliable alert delivery.")
    ]
    for r_idx, row in enumerate(stack_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t.cell(r_idx, c_idx)
            c.text = ""
            c.fill.solid()
            c.fill.fore_color.rgb = c_light_bg if r_idx % 2 == 1 else c_white
            p = c.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            r.font.color.rgb = c_dark
            if c_idx < 2:
                r.font.bold = True

    # ==================== SLIDE 12: Conclusion ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_white_bg(s12)
    add_slide_header(s12, "11. Conclusion & Expected Impact")
    
    impacts = [
        ("Empowering Citizens", [
            "• Turns ordinary commuters into 'the eyes of the system'.",
            "• Allows fast reporting of potholes, broken roads, and traffic violations with photos.",
            "• Fosters community participation in public infrastructure."
        ], Inches(0.8)),
        ("Contractor Accountability", [
            "• Encourages high construction quality across project sites.",
            "• Requires photographic evidence before milestones are approved.",
            "• Reduces project delays and premature road failures."
        ], Inches(4.7)),
        ("Better Official Oversight", [
            "• Provides road authorities with an up-to-date spatial dashboard.",
            "• Automated alert engine ensures overdue inspections are never missed.",
            "• Enhances data-driven maintenance planning."
        ], Inches(8.6))
    ]
    for title, bullets, left in impacts:
        add_card_box(s12, left, Inches(1.8), Inches(3.9), Inches(4.5), title, bullets, c_blue_tint, c_navy)
        
    tx_end = s12.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.73), Inches(0.6))
    tf_e = tx_end.text_frame
    p_e = tf_e.paragraphs[0]
    p_e.alignment = PP_ALIGN.CENTER
    r_e = p_e.add_run()
    r_e.text = "Thank you. We welcome your questions and feedback."
    r_e.font.name = "Calibri"
    r_e.font.size = Pt(14)
    r_e.font.bold = True
    r_e.font.color.rgb = c_navy

    out_file = "Nigeria_Road_Management_System_Defense_Deck_Phone_Fixed.pptx"
    prs.save(out_file)
    print(f"Phone-fixed presentation created at {out_file}")

if __name__ == "__main__":
    create_presentation()
