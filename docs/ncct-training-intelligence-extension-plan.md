# NCCT SahakarDrishti AI Extension Plan
**Platform:** NCCT Training Intelligence & Outcome Ecosystem  
**Tagline:** "From training records to early intervention and measurable outcomes."

---

## 1. Existing Features Found
Based on codebase inspection:
- **Frontend (React + Vite + Tailwind CSS):**
  - Routes: `/login`, `/dashboard`, `/cooperatives`, `/members`, `/courses`, `/learning`, `/assessments`, `/opportunities`, `/applications`, `/placements`, `/analytics`, `/notifications`, `/admin/users`, `/kiosk`, `/hq/dashboard`, `/hq/institutes`, `/hq/programme-approvals`, `/hq/national-calendar`, `/hq/certificates`.
  - Context & Utilities: `AuthContext`, `LanguageContext` (en/hi), `api.ts`, `offlineStore.ts`.
- **Backend (FastAPI + SQLAlchemy + SQLite/PostgreSQL):**
  - Routers: `auth`, `cooperatives`, `members`, `skills`, `assessments`, `courses`, `quizzes`, `opportunities`, `applications`, `placements`, `dashboards`, `sync`, `integrations`, `ai`, `districts`, `employees`, `notifications`, `hq`.
  - Models (32 models): `Institute`, `Programme`, `Batch`, `AttendanceRecord`, `NationalTemplate`, `CertificateRevocationLog`, `User`, `Role`, `Permission`, `RolePermission`, `District`, `Cooperative`, `MemberProfile`, `EmployeeProfile`, `Skill`, `RoleCatalog`, `RoleRequiredSkill`, `MemberSkill`, `SkillAssessment`, `AssessmentQuestion`, `AssessmentAnswer`, `SkillGap`, `Course`, `CourseLesson`, `CourseSkill`, `Enrollment`, `Quiz`, `QuizQuestion`, `QuizAttempt`, `Certificate`, `Opportunity`, `OpportunityRequiredSkill`, `Application`, `Placement`, `SyncEvent`, `ExternalErpRecord`, `AuditLog`, `Notification`.
  - ML Modules: `course_recommender.py`, `opportunity_matcher.py`, `quiz_generator.py`, `skill_gap_engine.py`, `evaluation.py`.
- **Mobile (Flutter + SQLite):**
  - Screens: `splash_screen.dart`, `login_screen.dart`, `member_dashboard_screen.dart`, `sync_centre_screen.dart`.
  - Core: `db_helper.dart` (10 tables: `cached_user`, `cached_member_profile`, `cached_skills`, `cached_courses`, `cached_lessons`, `cached_quizzes`, `cached_opportunities`, `cached_applications`, `pending_sync_operations`, `sync_metadata`), `sync_engine.dart`.
- **Authentication & RBAC:**
  - JWT Bearer tokens, password hashing with passlib/bcrypt.
  - Roles: `NCCT_SUPER_ADMIN`, `NCCT_PROGRAMME_ADMIN`, `NCCT_ANALYTICS_OFFICER`, `NCCT_CERTIFICATE_AUTHORITY`, `NCCT_AUDITOR`, `INSTITUTE_ADMIN`, `TRAINER`, `TRAINEE`, `PLACEMENT_OFFICER`, `KIOSK_OPERATOR`, `INSTITUTE_AUDITOR`.

---

## 2. Features to Preserve Unchanged
- **LMS & Course Player:** Lesson video/text player, quiz engine, automated certificate generation with QR verification.
- **Offline Kiosk & Mobile Mode:** Offline SQLite caching, draft offline quiz attempts, local check-in, background synchronization.
- **Existing User Profiles & Authentication:** JWT token generation, role verification dependencies (`deps.py`), password security.
- **Existing Cooperative & Member Management:** Cooperative directory, PACS mapping, member profile completion metrics.
- **Existing AI Engines:** Skill gap analysis, course recommender, candidate matcher, LLM/Rule quiz generator.

---

