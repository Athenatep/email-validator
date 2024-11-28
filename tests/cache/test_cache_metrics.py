import pytest
from datetime import datetime, timedelta
from src.cache.cache_metrics import CacheMetrics

@pytest.fixture
def metrics():
    return CacheMetrics()

def test_hit_rate_calculation(metrics):
    metrics.record_hit()
    metrics.record_hit()
    metrics.record_miss()
    
    assert metrics.get_hit_rate() == 2/3

def test_zero_hit_rate(metrics):
    assert metrics.get_hit_rate() == 0

def test_stats_collection(metrics):
    metrics.record_hit()
    metrics.record_miss()
    metrics.record_eviction()
    metrics.update_total_entries(10)
    
    stats = metrics.get_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["evictions"] == 1
    assert stats["total_entries"] == 10
    assert 0 < stats["uptime_seconds"] < 1  # Should be nearly instant

def test_uptime_calculation(metrics):
    # Set start time to 1 hour ago
    metrics.start_time = datetime.now() - timedelta(hours=1)
    stats = metrics.get_stats()
    
    # Allow for small timing differences
    assert 3590 <= stats["uptime_seconds"] <= 3610