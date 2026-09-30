from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str = "ERROR"
    message: str
    details: Optional[List[Any]] = None

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "Operation completed successfully"
    meta: Optional[Dict[str, Any]] = None
    error: Optional[ErrorDetail] = None

class PaginatedMeta(BaseModel):
    page: int = 1
    page_size: int = 20
    total: int = 0
    pages: int = 1

def success_response(data: Any = None, message: str = "Operation completed successfully", meta: Optional[Any] = None) -> dict:
    return {
        "success": True,
        "data": data,
        "message": message,
        "meta": meta or {}
    }

def error_response(code: str, message: str, details: Optional[List[Any]] = None) -> dict:
    return {
        "success": False,
        "data": None,
        "message": message,
        "meta": {},
        "error": {
            "code": code,
            "message": message,
            "details": details or []
        }
    }
