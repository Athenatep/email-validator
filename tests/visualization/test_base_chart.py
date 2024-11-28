import pytest
import pandas as pd
from pathlib import Path
from src.visualization.charts.base_chart import BaseChart

@pytest.fixture
def base_chart(tmp_path):
    return BaseChart(tmp_path)

def test_validate_data_with_valid_columns(base_chart):
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']
    })
    
    assert base_chart.validate_data(df, ['col1', 'col2'])

def test_validate_data_with_missing_columns(base_chart):
    df = pd.DataFrame({
        'col1': [1, 2, 3]
    })
    
    assert not base_chart.validate_data(df, ['col1', 'col2'])

def test_save_plot_creates_file(base_chart):
    import matplotlib.pyplot as plt
    
    # Create simple plot
    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    
    filepath = base_chart.save_plot('test_plot.png')
    assert Path(filepath).exists()

def test_setup_plot_with_custom_config(base_chart):
    config = {
        'figsize': (10, 5),
        'dpi': 150,
        'style': 'default'
    }
    
    base_chart.setup_plot(config)
    # No assertion needed - just checking it doesn't raise exceptions

def test_setup_plot_with_default_config(base_chart):
    base_chart.setup_plot()
    # No assertion needed - just checking it doesn't raise exceptions