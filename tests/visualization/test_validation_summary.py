import pytest
import pandas as pd
from pathlib import Path
from src.visualization.charts.validation_summary import ValidationSummaryChart

@pytest.fixture
def test_data():
    return pd.DataFrame({
        'is_valid': [True, True, False, True, False],
        'email': ['test1@example.com', 'test2@example.com', 
                 'test3@example.com', 'test4@example.com', 
                 'test5@example.com']
    })

@pytest.fixture
def chart_generator(tmp_path):
    return ValidationSummaryChart(tmp_path)

def test_generate_validation_summary(chart_generator, test_data):
    # Generate chart
    filepath = chart_generator.generate(test_data)
    
    # Check if file was created
    assert Path(filepath).exists()
    
    # Check if file is not empty
    assert Path(filepath).stat().st_size > 0

def test_generate_validation_summary_missing_column(chart_generator):
    # Create DataFrame without required column
    invalid_data = pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com']
    })
    
    # Generate chart should return empty string
    filepath = chart_generator.generate(invalid_data)
    assert filepath == ""

def test_generate_validation_summary_empty_data(chart_generator):
    # Create empty DataFrame with required column
    empty_data = pd.DataFrame(columns=['is_valid'])
    
    # Generate chart
    filepath = chart_generator.generate(empty_data)
    
    # Should still create file
    assert Path(filepath).exists()

def test_generate_validation_summary_custom_config(chart_generator, test_data):
    config = {
        'figsize': (8, 8),
        'dpi': 150,
        'style': 'default'
    }
    
    filepath = chart_generator.generate(test_data, config)
    assert Path(filepath).exists()