## 3. Database Migrations Required (Alembic)
1. **`institutes` table verification & 17 NCCT demo institute seed data:**
   - Seed 17 demo institute records ("Demo NCCT Institute 01" to "Demo NCCT Institute 17").
   - Ensure foreign keys `institute_id` across `users`, `programmes`, `batches`, `attendance_records`, `certificates`, etc.
2. **`venues` & `timetable_sessions` tables:**
   - `venues`: `id`, `institute_id`, `name`, `type` (CLASSROOM, LAB, HALL, ONLINE), `capacity`, `equipment_json`, `availability_status`.
   - `timetable_sessions`: `id`, `institute_id`, `programme_id`, `batch_id`, `module_id`, `title`, `session_date`, `start_time`, `end_time`, `venue_id`, `trainer_id`, `delivery_mode`, `session_status`, `attendance_required`, `notes`.
3. **`timetable_conflicts` table:**
   - `session_id`, `conflict_type` (TRAINER_DOUBLE_BOOKED, VENUE_DOUBLE_BOOKED, CAPACITY_EXCEEDED, OUTSIDE_PROGRAMME_DATE), `severity`, `details`, `status`, `resolved_by`, `resolved_at`.
4. **`attendance_records` extension:**
   - Fields: `timetable_session_id`, `attendance_status` (PRESENT, ABSENT, LATE, EXCUSED), `check_in_at`, `check_out_at`, `source_type` (BIOMETRIC_IMPORT, QR_KIOSK, MOBILE_CHECKIN, TRAINER_MANUAL, CSV_IMPORT, EXTERNAL_API), `external_reference_id`, `correction_reason`.
5. **`training_health_scores` table:**
   - `trainee_id`, `institute_id`, `programme_id`, `batch_id`, `attendance_component`, `learning_component`, `assessment_component`, `engagement_component`, `support_component`, `total_score`, `risk_level` (LOW, MEDIUM, HIGH), `risk_reasons_json`, `recommended_actions_json`, `model_version`, `calculated_at`.
6. **`risk_alerts` table:**
   - `trainee_id`, `institute_id`, `programme_id`, `batch_id`, `health_score_id`, `alert_type`, `severity`, `reasons_json`, `status`, `assigned_to`, `resolved_at`.
7. **`trainee_interventions` table:**
   - `trainee_id`, `institute_id`, `programme_id`, `batch_id`, `risk_alert_id`, `intervention_type` (REMEDIAL_COURSE, MENTOR_SESSION, TRAINER_CALL, LANGUAGE_SUPPORT, OFFLINE_CONTENT_PACKAGE, EXTRA_PRACTICE_QUIZ, ATTENDANCE_FOLLOWUP, TECHNICAL_SUPPORT), `reason`, `assigned_by`, `assigned_to`, `due_date`, `status`, `outcome_notes`, `completed_at`.
8. **`employers` & `recruiter_profiles` tables:**
   - `employers`: `id`, `institute_id` (nullable), `organisation_name`, `organisation_type`, `contact_person`, `email`, `phone`, `state`, `district`, `address`, `verified_status`.
   - `recruiter_profiles`: `id`, `user_id`, `employer_id`, `designation`, `is_active`.
9. **`candidate_recommendations` & `placements` extensions:**
   - `candidate_recommendations`: `opportunity_id`, `trainee_id`, `match_score`, `skill_similarity_score`, `explanation_json`, `status`.
   - `placements`: `followup_30_status`, `followup_60_status`, `followup_90_status`, `outcome_notes`.

---

## 4. New Roles & Permissions
- **HQ Level:** `NCCT_SUPER_ADMIN`, `NCCT_PROGRAMME_ADMIN`, `NCCT_ANALYTICS_OFFICER`, `NCCT_CERTIFICATE_AUTHORITY`, `NCCT_AUDITOR`.
- **Institute Level:** `INSTITUTE_ADMIN`, `INSTITUTE_PROGRAMME_COORDINATOR`, `TRAINER`, `ATTENDANCE_OPERATOR`, `PLACEMENT_OFFICER`, `RECRUITER`, `KIOSK_OPERATOR`, `INSTITUTE_AUDITOR`, `TRAINEE`.
- **Backend Scope Enforcement:**
  - `require_hq_role(...)`
  - `require_institute_role(...)`
  - `verify_institute_scope(user, target_institute_id)`
  - `verify_trainee_self_scope(user, trainee_id)`
  - `verify_recruiter_scope(user, employer_id)`

