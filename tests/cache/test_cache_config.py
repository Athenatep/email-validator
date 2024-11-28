import pytest
from src.cache.cache_config import CacheConfig

def test_default_config():
    config = CacheConfig()
    assert config.enabled
    assert config.default_ttl == 3600
    assert config.max_size == 10000
    assert config.cleanup_interval == 300

def test_custom_config():
    config = CacheConfig(
        enabled=False,
        default_ttl=1800,
        max_size=5000,
        cleanup_interval=600
    )
    assert not config.enabled
    assert config.default_ttl == 1800
    assert config.max_size == 5000
    assert config.cleanup_interval == 600

def test_validation_ttls():
    config = CacheConfig()
    assert "domain" in config.validation_ttls
    assert "mx" in config.validation_ttls
    assert "reputation" in config.validation_ttls
    assert "disposable" in config.validation_ttls
    assert "validation" in config.validation_ttls

def test_custom_validation_ttls():
    custom_ttls = {
        "domain": 7200,
        "validation": 900
    }
    config = CacheConfig(validation_ttls=custom_ttls)
    assert config.validation_ttls == custom_ttls