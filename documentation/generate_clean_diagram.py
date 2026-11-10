import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 97, 'NIGERIA ROAD MANAGEMENT SYSTEM (NRMS)', fontsize=15, fontweight='bold', ha='center', va='center', color='#0B5394')
ax.text(50, 94.5, 'Multi-Tier System Architecture (Client - Logic - Data - Output)', fontsize=10.5, fontstyle='italic', ha='center', va='center', color='#4A5568')

def draw_tier(y_bottom, height, title_text, bg_color, border_color):
    rect = patches.FancyBboxPatch((4, y_bottom), 92, height, boxstyle='round,pad=1.0,rounding_size=1.2',
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.6)
    ax.add_patch(rect)
    tag = patches.FancyBboxPatch((6, y_bottom + height - 2.8), 32, 3.0, boxstyle='round,pad=0.3,rounding_size=0.6',
                                facecolor=border_color, edgecolor='none')
    ax.add_patch(tag)
    ax.text(22, y_bottom + height - 1.3, title_text, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

# 1. CLIENT TIER
draw_tier(73, 19, 'TIER 1: CLIENT TIER (USER INTERFACES)', '#F0F4F8', '#1A5276')
clients = [
    (6.5, 74.5, 27.5, 13.5, 'Citizen Portal (Web & Mobile)\n\n• Report road defects (potholes, erosion)\n• Report traffic violations (one-way, parking)\n• Upload photos and GPS location\n• Track report status (Pending/Resolved)'),
    (36.5, 74.5, 27.5, 13.5, 'Contractor Portal\n\n• View assigned road projects\n• Upload construction progress photos\n• Submit stage completion logs\n• Request project inspection'),
    (66.5, 74.5, 27.5, 13.5, 'Officials Dashboard\n\n• View road condition map and summary\n• Review citizen reports and assign tasks\n• Monitor ongoing contractor work\n• Track overdue inspections')
]
for x, y, w, h, text in clients:
    b = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=0.8', facecolor='#FFFFFF', edgecolor='#1A5276', linewidth=1.1)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, fontsize=8.5, ha='center', va='center', color='#1A202C', multialignment='left', linespacing=1.3)

# 2. LOGIC TIER
draw_tier(45, 23.5, 'TIER 2: LOGIC TIER (APPLICATION SERVICES)', '#E8F8F5', '#117A65')
logic = [
    (6.0, 46.8, 16.5, 16.5, 'User Management &\nSecurity Module\n\n• User registration & login\n• Role control\n  (Citizen, Contractor,\n  Officer, Admin)\n• Password encryption\n• Session management'),
    (24.5, 46.8, 16.5, 16.5, 'Report Management\nModule\n\n• Validates report data\n• Checks for duplicate\n  reports nearby (<100m)\n• Assigns severity priority\n• Updates report status'),
    (43.0, 46.8, 16.5, 16.5, 'Contractor Progress\nModule\n\n• Records milestone logs\n• Stores progress photos\n• Calculates % completion\n• Prepares project records\n  for inspection'),
    (61.5, 46.8, 16.5, 16.5, 'Inspection Alert\nEngine\n\n• Runs daily system check\n• Finds roads not inspected\n  for > 30 days\n• Flags overdue projects\n• Prepares alerts for staff'),
    (80.0, 46.8, 14.5, 16.5, 'Map & Analytics\nService\n\n• Processes GPS data\n• Groups defects by zone\n• Calculates road health\n• Prepares map data for\n  the dashboard')
]
for x, y, w, h, text in logic:
    b = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=0.6', facecolor='#FFFFFF', edgecolor='#117A65', linewidth=1.1)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, fontsize=8.0, ha='center', va='center', color='#1A202C', multialignment='left', linespacing=1.25)

# 3. DATA TIER
draw_tier(23, 17.5, 'TIER 3: DATA TIER (STORAGE & CACHING)', '#FEF9E7', '#B7950B')
data = [
    (6.5, 24.5, 27.5, 11.5, 'Relational Database (PostgreSQL)\n\n• Stores users, roads, and projects\n• Stores defect and violation records\n• Uses PostGIS for GPS spatial queries'),
    (36.5, 24.5, 27.5, 11.5, 'Cloud Media Storage (Cloudinary / S3)\n\n• Stores defect and violation photos\n• Stores contractor progress photos\n• Provides secure image links'),
    (66.5, 24.5, 27.5, 11.5, 'Cache & Queue (Redis)\n\n• Caches dashboard summary counts\n• Manages background notification queue\n• Coordinates daily inspection checks')
]
for x, y, w, h, text in data:
    b = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=0.6', facecolor='#FFFFFF', edgecolor='#B7950B', linewidth=1.1)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, fontsize=8.2, ha='center', va='center', color='#1A202C', multialignment='left', linespacing=1.3)

# 4. OUTPUT TIER
draw_tier(3, 16, 'TIER 4: OUTPUT & NOTIFICATION TIER', '#F4ECF7', '#7D3C98')
output = [
    (6.5, 4.5, 27.5, 10.0, 'Interactive Map Gateway (Leaflet / OSM)\n\n• Shows road markers and defect spots\n• Displays color-coded road conditions'),
    (36.5, 4.5, 27.5, 10.0, 'Notification Gateway (SMS & Email)\n\n• Sends SMS alerts for overdue inspections\n• Sends email updates on report status'),
    (66.5, 4.5, 27.5, 10.0, 'Reporting Gateway (PDF & CSV Export)\n\n• Generates road condition summary reports\n• Exports project audit records for officials')
]
for x, y, w, h, text in output:
    b = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=0.6', facecolor='#FFFFFF', edgecolor='#7D3C98', linewidth=1.1)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, fontsize=8.2, ha='center', va='center', color='#1A202C', multialignment='left', linespacing=1.3)

# Connectors
ax.annotate('', xy=(50, 69), xytext=(50, 73), arrowprops=dict(arrowstyle='<->', color='#37474F', lw=2))
ax.text(50.8, 71, 'HTTPS / JSON API Requests', fontsize=8.5, fontweight='bold', color='#1A5276', va='center')

ax.annotate('', xy=(50, 41), xytext=(50, 45), arrowprops=dict(arrowstyle='<->', color='#37474F', lw=2))
ax.text(50.8, 43, 'Database Queries & File Uploads', fontsize=8.5, fontweight='bold', color='#B7950B', va='center')

ax.annotate('', xy=(20, 19.5), xytext=(20, 23), arrowprops=dict(arrowstyle='<->', color='#37474F', lw=1.6))
ax.annotate('', xy=(50, 19.5), xytext=(50, 23), arrowprops=dict(arrowstyle='<->', color='#37474F', lw=1.6))
ax.annotate('', xy=(80, 19.5), xytext=(80, 23), arrowprops=dict(arrowstyle='<->', color='#37474F', lw=1.6))
ax.text(50, 21.2, 'SMS / Email Alerts, Map Rendering & Report Downloads', fontsize=8.5, fontweight='bold', color='#7D3C98', ha='center', va='center')

plt.tight_layout()
plt.savefig('figures/nrms_clean_architecture.png', dpi=300, bbox_inches='tight')
print('Clean architecture diagram created at figures/nrms_clean_architecture.png')
