import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("documentation/figures", exist_ok=True)
output_path = "documentation/figures/nrms_database_erd.png"

fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Block
ax.text(50, 97.5, "NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)", fontsize=16, fontweight="bold", ha="center", va="center", color="#0B5394")
ax.text(50, 95.2, "Complete Relational Database Entity-Relationship Diagram (ERD) — 3NF Normalized Schema", fontsize=11, fontstyle="italic", ha="center", va="center", color="#4A5568")

# Color Palette by Domain
COLORS = {
    "auth": {"header": "#1A5276", "bg": "#EBF5FB", "border": "#2980B9"},       # Blue
    "infra": {"header": "#117A65", "bg": "#E8F8F5", "border": "#16A085"},      # Teal/Green
    "reports": {"header": "#7D3C98", "bg": "#F4ECF7", "border": "#8E44AD"},    # Purple
    "projects": {"header": "#B9770E", "bg": "#FEF9E7", "border": "#D68910"},   # Amber
    "audits": {"header": "#922B21", "bg": "#FDEDEC", "border": "#C0392B"}      # Crimson
}

def draw_table_card(x, y, w, h, table_name, columns, domain_type):
    palette = COLORS[domain_type]
    
    # Outer box
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=0.6",
                                  facecolor=palette["bg"], edgecolor=palette["border"], linewidth=1.5)
    ax.add_patch(rect)
    
    # Header box
    hdr_h = 2.4
    hdr_rect = patches.FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0.2,rounding_size=0.4",
                                      facecolor=palette["header"], edgecolor="none")
    ax.add_patch(hdr_rect)
    
    # Table Title
    ax.text(x + w/2, y + h - hdr_h/2, table_name, fontsize=9.5, fontweight="bold", color="#FFFFFF", ha="center", va="center")
    
    # Columns List
    start_y = y + h - hdr_h - 0.7
    line_spacing = (h - hdr_h - 1.0) / max(len(columns), 1)
    
    for i, col in enumerate(columns):
        col_y = start_y - (i * line_spacing)
        prefix = ""
        fw = "normal"
        color = "#1A202C"
        
        if col.startswith("[PK]"):
            prefix = "[PK] "
            col = col.replace("[PK]", "").strip()
            fw = "bold"
            color = "#9A7D0A"
        elif col.startswith("[FK]"):
            prefix = "[FK] "
            col = col.replace("[FK]", "").strip()
            fw = "bold"
            color = "#2471A3"
        elif col.startswith("[PFK]"):
            prefix = "[PK,FK] "
            col = col.replace("[PFK]", "").strip()
            fw = "bold"
            color = "#7D3C98"
            
        ax.text(x + 0.6, col_y, prefix, fontsize=7.5, fontweight="bold", color=color, va="center")
        ax.text(x + 2.4, col_y, col, fontsize=7.5, fontweight=fw, color="#2D3748", va="center")

# 1. ROLES
draw_table_card(4, 76, 17, 14, "roles", [
    "[PK] id : INT (AI)",
    "name : VARCHAR(50) [UQ]",
    "description : VARCHAR(255)"
], "auth")

# 2. USER_ROLES (Association Table)
draw_table_card(24, 76, 17, 14, "user_roles", [
    "[PFK] user_id : INT",
    "[PFK] role_id : INT"
], "auth")

# 3. USERS
draw_table_card(4, 38, 20, 32, "users", [
    "[PK] id : INT (AI)",
    "username : VARCHAR(50) [UQ]",
    "email : VARCHAR(100) [UQ]",
    "hashed_password : VARCHAR(255)",
    "full_name : VARCHAR(100)",
    "phone_number : VARCHAR(25)",
    "organization : VARCHAR(100)",
    "is_active : BOOLEAN",
    "created_at : DATETIME"
], "auth")

# 4. AUDIT_LOGS
draw_table_card(4, 4, 21, 29, "audit_logs", [
    "[PK] id : INT (AI)",
    "[FK] user_id : INT (NULL)",
    "action : VARCHAR(100)",
    "entity_type : VARCHAR(50)",
    "entity_id : INT",
    "old_values : TEXT (JSON)",
    "new_values : TEXT (JSON)",
    "ip_address : VARCHAR(45)",
    "created_at : DATETIME"
], "audits")

# 5. ROADS (Core Spatial Infrastructure)
draw_table_card(28, 38, 23, 32, "roads", [
    "[PK] id : INT (AI)",
    "road_code : VARCHAR(50) [UQ]",
    "name : VARCHAR(150)",
    "classification : VARCHAR(50)",
    "state : VARCHAR(50)",
    "lga : VARCHAR(100)",
    "length_km : FLOAT",
    "start_lat, start_lng : FLOAT",
    "end_lat, end_lng : FLOAT",
    "condition_status : VARCHAR(50)",
    "last_inspected_at : DATETIME",
    "is_inspection_overdue : BOOL",
    "created_at : DATETIME"
], "infra")

# 6. ROAD_REPORTS (Crowdsourced Defects & Violations)
draw_table_card(55, 52, 23, 38, "road_reports", [
    "[PK] id : INT (AI)",
    "ticket_number : VARCHAR(50) [UQ]",
    "report_type : VARCHAR(50)",
    "category : VARCHAR(100)",
    "description : TEXT",
    "latitude, longitude : FLOAT",
    "location_description : VARCHAR(255)",
    "photo_url : VARCHAR(500)",
    "severity : VARCHAR(50)",
    "status : VARCHAR(50)",
    "is_duplicate : BOOLEAN",
    "[FK] duplicate_of_id : INT (NULL)",
    "[FK] citizen_id : INT (NULL)",
    "[FK] road_id : INT (NULL)",
    "assigned_team : VARCHAR(100)",
    "resolved_at : DATETIME",
    "created_at : DATETIME"
], "reports")

