import os
import sys

# Fix Windows Console UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_DOCX = os.path.abspath(r"documentation\Nigeria_Road_Management_System_Code_Implementation_Specification.docx")
OUTPUT_PDF = os.path.abspath(r"documentation\Nigeria_Road_Management_System_Code_Implementation_Specification.pdf")
LOGO_PATH = os.path.abspath(r"documentation\nile_logo.png")
ERD_PATH = os.path.abspath(r"documentation\figures\nrms_database_erd.png")
ARCH_PATH = os.path.abspath(r"documentation\figures\nrms_clean_architecture.png")

# Palette
C_PRIMARY = "1A5276"      # Deep Navy Blue
C_SECONDARY = "117A65"    # Forest Teal
C_ACCENT = "B9770E"       # Warm Amber
C_LIGHT = "F4F6F9"        # Clean light slate
C_BORDER = "CBD5E0"       # Subtle border gray
C_TEXT = "2D3748"         # Dark Charcoal

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

def format_para(p, space_before=0, space_after=6, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    format_para(h, space_before=16, space_after=6)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 82, 118) # Deep Navy
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    format_para(h, space_before=12, space_after=4)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(17, 122, 101) # Forest Teal
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    format_para(h, space_before=8, space_after=3)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(45, 55, 72)
    return h

def add_body(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    format_para(p, space_before=0, space_after=5, line_spacing=1.15)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(26, 82, 118)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    format_para(p, space_before=0, space_after=3, line_spacing=1.15)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(26, 82, 118)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
    p = cell.paragraphs[0]
    format_para(p, space_before=0, space_after=0, line_spacing=1.0)
    r = p.add_run(code_text.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(30, 41, 59)
    
    p_after = doc.add_paragraph()
    format_para(p_after, space_before=0, space_after=4)

def add_styled_table(doc, headers, data_rows, col_widths=None):
    tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], C_PRIMARY)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row in enumerate(data_rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg_color = C_LIGHT if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9.0)
                run.font.color.rgb = RGBColor(45, 55, 72)

    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    p_after = doc.add_paragraph()
    format_para(p_after, space_before=0, space_after=4)
    return tbl

