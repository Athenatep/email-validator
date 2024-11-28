import pytest
from src.cache.cache_manager import CacheManager

@pytest.fixture
async def cache_manager():
    return CacheManager(ttl_seconds=1)

@pytest.mark.asyncio
async def test_validation_result_caching(cache_manager):
    email = "test@example.com"
    result = {
        "is_valid": True,
        "score": 100,
        "issues": []
    }
    
    # Cache result
    success = await cache_manager.cache_validation_result(email, result)
    assert success
    
    # Get cached result
    cached = await cache_manager.get_validation_result(email)
    assert cached == result

@pytest.mark.asyncio
async def test_domain_info_caching(cache_manager):
    domain = "example.com"
    info = {
        "has_mx": True,
        "created_date": "2020-01-01"
    }
    
    # Cache domain info
    success = await cache_manager.cache_domain_info(domain, info)
    assert success
    
    # Get cached info
    cached = await cache_manager.get_domain_info(domain)
    assert cached == info

@pytest.mark.asyncio
async def test_validation_with_options(cache_manager):
    email = "test@example.com"
    options = {"check_mx": True, "check_spam": False}
    result = {"is_valid": True}
    
    # Cache with options
    await cache_manager.cache_validation_result(email, result, options)
    
    # Should get different results for different options
    cached1 = await cache_manager.get_validation_result(email, options)
    cached2 = await cache_manager.get_validation_result(email, {"check_mx": False})
    
    assert cached1 == result
    assert cached2 is None

@pytest.mark.asyncio
async def test_ttl_expiration(cache_manager):
    email = "test@example.com"
    result = {"is_valid": True}
    
    # Cache with 1 second TTL
    await cache_manager.cache_validation_result(email, result)
    
    # Wait for expiration
    await asyncio.sleep(1.1)
    
    # Should return None after expiration
    assert await cache_manager.get_validation_result(email) is None