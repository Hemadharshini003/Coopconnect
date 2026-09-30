# NCCT SahakarDrishti AI — Role-Based Access Control (RBAC) & Scope Specification

## 1. Hierarchy Overview

```
                          ┌─────────────────────────────┐
                          │   NCCT Headquarters Layer   │
                          └──────────────┬──────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
    ┌────────────▼───────────┐                       ┌───────────▼────────────┐
    │ NCCT Governance Roles  │                       │   National Analytics   │
    │ NCCT_SUPER_ADMIN       │                       │ NCCT_ANALYTICS_OFFICER │
    │ NCCT_PROGRAMME_ADMIN   │                       │ NCCT_AUDITOR           │
    │ NCCT_CERTIFICATE_AUTH  │                       └────────────────────────┘
    └────────────┬───────────┘
                 │
  ───────────────┼─────────────────────────────────────────────────────────────
                 │  (20 NCCT Institutes Boundary - Strict Isolation)
  ───────────────┼─────────────────────────────────────────────────────────────
                 │
    ┌────────────▼───────────┐
    │   Institute 01 .. 20   │
    ├────────────────────────┤
    │ INSTITUTE_ADMIN        │
    │ PROGRAMME_COORDINATOR  │
    │ TRAINER                │
    │ ATTENDANCE_OPERATOR    │
    │ PLACEMENT_OFFICER      │
    │ KIOSK_OPERATOR         │
    └────────────┬───────────┘
                 │
        ┌────────┴────────┐
        │                 │
 ┌──────▼──────┐   ┌──────▼───────┐
 │   TRAINEE   │   │  RECRUITER   │
 └─────────────┘   └──────────────┘
```

---

## 2. Role Definitions & Access Matrix

### A. NCCT Headquarters Roles (National Scope)
1. **`NCCT_SUPER_ADMIN`**: Unrestricted read/write across all 20 NCCT Institutes, users, national templates, approvals, and audit logs.
2. **`NCCT_PROGRAMME_ADMIN`**: Can review and approve/reject programme proposals from institutes, view national calendar, and manage national training templates. Cannot alter individual trainee assessment marks.
3. **`NCCT_ANALYTICS_OFFICER`**: Read-only national analytics, institute comparisons, and outcome reporting. Cannot modify operational data.
4. **`NCCT_CERTIFICATE_AUTHORITY`**: Central certificate registry access, verification code search, certificate revocation with reason & audit logging.
5. **`NCCT_AUDITOR`**: Read-only access to audit logs, data health, sync events, and approval records across all institutes.

### B. Institute Level Roles (Strict Single-Institute Scope)
1. **`INSTITUTE_ADMIN`**: Full administrative access confined strictly to their own institute. Manages local staff, programmes, batches, venues, timetable, attendance, assessments, and local placement records.
2. **`INSTITUTE_PROGRAMME_COORDINATOR`**: Manages assigned programmes, batches, venues, timetable sessions, and trainer allocations.
3. **`TRAINER`**: Can view assigned batches, conduct sessions, record session completion, submit attendance (when authorized), launch quizzes, view trainee risk alerts, and assign remedial interventions.
4. **`ATTENDANCE_OPERATOR`**: Authorized to check in trainees and record/upload attendance data.
5. **`PLACEMENT_OFFICER`**: Manages institute opportunities, applications, candidate recommendations, and 30/60/90-day placement follow-ups.
6. **`KIOSK_OPERATOR`**: Manages shared institute kiosk device states and assists trainee session check-ins without storing lingering sensitive data.
7. **`INSTITUTE_AUDITOR`**: Read-only access to local institute records and data quality reports.

### C. Participant Roles
1. **`TRAINEE`**: Confined strictly to own profile, registered batch timetable, learning player, assessments, certificates, and job applications.
2. **`RECRUITER`**: Organization-scoped opportunity creator. Can access consented eligible candidate recommendations and process job applications for their organization.

---

## 3. Backend Scope Validation API (`app/api/deps.py`)

- **`require_hq_role(current_user)`**: Ensures caller has an HQ role.
- **`require_institute_role(current_user)`**: Ensures caller has an authorized Institute or HQ role.
- **`verify_institute_scope(target_institute_id, current_user)`**:
  - HQ users can target any institute or pass `None` for national view.
  - Institute users are locked to `current_user.institute_id`. Cross-institute access attempts raise `HTTP 403 Forbidden`.
- **`verify_trainee_self_scope(target_trainee_id, current_user)`**:
  - Trainees can only access their own user ID.
  - Staff / HQ users can access trainee data within their institute scope.
- **`verify_recruiter_scope(target_employer_id, current_user)`**:
  - Validates recruiter organizational boundaries.

