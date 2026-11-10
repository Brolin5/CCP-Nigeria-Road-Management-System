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
    
    c_white = RGBColor(255, 255, 255)
    c_navy = RGBColor(11, 83, 148) # NJC Blue
    c_dark = RGBColor(33, 33, 33)
    c_grey = RGBColor(100, 116, 139)
    c_light_bg = RGBColor(248, 250, 252)
    c_blue_tint = RGBColor(238, 242, 255)
    
    def set_white_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = c_white
        
    def add_slide_header(slide, title_text, category_text="NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)"):
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_grey
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = c_navy
        p_title.space_before = Pt(4)

    # ==================== SLIDE 1 ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)
    
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.33), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "NILE UNIVERSITY OF NIGERIA | DEPARTMENT OF COMPUTER SCIENCE"
    p0.font.name = "Calibri"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = c_grey
    
    p1 = tf.add_paragraph()
    p1.text = "Nigeria Road Management System: A Citizen-Centric Platform for Road Monitoring, Reporting, and Progress Tracking"
    p1.font.name = "Calibri"
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = c_navy
    p1.space_before = Pt(8)
    
    p2 = tf.add_paragraph()
    p2.text = "Undergraduate Software Engineering Project Defense | Academic Session 2025/2026"
    p2.font.name = "Calibri"
    p2.font.size = Pt(13)
    p2.font.color.rgb = c_grey
    p2.space_before = Pt(6)
    
    table_shape = s1.shapes.add_table(7, 3, Inches(1.5), Inches(3.3), Inches(10.33), Inches(3.4))
    table = table_shape.table
    table.columns[0].width = Inches(1.0)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(6.33)
    
    headers = ["S/N", "Matriculation No.", "Full Student Name & Role"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_white
        
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
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_light_bg if row_idx % 2 == 1 else c_white
            p = cell.text_frame.paragraphs[0]
            if col_idx < 2:
                p.alignment = PP_ALIGN.CENTER
            else:
                p.alignment = PP_ALIGN.LEFT
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.font.color.rgb = c_dark
            if "Leader" in val:
                p.font.bold = True
                p.font.color.rgb = c_navy

    # ==================== SLIDE 2 ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)
    add_slide_header(s2, "1. Introduction & Background")
    
    cards = [
        ("Nigeria Road Network", "• Over 193,200 km of roads (largest in West Africa).\n• Carries over 90% of passenger and freight traffic.\n• Vital for interstate trade and daily commuting.", Inches(0.8)),
        ("Current Road Conditions", "• Frequent potholes, erosion, and broken bridges.\n• Causes severe vehicle damage and travel delays.\n• High financial burden on motorists and businesses.", Inches(4.7)),
        ("Management Inefficiencies", "• Roads managed by separate federal, state, and local agencies.\n• Reliance on manual visits and paper records.\n• No simple way for citizens to report problems with photos.", Inches(8.6))
    ]
    for title, body, left in cards:
        shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.9), Inches(5.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_blue_tint
        shape.line.color.rgb = c_navy
        tf = shape.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = c_navy
        
        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = c_dark
        p_b.space_before = Pt(12)

    # ==================== SLIDE 3 ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_white_bg(s3)
    add_slide_header(s3, "2. Problem Statement: Key Flaws in the Current System")
    
    flaws = [
        ("1. Slow Defect Reporting", "Citizens have no direct way to report potholes and road damage with photos and GPS locations. Complaints take months to reach maintenance units (Farouq et al., 2017).", Inches(1.8)),
        ("2. Contractor Opacity", "Construction and repair progress is not tracked using open photo records, allowing substandard materials and delayed milestones to go unverified (Adepoju, 2021).", Inches(3.1)),
        ("3. Unchecked Traffic Violations", "Driving against one-way traffic, illegal parking, and dumping dirt on roads frequently occur without penalty because officers cannot be everywhere (Umar et al., 2021).", Inches(4.4)),
        ("4. Missed Inspection Cycles", "Maintenance agencies lack an automated alert system when road inspections or contractor site checks are overdue (Odinfono & Olawole, 2024).", Inches(5.7))
    ]
    for title, desc, top in flaws:
        shape = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_light_bg
        shape.line.color.rgb = c_navy
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(2)

    # ==================== SLIDE 4 ====================
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
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = c_navy
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = c_white
        
    lit_rows = [
        ("Afieroho et al. (2023)", "Web E-Gov Survey", "Citizen adoption survey of public project tracking", "Showed public willingness to adopt digital monitoring", "Survey only; no working software tool with photo reporting."),
        ("Farouq et al. (2017)", "Database Audit", "Kano road defect logs & user satisfaction survey", "Demonstrated dissatisfaction with manual defect logging", "Paper-based; no citizen-facing web or mobile platform."),
        ("Sese (2020)", "Client-Server DB", "Centralized traffic offence database for FRSC", "Shared offence records across state commands", "Internal officers only; no citizen reporting or road defect logs."),
        ("Audu et al. (2021)", "Spatial GIS", "Crash hotspot map & shortest ambulance routes", "Improved post-crash ambulance response times", "Post-crash only; no defect prevention or public reporting.")
    ]
    for r_idx, row in enumerate(lit_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = c_light_bg if r_idx % 2 == 1 else c_white
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = c_dark
            if c_idx == 0:
                p.font.bold = True

    # ==================== SLIDE 5 ====================
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
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = c_navy
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = c_white
        
    val_rows = [
        ("Citizen Defect Reporting", "Slow verbal complaints or unverified social media posts without location data.", "Simple web and mobile interface where citizens report potholes and violations with photos and GPS."),
        ("Contractor Progress Tracking", "Contractor-submitted paperwork with little or no public photo verification.", "Contractor portal requiring timestamped progress photos for each milestone before inspection sign-off."),
        ("Inspection Alerts", "Irregular manual visits with no automated reminder system when inspections are overdue.", "Automated background engine that checks the database daily and sends email/SMS alerts (> 30 days)."),
        ("Official Dashboard & Analytics", "Disorganized paper files and separate spreadsheets with no interactive map.", "Central dashboard showing monitored roads, critical road counts, and overdue inspections on a map.")
    ]
    for r_idx, row in enumerate(val_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = c_blue_tint if c_idx == 2 else (c_light_bg if r_idx % 2 == 1 else c_white)
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = c_navy if c_idx == 2 else c_dark
            if c_idx == 0 or c_idx == 2:
                p.font.bold = True

    # ==================== SLIDE 6 ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_white_bg(s6)
    add_slide_header(s6, "5. One Overarching Project Aim (The Golden Rule)")
    
    shape = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(10.33), Inches(3.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = c_blue_tint
    shape.line.color.rgb = c_navy
    shape.line.width = Pt(2)
    tf = shape.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "THE OVERARCHING PROJECT AIM"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy
    
    p2 = tf.add_paragraph()
    p2.text = '"To design, implement, and test a web-based Nigeria Road Management System (NRMS) that enables citizen defect and violation reporting, tracks construction progress, and alerts officials to overdue inspections."'
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Calibri"
    p2.font.size = Pt(19)
    p2.font.bold = True
    p2.font.color.rgb = c_navy
    p2.space_before = Pt(16)
    
    tx = s6.shapes.add_textbox(Inches(1.5), Inches(5.6), Inches(10.33), Inches(1.0))
    tf2 = tx.text_frame
    p_note = tf2.paragraphs[0]
    p_note.text = "Strict adherence to departmental guideline: Exactly ONE clear, overarching aim with no competing secondary aims."
    p_note.alignment = PP_ALIGN.CENTER
    p_note.font.italic = True
    p_note.font.size = Pt(12)
    p_note.font.color.rgb = c_grey

    # ==================== SLIDE 7 ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_white_bg(s7)
    add_slide_header(s7, "6. Project Milestones: Exactly Three Objectives")
    
    objs = [
        ("OBJECTIVE 1: DESIGN", "Architecture, Database & UI", "• Multi-tier system architecture\n• PostgreSQL + PostGIS database schema\n• Responsive web wireframes for citizens, contractors, and officials", Inches(0.8)),
        ("OBJECTIVE 2: IMPLEMENT", "Core Software Modules", "• Citizen reporting with photo uploads\n• Contractor milestone progress tracker\n• Automated overdue inspection alert engine\n• Officials' monitoring dashboard", Inches(4.7)),
        ("OBJECTIVE 3: TEST", "System Testing & Validation", "• Functional testing of all modules\n• Verification of duplicate report detection\n• Testing of alert dispatch under sample delays\n• Usability testing across user roles", Inches(8.6))
    ]
    for tag, subtitle, body, left in objs:
        shape = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.9), Inches(5.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_light_bg
        shape.line.color.rgb = c_navy
        tf = shape.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = c_navy
        p_sub.font.bold = True
        p_sub.space_before = Pt(4)
        
        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = c_dark
        p_b.space_before = Pt(14)

    # ==================== SLIDE 8 ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_white_bg(s8)
    add_slide_header(s8, "7. Proposed System Overview")
    
    modules = [
        ("Citizen Reporting Portal", "Citizens use a web or mobile browser to report potholes, erosion, or traffic violations, attaching a photo and submitting automatic GPS coordinates.", Inches(0.8), Inches(1.8)),
        ("Contractor Portal", "Road contractors log into their portal to view assigned road projects, upload on-site progress photos, and submit milestone completion updates.", Inches(6.8), Inches(1.8)),
        ("Inspection Alert Engine", "A background engine scans road records daily and automatically sends SMS/email alerts to engineers when an inspection is overdue (> 30 days).", Inches(0.8), Inches(4.3)),
        ("Officials Dashboard", "Officials monitor road conditions on an interactive map, view counts of critical roads and ongoing projects, and assign maintenance teams.", Inches(6.8), Inches(4.3))
    ]
    for title, desc, left, top in modules:
        shape = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_blue_tint
        shape.line.color.rgb = c_navy
        tf = shape.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(8)

    # ==================== SLIDE 9: System Architecture Diagram ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_white_bg(s9)
    add_slide_header(s9, "8. Multi-Tier System Architecture Diagram")
    
    img_path = 'figures/nrms_clean_architecture.png'
    if os.path.exists(img_path):
        s9.shapes.add_picture(img_path, Inches(1.8), Inches(1.6), width=Inches(9.73))

    # ==================== SLIDE 10 ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_white_bg(s10)
    add_slide_header(s10, "9. Architecture Component Details")
    
    tiers = [
        ("Tier 1: Client Tier", "• Citizen web & mobile reporting form\n• Contractor milestone progress portal\n• Officials' interactive map dashboard", Inches(0.8)),
        ("Tier 2: Logic Tier", "• User authentication & role control\n• Report manager with duplicate checking\n• Contractor milestone progress module\n• Inspection alert scheduler & map service", Inches(3.8)),
        ("Tier 3: Data Tier", "• PostgreSQL + PostGIS (spatial tables)\n• Cloudinary / AWS S3 (photo storage)\n• Redis (caching and task queues)", Inches(6.8)),
        ("Tier 4: Output Tier", "• Leaflet.js interactive road map\n• SMS & email notification gateways\n• PDF/CSV report generation for officials", Inches(9.8))
    ]
    for title, body, left in tiers:
        shape = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), Inches(2.73), Inches(5.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_light_bg
        shape.line.color.rgb = c_navy
        tf = shape.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(12)

    # ==================== SLIDE 11 ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_white_bg(s11)
    add_slide_header(s11, "10. Proposed Technology Stack")
    
    t_shape = s11.shapes.add_table(6, 3, Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    t = t_shape.table
    t.columns[0].width = Inches(2.5)
    t.columns[1].width = Inches(3.0)
    t.columns[2].width = Inches(6.23)
    
    headers_tech = ["Layer", "Technology Selected", "Practical Reason for Selection"]
    for i, h in enumerate(headers_tech):
        c = t.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = c_navy
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = c_white
        
    stack_rows = [
        ("Frontend (Client)", "Next.js (React) + Tailwind CSS", "Responsive on mobile devices; fast loading and modular UI components."),
        ("Backend (Logic)", "Node.js + Express.js", "Asynchronous non-blocking I/O; efficiently handles concurrent photo uploads."),
        ("Database (Data)", "PostgreSQL + PostGIS", "Reliable relational database with native support for GPS latitude and longitude."),
        ("Media Storage", "Cloudinary (or AWS S3)", "Stores defect and progress photos safely without overloading the database."),
        ("Mapping & Alerts", "Leaflet.js + SMS / Email API", "Open-source map library without licensing fees; reliable alert delivery.")
    ]
    for r_idx, row in enumerate(stack_rows, start=1):
        for c_idx, val in enumerate(row):
            c = t.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = c_light_bg if r_idx % 2 == 1 else c_white
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = c_dark
            if c_idx < 2:
                p.font.bold = True

    # ==================== SLIDE 12 ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_white_bg(s12)
    add_slide_header(s12, "11. Conclusion & Expected Impact")
    
    impacts = [
        ("Empowering Citizens", "Turns ordinary commuters into 'the eyes of the system' by allowing them to quickly report potholes, broken roads, and traffic violations with photos.", Inches(0.8)),
        ("Contractor Accountability", "Encourages quality construction by requiring photo evidence of progress before project milestones are signed off.", Inches(4.7)),
        ("Better Official Decision-Making", "Provides road agencies with an up-to-date map dashboard and automated alerts so overdue inspections are never missed.", Inches(8.6))
    ]
    for title, desc, left in impacts:
        shape = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.9), Inches(4.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_blue_tint
        shape.line.color.rgb = c_navy
        tf = shape.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(14)
        
    p_end = s12.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.73), Inches(0.6))
    tf_e = p_end.text_frame
    p_e = tf_e.paragraphs[0]
    p_e.text = "Thank you. We welcome your questions and feedback."
    p_e.alignment = PP_ALIGN.CENTER
    p_e.font.name = "Calibri"
    p_e.font.size = Pt(14)
    p_e.font.bold = True
    p_e.font.color.rgb = c_navy

    out_file = "Nigeria_Road_Management_System_Defense_Deck_Updated.pptx"
    prs.save(out_file)
    print(f"Presentation successfully updated at {out_file}")

if __name__ == "__main__":
    create_presentation()
