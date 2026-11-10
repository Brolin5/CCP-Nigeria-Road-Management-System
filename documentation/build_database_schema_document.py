import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

OUTPUT_DOCX = r"documentation\Nigeria_Road_Management_System_Database_Schema_Specification.docx"
LOGO_PATH = r"documentation\nile_logo.png"
ERD_PATH = r"documentation\figures\nrms_database_erd.png"

# Color Palette
COLOR_PRIMARY_HEX = "1A5276"      # Deep Navy
COLOR_SECONDARY_HEX = "117A65"    # Teal/Green
COLOR_ACCENT_HEX = "B9770E"       # Amber
COLOR_LIGHT_HEX = "F0F4F8"        # Soft Gray/Blue
COLOR_TEXT_HEX = "2D3748"         # Dark Charcoal

def set_cell_background(cell, fill_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
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
        hdr = s.header.paragraphs[0]
        hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hdr.add_run("Nigeria Road Management System | Database Schema Specification")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)

        # Footer
        ftr = s.footer.paragraphs[0]
        ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = ftr.add_run("Department of Computer Science — Nile University of Nigeria")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

def format_para(p, space_before=0, space_after=6, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    format_para(h, space_before=14, space_after=6)
    run = h.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(26, 82, 118) # Navy
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    format_para(h, space_before=10, space_after=4)
    run = h.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(17, 122, 101) # Teal
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    format_para(h, space_before=8, space_after=3)
    run = h.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(45, 55, 72)
    return h

def add_body_p(doc, text, bold_prefix="", italic_prefix=""):
    p = doc.add_paragraph()
    format_para(p, space_before=0, space_after=6, line_spacing=1.2)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        brun = p.add_run(bold_prefix)
        brun.font.name = "Times New Roman"
        brun.font.size = Pt(10.5)
        brun.font.bold = True
        brun.font.color.rgb = RGBColor(45, 55, 72)
        
    if italic_prefix:
        irun = p.add_run(italic_prefix)
        irun.font.name = "Times New Roman"
        irun.font.size = Pt(10.5)
        irun.font.italic = True
        irun.font.color.rgb = RGBColor(74, 85, 104)

    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    format_para(p, space_before=0, space_after=3, line_spacing=1.15)
    if bold_prefix:
        brun = p.add_run(bold_prefix + " ")
        brun.font.name = "Times New Roman"
        brun.font.size = Pt(10)
        brun.font.bold = True
        brun.font.color.rgb = RGBColor(26, 82, 118)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(45, 55, 72)
    return p

def create_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], COLOR_PRIMARY_HEX)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        format_para(p, space_before=0, space_after=0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row_values in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F9FBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            format_para(p, space_before=0, space_after=0)
            if c_idx == 0 or "ID" in headers[c_idx] or "Type" in headers[c_idx]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(45, 55, 72)

    # Column widths
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    doc.add_paragraph() # Spacer
    return table

print("Generating database schema specification document...")
doc = docx.Document()
add_header_footer(doc)

# ==================== COVER PAGE ====================
if os.path.exists(LOGO_PATH):
    lp = doc.add_paragraph()
    lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lp.paragraph_format.space_before = Pt(20)
    lp.paragraph_format.space_after = Pt(15)
    doc.add_picture(LOGO_PATH, width=Inches(1.8))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

title_p = doc.add_paragraph()
format_para(title_p, space_before=15, space_after=8)
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
trun = title_p.add_run("NILE UNIVERSITY OF NIGERIA\n")
trun.font.name = "Times New Roman"
trun.font.size = Pt(15)
trun.font.bold = True
trun.font.color.rgb = RGBColor(26, 82, 118)

s_run = title_p.add_run("FACULTY OF NATURAL AND APPLIED SCIENCES\nDEPARTMENT OF COMPUTER SCIENCE\n")
s_run.font.name = "Times New Roman"
s_run.font.size = Pt(12)
s_run.font.bold = True
s_run.font.color.rgb = RGBColor(45, 55, 72)

doc_title = doc.add_paragraph()
format_para(doc_title, space_before=20, space_after=10)
doc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
dt_run = doc_title.add_run("NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)\n")
dt_run.font.name = "Times New Roman"
dt_run.font.size = Pt(17)
dt_run.font.bold = True
dt_run.font.color.rgb = RGBColor(17, 122, 101)

sub_run = doc_title.add_run("TECHNICAL DATABASE SCHEMA & RELATIONAL ARCHITECTURE SPECIFICATION\n")
sub_run.font.name = "Times New Roman"
sub_run.font.size = Pt(12)
sub_run.font.bold = True
sub_run.font.color.rgb = RGBColor(74, 85, 104)

det_run = doc_title.add_run("Third Normal Form (3NF) Normalization, Role-Based Access Control (RBAC), and Enterprise Audit Trail")
det_run.font.name = "Times New Roman"
det_run.font.size = Pt(10.5)
det_run.font.italic = True
det_run.font.color.rgb = RGBColor(100, 116, 139)

# Group Roster
r_hdr = doc.add_paragraph()
format_para(r_hdr, space_before=30, space_after=6)
r_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
rh_run = r_hdr.add_run("PROJECT GROUP MEMBERS ROSTER")
rh_run.font.name = "Times New Roman"
rh_run.font.size = Pt(11)
rh_run.font.bold = True
rh_run.font.color.rgb = RGBColor(26, 82, 118)

roster_data = [
    ["1", "241030116", "Chibuzor Clinton AGADA", "Group Leader / Database Architect"],
    ["2", "241030026", "Ephraim Ayokunle Tackie OFOLI", "Group Member / Software Engineer"],
    ["3", "241030081", "Isaac Akorede-Abayomi ODUJOKO", "Group Member / Backend Developer"],
    ["4", "241030123", "Aisha Mohammed RASHEED", "Group Member / Quality Assurance"],
    ["5", "241030021", "Prince Arinze Wenceslaus OBINABO", "Group Member / Systems Analyst"],
    ["6", "241030039", "Mubarak Ibrahim AUDU", "Group Member / Geospatial Analyst"],
    ["7", "—", "Dr. Johnwendy C.N.", "Course Lecturer & Project Supervisor"]
]
create_table(doc, ["S/N", "Matric No.", "Full Student Name", "Designated Role"], roster_data, [0.6, 1.4, 2.6, 2.0])

date_p = doc.add_paragraph()
format_para(date_p, space_before=15, space_after=0)
date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
drun = date_p.add_run("Academic Session: 2025/2026 | Date: October 2026")
drun.font.name = "Times New Roman"
drun.font.size = Pt(9.5)
drun.font.italic = True
drun.font.color.rgb = RGBColor(120, 120, 120)

doc.add_page_break()

# ==================== SECTION 1: EXECUTIVE OVERVIEW ====================
add_heading_1(doc, "1. EXECUTIVE DATABASE ARCHITECTURE & DESIGN PRINCIPLES")

add_body_p(doc, 
    "This technical documentation specifies the complete, third-normal-form (3NF) relational database architecture for the Nigeria Road Management System (NRMS). NRMS is a citizen-centric, crowdsourced road infrastructure monitoring, contractor milestone verification, and automated maintenance alert platform designed to address chronic road decay, unchecked traffic contraventions, contractor milestone opacity, and neglected inspection cycles across Nigeria's 193,200 km road transport network.",
    bold_prefix="System Context: "
)

add_body_p(doc, 
    "In strict compliance with modern software engineering paradigms and departmental database provisioning guidelines, the persistence layer is engineered on MySQL 8.0+ utilizing the InnoDB storage engine. The application utilizes SQLAlchemy Core and Object-Relational Mapping (ORM) for declarative schema modeling and Alembic for deterministic schema versioning and zero-touch startup migrations.",
    bold_prefix="Persistence Foundation: "
)

add_heading_2(doc, "1.1 Core Engineering & Architectural Decisions")

add_bullet(doc, "Employs MySQL's native transactional InnoDB storage engine supporting ACID compliance (Atomicity, Consistency, Isolation, Durability), row-level locking for concurrent crowdsourced writes, and foreign key referential integrity constraints.", bold_prefix="Storage Engine (InnoDB):")
add_bullet(doc, "Configured with CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci. Unlike legacy 3-byte MySQL utf8 (utf8mb3), utf8mb4 allocates up to 4 bytes per character, natively supporting emojis (e.g. 🚗, 🚧, ⚠️ in citizen reports), specialized mathematical symbols, and Nigerian indigenous language diacritics (e.g., Hausa, Yoruba, and Igbo tone markings: Ẹ, Ọ, Ṣ, Ɗ, Ƙ) without string truncation or encoding exceptions.", bold_prefix="Encoding Standard (utf8mb4):")
add_bullet(doc, "Mandates strict Role-Based Access Control (RBAC) separating administrative road officials (FERMA / Ministry of Works), registered civil contractors, field quality inspectors, and general public commuters.", bold_prefix="Access Control Mandate:")
add_bullet(doc, "Implements an immutable audit trail subsystem (audit_logs and notification_logs) capturing state changes, photographic upload verification, actor user IDs, and automated SMS/Email alert dispatches.", bold_prefix="Audit Trail Mandate:")

# ==================== SECTION 2: ACCESS CONTROL ARCHITECTURE ====================
add_heading_1(doc, "2. ACCESS CONTROL & ROLE-BASED AUTHORIZATION ARCHITECTURE")

add_body_p(doc, 
    "Security and data sovereignty are enforced at the persistence tier through a normalized Role-Based Access Control (RBAC) schema. The architecture strictly adheres to the Principle of Least Privilege (PoLP), ensuring that database actors cannot inspect, modify, or approve entities beyond their statutory domain.",
    bold_prefix="Access Control Philosophy: "
)

add_heading_2(doc, "2.1 Access Control Entities & Permissions Matrix")

add_body_p(doc, 
    "The access control subsystem decomposes user authentication and authorization into three decoupled entities: users, roles, and the junction association table user_roles. This many-to-many relationship prevents transitive role duplication and permits fine-grained role assignment (e.g. a user acting as both an Inspector and an Administrator).",
    bold_prefix="Schema Decoupling: "
)

rbac_matrix = [
    ["citizen", "Public Road User", "Create defect/violation reports; upload GPS & photos; view public road condition map; track submitted ticket status.", "Cannot access contractor portals, assign maintenance crews, or approve milestones."],
    ["contractor", "Licensed Civil Contractor", "View awarded road contracts; submit milestone progress %; upload mandatory timestamped on-site photo evidence.", "Cannot modify road condition ratings, alter contract budgets, or self-approve milestones."],
    ["inspector", "Field Engineer / FRSC", "Conduct physical site audits; verify milestone physical completion; log inspection ratings; trigger alert scans.", "Cannot award contracts, disburse milestone funds, or purge audit trail records."],
    ["admin", "Road Authority Official (FERMA)", "Access GIS spatial dashboard; triage reports; assign maintenance teams; manage road inventory; export audit PDFs.", "Full administrative authority; all administrative actions logged to immutable audit trail."]
]
create_table(doc, ["Role Identifier", "Actor Type", "Permitted Database Operations", "Enforced System Restrictions"], rbac_matrix, [1.0, 1.4, 2.6, 2.0])

add_heading_2(doc, "2.2 Credential Protection & Password Security")
add_body_p(doc, "User authentication credentials never persist in plaintext. Passwords undergo cryptographic stretching utilizing PBKDF2 (Password-Based Key Derivation Function 2) with HMAC-SHA256, 100,000 algorithmic iterations, and cryptographically random 16-byte hex salts (formatted as pbkdf2:sha256:100000$salt$hash). This defends against rainbow table attacks and credential harvesting.")

# ==================== SECTION 3: AUDIT TRAIL ARCHITECTURE ====================
add_heading_1(doc, "3. SYSTEM AUDIT TRAIL & TRANSACTIONAL LOGGING SUBSYSTEM")

add_body_p(doc, 
    "To satisfy the departmental mandate that 'every system must have access control and audit trail,' NRMS embeds an immutable logging layer. This ensures absolute traceability, non-repudiation, and legal transparency during road contract disputes, contractor abandonment claims, or traffic infraction appeals.",
    bold_prefix="Audit Trail Purpose: "
)

add_heading_2(doc, "3.1 Audit Trail Structure & Event Capture")
add_body_p(doc, "The audit subsystem is structured around two dedicated relational tables:")
add_bullet(doc, "audit_logs: Captures all state mutations across critical business entities (RoadReport, RoadProject, ProjectMilestone, Inspection). Each log entry records the acting user_id, action verb (e.g. MILESTONE_APPROVED, TICKET_ASSIGNED), target entity_type, target entity_id, JSON-serialized old_values snapshot, JSON-serialized new_values snapshot, client ip_address, and UTC timestamp.", bold_prefix="1. Entity Mutation Audit (audit_logs):")
add_bullet(doc, "notification_logs: Captures all automated and manual system dispatches. Stores delivery channel (SMS, EMAIL), recipient identifier (phone number or email), subject header, full message body, delivery status (SENT, FAILED, QUEUED), and dispatch timestamp. This verifies that 30-day inspection alerts were legitimately triggered and delivered to zonal engineers.", bold_prefix="2. Alert & Communication Audit (notification_logs):")

add_heading_2(doc, "3.2 Tracked State Transitions in NRMS Workflows")
state_transitions = [
    ["Citizen Report Submission (F1)", "road_reports", "INSERT", "status: 'Pending', is_duplicate: false, ticket_number generated."],
    ["Duplicate Report Detection (F1)", "road_reports", "INSERT", "status: 'Duplicate', is_duplicate: true, duplicate_of_id linked."],
    ["Administrative Triage (F4)", "road_reports", "UPDATE", "status: 'Pending' -> 'Under Review' -> 'Assigned' to maintenance team."],
    ["Milestone Progress Upload (F2)", "project_milestones", "UPDATE", "progress_pct_achieved updated; mandatory photo_evidence_url attached."],
    ["Milestone Verification (F2)", "project_milestones", "UPDATE", "status: 'Pending Inspection' -> 'Approved' or 'Rejected' by engineer."],
    ["Inspection Alert Trigger (F3)", "roads / notification_logs", "CRON SCAN", "is_inspection_overdue flagged true; SMS alert logged to notification_logs."]
]
create_table(doc, ["Operational Event", "Target Table", "DML Type", "Audit Trail Value Snapshot"], state_transitions, [1.8, 1.4, 0.9, 2.9])

# ==================== SECTION 4: NORMALIZATION ANALYSIS ====================
add_heading_1(doc, "4. DATABASE NORMALIZATION PROOF & THEORETICAL ANALYSIS")

add_body_p(doc, 
    "Database normalization is the formal mathematical technique of organizing relations to minimize data redundancy, prevent insertion, update, and deletion anomalies, and enforce relational integrity. The NRMS schema strictly complies with Third Normal Form (3NF). Below is the systematic normalization proof:",
    bold_prefix="Normalization Rationale: "
)

add_heading_2(doc, "4.1 First Normal Form (1NF) Compliance")
add_body_p(doc, "A relation R is in 1NF if and only if all domain values are atomic (indivisible) and there are no repeating groups or multi-valued attributes.")
add_bullet(doc, "Every attribute in all 10 tables holds strictly atomic values (single scalar integers, floats, strings, or dates).", bold_prefix="Atomicity:")
add_bullet(doc, "Composite attributes are decomposed: GPS coordinates are split into independent atomic columns: latitude and longitude; road terminal endpoints are decomposed into start_latitude, start_longitude, end_latitude, and end_longitude.", bold_prefix="Decomposition:")
add_bullet(doc, "Repeating groups are eliminated: A road project does not store milestone columns inside the project table (e.g. milestone1, milestone2); instead, milestones are segregated into an independent relation (project_milestones) with a foreign key back-referencing project_id.", bold_prefix="No Repeating Groups:")
add_bullet(doc, "Every table possesses an explicit primary key (id) enforcing entity uniqueness.", bold_prefix="Unique Identification:")

add_heading_2(doc, "4.2 Second Normal Form (2NF) Compliance")
add_body_p(doc, "A relation R is in 2NF if and only if it is in 1NF and every non-prime attribute is fully functionally dependent on the entire primary key (no partial functional dependencies on candidate keys).")
add_bullet(doc, "Tables with Single-Attribute Primary Keys: 9 out of 10 tables (users, roles, roads, road_reports, road_projects, project_milestones, inspections, audit_logs, notification_logs) utilize a single-column surrogate primary key (id). By mathematical definition, partial dependency is impossible when the primary key contains only one attribute.", bold_prefix="Single-Column Keys:")
add_bullet(doc, "Composite Key Table (user_roles): The junction table user_roles possesses a composite primary key (user_id, role_id). It contains zero non-prime attributes; therefore, no non-key attribute can exhibit partial dependency on either user_id or role_id.", bold_prefix="Composite Key Integrity:")

add_heading_2(doc, "4.3 Third Normal Form (3NF) Compliance")
add_body_p(doc, "A relation R is in 3NF if and only if it is in 2NF and no non-prime attribute is transitively dependent on the primary key (X -> Y and Y -> Z where Z is non-prime is disallowed).")
add_bullet(doc, "Decoupling User and Role: User entities store only contractor_id, citizen_id, or inspector_id foreign keys. Role descriptions and role names are stored exclusively in roles, preventing transitive dependencies such as user_id -> role_name -> role_description.", bold_prefix="User-Role Separation:")
add_bullet(doc, "Decoupling Project and Road: Road projects reference road_id. Road metadata (name, classification, state, length_km) is not duplicated inside road_projects, preventing project_id -> road_id -> road_name.", bold_prefix="Project-Road Separation:")
add_bullet(doc, "Decoupling Milestone and Project: Milestones reference project_id. Project budgets and contractor identities are not stored inside project_milestones, eliminating milestone_id -> project_id -> contractor_id.", bold_prefix="Milestone-Project Separation:")
add_bullet(doc, "Duplicate Report Lineage: When a citizen submits a duplicate report within 100m, the duplicate record simply stores duplicate_of_id referencing the original road_reports.id, avoiding redundant replication of the master report's investigation notes or assigned crews.", bold_prefix="Duplicate Report Referencing:")

# ==================== SECTION 5: ER DIAGRAM ====================
add_heading_1(doc, "5. ENTITY-RELATIONSHIP DIAGRAM (ERD) & CARDINALITIES")

add_body_p(doc, 
    "Figure 5.1 delineates the complete Entity-Relationship Diagram (ERD) of the Nigeria Road Management System. The diagram visualizes all 10 relational entities, their attribute definitions (PK, FK, and unique constraints), and cardinality connections across the 5 architectural domain modules.",
    bold_prefix="Structural Topology: "
)

if os.path.exists(ERD_PATH):
    ep = doc.add_paragraph()
    ep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(ep, space_before=6, space_after=6)
    doc.add_picture(ERD_PATH, width=Inches(6.5))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    cap = doc.add_paragraph()
    format_para(cap, space_before=2, space_after=12)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    crun = cap.add_run("Figure 5.1: High-Resolution Entity-Relationship Diagram (ERD) of NRMS (3NF Normalized).")
    crun.font.name = "Times New Roman"
    crun.font.size = Pt(9.5)
    crun.font.bold = True
    crun.font.color.rgb = RGBColor(26, 82, 118)

add_heading_2(doc, "5.1 System Relationship Cardinalities & Constraint Rules")

rel_data = [
    ["users : roles", "N : M", "user_roles (user_id, role_id)", "ON DELETE CASCADE", "Users can hold multiple authorization roles; roles contain many users."],
    ["users : audit_logs", "1 : N", "audit_logs.user_id -> users.id", "ON DELETE SET NULL", "One user generates multiple audit log entries; audit history preserved on user purge."],
    ["users : road_reports", "1 : N", "road_reports.citizen_id -> users.id", "ON DELETE SET NULL", "One citizen submits multiple defect reports; citizen deletion preserves public hazard reports."],
    ["roads : road_reports", "1 : N", "road_reports.road_id -> roads.id", "ON DELETE SET NULL", "One road segment contains multiple reported potholes and traffic violations."],
    ["road_reports : road_reports", "1 : N", "road_reports.duplicate_of_id -> road_reports.id", "ON DELETE SET NULL", "Self-referencing relationship linking crowdsourced duplicates within 100m."],
    ["users : road_projects", "1 : N", "road_projects.contractor_id -> users.id", "ON DELETE RESTRICT", "One contractor manages multiple contracts; prevents accidental deletion of active contractors."],
    ["roads : road_projects", "1 : N", "road_projects.road_id -> roads.id", "ON DELETE CASCADE", "One road asset can host multiple construction/overlay rehabilitation contracts."],
    ["road_projects : project_milestones", "1 : N", "project_milestones.project_id -> road_projects.id", "ON DELETE CASCADE", "One contract contains ordered verifiable milestone stages with photographic proof."],
    ["roads : inspections", "1 : N", "inspections.road_id -> roads.id", "ON DELETE CASCADE", "One road segment undergoes periodic routine and emergency physical inspections."],
    ["users : inspections", "1 : N", "inspections.inspector_id -> users.id", "ON DELETE SET NULL", "One field engineer / inspector conducts and signs off multiple site inspection logs."]
]
create_table(doc, ["Relationship", "Cardinality", "Foreign Key Mapping", "Referential Action", "Business Semantic Rule"], rel_data, [1.5, 0.7, 1.8, 1.3, 1.7])

# ==================== SECTION 6: DATA DICTIONARY ====================
doc.add_page_break()
add_heading_1(doc, "6. COMPREHENSIVE DATA DICTIONARY (DETAILED TABLE SPECIFICATIONS)")

add_body_p(doc, 
    "The data dictionary defines the physical implementation details of all 10 relational tables in MySQL 8.0, specifying column names, storage data types, nullability, primary/foreign key constraints, default values, and operational descriptions.",
    bold_prefix="Physical Schema Definition: "
)

# Table 1: roles
add_heading_2(doc, "6.1 Table: roles (User Authorization Roles)")
roles_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for authorization role."],
    ["name", "VARCHAR(50)", "No", "—", "UNIQUE, INDEX", "Unique role code ('citizen', 'contractor', 'inspector', 'admin')."],
    ["description", "VARCHAR(255)", "Yes", "NULL", "—", "Formal explanation of role privileges and statutory duties."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], roles_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 2: users
add_heading_2(doc, "6.2 Table: users (System User Identity & Credentials)")
users_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for user."],
    ["username", "VARCHAR(50)", "No", "—", "UNIQUE, INDEX", "Unique user authentication handle."],
    ["email", "VARCHAR(100)", "No", "—", "UNIQUE, INDEX", "Verified corporate or personal email address."],
    ["hashed_password", "VARCHAR(255)", "No", "—", "—", "PBKDF2-HMAC-SHA256 hashed password string."],
    ["full_name", "VARCHAR(100)", "Yes", "NULL", "—", "Legal full name of commuter, contractor, or official."],
    ["phone_number", "VARCHAR(25)", "Yes", "NULL", "—", "Telephone number utilized for automated SMS alert delivery."],
    ["organization", "VARCHAR(100)", "Yes", "NULL", "—", "Affiliated agency (e.g. FERMA, FRSC, Julius Berger)."],
    ["is_active", "BOOLEAN", "No", "TRUE", "—", "Account status flag; disables access upon deactivation."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Timestamp of account registration."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], users_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 3: user_roles
add_heading_2(doc, "6.3 Table: user_roles (Many-to-Many RBAC Association)")
ur_dict = [
    ["user_id", "INT", "No", "—", "PRIMARY KEY, FK -> users(id)", "References parent user account. Cascades on delete."],
    ["role_id", "INT", "No", "—", "PRIMARY KEY, FK -> roles(id)", "References assigned role. Cascades on delete."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], ur_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 4: roads
add_heading_2(doc, "6.4 Table: roads (National Road Infrastructure Inventory)")
roads_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for road segment."],
    ["road_code", "VARCHAR(50)", "No", "—", "UNIQUE, INDEX", "Official asset code (e.g., 'FED-A234-ABJ')."],
    ["name", "VARCHAR(150)", "No", "—", "—", "Gazetted road corridor name (e.g. 'Abuja-Keffi Expressway')."],
    ["classification", "VARCHAR(50)", "No", "'Federal'", "—", "Jurisdiction tier ('Federal', 'State', 'Local')."],
    ["state", "VARCHAR(50)", "No", "—", "INDEX", "State where road asset is situated (e.g. 'FCT', 'Lagos')."],
    ["lga", "VARCHAR(100)", "Yes", "NULL", "—", "Local Government Area traversing the road section."],
    ["length_km", "FLOAT", "Yes", "NULL", "—", "Surveyed length of road corridor in kilometres."],
    ["start_latitude", "FLOAT", "Yes", "NULL", "—", "Starting terminal GPS latitude."],
    ["start_longitude", "FLOAT", "Yes", "NULL", "—", "Starting terminal GPS longitude."],
    ["end_latitude", "FLOAT", "Yes", "NULL", "—", "Ending terminal GPS latitude."],
    ["end_longitude", "FLOAT", "Yes", "NULL", "—", "Ending terminal GPS longitude."],
    ["condition_status", "VARCHAR(50)", "No", "'Fair'", "—", "Pavement health ('Good', 'Fair', 'Poor', 'Critical')."],
    ["last_inspected_at", "DATETIME", "Yes", "NULL", "INDEX", "Timestamp of most recent field audit (drives 30-day alert)."],
    ["is_inspection_overdue", "BOOLEAN", "No", "FALSE", "—", "Flag set true when last_inspected_at exceeds 30 days."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Asset registration timestamp."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], roads_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 5: road_reports
add_heading_2(doc, "6.5 Table: road_reports (Crowdsourced Defect & Violation Reports)")
rep_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for incident report."],
    ["ticket_number", "VARCHAR(50)", "No", "—", "UNIQUE, INDEX", "Tracking code issued to citizen (e.g. 'NRMS-2026-X89J21')."],
    ["report_type", "VARCHAR(50)", "No", "—", "INDEX", "Classification ('defect' for hazards, 'violation' for traffic laws)."],
    ["category", "VARCHAR(100)", "No", "—", "INDEX", "Fault category ('Pothole', 'Erosion', 'One-Way Driving', etc.)."],
    ["description", "TEXT", "Yes", "NULL", "—", "Detailed narrative provided by the reporting commuter."],
    ["latitude", "FLOAT", "No", "—", "INDEX", "Device GPS latitude coordinate captured on submission."],
    ["longitude", "FLOAT", "No", "—", "INDEX", "Device GPS longitude coordinate captured on submission."],
    ["location_description", "VARCHAR(255)", "Yes", "NULL", "—", "Landmark description (e.g. 'Opposite Kugbo mechanic village')."],
    ["photo_url", "VARCHAR(500)", "No", "—", "—", "Cloudinary/S3 URL of mandatory photographic proof."],
    ["severity", "VARCHAR(50)", "No", "'Medium'", "—", "Triage urgency rank ('Low', 'Medium', 'High', 'Critical')."],
    ["status", "VARCHAR(50)", "No", "'Pending'", "INDEX", "Workflow state ('Pending', 'Under Review', 'Assigned', 'Resolved')."],
    ["is_duplicate", "BOOLEAN", "No", "FALSE", "—", "Set true by Haversine engine if report is within 100m of open fault."],
    ["duplicate_of_id", "INT", "Yes", "NULL", "FK -> road_reports(id)", "Self-referencing FK pointing to master incident ticket."],
    ["citizen_id", "INT", "Yes", "NULL", "FK -> users(id)", "Submitting commuter ID. Set NULL if user is removed."],
    ["road_id", "INT", "Yes", "NULL", "FK -> roads(id)", "Associated road corridor ID. Set NULL if road asset purged."],
    ["assigned_team", "VARCHAR(100)", "Yes", "NULL", "—", "Field maintenance crew dispatched to remediate defect."],
    ["resolved_at", "DATETIME", "Yes", "NULL", "—", "Timestamp when maintenance unit completes remediation."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Report submission timestamp."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], rep_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 6: road_projects
add_heading_2(doc, "6.6 Table: road_projects (Contractor Projects & Construction Contracts)")
prj_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for construction project."],
    ["project_code", "VARCHAR(50)", "No", "—", "UNIQUE, INDEX", "Gazetted contract code (e.g. 'PRJ-2026-FCT-04')."],
    ["title", "VARCHAR(200)", "No", "—", "—", "Official contract title (e.g. 'Dualization of Nyanya Corridor')."],
    ["description", "VARCHAR(500)", "Yes", "NULL", "—", "Engineering scope of works and specifications."],
    ["road_id", "INT", "No", "—", "FK -> roads(id)", "Associated road asset. Cascades on road deletion."],
    ["contractor_id", "INT", "No", "—", "FK -> users(id)", "Assigned licensed contractor user. Restricted from deletion."],
    ["supervising_agency", "VARCHAR(100)", "No", "'FERMA'", "—", "Government supervisory body overseeing execution."],
    ["budget_naira", "NUMERIC(15,2)", "Yes", "NULL", "—", "Approved contract mobilization and execution sum."],
    ["start_date", "DATE", "Yes", "NULL", "—", "Official site mobilization date."],
    ["expected_completion_date", "DATE", "Yes", "NULL", "—", "Contractual milestone delivery deadline."],
    ["current_progress_pct", "FLOAT", "No", "0.0", "—", "Cumulative progress % dynamically recalculated from milestones."],
    ["status", "VARCHAR(50)", "No", "'Ongoing'", "INDEX", "Contract state ('Not Started', 'Ongoing', 'Completed', 'Abandoned')."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Project provisioning timestamp."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], prj_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 7: project_milestones
add_heading_2(doc, "6.7 Table: project_milestones (Milestone Quality Verification & Evidence)")
mst_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for milestone stage."],
    ["project_id", "INT", "No", "—", "FK -> road_projects(id)", "Parent contract reference. Cascades on project deletion."],
    ["milestone_name", "VARCHAR(150)", "No", "—", "—", "Stage title (e.g. 'Sub-base Grading', 'Binder Course')."],
    ["milestone_order", "INT", "No", "1", "—", "Sequential execution order of the construction milestone."],
    ["percentage_weight", "FLOAT", "No", "0.0", "—", "Weight contribution towards total project completion (0-100%)."],
    ["progress_pct_achieved", "FLOAT", "No", "0.0", "—", "Physical completion percentage claimed by contractor."],
    ["photo_evidence_url", "VARCHAR(500)", "Yes", "NULL", "—", "Mandatory timestamped on-site photographic evidence URL."],
    ["contractor_notes", "TEXT", "Yes", "NULL", "—", "Technical remarks submitted by site project manager."],
    ["status", "VARCHAR(50)", "No", "'Pending'", "INDEX", "Verification status ('Pending', 'Pending Inspection', 'Approved')."],
    ["submitted_at", "DATETIME", "Yes", "NULL", "—", "Timestamp of milestone evidence submission."],
    ["inspected_at", "DATETIME", "Yes", "NULL", "—", "Timestamp of physical field inspection sign-off."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Milestone creation timestamp."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], mst_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 8: inspections
add_heading_2(doc, "6.8 Table: inspections (Routine & Emergency Field Audits)")
insp_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for site inspection."],
    ["road_id", "INT", "No", "—", "FK -> roads(id)", "Audited road corridor. Cascades on road deletion."],
    ["project_id", "INT", "Yes", "NULL", "FK -> road_projects(id)", "Optional ongoing contract undergoing milestone check."],
    ["inspector_id", "INT", "Yes", "NULL", "FK -> users(id)", "Certified field engineer conducting audit."],
    ["scheduled_date", "DATE", "No", "—", "—", "Target calendar date for physical site walkthrough."],
    ["conducted_date", "DATE", "Yes", "NULL", "—", "Actual execution date of field inspection."],
    ["status", "VARCHAR(50)", "No", "'Scheduled'", "INDEX", "Inspection state ('Scheduled', 'Completed', 'Overdue', 'Cancelled')."],
    ["findings_summary", "TEXT", "Yes", "NULL", "—", "Detailed engineering observations on pavement distress."],
    ["quality_rating", "VARCHAR(50)", "Yes", "NULL", "—", "Quality verdict ('Satisfactory', 'Minor Defects', 'Non-Compliance')."],
    ["evidence_photos_json", "TEXT", "Yes", "NULL", "—", "JSON array of inspection photographic proof links."],
    ["alert_dispatched", "BOOLEAN", "No", "FALSE", "—", "Flag indicating whether 30-day overdue alert was sent."],
    ["alert_dispatched_at", "DATETIME", "Yes", "NULL", "—", "Timestamp when automated overdue alert was dispatched."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Inspection record creation timestamp."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], insp_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 9: audit_logs
add_heading_2(doc, "6.9 Table: audit_logs (System-Wide Immutable Audit Trail)")
al_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for audit log entry."],
    ["user_id", "INT", "Yes", "NULL", "FK -> users(id)", "Actor who initiated action. Retained if user deleted."],
    ["action", "VARCHAR(100)", "No", "—", "INDEX", "Event verb ('REPORT_SUBMITTED', 'MILESTONE_APPROVED', etc.)."],
    ["entity_type", "VARCHAR(50)", "No", "—", "INDEX", "Target domain model ('RoadReport', 'ProjectMilestone', etc.)."],
    ["entity_id", "INT", "Yes", "NULL", "—", "Primary key ID of affected entity."],
    ["old_values", "TEXT", "Yes", "NULL", "—", "JSON serialization of record state prior to mutation."],
    ["new_values", "TEXT", "Yes", "NULL", "—", "JSON serialization of record state following mutation."],
    ["ip_address", "VARCHAR(45)", "Yes", "NULL", "—", "Client IPv4/IPv6 address originating the request."],
    ["created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Immutable timestamp of transaction."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], al_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# Table 10: notification_logs
add_heading_2(doc, "6.10 Table: notification_logs (Automated SMS & Email Dispatch Trail)")
nl_dict = [
    ["id", "INT", "No", "—", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique identifier for dispatch log."],
    ["channel", "VARCHAR(20)", "No", "—", "—", "Communication channel ('SMS', 'EMAIL')."],
    ["recipient", "VARCHAR(100)", "No", "—", "—", "Destination telephone number or email address."],
    ["subject", "VARCHAR(200)", "Yes", "NULL", "—", "Message subject header (e.g. 'OVERDUE ROAD INSPECTION')."],
    ["message", "TEXT", "No", "—", "—", "Complete textual content dispatched to recipient."],
    ["status", "VARCHAR(50)", "No", "'SENT'", "—", "Dispatch delivery outcome ('SENT', 'FAILED', 'QUEUED')."],
    ["sent_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "—", "Transmission timestamp."]
]
create_table(doc, ["Column Name", "Data Type", "Nullable", "Default", "Constraints", "Operational Description"], nl_dict, [1.2, 1.1, 0.7, 0.8, 1.6, 1.6])

# ==================== SECTION 7: DEFENSE & VIVA GUIDE ====================
doc.add_page_break()
add_heading_1(doc, "7. DEFENSE & VIVA PREPARATION GUIDE (FOR NEXT WEEK'S PRESENTATION)")

add_body_p(doc, 
    "To prepare every team member to defend and explain the database architecture with confidence during next week's presentation before Dr. Johnwendy and the panel, this section outlines the exact anticipated technical questions and high-scoring model responses:",
    bold_prefix="Viva Purpose: "
)

questions = [
    ("Q1: Why did you choose MySQL and utf8mb4 rather than the default utf8?",
     "Answer: Standard MySQL 'utf8' (utf8mb3) only allocates 3 bytes per character, which crashes with an 'Incorrect string value' error when users input emojis, Nigerian language diacritics, or special characters. We specified utf8mb4 (4-byte Unicode) with utf8mb4_unicode_ci collation to guarantee that crowdsourced citizen reports containing emojis (e.g. 🚗, ⚠️) and Nigerian language text (e.g. Ẹ, Ọ, Ṣ, Ɗ, Ƙ) are preserved without truncation or runtime crashes."),

    ("Q2: How does your database enforce Role-Based Access Control (RBAC)?",
     "Answer: Access control is normalized across three entities: users, roles, and the junction table user_roles. Instead of embedding static role strings in the user record, the many-to-many relationship decouples permissions. We define four distinct roles: citizen (reporting & viewing tickets), contractor (milestone photo uploads), inspector (site walkthrough ratings), and admin (crew assignment & GIS triage). Passwords are never stored in plaintext; they are protected using PBKDF2-HMAC-SHA256 with 100,000 rounds and unique 16-byte cryptographic salts."),

    ("Q3: Where is your audit trail, and how does it guarantee non-repudiation?",
     "Answer: Our schema features two dedicated audit tables: audit_logs and notification_logs. Whenever a critical business action occurs—such as a contractor uploading milestone photos, an engineer approving a milestone, or an admin re-assigning a road defect—the audit_logs table records the acting user_id, action verb, target entity, client IP address, and JSON snapshots of both old_values and new_values. Furthermore, notification_logs records every automated SMS and email dispatched by the 30-day alert engine, creating an immutable legal record that prevents contractor or agency denial."),

    ("Q4: Prove that your database schema satisfies Third Normal Form (3NF).",
     "Answer: \n"
     "• 1NF: All column attributes are atomic (GPS coordinates are split into latitude and longitude), repeating groups are eliminated into separate tables (milestones are separate from projects), and all tables have unique primary keys.\n"
     "• 2NF: No non-key attribute depends on part of a composite key. Nine tables have single-column primary keys, making partial dependency impossible. The only composite key table, user_roles (user_id, role_id), has zero non-key attributes.\n"
     "• 3NF: No non-key attribute depends on another non-key attribute (zero transitive dependencies). For example, road assets are separate from projects (project_id -> road_id, but road metadata is in roads), contractor profiles are separate from projects, and roles are separate from users."),

    ("Q5: How does the schema support the 100-meter duplicate report detection rule?",
     "Answer: The road_reports table stores atomic latitude and longitude columns with database B-Tree indices. When a new report is submitted, the system queries open reports of the same category and runs the spherical Haversine distance formula. If an existing report is found within 100 meters, the new record is flagged with is_duplicate = true and duplicate_of_id points back to the original road_reports.id via a self-referential foreign key constraint. This prevents database bloat and ensures maintenance units are not dispatched multiple times to the same pothole."),

    ("Q6: How does the schema enable automated alerts when inspections are overdue by 30 days?",
     "Answer: The roads table includes an indexed last_inspected_at column and an is_inspection_overdue boolean flag. A daily background scheduler scans records where last_inspected_at is null or older than 30 days (last_inspected_at < NOW() - INTERVAL 30 DAY). The engine sets is_inspection_overdue = true and writes an SMS/Email alert to notification_logs with the assigned zonal engineer's details. Once an engineer completes an inspection via the inspections table, last_inspected_at is updated to the current timestamp and the overdue flag resets.")
]

for q_title, q_ans in questions:
    add_heading_2(doc, q_title)
    add_body_p(doc, q_ans)

doc.save(OUTPUT_DOCX)
print(f"Document successfully created and saved to {OUTPUT_DOCX}")
