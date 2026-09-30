# COOPCONNECT — Missing Features & Incremental Extension Plan
**Platform:** COOPCONNECT (NCCT Training Intelligence & Outcome Ecosystem)  
**Tagline:** From training records to early intervention and measurable outcomes.

---

## 1. Existing Implemented Features

### A. Frontend (React + TypeScript + Vite + Tailwind CSS)
- **Authentication & Navigation:** `Login.tsx` with intelligent role-based routing and demo switchers, `Navbar.tsx` with multi-role themes and live language switcher (English / हिंदी), `Sidebar.tsx` with role-tailored navigation items.
- **Dashboards:** Role-differentiated `Dashboard.tsx` supporting HQ Command Center, Institute Admin Campus Operations, Faculty/Trainer Schedule & Support Roster, Recruiter & Placement Portal, District Governance GIS, and Trainee 5-step personal learning hub.
- **Operational & Learning Pages:** `Cooperatives.tsx`, `Members.tsx`, `Courses.tsx`, `CourseDetail.tsx`, `LearningPlayer.tsx`, `SkillGaps.tsx`, `Opportunities.tsx`, `OpportunityDetail.tsx`, `Applications.tsx`, `Placements.tsx`, `Analytics.tsx`, `Notifications.tsx`, `AdminUsers.tsx`, `KioskMode.tsx` (offline-first touchscreen with voice synthesis and local storage), and `HQGovernancePortal.tsx` (20 institutes governance, templates, certificate verification, audit logs).

### B. Backend (FastAPI + SQLAlchemy + SQLite/PostgreSQL)
- **Core Models (32 models preserved):** `Institute`, `Programme`, `Batch`, `AttendanceRecord`, `NationalTemplate`, `CertificateRevocationLog`, `User`, `Role`, `Permission`, `RolePermission`, `District`, `Cooperative`, `MemberProfile`, `EmployeeProfile`, `Skill`, `RoleCatalog`, `RoleRequiredSkill`, `MemberSkill`, `SkillAssessment`, `AssessmentQuestion`, `AssessmentAnswer`, `SkillGap`, `Course`, `CourseLesson`, `CourseSkill`, `Enrollment`, `Quiz`, `QuizQuestion`, `QuizAttempt`, `Certificate`, `Opportunity`, `OpportunityRequiredSkill`, `Application`, `Placement`, `SyncEvent`, `ExternalErpRecord`, `AuditLog`, `Notification`.
- **API Routers (17 v1 routers):** `auth`, `cooperatives`, `members`, `skills`, `assessments`, `courses`, `quizzes`, `opportunities`, `applications`, `placements`, `dashboards`, `sync`, `integrations`, `ai`, `districts`, `employees`, `notifications`, `hq`.
- **Security & RBAC:** OAuth2 Password Bearer JWT authentication with bcrypt hashing. Dependencies (`deps.py`) enforcing `require_hq_role`, `require_institute_role`, `verify_institute_scope` (strict 20 institutes isolation), `verify_trainee_self_scope`, and `verify_recruiter_scope`.
- **Initial AI/ML Modules:** `course_recommender.py`, `opportunity_matcher.py` (cosine similarity skill matching), `quiz_generator.py`, `skill_gap_engine.py`, `evaluation.py`.

### C. Mobile & Kiosk (Flutter + SQLite)
- **Screens:** `splash_screen.dart`, `login_screen.dart`, `member_dashboard_screen.dart`, `sync_centre_screen.dart`.
- **SQLite Database (`db_helper.dart`):** `cached_user`, `cached_member_profile`, `cached_skills`, `cached_courses`, `cached_lessons`, `cached_quizzes`, `cached_opportunities`, `cached_applications`, `pending_sync_operations`, `sync_metadata`.
- **Sync Engine:** `sync_engine.dart` for offline-first queue flushing.

---

## 2. Missing Features Found to Implement

