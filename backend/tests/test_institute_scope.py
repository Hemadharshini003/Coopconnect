import pytest
from fastapi import HTTPException
from app.db.models.user import (
    User, ROLE_NCCT_SUPER_ADMIN, ROLE_INSTITUTE_ADMIN, ROLE_TRAINEE
)
from app.api.deps import (
    require_hq_role, require_institute_role, verify_institute_scope, verify_trainee_self_scope
)

def test_hq_super_admin_has_all_institute_access():
    hq_user = User(
        id="hq-user-1",
        email="hq@ncct.gov.in",
        role=ROLE_NCCT_SUPER_ADMIN,
        institute_id=None
    )
    
    # HQ user should pass require_hq_role
    assert require_hq_role(hq_user) == hq_user
    
    # HQ user can query any target institute or view all institutes (None)
    assert verify_institute_scope("inst-01", hq_user) == "inst-01"
    assert verify_institute_scope("inst-02", hq_user) == "inst-02"
    assert verify_institute_scope(None, hq_user) is None

def test_institute_admin_data_isolation():
    inst1_admin = User(
        id="inst1-admin-id",
        email="admin@inst1.ncct.gov.in",
        role=ROLE_INSTITUTE_ADMIN,
        institute_id="inst-01"
    )
    
    # Institute admin fails require_hq_role
    with pytest.raises(HTTPException) as exc_info:
        require_hq_role(inst1_admin)
    assert exc_info.value.status_code == 403

    # Institute admin accessing own institute succeeds
    scope = verify_institute_scope("inst-01", inst1_admin)
    assert scope == "inst-01"

    # Institute admin attempting cross-institute access fails with 403 Forbidden
    with pytest.raises(HTTPException) as exc_info:
        verify_institute_scope("inst-02", inst1_admin)
    assert exc_info.value.status_code == 403
    assert "Cross-institute data access is strictly forbidden" in exc_info.value.detail

def test_trainee_self_scope_isolation():
    trainee_a = User(
        id="trainee-a-id",
        email="traineea@inst1.ncct.gov.in",
        role=ROLE_TRAINEE,
        institute_id="inst-01"
    )
    
    trainee_b = User(
        id="trainee-b-id",
        email="traineeb@inst1.ncct.gov.in",
        role=ROLE_TRAINEE,
        institute_id="inst-01"
    )
    
    # Trainee A can access Trainee A data
    assert verify_trainee_self_scope("trainee-a-id", trainee_a) == trainee_a
    
    # Trainee A trying to access Trainee B data is blocked with 403
    with pytest.raises(HTTPException) as exc_info:
        verify_trainee_self_scope("trainee-b-id", trainee_a)
    assert exc_info.value.status_code == 403
