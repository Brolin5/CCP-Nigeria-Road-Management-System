import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Nigeria Road Management System | Nile University of Nigeria")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Science - Project Documentation: Chapters 1 & 2")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

def create_document():
    doc = docx.Document()
    add_header_footer(doc)
    
    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(30, 30, 30)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)
    
    # ==================== TITLE PAGE ====================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(6)
    
    r_uni = title_p.add_run("NILE UNIVERSITY OF NIGERIA\n")
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(16)
    r_uni.bold = True
    r_uni.font.color.rgb = RGBColor(26, 35, 126) # Navy Blue
    
    r_fac = title_p.add_run("FACULTY OF NATURAL AND APPLIED SCIENCES\nDEPARTMENT OF COMPUTER SCIENCE\n\n")
    r_fac.font.name = "Times New Roman"
    r_fac.font.size = Pt(13)
    r_fac.bold = True
    r_fac.font.color.rgb = RGBColor(55, 71, 79)
    
    title_box = doc.add_paragraph()
    title_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_box.paragraph_format.space_before = Pt(16)
    title_box.paragraph_format.space_after = Pt(16)
    r_proj = title_box.add_run("NIGERIA ROAD MANAGEMENT SYSTEM:\nA CITIZEN-CENTRIC PLATFORM FOR ROAD MONITORING, REPORTING, AND PROGRESS TRACKING\n")
    r_proj.font.name = "Times New Roman"
    r_proj.font.size = Pt(15)
    r_proj.bold = True
    r_proj.font.color.rgb = RGBColor(26, 35, 126)
    
    sub_proj = title_box.add_run("\nA Technical Proposal and Multi-Tier Architectural Specification Submitted in Partial Fulfillment of the Requirements for Undergraduate Group Project Evaluation")
    sub_proj.font.name = "Times New Roman"
    sub_proj.font.size = Pt(11)
    sub_proj.italic = True
    sub_proj.font.color.rgb = RGBColor(90, 90, 90)
    
    # Members Table
    p_mem = doc.add_paragraph()
    p_mem.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mem.paragraph_format.space_before = Pt(14)
    p_mem.paragraph_format.space_after = Pt(6)
    r_team = p_mem.add_run("PROJECT GROUP MEMBERS ROSTER")
    r_team.bold = True
    r_team.font.size = Pt(11.5)
    r_team.font.color.rgb = RGBColor(26, 35, 126)
    
    table_m = doc.add_table(rows=7, cols=4)
    table_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_m.autofit = False
    
    headers = ["S/N", "Matriculation No.", "Full Student Name", "Designated Role"]
    col_widths = [Inches(0.6), Inches(1.8), Inches(2.8), Inches(1.5)]
    
    hdr_cells = table_m.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1A237E")
        set_cell_margins(hdr_cells[i], 100, 100, 150, 150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    members_data = [
        ("1", "241030116", "Chibuzor Clinton AGADA", "Group Leader"),
        ("2", "241030026", "Ephraim Ayokunle Tackie OFOLI", "Group Member"),
        ("3", "241030081", "Isaac Akorede-Abayomi ODUJOKO", "Group Member"),
        ("4", "241030123", "Aisha Mohammed RASHEED", "Group Member"),
        ("5", "241030021", "Prince Arinze Wenceslaus OBINABO", "Group Member"),
        ("6", "241030039", "Mubarak Ibrahim AUDU", "Group Member")
    ]
    
    for row_idx, data in enumerate(members_data, start=1):
        row_cells = table_m.rows[row_idx].cells
        bg_col = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 70, 70, 120, 120)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5)
                if col_idx == 3 and "Leader" in text:
                    r.bold = True
                    r.font.color.rgb = RGBColor(26, 35, 126)
                    
    for row in table_m.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width
            
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(24)
    r_sub = p_sub.add_run("Department of Computer Science\nFaculty of Natural and Applied Sciences\nNile University of Nigeria, Abuja, FCT\nAcademic Session: 2025/2026")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(55, 71, 79)
    
    doc.add_page_break()
    
    # Helper functions for sections
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(15)
        r.bold = True
        r.font.color.rgb = RGBColor(26, 35, 126)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = RGBColor(40, 53, 147)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.bold = True
        r.font.color.rgb = RGBColor(55, 71, 79)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_b = p.add_run(bold_prefix + ": ")
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(12)
        r_b.bold = True
        r_t = p.add_run(text)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(12)
        return p

    # ==================== ABSTRACT ====================
    p_abs_title = doc.add_paragraph()
    p_abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_title.paragraph_format.space_before = Pt(12)
    p_abs_title.paragraph_format.space_after = Pt(8)
    r_abs_t = p_abs_title.add_run("ABSTRACT")
    r_abs_t.font.name = "Times New Roman"
    r_abs_t.font.size = Pt(14)
    r_abs_t.bold = True
    r_abs_t.font.color.rgb = RGBColor(26, 35, 126)
    
    add_body(
        "Nigeria’s road transport infrastructure continues to suffer severe premature deterioration as a consequence of the use of substandard construction materials, "
        "misuse of capital appropriations, weak coordination across supervisory tiers, and continued reliance on manual, paper-based inspection procedures. "
        "Existing road management practices lack transparency, provide no standardized digital conduits for public defect or violation reporting, and fail to track ongoing contractor execution empirically. "
        "This project presents the design and architectural modeling of the Nigeria Road Management System (NRMS), a citizen-centric software platform engineered to bridge the operational divide "
        "between road users, construction contractors, and governmental authorities. The platform allows citizens to submit geotagged road defect reports and traffic infractions with photographic evidence, "
        "enforces contractor accountability through milestone progress photograph uploads, deploys an automated background scheduler to issue alerts for overdue road inspections, "
        "and supplies supervisory engineers with a spatial administrative dashboard. Built upon a decoupled four-tier architecture (Client, Logic, Data, and Output tiers), "
        "the system addresses critical gaps documented in empirical literature, advancing civic participation, maintenance transparency, and data-driven infrastructure stewardship in Nigeria."
    )
    
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_after = Pt(18)
    r_kw_lbl = p_kw.add_run("Keywords: ")
    r_kw_lbl.font.name = "Times New Roman"
    r_kw_lbl.font.size = Pt(11)
    r_kw_lbl.bold = True
    r_kw_txt = p_kw.add_run("Citizen reporting, road management system, crowdsourcing, construction progress tracking, inspection alerts, spatial dashboard, e-government, Nigeria infrastructure.")
    r_kw_txt.font.name = "Times New Roman"
    r_kw_txt.font.size = Pt(11)
    r_kw_txt.italic = True
    
    doc.add_page_break()

    # ==================== CHAPTER 1 ====================
    add_h1("CHAPTER 1: INTRODUCTION")
    
    add_h2("1.1 Domain Background")
    add_body(
        "Road transportation constitutes the predominant backbone of passenger mobility and freight distribution within developing economies. "
        "Nigeria possesses the largest road network in West Africa and the second largest south of the Sahara, spanning approximately 193,200 kilometers (Farouq et al., 2017). "
        "This extensive transportation artery accounts for over 90% of all inland socioeconomic vehicular traffic across urban centers and inter-state trade routes. "
        "Notwithstanding this indispensable strategic importance, the Nigerian road network is afflicted by accelerated physical deterioration, recurrent pavement distress, "
        "and systemic operational failures (Adepoju, 2021). The prevailing status of national road infrastructure is characterized by severe asphalt failures, unmanaged potholes, "
        "defective drainage channels, and widespread pavement degradation, precipitating catastrophic road traffic collisions, excessive vehicular operational depreciation, "
        "and staggering macroeconomic losses estimated to exceed 175 billion Naira annually (Jaiye & Elisha, 2020)."
    )
    add_body(
        "The administration and preservation of road infrastructure in Nigeria are institutionally fragmented across three administrative tiers: the Federal Road Maintenance Agency (FERMA) "
        "and Federal Ministry of Works at the federal level, State Ministries of Works and Infrastructure at the state tier, and Local Government Councils across municipal domains (Ogbu & Ezeh, 2019; Olojede et al., 2019). "
        "Concurrently, the enforcement of road safety regulations, traffic orderliness, and vehicular compliance falls under the statutory mandate of the Federal Road Safety Corps (FRSC) and State Traffic Management Agencies (Ajiboye et al., 2020; Tubobereni & Ikiriko, 2019). "
        "Historically, these institutions have operated via traditional, manual surveillance, physical inspections, and reactive paper-based defect reporting workflows (Odinfono & Olawole, 2024; Farouq et al., 2017). "
        "Physical inspection officers cannot feasibly maintain continuous surveillance over vast, dispersed road corridors. Consequently, road defects often deteriorate into severe structural cratering before regulatory discovery, "
        "while acute traffic infractions—including driving against directional traffic ('one-way'), illicit carriageway parking, and illegal refuse dumping—frequently transpire without deterrence or accountability (Umar et al., 2021; Medayese et al., 2019)."
    )
    add_body(
        "Modern computer science and e-governance paradigms demonstrate that participatory mobile crowdsensing and centralized geospatial web architectures offer transformative alternatives to legacy municipal surveillance models (Afieroho et al., 2023; Gambo & Musonda, 2021). "
        "By empowering road users—including motorists, transit operators, pedestrians, and local residents—with ubiquitous web and mobile interfaces to capture and transmit geotagged evidentiary reports, "
        "ordinary citizens can function as distributed sensory agents across the road network. When combined with automated construction milestone tracking, digital inspection escalation engines, "
        "and administrative decision-support spatial dashboards, computerized management frameworks provide unprecedented transparency, operational coordination, and empirical prioritization in highway asset stewardship."
    )
    
    add_h2("1.2 Problem Statement")
    add_body(
        "The management of road infrastructure and traffic enforcement in Nigeria suffers from systemic inefficiencies, acute governance deficits, and technological disconnects. "
        "An investigation into the domain friction reveals four core deficiencies in the operational status quo:"
    )
    add_bullet(
        "Absence of Real-Time Defect Capture",
        "Pavement distress, potholes, and erosion gullies currently rely on manual, sporadic officer patrols or informal complaints, resulting in months of latency before defects are cataloged, during which road safety rapidly deteriorates (Farouq et al., 2017; Babatunde et al., 2019)."
    )
    add_bullet(
        "Contractor Opacity and Quality Deficits",
        "Public road construction and maintenance contracts frequently utilize substandard asphalt and base materials, suffering from chronic project delays and abandoned milestones due to the lack of transparent, verifiable progress monitoring and public accountability mechanisms (Adepoju, 2021; Ugochi, 2020)."
    )
    add_bullet(
        "Pervasive Unchecked Traffic Infractions",
        "Pervasive violations—such as driving against traffic flow, speeding, obstructionist parking, and debris dumping—occur outside the localized physical presence of enforcement marshals, with no civic reporting conduit allowing road users to submit photographic and geospatial evidence (Umar et al., 2021; Ndugbu & Ndugbu, 2021)."
    )
    add_bullet(
        "Siloed Data and Lack of Decision-Support Analytics",
        "Road authorities operate without centralized spatial decision-support dashboards and automated inspection alert engines, leaving maintenance managers unable to identify critical road clusters, overdue inspections, or contractor performance deficits empirically (Audu et al., 2021; Ashara et al., 2020)."
    )
    add_body(
        "In the absence of a unified, computerized system bridging the informational divide between road users, construction contractors, and supervisory government agencies, "
        "public infrastructure will continue to experience premature structural degradation, fund misallocation, and elevated road crash risks. "
        "Therefore, there exists a critical engineering imperative to develop a centralized, citizen-centric road infrastructure monitoring and traffic violation reporting software platform."
    )
    
    add_h2("1.3 Research Questions")
    add_body(
        "To guide the systematic design, development, and algorithmic validation of the proposed system, this project addresses exactly three research inquiries formulated in direct alignment with the operational domain challenges:"
    )
    add_bullet(
        "Research Question 1 (Current Methods)",
        "What methods are currently used in Nigeria to manage road construction, maintenance, monitoring, and enforcement of traffic rules?"
    )
    add_bullet(
        "Research Question 2 (Systemic Limitations)",
        "What are the major limitations of the existing approaches to road management, especially regarding transparency, coordination, quality of materials, and public reporting?"
    )
    add_bullet(
        "Research Question 3 (Software Interventions)",
        "What features should a computerized Nigeria Road Management System include to enable citizen reporting, track construction progress, monitor road conditions, and support better decision-making by officials?"
    )
    
    add_h2("1.4 Project Aim")
    add_body(
        "The overarching aim of this project is to design, implement, and evaluate a web-based crowdsourced Nigeria Road Management System (NRMS) "
        "to enhance road maintenance transparency, defect triage, and civic accountability in Nigeria."
    )
    
    add_h2("1.5 Project Objectives")
    add_body(
        "In strict conformity with the departmental project lifecycle milestones, the project encompasses exactly three measurable objectives:"
    )
    add_bullet(
        "Objective 1: Design",
        "To design a multi-tier system architecture, spatial-relational database schema, and role-based user interfaces for civic crowdsourcing, contractor milestone tracking, and administrative decision-support."
    )
    add_bullet(
        "Objective 2: Implement",
        "To implement the core functional software modules, encompassing geotagged citizen defect and violation reporting with media uploads, contractor construction milestone tracking with photographic verification, an automated overdue inspection notification engine, and an interactive GIS spatial triage dashboard."
    )
    add_bullet(
        "Objective 3: Test",
        "To test and validate the implemented software system for functional correctness, report submission latency, notification dispatch reliability, and end-user usability across civic users and administrative personnel."
    )
    
    add_h2("1.6 Existing Research (Literature Audit)")
    add_body(
        "A rigorous literature discovery was conducted using peer-reviewed academic datasets indexed via Consensus AI to evaluate previous computerized interventions in road infrastructure, e-governance, and traffic safety. "
        "In accordance with project guidelines, the surveyed literature was audited across five essential technical variables: (1) System Architecture Developed, (2) Core Features Included, (3) Technology Stack Applied, (4) Specific Problem Resolved, and (5) Unaddressed Limitations/Gaps."
    )
    add_body(
        "The literature review establishes that while computerized systems have been explored for isolated aspects of traffic enforcement and emergency routing in Nigeria, "
        "substantial gaps persist regarding civic crowdsourced reporting, transparent contractor auditing, and proactive inspection notification. "
        "Table 1.1 synthesizes the empirical audit of the primary surveyed studies."
    )
    
    # Table 1.1 Literature Matrix
    add_h3("Table 1.1: Academic Literature Audit Matrix Across Key System Variables")
    table_lit = doc.add_table(rows=6, cols=6)
    table_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_lit.autofit = False
    
    lit_headers = ["Authors & Year", "System Architecture", "Core Features", "Tech Stack Applied", "Problem Resolved", "Unaddressed Gaps"]
    lit_col_widths = [Inches(1.1), Inches(1.0), Inches(1.2), Inches(1.0), Inches(1.1), Inches(1.1)]
    
    hdr_l = table_lit.rows[0].cells
    for i, title in enumerate(lit_headers):
        hdr_l[i].text = title
        set_cell_background(hdr_l[i], "1A237E")
        set_cell_margins(hdr_l[i], 100, 100, 100, 100)
        p = hdr_l[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    lit_rows = [
        (
            "Afieroho et al. (2023)",
            "Web-based E-Government Framework",
            "Public project tracking, citizen perception indices, survey instruments",
            "SPSS, PLS-SEM, E-Gov Portal",
            "Demonstrated high public readiness to monitor public infrastructure via digital tools",
            "Lacked an operational software implementation; provided theoretical modeling without real-time photo/GIS reporting modules."
        ),
        (
            "Farouq et al. (2017)",
            "Manual & Relational Database Audit",
            "Road defect categorization, maintenance logging, questionnaire analysis",
            "SPSS, Average Index Analysis",
            "Identified severe failures and citizen dissatisfaction in Kano State road defect logging",
            "No automated web portal or mobile crowdsourcing; defect tracking was entirely paper-based and manual."
        ),
        (
            "Sese (2020)",
            "Client-Server Distributed Database",
            "Relational traffic offence logging, centralized FRSC data repository, report generation",
            "Client-Server, Distributed SQL RDBMS",
            "Centralized driver traffic offence records across state and LGA headquarters",
            "Restricted to internal FRSC officers; zero public civic reporting, no photo evidence upload, no road condition monitoring."
        ),
        (
            "Audu et al. (2021)",
            "Spatial Decision Support System (GIS)",
            "Kernel density crash hotspot mapping, Dijkstra shortest emergency path routing",
            "ArcGIS 10.3, Network Analyst, GPS",
            "Optimized post-crash ambulance response times in Ibadan North-East",
            "Focused solely on emergency medical routing post-accident; excluded infrastructure defect prevention and traffic infraction crowdsourcing."
        ),
        (
            "Umar et al. (2021)",
            "Image Processing Client-Server System",
            "k-NN vehicle license plate localization, optical character recognition (OCR)",
            "k-Nearest Neighbor, MATLAB, Digital Camera",
            "Automated vehicle identification during red-light jumping violations",
            "Required fixed camera hardware; failed to address mobile citizen violation reporting, parking abuse, or road defect tracking."
        )
    ]
    
    for row_idx, data in enumerate(lit_rows, start=1):
        row_cells = table_lit.rows[row_idx].cells
        bg_col = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 70, 70, 90, 90)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                
    for row in table_lit.rows:
        for idx, width in enumerate(lit_col_widths):
            row.cells[idx].width = width
            
    add_body(
        "Further examination of related literature in developing transport environments highlights persistent technical fragmentation. "
        "Dabo and Yunus (2020) demonstrated the effectiveness of QGIS-based road facility inventorying in Katsina, yet the system remained static and inaccessible to ordinary commuters. "
        "Akanbi and Abegunde (2020) proposed a mobile platform for vehicle registration and basic accident logging for the FRSC, but omitted construction milestone monitoring and road surface defect reporting. "
        "Moreover, Odinfono and Olawole (2024) discovered that over 55% of transportation and safety agencies in Southwest Nigeria still rely on disparate, non-standardized paper forms, "
        "severely impeding inter-agency coordination. Toriola-Coker et al. (2020) emphasized that the exclusion and marginalization of public road users represents the primary cause of failure in road infrastructure projects. "
        "These empirical findings confirm that existing systems remain siloed, officer-dependent, and reactive, underscoring the necessity for a multi-stakeholder, crowdsourced digital platform."
    )
    
    add_h2("1.7 Proposed Improvement (Value Proposition & Value-Add Delta)")
    add_body(
        "To overcome the deficiencies identified across existing computerized systems, the proposed Nigeria Road Management System (NRMS) introduces a distinct value-add contribution. "
        "Rather than building an isolated reporting portal, the proposed system establishes a cohesive, multi-tier software architecture that links road users, contractors, and governmental authorities. "
        "Table 1.2 delineates the comparative delta between baseline operational systems and the proposed solution."
    )
    
    # Table 1.2 Value-Add Delta
    add_h3("Table 1.2: System Value-Add Delta (Baseline Features vs. Proposed NRMS Contribution)")
    table_delta = doc.add_table(rows=5, cols=3)
    table_delta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_delta.autofit = False
    
    delta_headers = ["Functional Dimension", "Baseline / Existing Systems", "Proposed NRMS Contribution (Value-Add Delta)"]
    delta_col_widths = [Inches(1.8), Inches(2.3), Inches(2.4)]
    
    hdr_d = table_delta.rows[0].cells
    for i, title in enumerate(delta_headers):
        hdr_d[i].text = title
        set_cell_background(hdr_d[i], "1A237E")
        set_cell_margins(hdr_d[i], 100, 100, 120, 120)
        p = hdr_d[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    delta_rows = [
        (
            "Civic Incident & Defect Reporting",
            "Sporadic paper complaints, toll phone lines, or physical visits; no GPS tagging or evidentiary photo attachment.",
            "Unified mobile/web crowdsourcing interface with automated geolocation capture, categorized defect/violation selection, and mandatory photographic proof upload."
        ),
        (
            "Contractor Progress & Quality Tracking",
            "Opaque milestone documentation, manual contractor-submitted spreadsheets, no public verification of materials or progress.",
            "Dedicated contractor milestone portal requiring timestamped on-site photographic proof of construction stages before administrative approval."
        ),
        (
            "Inspection Scheduling & Quality Assurance",
            "Ad-hoc, uncoordinated physical inspections; neglected maintenance cycles; delayed response to critical hazards.",
            "Automated background inspection engine with scheduled cron triggers alerting engineers when maintenance cycles or project inspections become overdue."
        ),
        (
            "Spatial Decision Support & Triage Analytics",
            "Fragmented tabular spreadsheets without GIS integration; absence of prioritized severity ranking or hot-spot visualization.",
            "Interactive administrative dashboard with geospatial road health heatmaps, incident severity triage, real-time KPI metrics, and PDF/CSV audit export."
        )
    ]
    
    for row_idx, data in enumerate(delta_rows, start=1):
        row_cells = table_delta.rows[row_idx].cells
        bg_col = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9)
                if col_idx == 0:
                    r.bold = True
                    
    for row in table_delta.rows:
        for idx, width in enumerate(delta_col_widths):
            row.cells[idx].width = width
            
    doc.add_page_break()
    
    # ==================== CHAPTER 2 ====================
    add_h1("CHAPTER 2: SYSTEM ARCHITECTURE")
    
    add_h2("2.1 System Introduction")
    add_body(
        "The Nigeria Road Management System software platform is formulated upon a decoupled, service-oriented multi-tier architectural pattern. "
        "In modern enterprise software engineering, multi-tier architectures guarantee high cohesion, low coupling, horizontal scalability, "
        "and stringent isolation between client-side rendering, business application logic, persistent spatial storage, and external communication gateways. "
        "By enforcing strict role-based access control (RBAC) and asynchronous background scheduling, the system reliably services diverse concurrent users, "
        "ranging from distributed citizens reporting defects on low-bandwidth mobile connections to municipal highway engineers reviewing spatial analytical heatmaps."
    )
    
    add_h2("2.2 System Architecture Diagram")
    add_body(
        "Figure 2.1 delineates the complete multi-tier architectural layout of the proposed NRMS platform. "
        "The architecture is partitioned into four functional tiers: Tier 1 (Presentation/Client Tier), Tier 2 (Application & Logic Tier), "
        "Tier 3 (Data Persistence Tier), and Tier 4 (Output & External Services Tier). Every architectural component translates directly into an implementable software module."
    )
    
    # Insert Diagram Image
    img_path = 'figures/system_architecture.png'
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(6)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run("Figure 2.1: Multi-Tier System Architecture of the Proposed Nigeria Road Management System (NRMS)")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.bold = True
        r_cap.font.color.rgb = RGBColor(26, 35, 126)
    
    add_h2("2.3 Component Breakdown")
    add_body(
        "To ensure end-to-end technical transparency, every box illustrated in the architectural model is decomposed into its underlying functional software component:"
    )
    
    add_h3("2.3.1 Tier 1: Presentation / Client Tier")
    add_bullet(
        "Citizen Mobile / Web Portal",
        "A responsive client interface built with Next.js and Tailwind CSS that enables road users to submit road defect reports (potholes, failed culverts, eroded shoulders) and traffic violations (one-way driving, obstructionist parking, littering). It leverages HTML5 Geolocation API to capture precise coordinates and provides a file picker for photographic evidence."
    )
    add_bullet(
        "Contractor Milestone Portal",
        "A secure web portal for road construction and maintenance contractors to log project stages, upload timestamped and geotagged progress photographs, and submit completion certificates for administrative auditing."
    )
    add_bullet(
        "Administrative Dashboard",
        "A centralized portal for supervisory highway engineers and law enforcement officials providing incident triage tables, real-time KPI indicators (critical road count, pending inspections, active repairs), and spatial interactive maps."
    )
    
    add_h3("2.3.2 Tier 2: Application & Logic Tier (API Services)")
    add_bullet(
        "Authentication & Role-Based Access Control (RBAC) Module",
        "Enforces stateless JSON Web Token (JWT) authentication, cryptographic password hashing (via Bcrypt), and role guards distinguishing Citizens, Contractors, Field Inspectors, and System Administrators."
    )
    add_bullet(
        "Civic Incident & Defect Triage Engine",
        "Validates incoming crowdsourced reports, sanitizes payloads, computes priority severity scores based on defect type and user volume, and flags potential duplicate submissions within a defined spatial radius (100 meters)."
    )
    add_bullet(
        "Contractor Tracking & Milestone Auditor",
        "Processes construction progress logs, tracks contractor compliance with contractual timelines, and verifies photographic uploads against scheduled project phases."
    )
    add_bullet(
        "Automated Inspection & Alert Engine",
        "A background task processor operating cron schedules that continuously scans the database for overdue road inspections or lagging contractor milestones, automatically triggering escalation notifications."
    )
    add_bullet(
        "Geospatial Analytics Service",
        "Parses spatial latitude/longitude coordinates, conducts PostGIS bounding-box queries, and aggregates report densities into cluster points for interactive heatmap visualization."
    )
    
    add_h3("2.3.3 Tier 3: Data Persistence Tier")
    add_bullet(
        "Relational & Spatial Database (PostgreSQL + PostGIS)",
        "The primary persistence store executing structured relational schemas for users, incident reports, road segments, and contractor milestones. PostGIS spatial extensions enable native indexing and high-speed execution of spatial queries (ST_DWithin, ST_Point)."
    )
    add_bullet(
        "Cloud Object Storage (AWS S3 / Cloudinary)",
        "Secure, highly scalable object repository for storing high-resolution photographic evidence of road defects, traffic violations, and contractor milestones, returning immutable secure URLs."
    )
    add_bullet(
        "Caching & Message Queue (Redis & BullMQ)",
        "In-memory data store utilized for caching frequently queried road condition statistics and managing asynchronous task queues for notification dispatching and scheduled background jobs."
    )
    
    add_h3("2.3.4 Tier 4: Output & External Services Tier")
    add_bullet(
        "GIS & Mapping Gateway (Leaflet.js & OpenStreetMap)",
        "Renders dynamic, interactive map tiles, displaying color-coded markers (Critical, Moderate, Resolved) and road defect clusters directly in the administrative dashboard."
    )
    add_bullet(
        "Notification Gateway (Twilio SMS & NodeMailer Email)",
        "Dispatches automated transactional alerts, SMS reminders to road inspection engineers when site audits are overdue, and email notifications to contractors upon milestone approvals."
    )
    add_bullet(
        "Reporting & Audit Engine",
        "Generates downloadable PDF executive summaries and CSV datasets for municipal infrastructure audits, enabling regulatory bodies (FERMA, FRSC, Ministry of Works) to maintain empirical compliance records."
    )
    
    add_h2("2.4 System Data Flow")
    add_body(
        "The operational lifecycle of the NRMS platform proceeds through four orchestrated end-to-end data flows:"
    )
    add_bullet(
        "Data Flow 1: Civic Defect & Traffic Violation Submission",
        "1. The citizen opens the reporting interface; the device captures current GPS coordinates via HTML5 Geolocation API.\n"
        "2. The citizen selects the incident category (e.g., Severe Pothole or Illegal One-Way Driving), inputs a descriptive note, and attaches an evidentiary photograph.\n"
        "3. The client issues a multipart POST request over HTTPS to the Logic Tier.\n"
        "4. The Civic Triage Engine validates inputs, transmits the media file to Cloud Object Storage, and receives a secure media URL.\n"
        "5. The incident record is committed into the PostgreSQL database with PostGIS spatial geometry (POINT).\n"
        "6. A confirmation payload with an incident tracking code is returned to the citizen."
    )
    add_bullet(
        "Data Flow 2: Contractor Milestone Logging & Verification",
        "1. The authenticated contractor logs into the Contractor Portal and selects an assigned road construction project.\n"
        "2. The contractor selects the active milestone stage (e.g., Base Course Asphalt Laying), inputs completion metrics, and uploads on-site progress photographs.\n"
        "3. The API validates contractor credentials, stores the progress imagery in Cloud Object Storage, and records the milestone submission in the database with status 'Pending Verification'.\n"
        "4. The supervisory road engineer receives a dashboard notification to audit the submitted milestone."
    )
    add_bullet(
        "Data Flow 3: Automated Overdue Inspection Notification Engine",
        "1. The background scheduler (Redis/BullMQ cron job) executes daily at 00:00 UTC.\n"
        "2. The Inspection Engine queries the PostGIS database for active road segments where `last_inspection_date` exceeds the statutory threshold (e.g., > 30 days) or where contractor milestones remain uninspected past deadlines.\n"
        "3. For every identified delinquent record, the engine constructs an alert payload and enqueues a job into the Notification Queue.\n"
        "4. The Notification Gateway dispatches SMS and email warnings directly to the designated field maintenance engineer and area supervisor."
    )
    add_bullet(
        "Data Flow 4: Administrative Spatial Triage and Resolution",
        "1. An administrator accesses the Administrative Dashboard; the frontend queries the Geospatial Analytics Service via REST API.\n"
        "2. The service executes spatial clustering queries and returns categorized incidents and road health indicators.\n"
        "3. The dashboard renders an interactive heatmap displaying critical defect hot-spots.\n"
        "4. The administrator updates the defect status (e.g., from 'Under Review' to 'Assigned to Maintenance Unit'). The status transition is logged, and audit trails are updated."
    )
    
    add_h2("2.5 Proposed Technology Stack")
    add_body(
        "In compliance with academic design principles, every layer of the proposed technology stack is selected based on rigorous technical merits, open-source accessibility, and functional requirements:"
    )
    
    # Table 2.1 Tech Stack Justification
    add_h3("Table 2.1: Architectural Technology Stack Specification and Academic Justification")
    table_tech = doc.add_table(rows=6, cols=3)
    table_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tech.autofit = False
    
    tech_headers = ["Layer / Component", "Selected Technology", "Technical & Academic Rationale"]
    tech_col_widths = [Inches(1.8), Inches(1.8), Inches(2.9)]
    
    hdr_t = table_tech.rows[0].cells
    for i, title in enumerate(tech_headers):
        hdr_t[i].text = title
        set_cell_background(hdr_t[i], "1A237E")
        set_cell_margins(hdr_t[i], 100, 100, 120, 120)
        p = hdr_t[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    tech_rows = [
        (
            "Frontend / Presentation",
            "Next.js (React) + Tailwind CSS",
            "Provides server-side rendering for optimal mobile load performance, modular component architecture, and responsive CSS styling accessible across low-end mobile browsers."
        ),
        (
            "Backend / Application Logic",
            "Node.js + Express.js",
            "Non-blocking, event-driven asynchronous I/O engine capable of efficiently handling high-concurrency multipart HTTP requests during simultaneous crowdsourced report submissions."
        ),
        (
            "Spatial Database Persistence",
            "PostgreSQL + PostGIS Extension",
            "Enterprise-grade relational database management system offering native spatial indexing (R-Tree / GiST) and spatial SQL functions (ST_DWithin, ST_Distance) essential for geospatial road mapping."
        ),
        (
            "Object Storage & Caching",
            "Cloudinary / AWS S3 + Redis",
            "Decouples large binary media storage (photographic evidence) from transactional database records; Redis accelerates session caching and powers asynchronous task queuing."
        ),
        (
            "GIS Mapping & Visualization",
            "Leaflet.js + OpenStreetMap API",
            "Lightweight, open-source geospatial mapping library that avoids proprietary licensing costs, providing responsive map rendering and interactive tile markers."
        )
    ]
    
    for row_idx, data in enumerate(tech_rows, start=1):
        row_cells = table_tech.rows[row_idx].cells
        bg_col = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9)
                if col_idx in [0, 1]:
                    r.bold = True
                    
    for row in table_tech.rows:
        for idx, width in enumerate(tech_col_widths):
            row.cells[idx].width = width
            
    doc.add_page_break()
    
    # ==================== REFERENCES ====================
    add_h1("REFERENCES (APA 7th EDITION)")
    
    references_list = [
        "Adeleke, O., Akande, K., Kolo, S., Odumosu, J., Sijuwola, O. O., & Ayanshola, A. M. (2020). Development of a GPS-GIS-based road signage management system for selected arterial roads. Malaysian Journal of Civil Engineering, 32(2), 649. https://doi.org/10.11113/mjce.v32n2.649",
        "Adepoju, O. O. (2021). Analysis of road transportation infrastructure construction and maintenance for sustainable development in South-Western Nigeria. Journal of Sustainable Development of Transport and Logistics, 6(1), 4–15. https://doi.org/10.14254/jsdtl.2021.6-1.4",
        "Afieroho, P., Perkins, R., Zhou, X., Hoanca, B., & Protasel, G. J. (2023). Adopting e-government to monitor public infrastructure projects execution in Nigeria: The public perspective. Heliyon, 9(7), e18552. https://doi.org/10.1016/j.heliyon.2023.e18552",
        "Ajiboye, A. O., Kolawole, O., & Adebanjo, A. A. (2020). Assessment of the statutory duties of Federal Road Safety Corps aimed at reducing crashes and carnages in Ibadan, Southwest Nigeria. Journal of Art, Architecture and Built Environment, 3(2), 968. https://doi.org/10.32350/jaabe/2020/32/968",
        "Akanbi, O. D., & Abegunde, O. (2020). Design and implementation of mobile information system for Federal Road Safety Corps (FRSC) of Nigeria. International Journal of Sensor Networks and Data Communications, 9(2), 1–6.",
        "Ashara, A. H., Saleh, S., Hassan, U., & Kaura, M. (2020). Traffic management system in Abuja city center, using Geographic Information Systems (GIS) and Global Positioning System (GPS). Journal of Physics: Conference Series, 1529(5), 052068. https://doi.org/10.1088/1742-6596/1529/5/052068",
        "Audu, A. A., Iyiola, O., Popoola, A., Adeleye, B., Medayese, S., Mosima, C., & Blamah, N. (2021). The application of geographic information system as an intelligent system towards emergency responses in road traffic accident in Ibadan. Journal of Transport and Supply Chain Management, 15, a546. https://doi.org/10.4102/jtscm.v15i0.546",
        "Babatunde, A. A., Adewuyi, G. K., & Oyekola, M. A. (2019). Road condition monitoring of major and minor route in part of Ibadan metropolis using geo-spatial approach. Journal of Geography, Environment and Earth Science International, 22(4), 1–12. https://doi.org/10.9734/jgeesi/2019/v22i430156",
        "Carlos, M. R., González, L. C., Wahlström, J., Cornejo, R., & Martínez, F. (2020). Becoming smarter at characterizing potholes and speed bumps from smartphone data—Introducing a second-generation inference problem. IEEE Transactions on Mobile Computing, 19(8), 1845–1858. https://doi.org/10.1109/TMC.2019.2939198",
        "Dabo, M. Z., & Yunus, S. (2020). Road transport information system: A panacea for road transport facility management in Katsina Local Government, Katsina State, Nigeria. FUDMA Journal of Sciences, 4(2), 230–238. https://doi.org/10.33003/fjs-2020-0402-230",
        "Daraghmi, Y. A., Wu, T. H., & Ik, T. U. (2020). Crowdsourcing-based road surface evaluation and indexing. IEEE Transactions on Intelligent Transportation Systems, 22(12), 7545–7556. https://doi.org/10.1109/TITS.2020.3041649",
        "Farouq, M. M., Anwar, F., Baba, Z., Labbo, M. S., & Aliyu, D. (2017). Road maintenance management in Kano State, Nigeria: Case study of Kano metropolitan. IOSR Journal of Mechanical and Civil Engineering, 14(3), 50–62. https://doi.org/10.9790/1684-1403035062",
        "Gambo, N., & Musonda, I. (2021). Effect of the Fourth Industrial Revolution on road transport asset management practice in Nigeria. Journal of Construction in Developing Countries, 26(1), 21–42. https://doi.org/10.21315/jcdc2021.26.1.2",
        "Jaiye, D., & Elisha, A. (2020). The menace of uncontrolled trailer/truck loads and the use of weigh-in-motion device on carriageways in Nigeria. International Journal of Transport Development and Integration, 4(1), 1–13. https://doi.org/10.2495/tdi-v4-n1-1-13",
        "Medayese, S., Alfa, M. T., Abd’Razack, N. T., & Agbawn, F. O. (2019). Analysis of the extent of red light running in Minna, North-Central Nigeria. Journal of Contemporary Urban Affairs, 3(2), 124–136. https://doi.org/10.25034/ijcua.2018.470zd9",
        "Ndugbu, L. N., & Ndugbu, U. K. (2021). Road offence information management system in Nigeria: A most needed technology intervention. Journal of Computer Science and Engineering, 2(1), 164–172. https://doi.org/10.36596/jcse.v2i1.164",
        "Odinfono, J., & Olawole, M. (2024). Road traffic crash data in Southwestern Nigeria: A qualitative analysis of sources, contents and management methods. Traffic Injury Prevention, 25(8), 1–9. https://doi.org/10.1088/15389588.2024.2398670",
        "Ogbu, S., & Ezeh, F. (2019). Federal vs. state roads: Assessing the influence of intergovernmental relations models on road maintenance in Nigeria. European Journal of Business and Management Research, 4(5), 94–102. https://doi.org/10.24018/ejbmr.2019.4.5.94",
        "Olojede, O., Agbola, S., & Samuel, K. (2019). Residents’ assessment of local government road infrastructure delivery in Ile-Ife, Nigeria. Local Economy: The Journal of the Local Economy Policy Unit, 34(6), 570–588. https://doi.org/10.1177/0269094219857044",
        "Sese, T. E. (2020). Framework for client-server distributed database system for Federal Road Safety Commission Nigeria. Advances in Social Sciences Research Journal, 7(5), 183–195. https://doi.org/10.14738/assrj.75.8237",
        "Toriola-Coker, L., Alaka, H., Agbali, M., Bello, W., Pathirage, C., & Oyedele, L. (2020). Marginalization of end-user stakeholders in public private partnership road projects in Nigeria. International Journal of Construction Management, 22(14), 2736–2748. https://doi.org/10.1080/15623599.2020.1766189",
        "Tubobereni, I. F., & Ikiriko, O. K. (2019). Highlighting the salient safety issues in the National Road Traffic Regulation 2012. Landscape Architecture and Regional Planning, 4(2), 11–20. https://doi.org/10.11648/j.larp.20190402.11",
        "Ugochi, M. U. (2020). Road pavement failure and exploratory analysis of requirements for effective management of highway maintenance projects. International Journal of Innovative Research and Development, 9(8), 57–67. https://doi.org/10.24940/ijird/2020/v9/i8/aug20057",
        "Umar, B., Olaniyi, O., Agajo, J., & Isah, O. R. (2021). Traffic violation detection system using image processing. Computer Engineering and Applications Journal, 10(2), 371–382. https://doi.org/10.18495/comengapp.v10i2.371",
        "Uzondu, C., Jamson, S., & Marsden, G. (2022). Road safety in Nigeria: Unravelling the challenges, measures, and strategies for improvement. International Journal of Injury Control and Safety Promotion, 29(4), 485–497. https://doi.org/10.1080/17457300.2022.2087230"
    ]
    
    for ref in references_list:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(6)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(11)

    out_file = "Nigeria_Road_Management_System_Chapters_1_and_2.docx"
    doc.save(out_file)
    print(f"Document successfully created at {out_file}")

if __name__ == "__main__":
    create_document()