1. **Venues, Timetable & Conflict Engine:**
   - Missing tables: `venues`, `timetable_sessions`, `timetable_conflicts`.
   - Missing real-time automated conflict detector (Trainer double-booking, Venue double-booking, Venue capacity exceeded, date range mismatch).
   - Missing trainer workload & session completion workflow.
2. **Attendance Integration Layer:**
   - Missing multi-source attendance integration (Biometric CSV import, QR kiosk check-in, trainer manual mark, external API connector).
   - Missing consecutive absence detector and certificate eligibility calculator.
3. **Rule-Based Training Health Score & Risk Alerts:**
   - Missing `training_health_scores` and `risk_alerts` tables.
   - Missing weighted 0-100 Training Health Score engine (Attendance 25%, Learning Completion 20%, Assessment Performance 25%, Inactivity 15%, Support Signals 15%).
   - Missing learner-friendly UI recommendation mappings.
4. **Trainer Intervention Workflow:**
   - Missing `trainee_interventions` table and intervention assignment/completion API.
5. **Recruiter / Employer Dashboard & Matching Engine:**
   - Missing `employers`, `recruiter_profiles`, and `candidate_recommendations` tables.
   - Missing multi-factor consented candidate recommendation engine (50% skill, 15% certificate, 10% assessment, 10% location, 10% availability, 5% education/experience) and 30/60/90-day placement outcome tracking.
6. **Synthetic ML Dataset & Training Pipeline:**
   - Missing `data/synthetic_training_outcome_dataset.csv` (1,500 synthetic trainees across 20 institutes) and ML classification pipeline (Random Forest / Logistic Regression with precision, recall, F1, and confusion matrix).
7. **Data Quality & Sync Health Monitoring:**
   - Missing automated data-quality checks across institutes (missing profiles, unapproved programmes, unsynced kiosks, duplicate certificate checks).

---

## 3. Database Models & Alembic Migrations

### A. Existing Models to Preserve Unchanged
All 32 existing models in `app/db/models/` (`Institute`, `User`, `Cooperative`, `MemberProfile`, `Skill`, `Course`, `Quiz`, `Certificate`, `Opportunity`, `Application`, `Placement`, `SyncEvent`, etc.) remain fully preserved.

### B. New Models to Add
1. `Venue` (`venues`)
2. `TimetableSession` (`timetable_sessions`)
3. `TimetableConflict` (`timetable_conflicts`)
4. `TrainingHealthScore` (`training_health_scores`)
5. `RiskAlert` (`risk_alerts`)
6. `TraineeIntervention` (`trainee_interventions`)
7. `Employer` (`employers`)
8. `RecruiterProfile` (`recruiter_profiles`)
9. `CandidateRecommendation` (`candidate_recommendations`)

### C. Migration Strategy
- Non-destructive Alembic migration scripts adding new tables and columns while preserving all existing data.

---

## 4. API Endpoints Plan

### Existing APIs Preserved
- `/api/v1/auth/*`, `/api/v1/members/*`, `/api/v1/courses/*`, `/api/v1/quizzes/*`, `/api/v1/assessments/*`, `/api/v1/sync/*`, `/api/v1/hq/*`.

