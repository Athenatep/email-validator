import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from src.visualization.charts.validation_timeline import ValidationTimelineChart

@pytest.fixture
def test_data():
    # Create sample data with timestamps
    timestamps = [
        datetime.now() + timedelta(hours=i)
        for i in range(24)
    ]
    
    return pd.DataFrame({
        'email': [f'test{i}@example.com' for i in range(24)],
        'is_valid': [i % 3 != 0 for i in range(24)],  # 2/3 valid, 1/3 invalid
        'timestamp': timestamps
    })

@pytest.fixture
def chart_generator(tmp_path):
    return ValidationTimelineChart(tmp_path)

def test_generate_validation_timeline(chart_generator, test_data):
    filepath = chart_generator.generate(test_data)
    assert Path(filepath).exists()
    assert Path(filepath).stat().st_size > 0

def test_generate_validation_timeline_missing_column(chart_generator):
    invalid_data = pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com']
    })
    filepath = chart_generator.generate(invalid_data)
    assert filepath == ""

def test_generate_validation_timeline_empty_data(chart_generator):
    empty_data = pd.DataFrame(columns=['is_valid', 'timestamp'])
    filepath = chart_generator.generate(empty_data)
    assert Path(filepath).exists()

def test_generate_validation_timeline_custom_config(chart_generator, test_data):
    config = {
        'figsize': (15, 10),
        'dpi': 150,
        'style': 'default'
    }
    filepath = chart_generator.generate(test_data, config)
    assert Path(filepath).exists()

def test_generate_validation_timeline_no_timestamp(chart_generator, test_data):
    # Test with data that has no timestamp column
    data_no_timestamp = test_data.drop('timestamp', axis=1)
    filepath = chart_generator.generate(data_no_timestamp)
    assert Path(filepath).exists()

def test_generate_validation_timeline_single_timestamp(chart_generator):
    # Test with all data points having the same timestamp
    now = datetime.now()
    data = pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com', 'test3@example.com'],
        'is_valid': [True, False, True],
        'timestamp': [now, now, now]
    })
    filepath = chart_generator.generate(data)
    assert Path(filepath).exists()