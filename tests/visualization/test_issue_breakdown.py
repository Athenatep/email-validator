import pytest
import pandas as pd
from pathlib import Path
from src.visualization.charts.issue_breakdown import IssueBreakdownChart

@pytest.fixture
def test_data():
    return pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com', 'test3@example.com'],
        'issues': [
            ['invalid_format', 'suspicious_domain'],
            ['invalid_format'],
            ['spam_trap', 'disposable_email']
        ]
    })

@pytest.fixture
def chart_generator(tmp_path):
    return IssueBreakdownChart(tmp_path)

def test_generate_issue_breakdown(chart_generator, test_data):
    filepath = chart_generator.generate(test_data)
    assert Path(filepath).exists()
    assert Path(filepath).stat().st_size > 0

def test_generate_issue_breakdown_missing_column(chart_generator):
    invalid_data = pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com']
    })
    filepath = chart_generator.generate(invalid_data)
    assert filepath == ""

def test_generate_issue_breakdown_empty_data(chart_generator):
    empty_data = pd.DataFrame(columns=['issues'])
    filepath = chart_generator.generate(empty_data)
    assert Path(filepath).exists()

def test_generate_issue_breakdown_custom_config(chart_generator, test_data):
    config = {
        'figsize': (12, 8),
        'dpi': 150,
        'style': 'default'
    }
    filepath = chart_generator.generate(test_data, config)
    assert Path(filepath).exists()

def test_generate_issue_breakdown_no_issues(chart_generator):
    data = pd.DataFrame({
        'email': ['test1@example.com', 'test2@example.com'],
        'issues': [[], []]
    })
    filepath = chart_generator.generate(data)
    assert Path(filepath).exists()