import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.visualization.charts.score_distribution import ScoreDistributionChart

@pytest.fixture
def test_data():
    return pd.DataFrame({
        'score': np.random.normal(80, 15, 100).clip(0, 100),
        'email': [f'test{i}@example.com' for i in range(100)]
    })

@pytest.fixture
def chart_generator(tmp_path):
    return ScoreDistributionChart(tmp_path)

def test_generate_score_distribution(chart_generator, test_data):
    filepath = chart_generator.generate(test_data)
    assert Path(filepath).exists()
    assert Path(filepath).stat().st_size > 0

def test_generate_score_distribution_missing_column(chart_generator):
    invalid_data = pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com']
    })
    filepath = chart_generator.generate(invalid_data)
    assert filepath == ""

def test_generate_score_distribution_empty_data(chart_generator):
    empty_data = pd.DataFrame(columns=['score'])
    filepath = chart_generator.generate(empty_data)
    assert Path(filepath).exists()

def test_generate_score_distribution_custom_config(chart_generator, test_data):
    config = {
        'figsize': (10, 8),
        'dpi': 150,
        'style': 'default'
    }
    filepath = chart_generator.generate(test_data, config)
    assert Path(filepath).exists()

def test_generate_score_distribution_data_validation(chart_generator, test_data):
    # Test with invalid scores
    invalid_data = test_data.copy()
    invalid_data['score'] = invalid_data['score'] * 2  # Scores above 100
    filepath = chart_generator.generate(invalid_data)
    assert Path(filepath).exists()  # Should still create chart with clipped values