import pytest
from src.validators.email_validator import EmailValidator

@pytest.fixture
def validator():
    return EmailValidator(cache_enabled=False)

@pytest.mark.asyncio
async def test_valid_email(validator):
    result = await validator.validate("test@example.com")
    assert result["is_valid"]
    assert result["score"] > 70
    assert not result["issues"]

@pytest.mark.asyncio
async def test_invalid_syntax(validator):
    result = await validator.validate("invalid-email")
    assert not result["is_valid"]
    assert result["score"] < 70
    assert result["issues"]
    assert "syntax" in result["checks"]

@pytest.mark.asyncio
async def test_disposable_email(validator):
    result = await validator.validate("test@tempmail.com")
    assert not result["is_valid"]
    assert "disposable" in result["checks"]
    assert any("disposable" in issue.lower() for issue in result["issues"])

@pytest.mark.asyncio
async def test_spam_patterns(validator):
    result = await validator.validate("test123456@example.com")
    assert "spam" in result["checks"]
    assert result["checks"]["spam"]["is_suspicious"]

@pytest.mark.asyncio
async def test_typo_detection(validator):
    result = await validator.validate("test@gmai.com")
    assert "typo" in result["checks"]
    assert result["checks"]["typo"]["has_typos"]
    assert "gmail.com" in str(result["suggestions"])

@pytest.mark.asyncio
async def test_duplicate_detection(validator):
    email = "test@example.com"
    # First submission
    result1 = await validator.validate(email)
    assert not result1["checks"]["duplicate"]["is_duplicate"]
    
    # Second submission
    result2 = await validator.validate(email)
    assert result2["checks"]["duplicate"]["is_duplicate"]

@pytest.mark.asyncio
async def test_custom_validation_options(validator):
    options = {
        "check_syntax": True,
        "check_spam": True,
        "check_disposable": False,
        "check_smtp": False
    }
    result = await validator.validate("test@example.com", options)
    assert "spam" in result["checks"]
    assert "disposable" not in result["checks"]
    assert "smtp" not in result["checks"]