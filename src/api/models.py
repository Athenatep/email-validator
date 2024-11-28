from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Any

class ValidationOptions(BaseModel):
    """Validation options configuration."""
    check_syntax: bool = True
    check_domain: bool = True
    check_spam: bool = True
    check_disposable: bool = True
    check_smtp: bool = True
    check_reputation: bool = True
    check_duplicates: bool = True
    check_typos: bool = True

class EmailValidationRequest(BaseModel):
    """Single email validation request."""
    email: EmailStr
    options: Optional[ValidationOptions] = None

class EmailValidationResponse(BaseModel):
    """Single email validation response."""
    email: str
    is_valid: bool
    score: int
    issues: List[str]
    checks: Dict[str, Any]
    suggestions: List[str]

class BatchValidationRequest(BaseModel):
    """Batch email validation request."""
    emails: List[str] = Field(..., min_items=1, max_items=1000)
    options: Optional[ValidationOptions] = None

class BatchValidationResponse(BaseModel):
    """Batch email validation response."""
    results: List[EmailValidationResponse]
    stats: Dict[str, int]
    invalid_format: List[Dict[str, Any]]
    duplicates: Dict[str, List[str]]

class CacheStats(BaseModel):
    """Cache statistics."""
    total_entries: int
    active_entries: int
    expired_entries: int

class ReportRequest(BaseModel):
    """Report generation request."""
    results: List[Dict[str, Any]]
    format: str = Field(default="html", pattern="^(html|pdf)$")