import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def sample_validation_data():
    """Generate sample validation data for testing."""
    return pd.DataFrame({
        'email': [
            'test1@example.com',
            'test2@example.com',
            'invalid@test.com',
            'test3@example.com'
        ],
        'is_valid': [True, True, False, True],
        'score': [95, 85, 45, 90],
        'issues': [
            [],
            ['minor_issue'],
            ['invalid_format', 'suspicious_domain'],
            []
        ],
        'timestamp': pd.date_range(start='2024-01-01', periods=4, freq='H')
    })

@pytest.fixture
def test_output_dir(tmp_path):
    """Create temporary directory for test outputs."""
    output_dir = tmp_path / "test_reports"
    output_dir.mkdir()
    return output_dir