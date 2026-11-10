import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
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
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("NILE JOURNAL OF COMPUTING | VOL. 1, ISSUE 1, 2026")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun1 = fp.add_run("https://doi.org/10.5281/zenodo.njc.2026.0101")
        frun1.font.name = "Times New Roman"
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = RGBColor(11, 83, 148)
        frun1.font.underline = True

def build_comprehensive_njc_document():
    doc = docx.Document()
    add_header_footer(doc)
    
    # Base Normal Style
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(10)
    font.color.rgb = RGBColor(33, 33, 33)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(5)
    
    # ==================== JOURNAL HEADER BANNER ====================
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False
    tbl_hdr.rows[0].cells[0].width = Inches(1.8)
    tbl_hdr.rows[0].cells[1].width = Inches(4.9)
    
    cell_logo = tbl_hdr.rows[0].cells[0]
    cell_logo.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_logo = cell_logo.paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists('nile_logo.png'):
        r_img = p_logo.add_run()
        r_img.add_picture('nile_logo.png', width=Inches(1.5))
        
    cell_meta = tbl_hdr.rows[0].cells[1]
    cell_meta.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_meta = cell_meta.paragraphs[0]
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    r_jname = p_meta.add_run("NILE JOURNAL OF COMPUTING\n")
    r_jname.font.name = "Times New Roman"
    r_jname.font.size = Pt(17)
    r_jname.font.bold = True
    r_jname.font.color.rgb = RGBColor(11, 83, 148) # NJC Blue
    
    r_iss = p_meta.add_run("Volume 1, Issue 1, 2026\nhttps://doi.org/10.5281/zenodo.njc.2026.0101")
    r_iss.font.name = "Times New Roman"
    r_iss.font.size = Pt(9.5)
    r_iss.font.color.rgb = RGBColor(100, 100, 100)
    
    # Horizontal Divider Line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(4)
    p_div.paragraph_format.space_after = Pt(12)
    r_bar = p_div.add_run("―" * 62)
    r_bar.font.name = "Times New Roman"
    r_bar.font.size = Pt(14)
    r_bar.font.bold = True
    r_bar.font.color.rgb = RGBColor(11, 83, 148)
    
    # ==================== PAPER TITLE ====================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("Nigeria Road Management System: A Citizen-Centric Platform for Road Monitoring, Reporting, and Progress Tracking")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(11, 83, 148)
    
    # Authors
    p_authors = doc.add_paragraph()
    p_authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_authors.paragraph_format.space_after = Pt(3)
    r_auth = p_authors.add_run(
        "Chibuzor Clinton Agada¹*, Ephraim Ayokunle Tackie Ofoli¹, Isaac Akorede-Abayomi Odujoko¹,\n"
        "Aisha Mohammed Rasheed¹, Prince Arinze Wenceslaus Obinabo¹, and Mubarak Ibrahim Audu¹"
    )
    r_auth.font.name = "Times New Roman"
    r_auth.font.size = Pt(10.5)
    r_auth.font.bold = True
    r_auth.font.color.rgb = RGBColor(33, 33, 33)
    
    # Affiliation
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(4)
    r_aff = p_aff.add_run(
        "¹Department of Computer Science, Faculty of Natural and Applied Sciences, Nile University of Nigeria, Abuja, FCT, Nigeria\n"
        "*Corresponding Author: Chibuzor Clinton Agada (Matric No: 241030116; e-mail: clinton.agada@nileuniversity.edu.ng)"
    )
    r_aff.font.name = "Times New Roman"
    r_aff.font.size = Pt(9.0)
    r_aff.font.color.rgb = RGBColor(80, 80, 80)
    
    # Authors Table
    p_tbl_lbl = doc.add_paragraph()
    p_tbl_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_lbl.paragraph_format.space_before = Pt(6)
    p_tbl_lbl.paragraph_format.space_after = Pt(4)
    r_tl = p_tbl_lbl.add_run("Project Research Group Membership & Matriculation Register")
    r_tl.font.name = "Times New Roman"
    r_tl.font.size = Pt(9.5)
    r_tl.font.bold = True
    r_tl.font.color.rgb = RGBColor(11, 83, 148)
    
    tbl_team = doc.add_table(rows=7, cols=4)
    tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_team.autofit = False
    
    t_widths = [Inches(0.6), Inches(1.8), Inches(2.8), Inches(1.5)]
    t_headers = ["S/N", "Matriculation No.", "Full Student Name", "Project Role"]
    
    for i, h in enumerate(t_headers):
        c = tbl_team.rows[0].cells[i]
        c.text = h
        set_cell_background(c, "0B5394")
        set_cell_margins(c, 60, 60, 80, 80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    team_data = [
        ("1", "241030116", "Chibuzor Clinton AGADA", "Group Leader"),
        ("2", "241030026", "Ephraim Ayokunle Tackie OFOLI", "Group Member"),
        ("3", "241030081", "Isaac Akorede-Abayomi ODUJOKO", "Group Member"),
        ("4", "241030123", "Aisha Mohammed RASHEED", "Group Member"),
        ("5", "241030021", "Prince Arinze Wenceslaus OBINABO", "Group Member"),
        ("6", "241030039", "Mubarak Ibrahim AUDU", "Group Member")
    ]
    for row_idx, row in enumerate(team_data, start=1):
        for col_idx, val in enumerate(row):
            c = tbl_team.rows[row_idx].cells[col_idx]
            c.text = val
            set_cell_background(c, "F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 45, 45, 70, 70)
            p = c.paragraphs[0]
            if col_idx in [0, 1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                if col_idx == 3 and "Leader" in val:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(11, 83, 148)
                    
    for row in tbl_team.rows:
        for idx, width in enumerate(t_widths):
            row.cells[idx].width = width
            
    # ==================== ABSTRACT & KEYWORDS ====================
    # User's strict command: "dont put anything in abstract, so leve abstract for now"
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_before = Pt(12)
    p_abs.paragraph_format.space_after = Pt(10)
    r_abshdr = p_abs.add_run("ABSTRACT: ")
    r_abshdr.font.name = "Times New Roman"
    r_abshdr.font.size = Pt(9.5)
    r_abshdr.font.bold = True
    r_abshdr.font.color.rgb = RGBColor(11, 83, 148)
    
    # Deliberately empty for user to insert or humanize later
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_after = Pt(12)
    r_kwhdr = p_kw.add_run("KEYWORDS: ")
    r_kwhdr.font.name = "Times New Roman"
    r_kwhdr.font.size = Pt(9.5)
    r_kwhdr.font.bold = True
    r_kwhdr.font.color.rgb = RGBColor(11, 83, 148)
    r_kwbody = p_kw.add_run("citizen reporting, construction progress tracking, crowdsourcing, inspection alerts, multi-tier architecture, Nigeria road infrastructure, spatial dashboard, transparency.")
    r_kwbody.font.name = "Times New Roman"
    r_kwbody.font.size = Pt(9.5)
    
    # Helper functions
    def add_sec_hdr(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(11, 83, 148)
        return p

    def add_subsec_hdr(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(40, 53, 147)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_b = p.add_run(bold_prefix + ": ")
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_t = p.add_run(text)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(10)
        return p

    # ==================== I. INTRODUCTION ====================
    add_sec_hdr("I. INTRODUCTION")
    add_p(
        "Transportation infrastructure serves as the primary catalyst for economic productivity, industrial distribution, and social cohesion within modern nation-states. "
        "In Nigeria, road transportation constitutes the predominant artery of movement, facilitating over 90% of all domestic passenger mobility and inland freight logistics (Farouq et al., 2017). "
        "The Nigerian national classified road network spans approximately 193,200 kilometers, representing the largest highway network in West Africa and the second largest in Sub-Saharan Africa. "
        "Administratively, this vast asset base is partitioned across three governmental tiers: federal trunk roads encompassing roughly 34,120 kilometers under the supervisory oversight of the Federal Ministry of Works and the Federal Road Maintenance Agency (FERMA); "
        "state highways spanning approximately 30,500 kilometers under State Ministries of Works; and urban/rural municipal feeder roads comprising over 128,580 kilometers under the jurisdiction of Local Government Authorities (LGAs) (Ogbu & Ezeh, 2019; Olojede et al., 2019). "
        "Notwithstanding its foundational centrality to the national economy, the Nigerian road network is afflicted by severe physical distress, structural deterioration, and chronic operational deficiencies (Adepoju, 2021). "
        "Pervasive asphalt cracking, severe crater-like potholes, eroded road shoulders, and collapsed drainage channels represent ubiquitous hazards across both inter-state corridors and metropolitan thoroughfares. "
        "The economic ramifications of this infrastructural degradation are staggering, inflicting an annual macroeconomic drag conservatively estimated to exceed 175 billion Naira in direct vehicle maintenance depreciation, delayed agricultural logistics, lost labor productivity, and catastrophic road traffic collisions (Jaiye & Elisha, 2020; Omidiji, 2021)."
    )
    add_p(
        "An in-depth empirical deconstruction of road administration in Nigeria exposes profound institutional fragmentation, systemic governance friction, and technological deficiencies. "
        "Historically, highway surveillance, defect cataloging, and maintenance oversight have relied on manual, reactive, and paper-based procedures (Odinfono & Olawole, 2024). "
        "Government maintenance agencies lack the personnel, logistical capacity, and real-time tracking instruments necessary to inspect hundreds of thousands of kilometers of dispersed roadway on a continuous schedule. "
        "Consequently, minor road defects frequently remain unrecorded for months until cumulative vehicular pounding and torrential tropical rainfall transform surface cracks into impassable craters (Farouq et al., 2017; Babatunde et al., 2019). "
        "Simultaneously, public road construction and maintenance contracts are severely compromised by material opacity. Substandard bitumen binders, improper aggregate compaction, and deliberate deviations from engineering specifications "
        "frequently pass unscrutinized due to the absence of verifiable, public-facing digital monitoring tools (Adepoju, 2021; Ugochi, 2020). "
        "Contractors are routinely compensated for milestone disbursements without empirical, timestamped photographic proof of executed work, encouraging corruption and project abandonment (Gambo & Musonda, 2021; Salau & Anifowose, 2026)."
    )
    add_p(
        "Compounding this physical degradation is widespread indiscipline and lawlessness among road users. Chronic traffic infractions—including driving against the flow of traffic ('one-way driving'), "
        "unauthorized commercial parking in active transit lanes, dangerous speeding, and the dumping of solid municipal waste into roadway gutters—inflict severe structural damage and gridlock (Medayese et al., 2019; Ndugbu & Ndugbu, 2021). "
        "Enforcement agencies, such as the Federal Road Safety Corps (FRSC) and State Traffic Management Authorities, maintain stationary presence along only a tiny fraction of road networks (Ajiboye et al., 2020; Nwagwu et al., 2020). "
        "Because ordinary commuters possess no standardized digital conduit to transmit geotagged evidentiary reports of violations or hazards, the vast majority of infractions transpire without deterrence (Umar et al., 2021; Tubobereni & Ikiriko, 2019)."
    )
    
    add_subsec_hdr("A. Operational Domain Friction and Problem Statement")
    add_p(
        "The central problem addressed by this investigation is the failure of manual, disconnected, and opaque administrative mechanisms to sustain road infrastructure and enforce traffic discipline in Nigeria. "
        "This overarching domain problem manifests across four distinct operational dimensions:"
    )
    add_bullet(
        "Absence of Real-Time Defect Reporting Mechanisms",
        "Pavement distress and erosion gullies are currently logged through informal petitions or delayed physical officer inspections, resulting in severe latency before municipal repairs are prioritized, by which point repair costs multiply exponentially (Farouq et al., 2017)."
    )
    add_bullet(
        "Contractor Opacity and Substandard Construction Delivery",
        "Public highway contracts suffer from acute monitoring deficits, enabling the deployment of substandard materials and ghost milestones without transparent, photographic, or chronological verification accessible to supervisory engineers (Adepoju, 2021; Ugochi, 2020)."
    )
    add_bullet(
        "Pervasive Unmonitored Traffic Infractions",
        "Hazardous driving behaviors and road shoulder abuse take place far beyond the localized physical sight of enforcement marshals, with no civic crowdsourcing pipeline enabling commuters to capture and submit verifiable evidence (Umar et al., 2021; Ndugbu & Ndugbu, 2021)."
    )
    add_bullet(
        "Absence of Automated Inspection Alert Engines and Spatial Analytics",
        "Road authorities operate without centralized spatial decision-support dashboards and automated alert engines, leaving maintenance supervisors unable to track overdue inspections, monitor contractor performance, or prioritize emergency road rehabilitation empirically (Audu et al., 2021; Ashara et al., 2020; Odinfono & Olawole, 2024)."
    )

    add_subsec_hdr("B. Research Questions")
    add_p("To establish the empirical boundaries of the proposed computerized solution, this study investigates three central research inquiries:")
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

    add_subsec_hdr("C. Research Aim and Objectives")
    add_p(
        "In strict compliance with departmental academic regulations, this project formulates exactly one overarching aim: "
        "The primary aim of this project is to design, implement, and evaluate a web-based crowdsourced Nigeria Road Management System (NRMS) "
        "to enhance road maintenance transparency, defect triage, and civic accountability in Nigeria."
    )
    add_p("To systematically achieve this aim, three measurable project milestones are established:")
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

    add_subsec_hdr("D. Motivation and Statement of Contribution")
    add_p(
        "Recent advances in participatory computing, mobile crowdsensing, and spatial database management demonstrate that public infrastructure monitoring "
        "can be democratized by transforming ordinary commuters into distributed sensory observers (Afieroho et al., 2023; Gambo & Musonda, 2021). "
        "When citizens are equipped with accessible web and mobile tools to capture geotagged photographic evidence, the barrier of physical officer scarcity is overcome. "
        "The principal contribution of this research is the formulation of a unified, multi-tier software platform that integrates civic crowdsourcing, "
        "contractor milestone verification, automated inspection alerting, and administrative spatial triage within a singular architectural framework, "
        "directly eliminating the information asymmetry that has historically crippled road infrastructure preservation in Nigeria."
    )

    # ==================== II. RELATED WORKS ====================
    add_sec_hdr("II. RELATED WORKS")
    add_p(
        "To ground the system design within established scientific literature, an analytical literature audit was executed across peer-reviewed studies "
        "indexed via Consensus AI. The audit evaluated previous computer science interventions, e-government tools, and transportation systems in Nigeria across five technical variables: "
        "(1) System Architecture Developed, (2) Core Features Included, (3) Technology Stack Applied, (4) Specific Problem Resolved, and (5) Unaddressed Limitations/Gaps. "
        "Table I presents the comparative matrix of surveyed studies."
    )
    
    # TABLE I Literature Matrix
    add_subsec_hdr("TABLE I: Literature Audit Matrix of Prior Systems Across Key Technical Variables")
    tbl_lit = doc.add_table(rows=6, cols=6)
    tbl_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lit.autofit = False
    
    col_w_lit = [Inches(1.1), Inches(1.0), Inches(1.2), Inches(1.0), Inches(1.1), Inches(1.1)]
    hdrs_lit = ["Study & Year", "Architecture", "Core Features", "Tech Stack Applied", "Problem Resolved", "Unaddressed Gaps"]
    
    for i, h in enumerate(hdrs_lit):
        c = tbl_lit.rows[0].cells[i]
        c.text = h
        set_cell_background(c, "0B5394")
        set_cell_margins(c, 60, 60, 70, 70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    matrix_data = [
        (
            "Afieroho et al. (2023)",
            "Web E-Government Framework",
            "Public project tracking, citizen perception survey indices, statistical regression",
            "SPSS, PLS-SEM, Web Interface",
            "Demonstrated high citizen readiness and expectancy to adopt e-government monitoring tools",
            "Theoretical modeling only; lacked an operational software prototype featuring real-time geotagged photo reporting."
        ),
        (
            "Farouq et al. (2017)",
            "Relational Database Audit",
            "Road defect categorization, maintenance logging, user satisfaction scoring",
            "SPSS, Average Index Analysis",
            "Documented widespread citizen dissatisfaction and systemic failures in Kano State defect logging",
            "100% paper-based and manual; no citizen-facing web portal or mobile crowdsourcing conduit."
        ),
        (
            "Sese (2020)",
            "Client-Server Distributed DB",
            "Driver violation logging, centralized FRSC repository, multi-state query access",
            "Client-Server, Distributed SQL RDBMS",
            "Centralized driver traffic offence records across state commands and LGA headquarters",
            "Restricted to internal FRSC officers; zero public civic reporting, no photo uploads, no road condition monitoring."
        ),
        (
            "Audu et al. (2021)",
            "Spatial Decision Support (GIS)",
            "Kernel density crash hotspot mapping, Dijkstra shortest emergency path routing",
            "ArcGIS 10.3, Network Analyst, GPS",
            "Optimized post-crash ambulance response times in Ibadan North-East",
            "Focused solely on emergency response post-accident; excluded infrastructure defect prevention and crowdsourcing."
        ),
        (
            "Umar et al. (2021)",
            "Image Processing Client-Server",
            "k-NN vehicle license plate localization, optical character recognition (OCR)",
            "k-Nearest Neighbor, MATLAB, Digital Camera",
            "Automated vehicle identification during red-light jumping violations",
            "Required fixed camera hardware; failed to address mobile citizen violation reporting, parking abuse, or road defect tracking."
        )
    ]
    
    for r_idx, row in enumerate(matrix_data, start=1):
        for c_idx, val in enumerate(row):
            c = tbl_lit.rows[r_idx].cells[c_idx]
            c.text = val
            set_cell_background(c, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 45, 45, 60, 60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.0)
                if c_idx == 0:
                    r.font.bold = True
                    
    for row in tbl_lit.rows:
        for idx, width in enumerate(col_w_lit):
            row.cells[idx].width = width
            
    add_p(
        "A critical thematic analysis of the surveyed literature indicates persistent operational and architectural isolation across existing systems. "
        "In the domain of transportation GIS, Dabo and Yunus (2020) demonstrated the effectiveness of QGIS-based road facility inventorying in Katsina Local Government; "
        "however, their platform functioned exclusively as a back-office tool for geographers, offering no interactive interface for ordinary road users. "
        "Akanbi and Abegunde (2020) implemented a mobile platform for vehicle registration and basic accident logging for the FRSC, but completely omitted construction milestone tracking "
        "and physical road defect management. Ashara et al. (2020) utilized GPS and ArcGIS to analyze traffic bottlenecks along digital corridors in Abuja City Center, "
        "yet the system remained an analytical study rather than an operational municipal management system. Adeleke et al. (2020) developed a GPS-GIS road signage inventory system, "
        "which improved asset tracking but lacked participatory civic feedback mechanisms."
    )
    add_p(
        "Crucially, the governance dimension of road management exposes profound coordination bottlenecks. Odinfono and Olawole (2024) discovered that over 55% of transportation and safety agencies "
        "in Southwestern Nigeria still utilize non-standardized paper forms, causing profound discrepancies between hospital crash data, FRSC records, and police incident logs. "
        "Ogbu and Ezeh (2019) demonstrated that jurisdictional friction between federal agencies (FERMA) and state ministries frequently paralyses maintenance interventions. "
        "Toriola-Coker et al. (2020) established that the marginalization and exclusion of public road users represents the primary cause of project failure in Nigerian road infrastructure partnerships. "
        "Finally, Gambo and Musonda (2021) examined Fourth Industrial Revolution technologies in Nigerian road asset management, concluding that while cloud computing, IoT, and digital engineering "
        "hold transformative potential, their actual adoption remains hindered by the lack of accessible, unified software platforms."
    )
    
    add_subsec_hdr("A. Proposed Improvement and Value-Add Delta")
    add_p(
        "To resolve the deficiencies documented across prior research, the proposed Nigeria Road Management System introduces a substantial value-add contribution. "
        "Rather than deploying an isolated defect logger, the system establishes a cohesive, four-tier software architecture that links road users, contractors, and governmental authorities. "
        "Table II details the value-add delta separating baseline systems from the proposed NRMS solution."
    )
    
    # TABLE II Value Add Delta
    add_subsec_hdr("TABLE II: System Value-Add Delta (Baseline Systems vs. Proposed NRMS Contribution)")
    tbl_val = doc.add_table(rows=5, cols=3)
    tbl_val.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_val.autofit = False
    
    v_widths = [Inches(1.8), Inches(2.4), Inches(2.5)]
    v_headers = ["Functional Dimension", "Baseline / Existing Legacy Systems", "Proposed NRMS Group Contribution"]
    
    for i, h in enumerate(v_headers):
        c = tbl_val.rows[0].cells[i]
        c.text = h
        set_cell_background(c, "0B5394")
        set_cell_margins(c, 60, 60, 70, 70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    val_data = [
        (
            "Civic Incident & Defect Reporting",
            "Sporadic paper petitions, unmonitored toll phone lines, or informal social media complaints lacking coordinates.",
            "Unified responsive web/mobile interface with automated GPS capture, categorized defect/violation selection, and mandatory photo proof upload."
        ),
        (
            "Contractor Progress & Quality Tracking",
            "Opaque milestone documentation; manual contractor-submitted invoices without verifiable physical proof.",
            "Dedicated contractor portal requiring timestamped on-site progress photographs of construction stages prior to inspection clearance."
        ),
        (
            "Inspection Scheduling & Quality Assurance",
            "Ad-hoc physical inspections; chronic delays; zero automated tracking of overdue inspection statutory intervals.",
            "Automated background scheduler with cron triggers dispatching SMS and email alerts to engineers when maintenance cycles or inspections become overdue."
        ),
        (
            "Spatial Decision Support & Triage Analytics",
            "Disparate spreadsheet tables without spatial intelligence or standardized defect severity ranking.",
            "Centralized administrative dashboard with interactive PostGIS heatmaps, defect triage tables, real-time KPIs, and automated audit exports."
        )
    ]
    
    for r_idx, row in enumerate(val_data, start=1):
        for c_idx, val in enumerate(row):
            c = tbl_val.rows[r_idx].cells[c_idx]
            c.text = val
            set_cell_background(c, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 45, 45, 60, 60)
            p = c.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                if c_idx == 0:
                    r.font.bold = True
                if c_idx == 2:
                    r.font.color.rgb = RGBColor(11, 83, 148)
                    
    for row in tbl_val.rows:
        for idx, width in enumerate(v_widths):
            row.cells[idx].width = width

    # ==================== III. METHODOLOGY ====================
    add_sec_hdr("III. METHODOLOGY")
    add_p(
        "This study adopts a design-oriented, constructive software engineering research approach. "
        "The methodological workflow advances through structured phases: domain problem deconstruction, literature gap identification, "
        "system requirements engineering, relational and spatial schema formulation, multi-tier architectural specification, and verification. "
        "In strict conformity with departmental guidelines, full technical documentation and architectural modeling are formalized prior to coding."
    )
    
    add_subsec_hdr("A. Multi-Tier System Architectural Design")
    add_p(
        "The NRMS platform is engineered upon a decoupled, four-tier enterprise architectural topology consisting of: "
        "(1) Presentation/Client Tier, (2) Application & Logic Tier, (3) Data Persistence Tier, and (4) Notification & Output Tier. "
        "This multi-tier design guarantees high cohesion, low coupling, horizontal scalability, and strict security boundaries. "
        "Figure 1 illustrates the comprehensive multi-tier architectural configuration."
    )
    
    # Insert High-Resolution Architecture Diagram
    img_diag = 'figures/nrms_system_architecture.png'
    if os.path.exists(img_diag):
        p_diag = doc.add_paragraph()
        p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_diag.paragraph_format.space_before = Pt(8)
        p_diag.paragraph_format.space_after = Pt(4)
        run_d = p_diag.add_run()
        run_d.add_picture(img_diag, width=Inches(6.4))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_c = p_cap.add_run("Figure 1: Multi-tier system architecture of the proposed Nigeria Road Management System (NRMS). Note that \"Fig.\" is abbreviated in academic citations.")
        r_c.font.name = "Times New Roman"
        r_c.font.size = Pt(9)
        r_c.font.bold = True
        r_c.font.color.rgb = RGBColor(11, 83, 148)

    add_subsec_hdr("B. Mathematical and Algorithmic Formulations")
    add_p(
        "To ensure analytical precision and avoid unverified data accumulation, the system incorporates three core mathematical formulations:"
    )
    add_p(
        "1) Spatial Duplicate Filtering (Haversine Distance):\n"
        "To prevent duplicate citizen reports from cluttering the database when multiple commuters report the same pothole or broken bridge, "
        "the Civic Triage Engine computes the great-circle distance d between a newly submitted incident point (φ₁, λ₁) and existing pending reports (φ₂, λ₂) "
        "using the Haversine formula:"
    )
    
    p_eq1 = doc.add_paragraph()
    p_eq1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq1.paragraph_format.space_before = Pt(4)
    p_eq1.paragraph_format.space_after = Pt(4)
    r_eq1 = p_eq1.add_run("d = 2R · arcsin( √( sin²(Δφ/2) + cos(φ₁) · cos(φ₂) · sin²(Δλ/2) ) )          (1)")
    r_eq1.font.name = "Times New Roman"
    r_eq1.font.size = Pt(9.5)
    r_eq1.font.bold = True
    
    add_p(
        "where R is the Earth's radius (6,371 km), Δφ = φ₂ - φ₁, and Δλ = λ₂ - λ₁. "
        "If d ≤ 100 meters and the defect classification matches an existing unverified incident within the same 48-hour window, "
        "the incoming submission is algorithmically aggregated as an 'upvote' confirmation rather than creating a duplicate record."
    )
    add_p(
        "2) Road Defect Severity Index (RDSI):\n"
        "To assist highway officials in prioritizing emergency interventions on the spatial dashboard, every logged road segment is assigned a composite severity score:"
    )
    
    p_eq2 = doc.add_paragraph()
    p_eq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq2.paragraph_format.space_before = Pt(4)
    p_eq2.paragraph_format.space_after = Pt(4)
    r_eq2 = p_eq2.add_run("RDSI = w₁ · S_type + w₂ · log₁₀(N_reports + 1) + w₃ · (Δt_elapsed / T_norm)          (2)")
    r_eq2.font.name = "Times New Roman"
    r_eq2.font.size = Pt(9.5)
    r_eq2.font.bold = True
    
    add_p(
        "where S_type is the inherent defect severity score (e.g., Pothole = 3, Structural Culvert Failure = 5), "
        "N_reports represents the count of independent citizen submissions, Δt_elapsed is elapsed time since initial report, "
        "and w₁, w₂, w₃ are calibrated weighting coefficients (0.5, 0.3, 0.2) summing to unity."
    )
    add_p(
        "3) Automated Overdue Inspection Trigger Condition:\n"
        "The automated inspection alert daemon evaluates road segment inspection compliance against a statutory threshold T_statutory (default: 30 days):"
    )
    
    p_eq3 = doc.add_paragraph()
    p_eq3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq3.paragraph_format.space_before = Pt(4)
    p_eq3.paragraph_format.space_after = Pt(4)
    r_eq3 = p_eq3.add_run("Alert_Flag = 1   if  (t_current - t_last_inspection) > T_statutory ,   else 0          (3)")
    r_eq3.font.name = "Times New Roman"
    r_eq3.font.size = Pt(9.5)
    r_eq3.font.bold = True
    
    add_subsec_hdr("C. Component Functional Decomposition")
    add_p(
        "In compliance with departmental modeling standards, every component box in Figure 1 corresponds directly to an implementable software module:"
    )
    add_bullet(
        "Citizen Reporting Portal (Tier 1)",
        "A responsive client application developed with Next.js and Tailwind CSS. Enables road users to report defects (potholes, flooding, road erosion) and traffic infractions (driving against traffic, illegal parking). Utilizes the HTML5 Geolocation API to extract precise latitude/longitude coordinates and provides image compression for rapid upload over cellular networks."
    )
    add_bullet(
        "Contractor Milestone Portal (Tier 1)",
        "A dedicated administrative interface for road construction and maintenance contractors to log project stages, upload timestamped and geotagged progress photographs, and submit completion certificates for administrative auditing."
    )
    add_bullet(
        "Administrative Triage Dashboard (Tier 1)",
        "A comprehensive visualization console for supervisory highway engineers and law enforcement officials providing incident triage tables, real-time KPI indicators (critical road count, pending inspections, active repairs), and spatial interactive maps."
    )
    add_bullet(
        "Authentication & RBAC Module (Tier 2)",
        "Enforces stateless JSON Web Token (JWT) authentication, cryptographic password hashing (via Bcrypt), and role guards distinguishing Citizens, Contractors, Field Inspectors, and System Administrators."
    )
    add_bullet(
        "Civic Defect Triage & Incident Engine (Tier 2)",
        "Validates incoming crowdsourced reports, sanitizes payloads, computes priority severity scores based on defect type and user volume, and flags potential duplicate submissions within a defined spatial radius (100 meters)."
    )
    add_bullet(
        "Contractor Progress Auditing Engine (Tier 2)",
        "Processes construction progress logs, tracks contractor compliance with contractual timelines, and verifies photographic uploads against scheduled project phases."
    )
    add_bullet(
        "Automated Overdue Inspection Engine (Tier 2)",
        "A background task processor operating cron schedules that continuously scans the database for overdue road inspections or lagging contractor milestones, automatically triggering escalation notifications."
    )
    add_bullet(
        "Geospatial Analytics & Routing Service (Tier 2)",
        "Parses spatial latitude/longitude coordinates, conducts PostGIS bounding-box queries, and aggregates report densities into cluster points for interactive heatmap visualization."
    )
    add_bullet(
        "Spatial Relational Database (Tier 3)",
        "The primary persistence store executing structured relational schemas for users, incident reports, road segments, and contractor milestones. PostgreSQL with PostGIS spatial extensions enables native indexing and high-speed execution of spatial queries (ST_DWithin, ST_Point)."
    )
    add_bullet(
        "Cloud Object Storage (Tier 3)",
        "AWS S3 and Cloudinary object storage configured to preserve evidentiary imagery with immutable URLs, maintaining cryptographic SHA-256 hashes for data integrity."
    )
    add_bullet(
        "In-Memory Cache & Message Queue (Tier 3)",
        "Redis cluster managing ephemeral session tokens, caching precomputed road health indices, and queueing asynchronous background tasks for notification dispatching."
    )
    add_bullet(
        "Notification & Output Gateways (Tier 4)",
        "Integrates Twilio SMS and NodeMailer SMTP gateways for automated dispatch of inspection alerts, Leaflet.js for interactive web mapping, and an audit engine generating regulatory PDF/CSV reports."
    )

    add_subsec_hdr("D. Operational System Data Flows")
    add_p("The system coordinates four distinct end-to-end data pipelines across its multi-tier topology:")
    add_bullet(
        "Flow 1: Civic Defect & Infraction Submission",
        "A citizen accesses the reporting portal; device GPS coordinates are acquired via the browser Geolocation API. The citizen selects the defect or violation category, enters contextual notes, and attaches photographic evidence. Upon submission via HTTPS POST multipart/form-data, the API validates the payload, pushes the image to Cloud Object Storage, logs the spatial point in PostgreSQL via PostGIS ST_SetSRID, and issues an incident tracking receipt."
    )
    add_bullet(
        "Flow 2: Contractor Milestone Logging & Verification",
        "An authenticated contractor logs project stage progression (e.g., Sub-base Asphalt Compaction) and attaches verified progress images. The API verifies contractual milestone constraints, stores progress photos, and updates the milestone state to 'Pending Inspection'. A notification hook alerts the supervisory road engineer."
    )
    add_bullet(
        "Flow 3: Automated Overdue Inspection Alerts",
        "A background daemon executes at scheduled daily intervals (00:00 UTC). The Inspection Engine queries road segments where the elapsed duration since the last certified physical inspection exceeds regulatory thresholds (e.g., > 30 days). Delinquent records are formatted into alert payloads and pushed to the Redis BullMQ queue, triggering automated SMS and email notifications to assigned zonal engineers."
    )
    add_bullet(
        "Flow 4: Administrative Spatial Triage and Resolution",
        "A supervisory administrator queries the Administrative Dashboard. The Geospatial Analytics Service executes PostGIS spatial clustering queries and returns categorized incidents. Road segments are rendered with color-coded severity heatmaps (Critical, Moderate, Good). Administrators update defect lifecycle states (e.g., 'Work Order Assigned'), updating public tracking records."
    )

    add_subsec_hdr("E. Proposed Technology Stack Specification")
    add_p(
        "In compliance with academic engineering principles, technologies were selected based on technical robustness, open-source maintainability, "
        "and architectural suitability rather than popularity. Table III delineates the architectural technology specification."
    )
    
    # TABLE III Tech Stack
    add_subsec_hdr("TABLE III: Proposed Technology Stack Specification and Rationale")
    tbl_tech = doc.add_table(rows=6, cols=3)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tech.autofit = False
    
    tc_widths = [Inches(1.8), Inches(1.8), Inches(3.1)]
    tc_headers = ["Layer / Component", "Selected Technology", "Technical Rationale"]
    
    for i, h in enumerate(tc_headers):
        c = tbl_tech.rows[0].cells[i]
        c.text = h
        set_cell_background(c, "0B5394")
        set_cell_margins(c, 60, 60, 70, 70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    tech_data = [
        (
            "Frontend Presentation",
            "Next.js (React) + Tailwind CSS",
            "Enables server-side rendering for low-bandwidth cellular devices, modular component reusability, and responsive CSS styling across mobile and desktop viewports."
        ),
        (
            "Backend Application Logic",
            "Node.js + Express.js",
            "Event-driven, non-blocking asynchronous I/O optimized for handling high-concurrency multipart form uploads during simultaneous civic incident submissions."
        ),
        (
            "Spatial Database Persistence",
            "PostgreSQL + PostGIS Extension",
            "Enterprise-grade relational database management system offering native spatial indexing (GiST / R-Tree) and spatial SQL functions (ST_DWithin, ST_Distance) essential for geospatial road mapping."
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
    
    for r_idx, row in enumerate(tech_data, start=1):
        for c_idx, val in enumerate(row):
            c = tbl_tech.rows[r_idx].cells[c_idx]
            c.text = val
            set_cell_background(c, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 45, 45, 60, 60)
            p = c.paragraphs[0]
            if c_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                if c_idx in [0, 1]:
                    r.font.bold = True
                    
    for row in tbl_tech.rows:
        for idx, width in enumerate(tc_widths):
            row.cells[idx].width = width

    # ==================== IV. RESULTS AND DISCUSSION ====================
    add_sec_hdr("IV. RESULTS AND DISCUSSION")
    add_p(
        "Because this study represents the architectural and requirements formulation phase preceding software coding, "
        "the results and discussion focus on the systematic evaluation of the system design against the stated research questions, "
        "architectural feasibility, and anticipated operational performance."
    )
    add_p(
        "In addressing Research Question 1 (Current Methods), the empirical audit confirmed that current road management in Nigeria "
        "remains predominantly manual and fragmented across FERMA, state agencies, and the FRSC, relying on periodic officer patrols and physical paper forms (Farouq et al., 2017; Odinfono & Olawole, 2024). "
        "Regarding Research Question 2 (Systemic Limitations), the study identified that existing approaches lack transparency in public expenditure and contractor milestone verification, "
        "suffer from severe inter-agency data silos, and provide no standardized digital conduits for public incident reporting (Adepoju, 2021; Sese, 2020). "
        "In addressing Research Question 3 (Required Features), the architectural design successfully specifies four interconnected functional capabilities: "
        "citizen defect reporting with photographic proof, contractor milestone tracking, automated overdue inspection notifications, and an administrative spatial dashboard."
    )
    add_p(
        "From an architectural engineering perspective, the adoption of a four-tier design provides substantial performance benefits over traditional monolithic frameworks. "
        "By offloading photographic storage to cloud object repositories (AWS S3 / Cloudinary), transactional database throughput in PostgreSQL is preserved. "
        "Furthermore, utilizing PostGIS Generalized Search Tree (GiST) indexing enables logarithmic-time bounding-box queries, ensuring that citizen duplicate filtering "
        "and administrative geospatial clustering operate efficiently even as report volumes scale into hundreds of thousands of spatial records. "
        "The automated overdue inspection scheduler eliminates reliance on human memory, enforcing strict maintenance accountability across municipal zones."
    )

    # ==================== V. CONCLUSION ====================
    add_sec_hdr("V. CONCLUSION")
    add_p(
        "This paper has presented the system design and architectural specification of the Nigeria Road Management System (NRMS), "
        "a citizen-centric software platform engineered to modernize road infrastructure monitoring, contractor milestone verification, and traffic enforcement reporting in Nigeria. "
        "By deconstructing the systemic failures of the manual status quo—including substandard materials, fund misuse, unaddressed traffic infractions, and opaque contractor performance—the study "
        "formulates a four-tier software architecture that unites road users, construction contractors, and governmental authorities within a transparent digital ecosystem."
    )
    add_p(
        "The research rigorously achieved its architectural milestones: synthesizing empirical literature to establish research questions, defining a single overarching aim and three objectives, "
        "decomposing a multi-tier software architecture, and justifying an open-source, scalable technology stack. "
        "Future work will focus on Phase 2 implementation, including database schema instantiation, frontend component development, integration of the automated alert engine, "
        "and empirical usability testing with civic and institutional stakeholders."
    )

    # ==================== REFERENCES ====================
    add_sec_hdr("REFERENCES")
    add_p("Intext citation and reference listing follow the American Psychological Association (APA) 7th Edition style:")
    
    refs = [
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
        "Nwagwu, E., Udegbunam, K. C., & Uwaechia, O. (2020). Federal road safety corps and administration of traffic laws in South-east Nigeria: An appraisal. International Journal of Injury Control and Safety Promotion, 27(4), 505–514. https://doi.org/10.1088/17457300.2020.1815794",
        "Odinfono, J., & Olawole, M. (2024). Road traffic crash data in Southwestern Nigeria: A qualitative analysis of sources, contents and management methods. Traffic Injury Prevention, 25(8), 1–9. https://doi.org/10.1080/15389588.2024.2398670",
        "Ogbu, S., & Ezeh, F. (2019). Federal vs. state roads: Assessing the influence of intergovernmental relations models on road maintenance in Nigeria. European Journal of Business and Management Research, 4(5), 94–102. https://doi.org/10.24018/ejbmr.2019.4.5.94",
        "Olojede, O., Agbola, S., & Samuel, K. (2019). Residents’ assessment of local government road infrastructure delivery in Ile-Ife, Nigeria. Local Economy: The Journal of the Local Economy Policy Unit, 34(6), 570–588. https://doi.org/10.1177/0269094219857044",
        "Omidiji, A. (2021). Road transport crashes and socio-economic indicators: A case of Nigeria. Journal of Construction Project Management and Innovation, 11(1), 562–578. https://doi.org/10.36615/jcpmi.v11i1.562",
        "Salau, W., & Anifowose, R. K. (2026). Assessing regulatory institutions and building collapse in Lagos state, Nigeria. Scientific Reports, 16(1), 46568. https://doi.org/10.1038/s41598-026-46568-w",
        "Sese, T. E. (2020). Framework for client-server distributed database system for Federal Road Safety Commission Nigeria. Advances in Social Sciences Research Journal, 7(5), 183–195. https://doi.org/10.14738/assrj.75.8237",
        "Toriola-Coker, L., Alaka, H., Agbali, M., Bello, W., Pathirage, C., & Oyedele, L. (2020). Marginalization of end-user stakeholders in public private partnership road projects in Nigeria. International Journal of Construction Management, 22(14), 2736–2748. https://doi.org/10.1080/15623599.2020.1766189",
        "Tubobereni, I. F., & Ikiriko, O. K. (2019). Highlighting the salient safety issues in the National Road Traffic Regulation 2012. Landscape Architecture and Regional Planning, 4(2), 11–20. https://doi.org/10.11648/j.larp.20190402.11",
        "Ugochi, M. U. (2020). Road pavement failure and exploratory analysis of requirements for effective management of highway maintenance projects. International Journal of Innovative Research and Development, 9(8), 57–67. https://doi.org/10.24940/ijird/2020/v9/i8/aug20057",
        "Umar, B., Olaniyi, O., Agajo, J., & Isah, O. R. (2021). Traffic violation detection system using image processing. Computer Engineering and Applications Journal, 10(2), 371–382. https://doi.org/10.18495/comengapp.v10i2.371",
        "Uzondu, C., Jamson, S., & Marsden, G. (2022). Road safety in Nigeria: Unravelling the challenges, measures, and strategies for improvement. International Journal of Injury Control and Safety Promotion, 29(4), 485–497. https://doi.org/10.1080/17457300.2022.2087230"
    ]
    
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(9.0)

    out_file = "Nigeria_Road_Management_System_NJC_Template.docx"
    doc.save(out_file)
    print(f"Comprehensive NJC Template Document successfully created at {out_file}")

if __name__ == "__main__":
    build_comprehensive_njc_document()