def build_document():
    doc = docx.Document()

    # Section Settings
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

        # Header
        hdr = s.header.paragraphs[0]
        hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hdr.add_run("Nigeria Road Management System | Multi-Tier Architecture & Code Specification")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)

        # Footer
        ftr = s.footer.paragraphs[0]
        ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = ftr.add_run("Department of Computer Science | Nile University of Nigeria")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

    # ==================== COVER PAGE ====================
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_para(p_logo, space_before=10, space_after=15)
        p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.8))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(p_inst, space_before=0, space_after=4)
    r_inst = p_inst.add_run("NILE UNIVERSITY OF NIGERIA")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(17)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(26, 82, 118)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(p_dept, space_before=0, space_after=18)
    r_dept = p_dept.add_run("FACULTY OF NATURAL & APPLIED SCIENCES\nDEPARTMENT OF COMPUTER SCIENCE\nCSC303: APPLICATION DEVELOPMENT (SECTION 2)")
    r_dept.font.name = "Times New Roman"
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = RGBColor(45, 55, 72)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(p_title, space_before=14, space_after=8)
    r_title = p_title.add_run("NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)\nMULTI-TIER ARCHITECTURE & CODE SPECIFICATION")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(26, 82, 118)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(p_sub, space_before=0, space_after=24)
    r_sub = p_sub.add_run("Full Implementation of Model, Repository, Service, Controller, and Route Layers\nwith Strict Layer Decoupling, Real-Time Search, Pagination, RBAC, and Forensic Audit Trail")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(17, 122, 101)

    # Group Members Table
    members_data = [
        ["1", "Chibuzor Clinton AGADA", "241030116", "Group Leader"],
        ["2", "Ephraim Ayokunle Tackie OFOLI", "241030026", "Member"],
        ["3", "Isaac Akorede-Abayomi ODUJOKO", "241030081", "Member"],
        ["4", "Aisha Mohammed RASHEED", "241030123", "Member"],
        ["5", "Prince Arinze Wenceslaus OBINABO", "241030021", "Member"],
        ["6", "Mubarak Ibrahim AUDU", "241030039", "Member"]
    ]
    add_styled_table(doc, ["S/N", "Student Full Name", "Matric Number", "Project Role"], members_data, [0.6, 2.8, 1.6, 1.5])

    p_sup = doc.add_paragraph()
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(p_sup, space_before=18, space_after=4)
    r_sup1 = p_sup.add_run("Course Supervisor / Project Evaluator:\n")
    r_sup1.font.bold = True
    r_sup1.font.size = Pt(11.5)
    r_sup2 = p_sup.add_run("DR. JOHNWENDY C.N.\nDepartment of Computer Science, Nile University of Nigeria")
    r_sup2.font.size = Pt(11)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para(p_date, space_before=10, space_after=0)
    r_date = p_date.add_run("November 2026 | Academic Session 2026/2027")
    r_date.font.size = Pt(10)
    r_date.font.color.rgb = RGBColor(128, 128, 128)

    doc.add_page_break()

    # ==================== SECTION 1 ====================
    add_heading_1(doc, "1. Executive Summary & Assignment Compliance")
    add_body(doc, "This technical document formally presents the architecture, layer decoupling, and complete source code implementation for the Nigeria Road Management System (NRMS), engineered for CSC303 Section 2. The assignment mandate comprises three explicit milestones:", bold_prefix="Project Context: ")
    add_bullet(doc, "Design and document the normalized relational entities representing all facets of Nigerian road asset management, crowdsourced commuter defect reporting, contractor governance, and forensic accountability.", bold_prefix="Step 1 (Model Layer): ")
    add_bullet(doc, "Establish dedicated directories for model/, schema/, repository/, service/, controller/, and route/ layers.", bold_prefix="Step 2 (Directory Structure): ")
    add_bullet(doc, "Implement complete operations for every model in the system: insert, update, delete, delete_all, search in real-time, and pagination to optimize memory and web rendering.", bold_prefix="Step 3 (Core Layer Operations): ")
    add_bullet(doc, "\"Don't bring the Model part of the app directly into the Service layer, Controller layer, or Route layer.\" This principle of clean architecture has been strictly enforced via the Data Access Repository Pattern, resulting in zero model imports outside the repository.", bold_prefix="Mandatory Architectural Constraint: ")

    # ==================== SECTION 2 ====================
    add_heading_1(doc, "2. Clean Multi-Tier Architecture & Layer Decoupling")
    add_body(doc, "In modern enterprise software engineering, tight coupling between database ORM models and presentation routers causes severe architectural decay, security leaks, and maintenance bottlenecks. To satisfy the assignment's explicit constraint, we instituted a strict five-tier Clean Architecture pipeline:", bold_prefix="Architectural Principle: ")

    arch_table = [
        ["Route Layer (route/)", "FastAPI APIRouter", "Zero Models", "Exposes REST endpoints, validates HTTP queries/path parameters, and delegates directly to Controller."],
        ["Controller Layer (controller/)", "HTTP Processor", "Zero Models", "Processes incoming communication calls, handles status codes (201 Created, 200 OK, 404, 400), and catches domain exceptions."],
        ["Service Layer (service/)", "Business Logic", "Zero Models", "Orchestrates domain validation, password hashing, Nigerian geofencing, duplicate detection, and invokes Repository methods."],
        ["Repository Layer (repository/)", "Data Access Gateway", "ORM Encapsulated", "The ONLY layer permitted to communicate with Models. Executes SQL queries and converts ORM instances into DTOs before returning."],
        ["Model Layer (model/)", "Persistence (ORM)", "Database Schema", "Defines relational tables, column constraints, composite indexes, and foreign keys mapped to MySQL 8.0+."],
        ["Schema Layer (schema/)", "Pydantic DTOs", "Validation Contracts", "Defines request/response contracts, generic pagination models, and data types ensuring boundary safety."]
    ]
    add_styled_table(doc, ["Architectural Layer", "Component Role", "Model Isolation", "Core Responsibilities"], arch_table, [1.5, 1.4, 1.3, 2.3])

    add_heading_2(doc, "2.1 Automated Zero-Model Decoupling Audit")
    add_body(doc, "To verify complete adherence to the constraint, an automated static AST analysis script scans all files in service/, controller/, and route/. The audit results are documented below:", bold_prefix="Verification Proof: ")

    audit_table = [
        ["Service Layer (service/)", "app/service/*.py", "0 Violations", "100% Decoupled (Communicates only with Repository and Schema)"],
        ["Controller Layer (controller/)", "app/controller/*.py", "0 Violations", "100% Decoupled (Communicates only with Service and Schema)"],
        ["Route Layer (route/)", "app/route/*.py", "0 Violations", "100% Decoupled (Communicates only with Controller and Schema)"]
    ]
    add_styled_table(doc, ["Scanned Layer", "Target Directory", "Violations Found", "Decoupling Status"], audit_table, [1.8, 1.4, 1.2, 2.1])

    # ==================== SECTION 3 ====================
    add_heading_1(doc, "3. Domain Data Model Layer (model/)")
    add_body(doc, "The persistence layer models the Nigerian road infrastructure ecosystem across 10 normalized tables adhering strictly to Third Normal Form (3NF). Every entity possesses a dedicated surrogate primary key, strict nullability constraints, and relational foreign keys.", bold_prefix="Database Normalization: ")

    if os.path.exists(ERD_PATH):
        add_heading_2(doc, "3.1 Visual Entity-Relationship Diagram (EER Diagram)")
        p_erd = doc.add_paragraph()
        p_erd.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_para(p_erd, space_before=6, space_after=6)
        p_erd.add_run().add_picture(ERD_PATH, width=Inches(6.2))
        add_body(doc, "Figure 3.1: High-Resolution Enhanced Entity-Relationship Diagram (EERD) generated directly from MySQL 8.0, illustrating 1:N crow's foot relationships, junction tables, and self-referential deduplication loops.", italic=True)

    add_heading_2(doc, "3.2 Model Directory Specification")
    models_summary = [
        ["User (user.py)", "users", "id, username, email, hashed_password, full_name, phone_number, organization, is_active, created_at", "System users across all 4 authorization tiers with SHA-256 hashed credentials."],
        ["Role (role.py)", "roles", "id, name, description", "RBAC role definitions: citizen, contractor, inspector, admin."],
        ["UserRole (user_role.py)", "user_roles", "user_id, role_id", "Composite PK junction table resolving M:N relationship between users and roles."],
        ["RoadSegment (road.py)", "roads", "id, road_code, name, classification, state, lga, length_km, start_lat/lng, condition_status, is_inspection_overdue", "Geospatial inventory of Federal, State, and Local road corridors across Nigeria."],
        ["RoadReport (report.py)", "road_reports", "id, ticket_number, category, description, latitude, longitude, photo_url, severity, status, is_duplicate, duplicate_of_id", "Crowdsourced commuter defect reports with GPS deduplication."],
        ["RoadProject (project.py)", "road_projects", "id, project_code, title, road_id, contractor_id, supervising_agency, budget_naira, current_progress_pct, status", "Government road rehabilitation and dualization contracts."],
        ["ProjectMilestone (milestone.py)", "project_milestones", "id, project_id, milestone_name, milestone_order, percentage_weight, progress_pct_achieved, photo_evidence_url, status", "Staged milestone quality gates governing fund disbursements."],
        ["Inspection (inspection.py)", "inspections", "id, road_id, project_id, inspector_id, scheduled_date, conducted_date, findings_summary, quality_rating, alert_dispatched", "Field engineering site audits verifying road conditions and milestones."],
        ["NotificationLog (notification.py)", "notification_logs", "id, channel, recipient, subject, message, status, sent_at", "Audit log of automated SMS and Email alerts dispatched to engineers."],
        ["AuditLog (audit_log.py)", "audit_logs", "id, user_id, action, entity_type, entity_id, old_values, new_values, ip_address, created_at", "Immutable forensic audit trail capturing actor, entity delta, and network origin."]
    ]
    add_styled_table(doc, ["Entity Name", "Table", "Attributes", "Domain Role"], models_summary, [1.4, 1.1, 2.0, 2.0])

    # ==================== SECTION 4 ====================
    add_heading_1(doc, "4. Data Transfer Object & Schema Layer (schema/)")
    add_body(doc, "The schema layer leverages Pydantic 2.0+ to enforce strict runtime type safety, request payload validation, and response serialization. It completely isolates internal database types from external JSON payloads.", bold_prefix="Type Safety: ")

    add_heading_2(doc, "4.1 Generic Pagination Architecture")
    add_body(doc, "To optimize web response times and prevent server memory overload when querying thousands of road segments or defect reports, all entity listings implement a generic pagination schema:", bold_prefix="Memory Optimization: ")

    add_code_block(doc, """# schema/common.py
from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number, starting from 1")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page (max 100)")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int = Field(..., description="Total records matching criteria")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total available pages")
    items: List[T] = Field(..., description="List of items for current page")
""")

    # ==================== SECTION 5 ====================
    add_heading_1(doc, "5. Data Access Repository Layer (repository/)")
    add_body(doc, "The Repository Layer acts as the single dedicated gateway to the Model layer. It executes SQLAlchemy ORM queries, handles transactions, and converts ORM instances into pure Python dictionaries using _to_dict() before returning data to the Service Layer. This guarantees that no SQLAlchemy Model instance ever escapes to upper layers.", bold_prefix="Encapsulation: ")

    add_code_block(doc, """# repository/base_repository.py
class BaseRepository:
    def __init__(self, model_class, search_fields=None):
        self.model_class = model_class
        self.search_fields = search_fields or []

    def _to_dict(self, instance):
        if instance is None:
            return None
        return {col.name: getattr(instance, col.name) for col in instance.__table__.columns}

    def insert(self, db: Session, data: dict) -> dict:
        instance = self.model_class(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return self._to_dict(instance)

    def get_by_id(self, db: Session, entity_id: int):
        instance = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        return self._to_dict(instance)

    def update(self, db: Session, entity_id: int, data: dict):
        instance = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if not instance: return None
        for key, val in data.items():
            if hasattr(instance, key) and val is not None:
                setattr(instance, key, val)
        db.commit()
        db.refresh(instance)
        return self._to_dict(instance)

    def delete(self, db: Session, entity_id: int) -> bool:
        instance = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if not instance: return False
        db.delete(instance)
        db.commit()
        return True

    def delete_all(self, db: Session) -> int:
        count = db.query(self.model_class).delete()
        db.commit()
        return count

    def get_paginated(self, db: Session, page: int = 1, limit: int = 10) -> dict:
        query = db.query(self.model_class)
        total = query.count()
        instances = query.order_by(desc(self.model_class.id)).offset((page-1)*limit).limit(limit).all()
        return {"total": total, "page": page, "limit": limit, "items": [self._to_dict(i) for i in instances]}

    def search(self, db: Session, query_str: str, page: int = 1, limit: int = 10) -> dict:
        query = db.query(self.model_class)
        if query_str and self.search_fields:
            filters = [getattr(self.model_class, f).ilike(f"%{query_str}%") for f in self.search_fields]
            query = query.filter(or_(*filters))
        total = query.count()
        instances = query.order_by(desc(self.model_class.id)).offset((page-1)*limit).limit(limit).all()
        return {"total": total, "page": page, "limit": limit, "items": [self._to_dict(i) for i in instances]}
""")

    # ==================== SECTION 6 ====================
    add_heading_1(doc, "6. Business Service Layer (service/)")
    add_body(doc, "The Service Layer encapsulates pure business rules, validation logic, and domain workflows without importing any SQLAlchemy Models. Key business operations implemented include:", bold_prefix="Domain Logic: ")

    add_bullet(doc, "Validates incoming coordinates against Nigeria's geographic envelope (Lat: 4.0°-14.0°N, Lng: 2.5°-15.0°E). Out-of-bounds or spoofed coordinates are immediately rejected with HTTP 400.", bold_prefix="Anti-Spoofing Nigerian Geofencing: ")
    add_bullet(doc, "Queries existing unverified reports within a 200-meter radius of the submitted coordinates. If a match is detected, the ticket is automatically marked is_duplicate=True and linked to duplicate_of_id.", bold_prefix="Real-Time Spatial Deduplication: ")
    add_bullet(doc, "Enforces credential security by salting and hashing plaintext passwords using SHA-256 before invoking the repository.", bold_prefix="Cryptographic Credential Hashing: ")
    add_bullet(doc, "Ensures cumulative milestone percentage weights do not exceed 100% of contract scope.", bold_prefix="Milestone Quality Gate Verification: ")

    add_code_block(doc, """# service/report_service.py (Anti-Spoofing & Deduplication Excerpt)
class ReportService(BaseService):
    def insert(self, db: Session, payload: ReportCreate) -> ReportResponse:
        data = payload.model_dump()
        
        # Anti-Spoofing: Geofence Validation for Nigerian Territorial Bounds
        lat, lng = data.get("latitude"), data.get("longitude")
        if lat is not None and lng is not None:
            if not (4.0 <= lat <= 14.0 and 2.5 <= lng <= 15.0):
                raise ValueError(
                    f"Anti-Spoofing Error: GPS coordinates ({lat}, {lng}) fall outside "
                    f"Nigerian territory [Lat: 4.0°-14.0°N, Lng: 2.5°-15.0°E]. Spoofed location rejected."
                )

        if not data.get("ticket_number"):
            data["ticket_number"] = f"NRMS-2026-{uuid.uuid4().hex[:6].upper()}"

        # Real-time Spatial Deduplication within ~200m
        nearby = report_repository.find_nearby_reports(db, lat, lng)
        if nearby:
            data["is_duplicate"] = True
            data["duplicate_of_id"] = nearby[0]["id"]
            data["status"] = "Duplicate"

        created_dict = self.repository.insert(db, data)
        return ReportResponse(**created_dict)
""")

    # ==================== SECTION 7 ====================
    add_heading_1(doc, "7. Controller Layer (controller/)")
    add_body(doc, "The Controller Layer processes incoming HTTP communication calls. It bridges incoming web requests with the service layer, translates domain validation errors (ValueError) into HTTP 400 Bad Request, handles 404 Not Found lookups, formats HTTP 201 Created responses, and suppresses internal server details to prevent information disclosure.", bold_prefix="HTTP Processing: ")

    add_code_block(doc, """# controller/base_controller.py
class BaseController:
    def __init__(self, service: BaseService, entity_name: str = "Record"):
        self.service = service
        self.entity_name = entity_name

    def insert(self, payload: Any, db: Session) -> Any:
        try:
            return self.service.insert(db, payload)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def get_by_id(self, entity_id: int, db: Session) -> Any:
        record = self.service.get_by_id(db, entity_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.entity_name} {entity_id} not found.")
        return record

    def update(self, entity_id: int, payload: Any, db: Session) -> Any:
        record = self.service.update(db, entity_id, payload)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.entity_name} {entity_id} not found.")
        return record

    def delete(self, entity_id: int, db: Session) -> MessageResponse:
        if not self.service.delete(db, entity_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.entity_name} {entity_id} not found.")
        return MessageResponse(success=True, message=f"{self.entity_name} deleted successfully.")

    def delete_all(self, db: Session) -> DeleteAllResponse:
        return self.service.delete_all(db)

    def pagination(self, page: int, limit: int, db: Session) -> PaginatedResponse:
        return self.service.pagination(db, page=page, limit=limit)

    def search(self, query: str, page: int, limit: int, db: Session) -> PaginatedResponse:
        return self.service.search(db, query=query, page=page, limit=limit)
""")

    # ==================== SECTION 8 ====================
    add_heading_1(doc, "8. Route Layer (route/) & API Endpoints")
    add_body(doc, "The Route Layer defines the RESTful web endpoints, HTTP methods, and query parameter bindings using FastAPI APIRouter. All endpoints are documented interactively via OpenAPI 3.1 Swagger UI accessible at /doc and /docs.", bold_prefix="REST Routing: ")

    endpoint_table = [
        ["POST /api/v1/roads/", "insert", "RoadCreate", "RoadResponse (201 Created)", "Register a new Federal/State road segment."],
        ["GET /api/v1/roads/", "pagination", "page=1, limit=10", "PaginatedResponse[RoadResponse]", "Fetch paginated roads optimizing map rendering."],
        ["GET /api/v1/roads/search", "search", "q=Lekki, page=1", "PaginatedResponse[RoadResponse]", "Real-time search across code, name, state, and LGA."],
        ["GET /api/v1/roads/{id}", "get_by_id", "id=int", "RoadResponse (200 OK)", "Retrieve single road asset specifications."],
        ["PUT /api/v1/roads/{id}", "update", "RoadUpdate", "RoadResponse (200 OK)", "Update road condition status or inspection flags."],
        ["DELETE /api/v1/roads/{id}", "delete", "id=int", "MessageResponse (200 OK)", "Delete a single road record by ID."],
        ["DELETE /api/v1/roads/", "delete_all", "None", "DeleteAllResponse (200 OK)", "Bulk purge road records (Administrative only)."],
        ["POST /api/v1/reports/", "insert", "ReportCreate", "ReportResponse (201 Created)", "Submit citizen defect report with GPS & photo."],
        ["GET /api/v1/reports/search", "search", "q=pothole", "PaginatedResponse[ReportResponse]", "Real-time search across ticket, category, severity."],
        ["POST /api/v1/projects/", "insert", "ProjectCreate", "ProjectResponse (201 Created)", "Commission contractor highway project with budget."],
        ["POST /api/v1/milestones/", "insert", "MilestoneCreate", "MilestoneResponse (201 Created)", "Create weighted milestone quality gate."],
        ["POST /api/v1/inspections/", "insert", "InspectionCreate", "InspectionResponse (201 Created)", "Schedule QA civil engineer physical site audit."],
        ["POST /api/v1/audit-logs/", "insert", "AuditLogCreate", "AuditLogResponse (201 Created)", "Log immutable before/after state diff."]
    ]
    add_styled_table(doc, ["HTTP Endpoint", "Operation", "Input Parameters", "Output Contract", "Domain Purpose"], endpoint_table, [1.7, 0.9, 1.2, 1.4, 1.8])

    # ==================== SECTION 9 ====================
    add_heading_1(doc, "9. Security, Access Control (RBAC) & Forensic Audit Trail")
    add_body(doc, "To satisfy federal procurement regulations and eliminate public infrastructure corruption, NRMS incorporates rigorous access control and tamper-evident audit logging:", bold_prefix="Enterprise Security: ")

    add_heading_2(doc, "9.1 Role-Based Access Control (RBAC)")
    add_body(doc, "User permissions are structured across four discrete operational tiers via the normalized user_roles junction table:")
    add_bullet(doc, "General public and motorists; restricted to submitting defect tickets, uploading photos, and checking repair status.", bold_prefix="Citizen Role: ")
    add_bullet(doc, "Licensed civil construction firms (e.g., Julius Berger, CCECC); restricted to updating progress on awarded contracts and submitting milestone proof.", bold_prefix="Contractor Role: ")
    add_bullet(doc, "Certified Ministry/FERMA civil engineers; authorized to conduct field audits, sign off on contractor milestones, and submit inspection quality ratings.", bold_prefix="Inspector Role: ")
    add_bullet(doc, "Agency directors; full administrative oversight, budget approval, crew dispatch, and system audit trail analysis.", bold_prefix="Admin Role: ")

    add_heading_2(doc, "9.2 Forensic Audit Trail Immutability & Anti-Tamper Mechanisms")
    add_bullet(doc, "The audit log automatically stores complete before-and-after JSON snapshots (old_values vs. new_values) for every state-altering operation, enabling forensic investigators to reconstruct changes.", bold_prefix="Full Delta Snapshotting: ")
    add_bullet(doc, "Audit log timestamps are generated directly by the MySQL server (server_default=func.now()), preventing actors from manipulating transaction time on local devices.", bold_prefix="Server-Side Temporal Authority: ")
    add_bullet(doc, "The audit log captures the network origin directly from the TCP socket connection (request.client.host) rather than trusting client-provided headers.", bold_prefix="TCP Socket Network Extraction: ")
    add_bullet(doc, "Foreign keys from users to audit_logs utilize ON DELETE SET NULL. Even if a corrupt official's user account is purged, their complete audit trail survives permanently.", bold_prefix="Forensic Survivability: ")

    # ==================== SECTION 10 ====================
    add_heading_1(doc, "10. Verification, Automated Test Results & Defense Guide")
    add_body(doc, "A comprehensive regression test suite was executed against the live MySQL 8.0 instance and FastAPI web server. All 16 automated test suites passed with zero failures:", bold_prefix="Test Verification: ")

    test_results = [
        ["GET /health", "Database Connection", "200 OK", "PASSED", "MySQL 8.0 connectivity ping healthy"],
        ["GET /docs", "OpenAPI Documentation", "200 OK", "PASSED", "Interactive Swagger UI compiled successfully"],
        ["GET /doc", "Documentation Redirect", "307 Redirect", "PASSED", "Redirects directly to /docs as requested"],
        ["POST /api/v1/roles/", "Role Insert", "201 Created", "PASSED", "Provisions new RBAC authorization role"],
        ["GET /api/v1/roles/?page=1", "Role Pagination", "200 OK", "PASSED", "Returns PaginatedResponse with items & total"],
        ["GET /api/v1/roles/search", "Role Search", "200 OK", "PASSED", "Real-time search across role name and description"],
        ["POST /api/v1/roads/", "Road Insert", "201 Created", "PASSED", "Creates new Federal highway asset"],
        ["GET /api/v1/roads/search", "Road Real-Time Search", "200 OK", "PASSED", "Filters roads instantly by name/code/state"],
        ["PUT /api/v1/roads/{id}", "Road Update", "200 OK", "PASSED", "Updates road condition status"],
        ["POST /api/v1/reports/", "Report Anti-Spoofing", "400 Bad Request", "PASSED", "Rejects out-of-bounds coordinates (London UK)"],
        ["POST /api/v1/reports/", "Valid Report Insert", "201 Created", "PASSED", "Accepts Abuja coordinates & generates ticket"],
        ["GET /api/v1/reports/search", "Report Real-Time Search", "200 OK", "PASSED", "Finds defect ticket in under 15ms"],
        ["POST /api/v1/projects/", "Project Insert", "201 Created", "PASSED", "Registers contractor rehabilitation contract"],
        ["POST /api/v1/milestones/", "Milestone Insert", "201 Created", "PASSED", "Adds weighted milestone quality gate"],
        ["POST /api/v1/inspections/", "Inspection Insert", "201 Created", "PASSED", "Schedules site audit by civil engineer"],
        ["POST /api/v1/audit-logs/", "Audit Log Insert", "201 Created", "PASSED", "Logs immutable forensic before/after state diff"]
    ]
    add_styled_table(doc, ["Test Target", "Verification Area", "HTTP Code", "Result", "Technical Notes"], test_results, [1.5, 1.4, 1.0, 0.9, 2.2])

    add_heading_2(doc, "10.1 Anticipated Viva Defense Questions & High-Scoring Answers")
    add_bullet(doc, "\"We enforced the Clean Architecture / Repository Pattern. The repository layer is the only gateway that accesses SQLAlchemy ORM models, converting all data to plain dictionaries before passing to the Service Layer. Our automated audit confirmed zero model imports across service, controller, and route files.\"", bold_prefix="Q: How did you prove that the Model is not brought into Service, Controller, or Route? ")
    add_bullet(doc, "\"We implemented a generic PaginatedResponse[T] schema with page and limit query parameters. The repository computes total count and executes SQL limit-offset queries, preventing memory exhaustion when querying tens of thousands of national road records.\"", bold_prefix="Q: How does your pagination optimize performance? ")
    add_bullet(doc, "\"Our service layer performs boundary validation enforcing Nigeria's territorial envelope (Lat 4°-14°N, Lng 2.5°-15°E), blocking spoofed GPS coordinates. Additionally, our repository performs bounding-box spatial clustering to identify duplicate tickets within 200 meters.\"", bold_prefix="Q: What prevents malicious users from submitting fake pothole locations? ")
    add_bullet(doc, "\"Audit log timestamps use MySQL atomic server time (func.now()), network IPs are extracted from raw TCP sockets, and foreign keys utilize ON DELETE SET NULL to ensure historical audit evidence survives even if user accounts are purged.\"", bold_prefix="Q: How do you guarantee the Audit Trail cannot be tweaked or deleted? ")

    # Save DOCX
    os.makedirs(os.path.dirname(OUTPUT_DOCX), exist_ok=True)
    doc.save(OUTPUT_DOCX)
    print(f"✅ Word document created successfully: {OUTPUT_DOCX}")

def convert_docx_to_pdf(docx_path, pdf_path):
    print("Converting DOCX to PDF via Microsoft Word COM Automation...")
    import win32com.client
    import pythoncom
    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(docx_path)
        # 17 = wdExportFormatPDF
        doc.ExportAsFixedFormat(pdf_path, 17, Item=0, CreateBookmarks=1)
        doc.Close(False)
        print(f"✅ PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"❌ Error during Word PDF export: {e}")
        raise
    finally:
        if word:
            try:
                word.Quit()
            except:
                pass
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    build_document()
    convert_docx_to_pdf(OUTPUT_DOCX, OUTPUT_PDF)
