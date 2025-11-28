import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data_loader import load_and_clean_data
from src import visualizations
from src import metrics

def test_visualizations():
    print("Testing visualizations...")
    data_path = project_root / "data" / "gbif_cleaned.csv"
    df = load_and_clean_data(str(data_path))
    
    # Test new visualizations
    try:
        # Taxonomy
        assert visualizations.plot_sunburst(df) is not None
        assert visualizations.plot_top_genera(df) is not None
        assert visualizations.plot_top_species(df) is not None
        assert visualizations.plot_taxonomy_pie(df) is not None
        
        # Maps
        # Note: Folium map object is returned, not None
        assert visualizations.plot_folium_map(df, map_type="Markers") is not None
        assert visualizations.plot_plotly_map(df) is not None
        
        # Temporal
        assert visualizations.plot_month_year_heatmap(df) is not None
        assert visualizations.plot_kingdom_over_time(df) is not None
        
        # Advanced
        assert visualizations.plot_country_richness(df) is not None
        assert visualizations.plot_state_richness(df) is not None
        
        print("All visualization functions returned valid objects.")
        return True
    except Exception as e:
        print(f"Visualization test failed: {e}")
        return False

def test_date_search():
    print("\nTesting date search...")
    # Just verify import and basic function existence
    try:
        from src.components import date_search
        assert hasattr(date_search, 'display_date_search_tab')
        print("Date search component verified.")
        return True
    except Exception as e:
        print(f"Date search test failed: {e}")
        return False

def test_metrics():
    print("\nTesting metrics...")
    data_path = project_root / "data" / "gbif_cleaned.csv"
    df = load_and_clean_data(str(data_path))
    
    try:
        assert metrics.observers_count(df) >= 0
        assert metrics.images_count(df) >= 0
        print("All metrics functions returned valid values.")
        return True
    except Exception as e:
        print(f"Metrics test failed: {e}")
        return False

if __name__ == "__main__":
    if test_visualizations() and test_metrics() and test_date_search():
        print("\nPhase 2 Verification Passed!")
    else:
        print("\nPhase 2 Verification Failed.")
