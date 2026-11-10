import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set high resolution and clean figure size
fig, ax = plt.subplots(figsize=(14, 11), dpi=350)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Main Header / Title in the graphic
ax.text(50, 97.5, 'NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)', fontsize=16, fontweight='bold', ha='center', va='center', color='#0B5394')
ax.text(50, 95.0, 'Multi-Tier System Architecture for Citizen Crowdsourcing, Contractor Auditing & Inspection Alerts', 
        fontsize=10, fontstyle='italic', ha='center', va='center', color='#455A64')

# Palette matching Nile Journal of Computing
colors = {
    'tier_client_bg': '#F0F4F8',
    'tier_client_border': '#1A5276',
    'tier_logic_bg': '#E8F8F5',
    'tier_logic_border': '#117A65',
    'tier_data_bg': '#FEF9E7',
    'tier_data_border': '#B7950B',
    'tier_output_bg': '#F4ECF7',
    'tier_output_border': '#7D3C98',
    'box_bg': '#FFFFFF',
    'text_dark': '#1B2631',
    'text_muted': '#5D6D7E'
}

def draw_tier_container(y_bottom, height, title_text, bg_color, border_color):
    # Rounded container for the tier
    rect = patches.FancyBboxPatch((3, y_bottom), 94, height, boxstyle='round,pad=1.2,rounding_size=1.5',
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.8, linestyle='-')
    ax.add_patch(rect)
    # Tier Title Banner Tag
    tag_box = patches.FancyBboxPatch((5, y_bottom + height - 2.8), 34, 3.2, boxstyle='round,pad=0.4,rounding_size=0.8',
                                     facecolor=border_color, edgecolor='none')
    ax.add_patch(tag_box)
    ax.text(22, y_bottom + height - 1.2, title_text, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

# ----------------- 1. CLIENT TIER -----------------
draw_tier_container(73.5, 19.5, 'TIER 1: PRESENTATION / CLIENT TIER', colors['tier_client_bg'], colors['tier_client_border'])

client_modules = [
    (5.5, 75.0, 28.0, 13.5, 'Citizen Reporting Portal\n(Web & Mobile Responsive)\n• Geotagged Defect Submission\n• Traffic Violation Reporting\n• Evidence Photo Attachment\n• Real-Time Incident Status Tracking'),
    (36.0, 75.0, 28.0, 13.5, 'Contractor Milestone Portal\n(Web Application)\n• Project Milestone Logging\n• Progress Photo Evidence Upload\n• Bill of Quantities Progress Tracker\n• Inspection Readiness Signaling'),
    (66.5, 75.0, 28.0, 13.5, 'Administrative Triage Dashboard\n(Supervisory Engineers & Agencies)\n• Geospatial Defect Heatmap & Triage\n• Overdue Inspection Monitoring\n• Critical vs Good Road KPI Cards\n• Maintenance Work-Order Dispatch')
]

for x, y, w, h, text in client_modules:
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.6,rounding_size=1.0',
                                facecolor=colors['box_bg'], edgecolor=colors['tier_client_border'], linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, fontsize=8.2, ha='center', va='center', color=colors['text_dark'], multialignment='center', linespacing=1.35)

# ----------------- 2. LOGIC TIER -----------------
draw_tier_container(46.0, 23.5, 'TIER 2: APPLICATION & LOGIC TIER', colors['tier_logic_bg'], colors['tier_logic_border'])

logic_modules = [
    (5.0, 47.8, 17.0, 16.5, 'Authentication &\nRBAC Module\n• JWT Token Security\n• Bcrypt Password Hash\n• Role Authorization\n  (Citizen/Contractor/\n  Inspector/Admin)\n• Profile & Session Mgmt'),
    (23.5, 47.8, 17.5, 16.5, 'Civic Defect Triage\n& Incident Engine\n• Payload Validation\n• Defect Severity Scoring\n• Spatial Duplicate Filter\n  (<100m Radius Guard)\n• Traffic Violation Intake'),
    (42.5, 47.8, 17.5, 16.5, 'Contractor Progress\nAuditing Engine\n• Milestone Verification\n• Completion Metric Audit\n• Progress Photo Hashing\n• Fund Release Readiness\n  Verification Checks'),
    (61.5, 47.8, 17.5, 16.5, 'Automated Overdue\nInspection Engine\n• Scheduled Cron Daemon\n• Inspection Cycle Scans\n• Statutory SLA Tracker\n• Automated Escalation\n  Alert Generation'),
    (80.5, 47.8, 15.0, 16.5, 'Geospatial Analytics\n& Routing Service\n• Coordinate Parser\n• PostGIS Spatial Index\n• Density Cluster Logic\n• Road Health Index\n  Aggregation Engine')
]

for x, y, w, h, text in logic_modules:
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=0.8',
                                facecolor=colors['box_bg'], edgecolor=colors['tier_logic_border'], linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, fontsize=7.6, ha='center', va='center', color=colors['text_dark'], multialignment='center', linespacing=1.3)

