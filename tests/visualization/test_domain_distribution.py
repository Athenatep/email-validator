import pytest
import pandas as pd
from pathlib import Path
from src.visualization.charts.domain_distribution import DomainDistributionChart

@pytest.fixture
def test_data():
    return pd.DataFrame({
        'email': [
            'test1@gmail.com', 'test2@gmail.com', 'test3@yahoo.com',
            'test4@hotmail.com', 'test5@gmail.com', 'test6@yahoo.com',
            'test7@outlook.com', 'test8@gmail.com', 'test9@custom.com'
        ]
    })

@pytest.fixture
def chart_generator(tmp_path):
    return DomainDistributionChart(tmp_path)

def test_generate_domain_distribution(chart_generator, test_data):
    filepath = chart_generator.generate(test_data)
    assert Path(filepath).exists()
    assert Path(filepath).stat().st_size > 0

def test_generate_domain_distribution_missing_column(chart_generator):
    invalid_data = pd.DataFrame({
        'score': [1, 2, 3]
    })
    filepath = chart_generator.generate(invalid_data)
    assert filepath == ""

def test_generate_domain_distribution_empty_data(chart_generator):
    empty_data = pd.DataFrame(columns=['email'])
    filepath = chart_generator.generate(empty_data)
    assert Path(filepath).exists()

def test_generate_domain_distribution_custom_config(chart_generator, test_data):
    config = {
        'figsize': (10, 6),
        'dpi': 150,
        'style': 'default'
    }
    filepath = chart_generator.generate(test_data, config)
    assert Path(filepath).exists()

def test_generate_domain_distribution_single_domain(chart_generator):
    data = pd.DataFrame({
        'email': ['test1@gmail.com', 'test2@gmail.com', 'test3@gmail.com']
    })
    filepath = chart_generator.generate(data)
    assert Path(filepath).exists()