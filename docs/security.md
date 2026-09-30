# Security & Scope Control Policy

## 1. Authentication & JWT Claims
* Password Hashing: `Passlib` bcrypt with salt.
* Bearer JWT Tokens: 24-hour expiration containing user `id`, `role`, and `institute_id`.

## 2. Multi-Tenant Scope Enforcers (`app/api/deps.py`)
1. **`require_hq_role`**:
   Allowed Roles: `NCCT_SUPER_ADMIN`, `NCCT_PROGRAMME_ADMIN`, `NCCT_ANALYTICS_OFFICER`, `NCCT_CERTIFICATE_AUTHORITY`, `NCCT_AUDITOR`, `SUPER_ADMIN`.
   Blocks any unauthorized institute user attempt to read/write national governance APIs.

2. **`verify_institute_scope`**:
   HQ users can access cross-institute aggregated data.
   Institute users are strictly scoped to their assigned `institute_id`. Attempting to access data from another institute returns `403 Forbidden`.

3. **`verify_trainee_self_scope`**:
   Protects trainee profile & privacy data.

## 3. Cryptographic Certificate Governance & QR Verification
* Central registry stores certificate hashes.
* Public QR verification endpoint `/api/v1/hq/certificates/verify/{certificate_number}` checks revocation status in real-time.
* Revocation requires explicit authorization and reason logging in `certificate_revocation_logs`.
