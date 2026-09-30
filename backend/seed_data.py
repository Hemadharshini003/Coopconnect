import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal, engine, Base
from app.db.models import *
from app.core.security import get_password_hash

def seed():
    print("Seeding COOPCONNECT with NCCT HQ & 20 Institutes Governance Data...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing demo data cleanly
    try:
        db.query(CertificateRevocationLog).delete()
        db.query(NationalTemplate).delete()
        db.query(AttendanceRecord).delete()
        db.query(Batch).delete()
        db.query(Programme).delete()
        db.query(Placement).delete()
        db.query(Application).delete()
        db.query(OpportunityRequiredSkill).delete()
        db.query(Opportunity).delete()
        db.query(Certificate).delete()
        db.query(QuizAttempt).delete()
        db.query(QuizQuestion).delete()
        db.query(Quiz).delete()
        db.query(Enrollment).delete()
        db.query(CourseSkill).delete()
        db.query(CourseLesson).delete()
        db.query(Course).delete()
        db.query(SkillGap).delete()
        db.query(AssessmentAnswer).delete()
        db.query(AssessmentQuestion).delete()
        db.query(SkillAssessment).delete()
        db.query(MemberSkill).delete()
        db.query(RoleRequiredSkill).delete()
        db.query(RoleCatalog).delete()
        db.query(Skill).delete()
        db.query(EmployeeProfile).delete()
        db.query(MemberProfile).delete()
        db.query(User).delete()
        db.query(Cooperative).delete()
        db.query(District).delete()
        db.query(Institute).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Clean warning: {e}")

    # 1. Seed 20 NCCT Training Institutes (RICMs & ICMs across India)
    institutes_data = [
        ("inst-01", "RICM-BLR", "RICM Bengaluru", "Regional Institute of Cooperative Management", "South", "Karnataka", "Bengaluru", "ricm.blr@ncct.gov.in", "+91 80 2334 1122"),
        ("inst-02", "RICM-GND", "RICM Gandhinagar", "Regional Institute of Cooperative Management", "West", "Gujarat", "Gandhinagar", "ricm.gnd@ncct.gov.in", "+91 79 2322 4455"),
        ("inst-03", "RICM-CHD", "RICM Chandigarh", "Regional Institute of Cooperative Management", "North", "Punjab", "Chandigarh", "ricm.chd@ncct.gov.in", "+91 172 260 1199"),
        ("inst-04", "RICM-KLY", "RICM Kalyani", "Regional Institute of Cooperative Management", "East", "West Bengal", "Kalyani", "ricm.kly@ncct.gov.in", "+91 33 2582 8844"),
        ("inst-05", "RICM-PAT", "RICM Patna", "Regional Institute of Cooperative Management", "East", "Bihar", "Patna", "ricm.pat@ncct.gov.in", "+91 612 228 3322"),
        ("inst-06", "ICM-PNE", "ICM Pune", "Institute of Cooperative Management", "West", "Maharashtra", "Pune", "icm.pne@ncct.gov.in", "+91 20 2565 7711"),
        ("inst-07", "ICM-JPR", "ICM Jaipur", "Institute of Cooperative Management", "North", "Rajasthan", "Jaipur", "icm.jpr@ncct.gov.in", "+91 141 270 4433"),
        ("inst-08", "ICM-LKO", "ICM Lucknow", "Institute of Cooperative Management", "North", "Uttar Pradesh", "Lucknow", "icm.lko@ncct.gov.in", "+91 522 238 9911"),
        ("inst-09", "ICM-BPL", "ICM Bhopal", "Institute of Cooperative Management", "Central", "Madhya Pradesh", "Bhopal", "icm.bpl@ncct.gov.in", "+91 755 267 2233"),
        ("inst-10", "ICM-DDN", "ICM Dehradun", "Institute of Cooperative Management", "North", "Uttarakhand", "Dehradun", "icm.ddn@ncct.gov.in", "+91 135 273 5566"),
        ("inst-11", "ICM-GHY", "ICM Guwahati", "Institute of Cooperative Management", "North-East", "Assam", "Guwahati", "icm.ghy@ncct.gov.in", "+91 361 226 7788"),
        ("inst-12", "ICM-HYD", "ICM Hyderabad", "Institute of Cooperative Management", "South", "Telangana", "Hyderabad", "icm.hyd@ncct.gov.in", "+91 40 2401 9922"),
        ("inst-13", "ICM-MDR", "ICM Madurai", "Institute of Cooperative Management", "South", "Tamil Nadu", "Madurai", "icm.mdr@ncct.gov.in", "+91 452 245 8833"),
        ("inst-14", "ICM-NGP", "ICM Nagpur", "Institute of Cooperative Management", "West", "Maharashtra", "Nagpur", "icm.ngp@ncct.gov.in", "+91 712 253 4411"),
        ("inst-15", "ICM-SML", "ICM Shimla", "Institute of Cooperative Management", "North", "Himachal Pradesh", "Shimla", "icm.sml@ncct.gov.in", "+91 177 283 1122"),
        ("inst-16", "ICM-TRV", "ICM Thiruvananthapuram", "Institute of Cooperative Management", "South", "Kerala", "Thiruvananthapuram", "icm.trv@ncct.gov.in", "+91 471 234 5566"),
        ("inst-17", "ICM-VNS", "ICM Varanasi", "Institute of Cooperative Management", "North", "Uttar Pradesh", "Varanasi", "icm.vns@ncct.gov.in", "+91 542 250 8899"),
        ("inst-18", "ICM-IMP", "ICM Imphal", "Institute of Cooperative Management", "North-East", "Manipur", "Imphal", "icm.imp@ncct.gov.in", "+91 385 244 1122"),
        ("inst-19", "ICM-RPR", "ICM Raipur", "Institute of Cooperative Management", "Central", "Chhattisgarh", "Raipur", "icm.rpr@ncct.gov.in", "+91 771 242 7744"),
        ("inst-20", "ICM-RNC", "ICM Ranchi", "Institute of Cooperative Management", "East", "Jharkhand", "Ranchi", "icm.rnc@ncct.gov.in", "+91 651 224 3355")
    ]

    institute_models = []
    for i_id, code, name, itype, reg, state, city, email, phone in institutes_data:
        inst = Institute(
            id=i_id,
            code=code,
            name=name,
            institute_type=itype,
            region=reg,
            state=state,
            city=city,
            address=f"NCCT Campus, {city}, {state}",
            contact_email=email,
            contact_phone=phone,
            director_name=f"Dr. Director ({code})",
            total_training_capacity=600,
            is_active=True,
            sync_status="HEALTHY"
        )
        institute_models.append(inst)
    db.add_all(institute_models)
    db.commit()

    # 2. District & Cooperative
    district = District(
        id="d1111111-1111-1111-1111-111111111111",
        name="Nashik",
        state="Maharashtra",
        country="India",
        code="NSK"
    )
    db.add(district)
    db.commit()

    coop1 = Cooperative(
        id="c1111111-1111-1111-1111-111111111111",
        name="Pragati Dairy Cooperative",
        registration_number="MH-NSK-DAIRY-2021-042",
        cooperative_type="Dairy Cooperative",
        description="Premier rural milk collection & processing cooperative society in Nashik district.",
        state="Maharashtra",
        district_id=district.id,
        institute_id="inst-06", # ICM Pune
        block="Sinnar",
        village="Panchale",
        address="Main Road, Panchale, Sinnar, Nashik - 422103",
        phone="+91 98230 11223",
        email="info@pragatifarmer.coop"
    )
    db.add(coop1)
    db.commit()

    # 3. Common Password Hash
    pwd_hash = get_password_hash("ChangeMe123!")

    # NCCT Headquarters Governance Users
    hq_super_admin = User(
        id="u-hq-001",
        email="hqadmin@ncct.gov.in",
        phone="+91 11 2651 0001",
        password_hash=pwd_hash,
        full_name="Director General NCCT HQ",
        role="NCCT_SUPER_ADMIN"
    )
    hq_prog_admin = User(
        id="u-hq-002",
        email="programmeadmin@ncct.gov.in",
        phone="+91 11 2651 0002",
        password_hash=pwd_hash,
        full_name="NCCT National Academic Coordinator",
        role="NCCT_PROGRAMME_ADMIN"
    )
    hq_cert_auth = User(
        id="u-hq-003",
        email="certauthority@ncct.gov.in",
        phone="+91 11 2651 0003",
        password_hash=pwd_hash,
        full_name="NCCT National Certificate Authority",
        role="NCCT_CERTIFICATE_AUTHORITY"
    )

    # Institute Level Users
    super_admin = User(
        id="u0000000-0000-0000-0000-000000000000",
        email="superadmin@example.com",
        phone="+91 90000 00001",
        password_hash=pwd_hash,
        full_name="System Administrator",
        role="SUPER_ADMIN"
    )

    district_admin = User(
        id="u1111111-1111-1111-1111-111111111111",
        email="districtadmin@example.com",
        phone="+91 90000 00002",
        password_hash=pwd_hash,
        full_name="District Collector / Rajesh Sharma",
        role="DISTRICT_ADMIN",
        district_id=district.id,
        institute_id="inst-06"
    )

    manager = User(
        id="u2222222-2222-2222-2222-222222222222",
        email="manager@pragati.coop",
        phone="+91 98230 11223",
        password_hash=pwd_hash,
        full_name="Priya Sharma (Cooperative Manager)",
        role="INSTITUTE_ADMIN",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    inst_blr_admin = User(
        id="u-inst-blr-admin",
        email="admin.blr@ricm.ncct.gov.in",
        phone="+91 80 2334 1123",
        password_hash=pwd_hash,
        full_name="Dr. K. Narayana (RICM Bengaluru Admin)",
        role="INSTITUTE_ADMIN",
        institute_id="inst-01"
    )

    inst_blr_trainer = User(
        id="u-inst-blr-trainer",
        email="trainer.blr@ricm.ncct.gov.in",
        phone="+91 80 2334 1124",
        password_hash=pwd_hash,
        full_name="Prof. S. R. Rao (RICM Bengaluru Faculty)",
        role="TRAINER",
        institute_id="inst-01"
    )

    trainer = User(
        id="u3333333-3333-3333-3333-333333333333",
        email="trainer@example.com",
        phone="+91 90000 00004",
        password_hash=pwd_hash,
        full_name="Priya Deshmukh (Capacity Master Trainer)",
        role="TRAINER",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    ramesh_user = User(
        id="u4444444-4444-4444-4444-444444444444",
        email="ramesh@example.com",
        phone="+91 98811 55443",
        password_hash=pwd_hash,
        full_name="Ramesh Kumar",
        role="TRAINEE",
        preferred_language="hi",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    meena_patil = User(
        id="u-trainee-meena-patil",
        email="meena.patil@ruralcoop.in",
        phone="+91 98811 99887",
        password_hash=pwd_hash,
        full_name="Meena Patil",
        role="TRAINEE",
        preferred_language="hi",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    meena_user = User(
        id="u6666666-6666-6666-6666-666666666666",
        email="member@example.com",
        phone="+91 98811 22334",
        password_hash=pwd_hash,
        full_name="Meena Jadhav",
        role="TRAINEE",
        preferred_language="hi",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    recruiter = User(
        id="u5555555-5555-5555-5555-555555555555",
        email="recruiter@example.com",
        phone="+91 90000 00006",
        password_hash=pwd_hash,
        full_name="Suresh Kulkarni (Dairy Recruiter)",
        role="PLACEMENT_OFFICER",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    recruiter_coop = User(
        id="u-recruiter-pragati",
        email="recruiter@pragatifarmer.coop",
        phone="+91 90000 00099",
        password_hash=pwd_hash,
        full_name="Anand Shinde (Pragati Talent Officer)",
        role="RECRUITER",
        district_id=district.id,
        cooperative_id=coop1.id,
        institute_id="inst-06"
    )

    auditor = User(
        id="u7777777-7777-7777-7777-777777777777",
        email="auditor@example.com",
        phone="+91 90000 00007",
        password_hash=pwd_hash,
        full_name="Auditor Verma",
        role="NCCT_AUDITOR",
        district_id=district.id
    )

    db.add_all([
        hq_super_admin, hq_prog_admin, hq_cert_auth, 
        super_admin, district_admin, manager, 
        inst_blr_admin, inst_blr_trainer, trainer, 
        ramesh_user, meena_patil, meena_user, 
        recruiter, recruiter_coop, auditor
    ])
    db.commit()

    # 4. Member Profiles
    profile_ramesh = MemberProfile(
        id="m4444444-4444-4444-4444-444444444444",
        user_id=ramesh_user.id,
        cooperative_id=coop1.id,
        membership_number="PRAGATI-M-2023-089",
        education_level="Higher Secondary (12th Pass)",
        occupation="Dairy Assistant & Milk Testing Operator",
        years_of_experience=3,
        profile_completion_percentage=85.0
    )
    profile_meena = MemberProfile(
        id="m6666666-6666-6666-6666-666666666666",
        user_id=meena_user.id,
        cooperative_id=coop1.id,
        membership_number="PRAGATI-M-2024-012",
        education_level="Bachelor of Commerce (B.Com)",
        occupation="Junior Accounts Clerk",
        years_of_experience=1,
        profile_completion_percentage=90.0
    )
    profile_meena_patil = MemberProfile(
        id="m-meena-patil-profile",
        user_id=meena_patil.id,
        cooperative_id=coop1.id,
        membership_number="NCCT-TR-2026-001",
        education_level="Graduate (B.Com / Rural Banking)",
        occupation="Cooperative ERP Trainee",
        years_of_experience=1,
        profile_completion_percentage=95.0
    )
    db.add_all([profile_ramesh, profile_meena, profile_meena_patil])
    db.commit()

    # 5. Skills & Role Catalog
    skills_data = [
        ("s1111111-1111-1111-1111-111111111111", "Cooperative Principles & Bye-laws", "COOP_PRINCIPLES", "Governance"),
        ("s2222222-2222-2222-2222-222222222222", "Basic Bookkeeping & Day Book Entry", "BOOKKEEPING", "Finance & Accounting"),
        ("s3333333-3333-3333-3333-333333333333", "PACS ERP Operations & Data Entry", "ERP_OPERATIONS", "Digital Tools"),
        ("s4444444-4444-4444-4444-444444444444", "Inventory & Warehouse Stock Management", "INVENTORY_MGMT", "Supply Chain"),
        ("s5555555-5555-5555-5555-555555555555", "Statutory Audit & Compliance Verification", "STATUTORY_AUDIT", "Governance")
    ]
    for s_id, s_name, s_code, s_cat in skills_data:
        db.add(Skill(id=s_id, name=s_name, code=s_code, category=s_cat, description=f"Skill descriptor for {s_name}"))
    db.commit()

    # 6. Courses & Lessons
    course1 = Course(
        id="course-c01",
        title="PACS ERP Operations & Digital Accounting",
        description="Comprehensive practical training on PACS ERP software, day book entry, trial balance reconciliation, and inventory tracking.",
        category="Digital Tools",
        difficulty="Intermediate",
        duration_minutes=180,
        status="Published"
    )
    db.add(course1)
    db.commit()

    lesson1 = CourseLesson(
        id="lesson-l01",
        course_id=course1.id,
        title="1. Introduction to PACS Day Book Entry",
        sequence_number=1,
        duration_minutes=30,
        text_content="Learn the step-by-step procedure for recording cash receipt and disbursement vouchers in modern cooperative ERP systems."
    )
    db.add(lesson1)
    db.commit()

    # 7. Opportunity & Placement Demo
    opp1 = Opportunity(
        id="opp-o01",
        cooperative_id=coop1.id,
        created_by=manager.id,
        title="Junior PACS ERP Accountant & Billing Assistant",
        description="Responsible for daily milk collection billing, day book reconciliation, member passbook updates, and ERP inventory entry.",
        opportunity_type="Job",
        location="Sinnar, Nashik",
        stipend_or_salary="₹18,000 - ₹22,000 / month",
        remote_allowed=False,
        status="Open"
    )
    db.add(opp1)
    db.commit()

    print("COOPCONNECT successfully seeded with 20 NCCT Institutes & all login accounts!")
    db.close()

if __name__ == "__main__":
    seed()