---

## 5. New API Endpoints
- **HQ Command Center & Data Quality:**
  - `GET /api/v1/hq/dashboard`
  - `GET /api/v1/hq/institutes`
  - `GET /api/v1/hq/training-intelligence`
  - `GET /api/v1/hq/at-risk-trainees`
  - `GET /api/v1/hq/institute-comparison`
  - `GET /api/v1/hq/national-calendar`
  - `GET /api/v1/hq/data-quality`
- **Programmes & Timetable:**
  - `POST /api/v1/programmes/{id}/submit-for-approval`
  - `POST /api/v1/programmes/{id}/approve`
  - `POST /api/v1/programmes/{id}/reject`
  - `GET /api/v1/timetable`
  - `POST /api/v1/timetable/sessions`
  - `POST /api/v1/timetable/sessions/{id}/reschedule`
  - `GET /api/v1/timetable/conflicts`
  - `POST /api/v1/timetable/conflicts/{id}/resolve`
  - `GET /api/v1/trainees/me/timetable`
  - `GET /api/v1/trainers/me/timetable`
- **Attendance Integration:**
  - `POST /api/v1/attendance/record`
  - `POST /api/v1/attendance/qr-checkin`
  - `POST /api/v1/attendance/import-csv`
  - `PATCH /api/v1/attendance/{id}/correct`
- **Training Intelligence & Interventions:**
  - `POST /api/v1/training-intelligence/recalculate/{trainee_id}`
  - `GET /api/v1/training-intelligence/trainee/{trainee_id}`
  - `GET /api/v1/training-intelligence/at-risk`
  - `POST /api/v1/training-intelligence/train-model`
  - `POST /api/v1/interventions`
  - `PATCH /api/v1/interventions/{id}`
  - `POST /api/v1/interventions/{id}/complete`
- **Recruiter & Opportunity Ecosystem:**
  - `POST /api/v1/employers`
  - `GET /api/v1/recruiters/dashboard`
  - `GET /api/v1/opportunities/{id}/recommended-candidates`
  - `POST /api/v1/placements/{id}/followup`
  - `GET /api/v1/data-quality/hq`

---

## 6. New React Pages / Routes
- **HQ Command Center Routes:**
  - `/hq/dashboard`, `/hq/institutes`, `/hq/programme-approvals`, `/hq/national-calendar`, `/hq/training-intelligence`, `/hq/at-risk-trainees`, `/hq/institute-comparison`, `/hq/certificate-registry`, `/hq/outcomes`, `/hq/data-quality`.
- **Institute Routes:**
  - `/institute/dashboard`, `/institute/programmes`, `/institute/batches`, `/institute/timetable`, `/institute/venues`, `/institute/trainers`, `/institute/attendance`, `/institute/training-intelligence`, `/institute/at-risk-trainees`, `/institute/interventions`, `/institute/certificates`, `/institute/placements`, `/institute/recruiters`, `/institute/data-quality`.
- **Trainer Routes:**
  - `/trainer/dashboard`, `/trainer/my-sessions`, `/trainer/my-timetable`, `/trainer/batch-progress`, `/trainer/at-risk-trainees`, `/trainer/interventions`, `/trainer/attendance`, `/trainer/assessments`.
- **Recruiter Routes:**
  - `/recruiter/dashboard`, `/recruiter/profile`, `/recruiter/opportunities`, `/recruiter/opportunities/new`, `/recruiter/candidates`, `/recruiter/applications`, `/recruiter/interviews`, `/recruiter/placements`, `/recruiter/followups`.
- **Trainee Routes:**
  - `/trainee/dashboard`, `/trainee/timetable`, `/trainee/my-learning`, `/trainee/assessments`, `/trainee/certificates`, `/trainee/opportunities`, `/trainee/applications`.

---

## 7. New Flutter Changes
- **SQLite Tables Added:**
  - `cached_timetable_sessions`, `cached_venues`, `cached_trainer_sessions`, `cached_opportunities`, `cached_applications`, `cached_interventions`, `cached_training_health_summary`, `pending_attendance_operations`, `pending_intervention_operations`.
