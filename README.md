# COOPCONNECT AI
**AI-Enabled Cooperative Capacity Building, ERP & Employment Ecosystem**
*SIH Problem Statement: SIH26087*

CoopConnect AI is an intelligent capacity building and employment intelligence platform designed for cooperative societies. It acts as an AI-powered intelligence layer over existing cooperative ERPs, identifying member skill gaps, recommending personalized learning paths, generating trainer-approved quizzes, matching trained candidates with cooperative job opportunities, and ensuring offline-first operation in rural areas.

---

## Key Features & Capabilities

1. **Role-Based Access Control (RBAC)**: Support for 8 distinct roles (`SUPER_ADMIN`, `DISTRICT_ADMIN`, `COOPERATIVE_ADMIN`, `TRAINER`, `MEMBER`, `EMPLOYEE`, `EMPLOYER_OR_COOPERATIVE_RECRUITER`, `AUDITOR`) with district & cooperative multi-tenant data isolation.
2. **Explainable AI Skill-Gap Engine**: Calculates normalized gap scores ($required - current$) weighted by role priorities, excluding sensitive demographic attributes.
3. **Safe AI Quiz Generator**: Synthesizes MCQs, True/False, and short-answer questions from lesson content with a mandatory Trainer review & approval guardrail.
4. **Explainable AI Opportunity Matcher**: Weighted scoring algorithm (50% skills, 15% location, 10% availability, 10% education, 10% experience, 5% certification) for job and task matching.
5. **Offline Digital Kiosk Mode**: Dedicated `/kiosk` route on web and mobile kiosk interface with voice instructions (Text-to-Speech), large touch targets, QR/membership ID lookup, and auto-sync when network returns.
6. **Mobile Offline-First Architecture**: Flutter application powered by local SQLite (`sqflite`), connectivity awareness, local notifications, and REST sync engine with conflict resolution.
7. **ERP Integration API**: REST import/export API module for integration with external cooperative ERP systems (e.g., Tally, SAP).

---

## Monorepo Architecture & Folder Structure

```
coopconnect-ai/
├── backend/                  # Python 3.12 & FastAPI Backend
│   ├── app/
│   │   ├── main.py           # FastAPI entry point & CORS configuration
│   │   ├── core/             # Security, JWT, permissions, config
│   │   ├── db/               # Session, Base, 32 SQLAlchemy models, migrations
│   │   ├── schemas/          # Pydantic v2 schemas & response formatters
│   │   ├── api/v1/           # 18 REST API modules (Auth, Members, AI, Courses, etc.)
│   │   └── ml/               # Explainable AI engines (Skill gap, Matcher, Quiz generator)
│   ├── tests/                # Pytest unit & API integration test suite
│   ├── seed_data.py          # Complete SIH demo dataset script
│   ├── Dockerfile
│   └── requirements.txt
├── web/                      # React 18, TypeScript & Tailwind CSS Portal
│   ├── src/
│   │   ├── components/       # UI layout, Recharts analytics, Leaflet GIS map
│   │   ├── pages/            # 16 page views + Digital Kiosk Mode
│   │   ├── context/          # Auth & Language (EN/HI) providers
│   │   └── services/         # API fetch client & IndexedDB offline cache
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── mobile/                   # Flutter Mobile App (Dart)
│   ├── lib/
│   │   ├── core/             # SQLite DbHelper (10 tables), SyncEngine
│   │   ├── screens/          # 22 mobile screens (Dashboard, Kiosk, Quiz, etc.)
│   │   └── main.dart
│   └── pubspec.yaml
├── infra/
│   └── README.md             # AWS Cloud Deployment Architecture Guide
├── docker-compose.yml        # Docker Compose configuration for local dev
├── .env.example
└── README.md
```

---

## SIH Demo Credentials

> **Default Password for all Demo Users:** `ChangeMe123!`