### New APIs to Implement
- **Programmes Approval:** `POST /api/v1/programmes/{id}/submit-for-approval`, `POST /api/v1/programmes/{id}/approve`, `POST /api/v1/programmes/{id}/reject`, `POST /api/v1/programmes/{id}/request-changes`.
- **Timetable & Venues:** `GET /api/v1/timetable`, `POST /api/v1/timetable/sessions`, `PATCH /api/v1/timetable/sessions/{id}`, `POST /api/v1/timetable/sessions/{id}/reschedule`, `GET /api/v1/timetable/conflicts`, `POST /api/v1/timetable/conflicts/{id}/resolve`, `GET /api/v1/trainees/me/timetable`, `GET /api/v1/trainers/me/timetable`.
- **Attendance Integration:** `POST /api/v1/attendance/record`, `POST /api/v1/attendance/qr-checkin`, `POST /api/v1/attendance/import-csv`, `GET /api/v1/attendance/batch/{batch_id}`, `PATCH /api/v1/attendance/{id}/correct`.
- **Training Intelligence & Alerts:** `POST /api/v1/training-intelligence/recalculate/{trainee_id}`, `GET /api/v1/training-intelligence/trainee/{trainee_id}`, `GET /api/v1/training-intelligence/at-risk`, `POST /api/v1/training-intelligence/train-model`, `GET /api/v1/training-intelligence/model-metrics`.
- **Interventions:** `POST /api/v1/interventions`, `GET /api/v1/interventions`, `PATCH /api/v1/interventions/{id}`, `POST /api/v1/interventions/{id}/complete`.
- **Recruiters & Opportunities:** `POST /api/v1/employers`, `GET /api/v1/recruiters/dashboard`, `GET /api/v1/opportunities/{id}/recommended-candidates`, `POST /api/v1/placements/{id}/followup`.
- **Data Quality:** `GET /api/v1/data-quality/hq`, `GET /api/v1/data-quality/institute`, `GET /api/v1/data-quality/sync-health`.

---

## 5. UI Routes & Frontend Extensions

### Existing UI Routes Preserved
`/login`, `/dashboard`, `/cooperatives`, `/members`, `/courses`, `/learning`, `/assessments`, `/opportunities`, `/applications`, `/placements`, `/analytics`, `/notifications`, `/admin/users`, `/kiosk`, `/hq/dashboard`, `/hq/institutes`, `/hq/programme-approvals`, `/hq/national-calendar`, `/hq/certificates`.

### New Dedicated UI Routes & Views
- **HQ Command Views:** `/hq/training-intelligence`, `/hq/at-risk-trainees`, `/hq/institute-comparison`, `/hq/data-quality`.
- **Institute Operations Views:** `/institute/timetable`, `/institute/venues`, `/institute/programmes`, `/institute/training-intelligence`, `/institute/interventions`.
- **Faculty / Trainer Views:** `/trainer/my-timetable`, `/trainer/my-sessions`, `/trainer/at-risk-trainees`, `/trainer/interventions`.
- **Recruiter Views:** `/recruiter/dashboard`, `/recruiter/opportunities/new`, `/recruiter/candidates`, `/recruiter/followups`.
- **Trainee Views:** `/trainee/timetable`, `/trainee/support-recommendations`.

---

## 6. Mobile & Kiosk (Flutter) Plan

### Existing SQLite Tables Preserved
`cached_user`, `cached_member_profile`, `cached_skills`, `cached_courses`, `cached_lessons`, `cached_quizzes`, `cached_opportunities`, `cached_applications`, `pending_sync_operations`, `sync_metadata`.

### New SQLite Tables to Add
`cached_timetable_sessions`, `cached_venues`, `cached_trainer_sessions`, `cached_interventions`, `cached_training_health_summary`, `pending_attendance_operations`, `pending_intervention_operations`.

---

## 7. Risks & Backward Compatibility Strategy
- **Zero Table Drops:** Database schema additions use non-destructive operations with default values for existing records.
- **Scope Isolation:** Strict backend enforcement in FastAPI dependencies preventing cross-institute data exposure.
- **Privacy Assurance:** Zero sensitive attributes (caste, religion, gender, Aadhaar, financial data) used in health scoring or recruiter matching.

---

## 8. Test Plan
- Unit tests for Timetable Conflict Engine (trainer and venue double booking detection).
- Unit tests for Attendance CSV import and check-in workflows.
- Unit tests for Rule-Based Training Health Score calculation and risk alert creation.
- Unit tests for Recruiter candidate recommendation engine and privacy masking.
- Full end-to-end integration test of the 27-step demonstration flow.
