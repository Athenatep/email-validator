import pytest
from src.validators.template.template_validator import TemplateValidator

@pytest.fixture
def validator():
    return TemplateValidator()

def test_corporate_template(validator):
    result = validator.validate("john.doe@company.com")
    assert result["matches_template"]
    assert result["template_name"] == "corporate"
    assert not result["validation_errors"]

def test_invalid_corporate_template(validator):
    result = validator.validate("john_doe@company.com")
    assert not result["matches_template"]
    assert "john.doe@company.com" in result["suggestions"]

def test_support_template(validator):
    result = validator.validate("support+sales@company.com")
    assert result["matches_template"]
    assert result["template_name"] == "support"
    assert not result["validation_errors"]

def test_invalid_support_template(validator):
    result = validator.validate("supports@company.com")
    assert not result["matches_template"]
    assert "support@company.com" in result["suggestions"]

def test_noreply_template(validator):
    variations = [
        "noreply@company.com",
        "no-reply@company.com",
        "donotreply@company.com"
    ]
    
    for email in variations:
        result = validator.validate(email)
        assert result["matches_template"]
        assert result["template_name"] == "no-reply"
        assert not result["validation_errors"]

def test_template_validation_rules(validator):
    # Test minimum length rule
    result = validator.validate("a.b@company.com")
    assert result["matches_template"]
    assert "too short" in result["validation_errors"][0]
    
    # Test maximum length rule
    long_email = "a" * 65 + ".lastname@company.com"
    result = validator.validate(long_email)
    assert result["matches_template"]
    assert "too long" in result["validation_errors"][0]
    
    # Test allowed characters rule
    result = validator.validate("john_doe@company.com")
    assert not result["matches_template"]
    assert any("Invalid characters" in s for s in result["suggestions"])

def test_suggestion_generation(validator):
    # Test name-like email
    result = validator.validate("johndoe@company.com")
    assert "john.doe@company.com" in result["suggestions"]
    
    # Test support-like email
    result = validator.validate("helpdesk@company.com")
    assert "support+helpdesk@company.com" in result["suggestions"]

def test_case_insensitivity(validator):
    result = validator.validate("John.Doe@Company.com")
    assert result["matches_template"]
    assert result["template_name"] == "corporate"