import pytest
from datetime import datetime, timedelta
from src.cache.cache_store import CacheStore
from src.cache.cache_config import CacheConfig

@pytest.fixture
def cache():
    config = CacheConfig(
        default_ttl=1,
        max_size=100,
        cleanup_interval=1
    )
    return CacheStore(config)

@pytest.mark.asyncio
async def test_cache_set_get(cache):
    await cache.set("test_key", "test_value")
    value = await cache.get("test_key")
    assert value == "test_value"

@pytest.mark.asyncio
async def test_ttl_expiration(cache):
    await cache.set("test_key", "test_value", ttl=1)
    assert await cache.get("test_key") == "test_value"
    
    await asyncio.sleep(1.1)
    assert await cache.get("test_key") is None

@pytest.mark.asyncio
async def test_category_ttl(cache):
    await cache.set(
        "domain_key",
        {"has_mx": True},
        category="domain"
    )
    assert await cache.get("domain_key") is not None

@pytest.mark.asyncio
async def test_max_size_eviction(cache):
    # Fill cache beyond max size
    for i in range(150):
        await cache.set(f"key_{i}", f"value_{i}")
        
    # Should have evicted oldest entries
    stats = await cache.get_stats()
    assert stats["size"] <= 100
    assert stats["evictions"] > 0

@pytest.mark.asyncio
async def test_cache_metrics(cache):
    # Generate some cache activity
    await cache.set("key1", "value1")
    await cache.get("key1")  # Hit
    await cache.get("key2")  # Miss
    
    stats = await cache.get_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["size"] == 1