# 7. ROAD_PROJECTS (Contractor Contracts)
draw_table_card(55, 16, 21, 31, "road_projects", [
    "[PK] id : INT (AI)",
    "project_code : VARCHAR(50) [UQ]",
    "title : VARCHAR(200)",
    "description : VARCHAR(500)",
    "[FK] road_id : INT",
    "[FK] contractor_id : INT",
    "supervising_agency : VARCHAR(100)",
    "budget_naira : NUMERIC(15,2)",
    "start_date, expected_date : DATE",
    "current_progress_pct : FLOAT",
    "status : VARCHAR(50)",
    "created_at : DATETIME"
], "projects")

# 8. PROJECT_MILESTONES (Quality & Evidence Verification)
draw_table_card(79, 16, 18, 31, "project_milestones", [
    "[PK] id : INT (AI)",
    "[FK] project_id : INT",
    "milestone_name : VARCHAR(150)",
    "milestone_order : INT",
    "percentage_weight : FLOAT",
    "progress_pct_achieved : FLOAT",
    "photo_evidence_url : VARCHAR(500)",
    "contractor_notes : TEXT",
    "status : VARCHAR(50)",
    "submitted_at : DATETIME",
    "inspected_at : DATETIME",
    "created_at : DATETIME"
], "projects")

# 9. INSPECTIONS (Field Audits)
draw_table_card(79, 57, 18, 33, "inspections", [
    "[PK] id : INT (AI)",
    "[FK] road_id : INT",
    "[FK] project_id : INT (NULL)",
    "[FK] inspector_id : INT (NULL)",
    "scheduled_date : DATE",
    "conducted_date : DATE",
    "status : VARCHAR(50)",
    "findings_summary : TEXT",
    "quality_rating : VARCHAR(50)",
    "evidence_photos_json : TEXT",
    "alert_dispatched : BOOLEAN",
    "alert_dispatched_at : DATETIME",
    "created_at : DATETIME"
], "infra")

# 10. NOTIFICATION_LOGS (Alert Trail)
draw_table_card(28, 4, 23, 29, "notification_logs", [
    "[PK] id : INT (AI)",
    "channel : VARCHAR(20) [SMS/EMAIL]",
    "recipient : VARCHAR(100)",
    "subject : VARCHAR(200)",
    "message : TEXT",
    "status : VARCHAR(50)",
    "sent_at : DATETIME"
], "audits")

# Connectors and Relationship Lines
def draw_line(p1, p2, label="", color="#4A5568", ls="-", lw=1.2, rad=0.0):
    con = patches.ConnectionStyle("arc3", rad=rad)
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="->", color=color, lw=lw, ls=ls,
                                connectionstyle=con))
    if label:
        mx = (p1[0] + p2[0]) / 2
        my = (p1[1] + p2[1]) / 2 + (rad * 4)
        ax.text(mx, my, label, fontsize=7.5, fontweight="bold", color=color,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.9))

# Relationships
# 1. users <-> user_roles <-> roles
draw_line((14, 76), (24, 82), "1 : N", color="#2980B9")
draw_line((14, 70), (24, 77), "1 : N", color="#2980B9")

# 2. users -> audit_logs
draw_line((14, 38), (14, 33), "1 : N", color="#922B21")

# 3. users -> road_reports (citizen)
draw_line((24, 55), (55, 70), "1 : N (citizen)", color="#7D3C98", rad=0.15)

# 4. roads -> road_reports
draw_line((51, 62), (55, 62), "1 : N", color="#117A65")

# 5. road_reports -> road_reports (duplicate self-referential)
draw_line((78, 68), (78, 76), "1 : N (dup)", color="#8E44AD", rad=0.4)

# 6. users -> road_projects (contractor)
draw_line((24, 45), (55, 32), "1 : N (contractor)", color="#B9770E", rad=-0.1)

# 7. roads -> road_projects
draw_line((45, 38), (55, 26), "1 : N", color="#117A65", rad=-0.1)

# 8. road_projects -> project_milestones
draw_line((76, 30), (79, 30), "1 : N", color="#D68910")

# 9. roads -> inspections
draw_line((51, 50), (79, 70), "1 : N", color="#117A65", rad=0.2)

# 10. users -> inspections (inspector)
draw_line((24, 62), (79, 78), "1 : N (inspector)", color="#2980B9", rad=0.25)

# Legend block
leg_x, leg_y = 4, 91
ax.text(leg_x, leg_y, "Domain Modules:", fontsize=8.5, fontweight="bold", color="#2D3748")
modules = [
    ("Access Control & RBAC", COLORS["auth"]["header"]),
    ("Road Infrastructure Assets", COLORS["infra"]["header"]),
    ("Crowdsourced Incident Reports", COLORS["reports"]["header"]),
    ("Contractor Milestone Tracking", COLORS["projects"]["header"]),
    ("System Audit Trail & Alerts", COLORS["audits"]["header"])
]
for idx, (m_name, m_color) in enumerate(modules):
    bx = leg_x + 14 + (idx * 17)
    rect = patches.Rectangle((bx, leg_y - 0.7), 1.6, 1.4, facecolor=m_color, edgecolor="none")
    ax.add_patch(rect)
    ax.text(bx + 2.1, leg_y, m_name, fontsize=7.5, color="#2D3748", va="center")

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"High-resolution ERD saved to {output_path}")
