import sys
from pathlib import Path
import pandas as pd
import time
import folium

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.visualizations import plot_folium_map

def test_map_generation():
    print("Testing map generation performance...")
    
    # Create a mock dataframe with 5000 rows
    data = {
        'decimalLatitude': [10.0 + i*0.01 for i in range(5000)],
        'decimalLongitude': [20.0 + i*0.01 for i in range(5000)],
        'species': [f'Species {i}' for i in range(5000)],
        'eventDate': ['2023-01-01'] * 5000
    }
    df = pd.DataFrame(data)
    
    # Test Cluster Map
    start_time = time.time()
    m_cluster = plot_folium_map(df, map_type="Cluster")
    end_time = time.time()
    print(f"Cluster Map generation time: {end_time - start_time:.4f} seconds")
    
    if not isinstance(m_cluster, folium.Map):
        print("Error: Cluster Map did not return a folium.Map object")
        return False
        
    # Test Heatmap
    start_time = time.time()
    m_heatmap = plot_folium_map(df, map_type="Heatmap")
    end_time = time.time()
    print(f"Heatmap generation time: {end_time - start_time:.4f} seconds")
    
    if not isinstance(m_heatmap, folium.Map):
        print("Error: Heatmap did not return a folium.Map object")
        return False

    # Test Markers Map
    start_time = time.time()
    m_markers = plot_folium_map(df, map_type="Markers")
    end_time = time.time()
    print(f"Markers Map generation time: {end_time - start_time:.4f} seconds")
    
    if not isinstance(m_markers, folium.Map):
        print("Error: Markers Map did not return a folium.Map object")
        return False
        
    return True

if __name__ == "__main__":
    if test_map_generation():
        print("\nMap generation tests passed!")
    else:
        print("\nMap generation tests failed.")