# ----------------- 3. DATA PERSISTENCE TIER -----------------
draw_tier_container(24.0, 18.0, 'TIER 3: DATA PERSISTENCE TIER', colors['tier_data_bg'], colors['tier_data_border'])

data_modules = [
    (6.5, 25.8, 27.5, 11.5, 'Spatial Relational Database\n(PostgreSQL + PostGIS Extension)\n• Tables: Users, Roads, Reports, Projects, Audits\n• Native Geometry Storage (ST_Point, Polygon)\n• High-Speed Spatial Indexing (GiST / R-Tree)'),
    (36.5, 25.8, 27.0, 11.5, 'Secure Cloud Object Storage\n(AWS S3 / Cloudinary)\n• Geotagged Defect & Violation Imagery\n• Contractor Milestone Progress Photos\n• Tamper-Evident SHA-256 Media Hashes'),
    (66.0, 25.8, 28.5, 11.5, 'In-Memory Cache & Message Queue\n(Redis + BullMQ Task Manager)\n• Fast Cached Road Condition Indices\n• Asynchronous Alert Notification Jobs\n• Distributed Cron Task Scheduler State')
]

for x, y, w, h, text in data_modules:
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=0.8',
                                facecolor=colors['box_bg'], edgecolor=colors['tier_data_border'], linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, fontsize=8.0, ha='center', va='center', color=colors['text_dark'], multialignment='center', linespacing=1.3)

# ----------------- 4. NOTIFICATION & OUTPUT TIER -----------------
draw_tier_container(3.0, 17.0, 'TIER 4: NOTIFICATION & EXTERNAL OUTPUT TIER', colors['tier_output_bg'], colors['tier_output_border'])

output_modules = [
    (6.5, 4.8, 27.5, 10.5, 'GIS Mapping Gateway\n(Leaflet.js + OpenStreetMap API)\n• Interactive Tile Rendering\n• Color-Coded Defect Pinpoints\n• Critical Corridor Heatmap Layering'),
    (36.5, 4.8, 27.0, 10.5, 'Multi-Channel Alert Gateway\n(Twilio SMS & NodeMailer Email API)\n• Overdue Inspection Field SMS\n• Contractor Milestone Notifications\n• Citizen Report Status Email Dispatch'),
    (66.0, 4.8, 28.5, 10.5, 'Regulatory Compliance Reporting Engine\n(Automated PDF / CSV Exporter)\n• Executive Road Quality Indices\n• Federal (FERMA) & State Audit Exports\n• Contractor Accountability Summaries')
]

for x, y, w, h, text in output_modules:
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=0.8',
                                facecolor=colors['box_bg'], edgecolor=colors['tier_output_border'], linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, fontsize=8.0, ha='center', va='center', color=colors['text_dark'], multialignment='center', linespacing=1.3)

# ----------------- COMMUNICATION FLOW ARROWS -----------------
# Tier 1 <-> Tier 2
ax.annotate('', xy=(50, 69.8), xytext=(50, 73.5),
            arrowprops=dict(arrowstyle='<->', color='#2C3E50', lw=2.2, shrinkA=0, shrinkB=0))
ax.text(50.8, 71.6, 'HTTPS REST API / JSON Payloads / Multipart Form-Data', fontsize=8.2, fontweight='bold', color='#1A5276', va='center')

# Tier 2 <-> Tier 3
ax.annotate('', xy=(50, 42.2), xytext=(50, 46.0),
            arrowprops=dict(arrowstyle='<->', color='#2C3E50', lw=2.2, shrinkA=0, shrinkB=0))
ax.text(50.8, 44.1, 'SQL Spatial Queries / S3 Object Uploads / Redis IPC Queue', fontsize=8.2, fontweight='bold', color='#B7950B', va='center')

# Tier 2 <-> Tier 4
# Side connectors for external output
ax.annotate('', xy=(20, 20.2), xytext=(20, 24.0),
            arrowprops=dict(arrowstyle='<->', color='#2C3E50', lw=1.8, shrinkA=0, shrinkB=0))
ax.annotate('', xy=(50, 20.2), xytext=(50, 24.0),
            arrowprops=dict(arrowstyle='<->', color='#2C3E50', lw=1.8, shrinkA=0, shrinkB=0))
ax.annotate('', xy=(80, 20.2), xytext=(80, 24.0),
            arrowprops=dict(arrowstyle='<->', color='#2C3E50', lw=1.8, shrinkA=0, shrinkB=0))
ax.text(50, 22.1, 'Asynchronous Event Hooks / SMTP / SMS Gateways / Leaflet GeoJSON', fontsize=8.2, fontweight='bold', color='#7D3C98', ha='center', va='center')

plt.tight_layout()
out_img = 'figures/nrms_system_architecture.png'
plt.savefig(out_img, dpi=350, bbox_inches='tight')
print(f'Enhanced high-resolution architecture diagram created at {out_img}')
