import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token

def test_password_hashing():
    pwd = "SecretPassword123!"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_creation_and_decoding():
    user_id = "test-user-uuid-123"
    token = create_access_token(user_id, extra_claims={"role": "MEMBER"})
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["role"] == "MEMBER"
    assert payload["type"] == "access"
