# SIH Demo Guide - NCCT Governance Layer

## 1. Demo Credentials

> **Default Password for all accounts**: `ChangeMe123!`

### NCCT Headquarters Governance Persona Accounts
* **NCCT Super Admin**: `hqadmin@ncct.gov.in` (Director General)
* **NCCT Programme Admin**: `programmeadmin@ncct.gov.in` (National Academic Coordinator)
* **NCCT Certificate Authority**: `certauthority@ncct.gov.in` (National Certificate Authority)
* **NCCT Auditor**: `auditor@example.com` (National Security Auditor)

### Institute Level Persona Accounts
* **Institute Admin**: `manager@pragati.coop` (Priya Sharma - ICM Pune)
* **Master Trainer**: `trainer@example.com` (Priya Deshmukh - ICM Pune)
* **Trainee (Ramesh Kumar)**: `ramesh@example.com` (Panchale, Sinnar, Nashik)
* **Placement Officer**: `recruiter@example.com` (Suresh Kulkarni)

---

## 2. Key Demo Navigation Paths

1. **National Dashboard**: Navigate to `http://localhost:5173/hq/dashboard` after logging in as `hqadmin@ncct.gov.in`.
   - View 20 NCCT Institutes summary cards.
   - Inspect the national 20 institutes comparison table.
   - View real-time sync health for all 20 institutes.

2. **20 NCCT Institutes Directory**: Navigate to `/hq/institutes`.
   - Filter institutes by State and Region (North, South, East, West, Central, North-East).

3. **Programme Approvals Workflow**: Navigate to `/hq/programme-approvals`.
   - Review pending programme proposals from institutes.
   - Click **Approve Programme** to grant national accreditation.

4. **Certificate Registry & QR Verification**: Navigate to `/hq/certificates` or `/hq/certificate-verification`.
   - Test certificate verification with code: `CERT-SIH-2026-RAMESH-ERP`.
   - Test real-time revocation with audit logging.
