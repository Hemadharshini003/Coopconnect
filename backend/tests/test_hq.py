from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)

def test_hq_dashboard_and_institutes():
    # Login token for HQ Super Admin
    hq_token = create_access_token("u-hq-001", extra_claims={"role": "NCCT_SUPER_ADMIN"})
    headers = {"Authorization": f"Bearer {hq_token}"}

    # Test GET /api/v1/hq/dashboard
    res = client.get("/api/v1/hq/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["metrics"]["total_institutes"] == 20
    assert len(data["institute_comparison"]) == 20

    # Test GET /api/v1/hq/institutes
    res_inst = client.get("/api/v1/hq/institutes", headers=headers)
    assert res_inst.status_code == 200
    institutes = res_inst.json()["data"]
    assert len(institutes) == 20
    assert institutes[0]["code"] == "ICM-BPL" or institutes[0]["code"].startswith("ICM") or institutes[0]["code"].startswith("RICM")

def test_hq_role_forbidden():
    # Regular member token
    member_token = create_access_token("u4444444-4444-4444-4444-444444444444", extra_claims={"role": "TRAINEE"})
    headers = {"Authorization": f"Bearer {member_token}"}

    res = client.get("/api/v1/hq/dashboard", headers=headers)
    assert res.status_code == 403