- **Flutter UI Extensions:**
  - "My Timetable" screen with offline support and notification reminders.
  - "My Learning Health & Support Recommendations" (friendly learner UI: "You may benefit from extra support", "Recommended next step: complete ERP Reporting Basics").
  - Kiosk session QR scanner & instant check-in.
  - Trainer mobile check-in mode & intervention action recorder.

---

## 8. ML Dataset Schema (`data/synthetic_training_outcome_dataset.csv`)
Columns:
- `anonymized_trainee_id`
- `institute_id`
- `programme_id`
- `batch_id`
- `attendance_pct`
- `attendance_trend`
- `lesson_completion_pct`
- `quiz_average_score`
- `latest_quiz_score`
- `days_inactive`
- `failed_attempt_count`
- `assessment_completion_pct`
- `feedback_score`
- `trainer_intervention_count`
- `language_support_needed`
- `connectivity_issue_flag`
- `final_training_status` (0 = Completed, 1 = Dropped / Failed / Incomplete)

---

## 9. ML Model Plan
- **Rule-Based Training Health Score (0–100):**
  - Attendance (25%), Lesson Completion (20%), Assessment Performance (25%), Engagement/Inactivity (15%), Feedback & Support Signals (15%).
  - Risk categories: LOW (80–100), MEDIUM (60–79), HIGH (<60).
- **Machine Learning Classifier:**
  - Baseline: Logistic Regression.
  - Classifier: Random Forest Classifier.
  - Evaluated on Precision, Recall, F1-Score, ROC-AUC. Feature importances extracted for explainability.
  - Privacy guarantee: Zero sensitive attributes (caste, religion, gender, Aadhaar, financial status) used.

---

## 10. Timetable Workflow
```
Coordinator creates Programme & Batch 
  └─► Defines Sessions (Date, Time, Venue, Trainer)
        └─► Automated Conflict Engine checks:
              ├─ Trainer Double Booking?
              ├─ Venue Double Booking?
              ├─ Venue Capacity Exceeded?
              └─ Outside Programme Date Range?
        └─► If Conflict detected: Generates alert record
        └─► If Clean: Session confirmed & pushed to Trainee/Trainer timetable
```

---

## 11. Recruiter Dashboard Workflow
```
Recruiter posts Opportunity
  └─► Match Engine evaluates consented candidates:
        ├─ Skill alignment (50%)
        ├─ Certificate relevance (15%)
        ├─ Assessment score (10%)
        ├─ Location compatibility (10%)
        ├─ Availability (10%)
        └─ Education/Experience (5%)
  └─► Displays candidate with explainable match breakdown
  └─► Candidate applies / Recruiter shortlists
  └─► Interview scheduled -> Selection marked -> Placement created
  └─► Outcome follow-up logged at 30, 60, 90 days
```

---

## 12. Backward Compatibility Plan
- Existing database tables (`users`, `programmes`, `certificates`, `courses`, `assessments`) remain fully intact.
- Existing routes remain unchanged.
- `institute_id` defaults to Demo Institute 01 for existing unassigned records.
- Role mappings map legacy roles (`SUPER_ADMIN`, `DISTRICT_ADMIN`, `MEMBER`, etc.) to new HQ / Institute roles seamlessly.

---

## 13. Testing Plan
- **Backend Tests (`pytest`):**
  - Scope checks for HQ, Institute Admin, Trainer, Trainee, Recruiter.
  - Timetable conflict detector tests (trainer double booking, venue double booking).
  - Attendance check-in & CSV import verification.
  - Health score engine and intervention creation logic.
  - Recruiter match score calculation & consent enforcement.
- **Frontend & UI Verification:**
  - HQ command center widget & institute comparison render checks.
  - Interactive timetable drag-and-drop / modal calendar checks.
  - Recruiter candidate breakdown modal.
  - Trainee support recommendation view.
- **Flutter & Offline Sync Tests:**
  - SQLite schema creation test.
  - Offline attendance check-in & queue flush to FastAPI endpoint.

