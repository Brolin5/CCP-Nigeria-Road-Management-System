# Nigeria Road Management System (NRMS)
**Citizen-Centric Platform for Road Monitoring, Crowdsourced Reporting, Contractor Tracking, and Automated Inspection Alerts**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![MySQL 8.0](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()

---

## 🏛️ Academic & Group Metadata
* **Institution:** Nile University of Nigeria
* **Faculty:** Faculty of Natural & Applied Sciences
* **Department:** Department of Computer Science
* **Course:** CSC303: Application Development (Section 2)
* **Supervisor:** Dr. Johnwendy C.N.
* **Session:** 2026/2027 Academic Session

### 👥 Project Team Members
| S/N | Student Name | Matric Number | Role |
| :---: | :--- | :---: | :--- |
| 1 | **Chibuzor Clinton AGADA** | 241030116 | Group Leader |
| 2 | Ephraim Ayokunle Tackie OFOLI | 241030026 | Member |
| 3 | Isaac Akorede-Abayomi ODUJOKO | 241030081 | Member |
| 4 | Aisha Mohammed RASHEED | 241030123 | Member |
| 5 | Prince Arinze Wenceslaus OBINABO | 241030021 | Member |
| 6 | Mubarak Ibrahim AUDU | 241030039 | Member |

---

## 🏗️ Architectural Overview (Clean Multi-Tier Architecture)
In strict compliance with modern software engineering paradigms and departmental requirements:
> *"Don't bring the Model part of the app directly into the Service layer, Controller layer, or Route layer."*

This project strictly enforces the **Repository Pattern / Data Access Layer** separating concerns across 6 distinct tiers:

```text
┌─────────────────┐       HTTP Requests (Browser / Mobile / Swagger)
│   Route Layer   │ ◄───────────────────────────────────────────────
└────────┬────────┘
         │ Passes Schemas & Parameters (ZERO Model imports)
         ▼
┌─────────────────┐
│Controller Layer │ ◄── Processes HTTP calls, status codes (201, 200, 404, 400)
└────────┬────────┘
         │ Invokes Domain Operations (ZERO Model imports)
         ▼
┌─────────────────┐
│  Service Layer  │ ◄── Pure Business Logic, Geofencing & Deduplication
└────────┬────────┘
         │ Passes & Returns DTOs (ZERO Model imports)
         ▼
┌─────────────────┐
│Repository Layer │ ◄── THE ONLY LAYER THAT TOUCHES THE MODEL!
└────────┬────────┘      (Translates ORM Models ⇄ Plain DTOs/Dicts)
         │
         ▼
┌─────────────────┐
│   Model Layer   │ ◄── SQLAlchemy Declarative ORM (MySQL 8.0)
└─────────────────┘
```

---

## 📂 Project Directory Structure

```text
CCP-Nigeria Road Management System/
│
├── model/                     # Step 1: Database ORM Models (User, Road, Report, Project, etc.)
├── repository/                # Data Access Layer (Isolates Models from higher tiers)
├── service/                   # Step 2: Pure Business Logic (Geofencing, Deduplication, Hashing)
├── controller/                # Step 2: HTTP Processing, Status Codes & Exception Mapping
├── route/                     # Step 2: FastAPI Endpoints (Swagger /doc routing)
├── schema/                    # Pydantic Schemas / DTOs (Request & Response validation)
│
├── app/                       # Core Application Package (Mirrors clean architecture)
│   ├── config.py              # Environment configuration & Pydantic settings
│   ├── database.py            # SQLAlchemy connection pool & get_db dependency
│   └── main.py                # FastAPI ASGI application with lifespan migrations
│
├── documentation/             # Project Reports & Presentation Deliverables
│   ├── figures/               # High-Resolution EER Diagrams & Architecture Schematics
│   ├── Nigeria_Road_Management_System_Code_Implementation_Specification.docx
│   └── Nigeria_Road_Management_System_Code_Implementation_Specification.pdf
│
├── alembic/                   # Database versioning and migration scripts
├── .env.example               # Template environment configuration
├── requirements.txt           # Project Python dependencies
└── README.md                  # Project Documentation
```

---

## 🚀 Quickstart Guide for Team Members

### 1. Clone the Repository
```bash
git clone https://github.com/Brolin5/CCP-Nigeria-Road-Management-System.git
cd CCP-Nigeria-Road-Management-System
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows PowerShell:
.\env\Scripts\Activate.ps1
# Windows Command Prompt:
.\env\Scripts\activate.bat
# Linux/macOS:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database (.env)
Create a `.env` file in the root directory based on `.env.example`:
```ini
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/nrms_db
APP_ENV=development
SECRET_KEY=nrms-super-secret-key-2026-production-grade
ALERTS_OVERDUE_DAYS=30
DUPLICATE_RADIUS_METERS=100
```

### 4. Create MySQL Database
In your MySQL Shell / Workbench:
```sql
CREATE DATABASE IF NOT EXISTS nrms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Run the Application
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🧪 Interactive API Documentation & Testing
Once the server is running, open your web browser:
* **Interactive Swagger UI**: [http://127.0.0.1:8000/doc](http://127.0.0.1:8000/doc) (or `/docs`)
* **Alternative ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **System Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Seed Demo Data
To immediately populate the database with demonstration roads, projects, and reports:
Execute `POST /seed-nrms-data` directly from the Swagger UI or via cURL:
```bash
curl -X POST http://127.0.0.1:8000/seed-nrms-data
```

---

## 🛡️ Key Features Implemented

1. **Strict Layer Decoupling**: Static AST check proves **0 model imports** in `service/`, `controller/`, and `route/`.
2. **Real-Time Text Search**: Multi-field SQL `LIKE` searching across all 9 domain models.
3. **Generic Pagination**: `PaginatedResponse[T]` preventing memory overhead on high-volume national road queries.
4. **Anti-Spoofing Nigerian Geofencing**: Server-side bounding box validation ($4.0^\circ\text{N} \le \text{Lat} \le 14.0^\circ\text{N}$, $2.5^\circ\text{E} \le \text{Lng} \le 15.0^\circ\text{E}$) rejecting foreign or spoofed coordinates.
5. **Real-Time Spatial Deduplication**: Automatically clusters defect reports within ~200 meters.
6. **Role-Based Access Control (RBAC)**: 4-tier domain governance (`citizen`, `contractor`, `inspector`, `admin`).
7. **Forensic Audit Trail**: Immutable `audit_logs` table capturing JSON delta before/after states, atomic server timestamps, and TCP socket IP addresses with `ON DELETE SET NULL` survivability.
