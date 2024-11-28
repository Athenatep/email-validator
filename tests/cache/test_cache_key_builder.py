import pytest
from src.cache.cache_key_builder import CacheKeyBuilder

def test_validation_key_basic():
    key = CacheKeyBuilder.build_validation_key("Test@Example.com")
    assert key == "validation:test@example.com"

def test_validation_key_with_options():
    options = {"check_mx": True, "check_spam": False}
    key1 = CacheKeyBuilder.build_validation_key("test@example.com", options)
    key2 = CacheKeyBuilder.build_validation_key("test@example.com", {})
    
    assert key1 != key2
    assert "opts:" in key1
    assert "validation:test@example.com" in key1

def test_validation_key_consistent():
    options = {"a": 1, "b": 2}
    key1 = CacheKeyBuilder.build_validation_key("test@example.com", options)
    key2 = CacheKeyBuilder.build_validation_key("test@example.com", options)
    
    assert key1 == key2

def test_domain_key():
    key = CacheKeyBuilder.build_domain_key("Example.com")
    assert key == "domain:example.com"

def test_domain_key_consistent():
    key1 = CacheKeyBuilder.build_domain_key("example.com")
    key2 = CacheKeyBuilder.build_domain_key("EXAMPLE.COM")
    
    assert key1 == key2