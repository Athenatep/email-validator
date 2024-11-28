import pytest
from src.preprocessing.batch_deduplicator import BatchDeduplicator

@pytest.fixture
def deduplicator():
    return BatchDeduplicator(similarity_threshold=2)

def test_exact_duplicates(deduplicator):
    emails = [
        "test@example.com",
        "TEST@example.com",
        "test@EXAMPLE.COM",
        "unique@example.com"
    ]
    
    results = deduplicator.deduplicate(emails)
    
    assert len(results["unique_emails"]) == 2
    assert results["stats"]["exact_duplicates"] == 2
    assert "test@example.com" in results["duplicates"]

def test_similar_emails(deduplicator):
    emails = [
        "john.doe@example.com",
        "johndoe@example.com",
        "jon.doe@example.com",
        "different@example.com"
    ]
    
    results = deduplicator.deduplicate(emails)
    
    assert len(results["similar_groups"]) > 0
    assert results["stats"]["similar"] > 0

def test_different_domains(deduplicator):
    emails = [
        "test@example.com",
        "test@different.com",
        "test@another.com"
    ]
    
    results = deduplicator.deduplicate(emails)
    
    assert len(results["unique_emails"]) == 3
    assert len(results["similar_groups"]) == 0

def test_empty_list(deduplicator):
    results = deduplicator.deduplicate([])
    
    assert len(results["unique_emails"]) == 0
    assert results["stats"]["total"] == 0

def test_invalid_emails(deduplicator):
    emails = [
        "test@example.com",
        "invalid-email",
        "another@example.com"
    ]
    
    results = deduplicator.deduplicate(emails)
    
    assert len(results["unique_emails"]) == 3  # Should keep invalid emails
    assert "error" not in results["stats"]

def test_case_sensitivity(deduplicator):
    emails = [
        "Test.User@Example.com",
        "test.user@example.com",
        "TEST.USER@EXAMPLE.COM"
    ]
    
    results = deduplicator.deduplicate(emails)
    
    assert len(results["unique_emails"]) == 1
    assert results["stats"]["exact_duplicates"] == 2