| Role | Email | Purpose |
| :--- | :--- | :--- |
| **Cooperative Admin** | `manager@pragati.coop` | Pragati Dairy Cooperative Manager |
| **Member** | `member@example.com` | Meena Jadhav (Dairy Member) |
| **Trainer** | `trainer@example.com` | Capacity Master Trainer |
| **Recruiter** | `recruiter@example.com` | Dairy Job Recruiter |
| **District Admin** | `districtadmin@example.com` | Nashik District Officer |
| **Super Admin** | `superadmin@example.com` | System Administrator |

---

## Step-by-Step SIH Demonstration Script

1. **Login as Cooperative Manager**: Sign in with `manager@pragati.coop`.
2. **Open Pragati Dairy Cooperative**: View society details, 45 members, and critical skill gaps.
3. **Inspect Member Meena**: View Meena Jadhav's member profile.
4. **Target Role Selection**: Select target role `Digital Inventory Assistant`.
5. **Skill Assessment**: Run initial readiness assessment.
6. **Show Skill Profile**: View Meena's current skill competencies.
7. **Show Identified Skill Gaps**:
   - ERP Operation (Critical Gap: L1 -> L4)
   - Inventory Management (High Priority: L1 -> L4)
   - Report Generation (High Priority: L1 -> L3)
8. **Generate AI Recommendations**: View personalized course path recommendation (`ERP Fundamentals`).
9. **Enrol Meena in Course**: Enrol Meena in `ERP Fundamentals for Cooperative Staff`.
10. **Login as Trainer**: Sign in with `trainer@example.com`.
11. **Approve AI Quiz**: Review AI-generated lesson quiz and click "Approve".
12. **Login as Meena**: Sign in with `member@example.com`.
13. **Complete Course & Quiz**: Complete lesson reading, listen to voice assistant, and score 100% on quiz.
14. **Show Improved Readiness**: Verify Meena's readiness score increased to 78.5% and certificate was issued.
15. **Login as Recruiter**: Sign in with `recruiter@example.com`.
16. **Post Job Opportunity**: View `Digital Inventory Assistant` opportunity for Pragati Dairy.
17. **Explainable Candidate Match**: Inspect Meena's 92.5% explainable match score (50% skills, 15% location).
18. **Submit Application**: Apply Meena to the opportunity.
19. **Accept Candidate**: Recruiter accepts application status.
20. **Record Placement**: Record placement outcome (Income increased from ₹8,000 to ₹18,500/mo).
21. **Cooperative Dashboard Update**: Verify updated placed counts and capacity growth.
22. **Launch Digital Kiosk**: Navigate to `/kiosk` (Rural Kiosk mode).
23. **Member Lookup**: Input Meena's ID (`PRAGATI-MBR-2024-089`) or scan QR code.
24. **Voice Assistance**: Trigger Hindi/English audio instructions.
25. **Offline Quiz Attempt**: Complete offline quiz assessment on kiosk.
26. **Pending Sync Queue**: Verify result stored in local IndexedDB / SQLite queue.
27. **Restore Network & Sync**: Trigger synchronization.
28. **Verify Web Sync**: Confirm synced attempt reflected on central web portal.
29. **District Analytics**: View Nashik GIS map coverage and placement charts.

---

## Local Development & Setup Instructions

### 1. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```
Backend API OpenAPI Docs: `http://localhost:8000/docs`

### 2. Web Portal Setup (React)
```bash
cd web
npm install
npm run dev
```
Web App URL: `http://localhost:5173`

### 3. Mobile App Setup (Flutter)
```bash
cd mobile
flutter pub get
flutter run
```

### 4. Running via Docker Compose
```bash
docker-compose up --build -d
```

---

## Testing Commands

- **Backend Pytest Suite**:
  ```bash
  cd backend
  pytest
  ```
- **Web Frontend Build Check**:
  ```bash
  cd web
  npm run build
  ```
- **Flutter Widget Test**:
  ```bash
  cd mobile
  flutter test
  ```

---

## License & Compliance
Built for **Smart India Hackathon (SIH26087)** following strict algorithmic fairness, WCAG accessibility, and public-service design guidelines.
