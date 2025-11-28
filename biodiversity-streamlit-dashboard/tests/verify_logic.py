import sys
from pathlib import Path
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data_loader import load_and_clean_data

def test_data_loading():
    print("Testing data loading...")
    data_path = project_root / "data" / "gbif_cleaned.csv"
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        return False
    
    try:
        df = load_and_clean_data(str(data_path))
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Check for expected columns
        expected_cols = ['gbifID', 'species', 'kingdom_grouped', 'countryCode', 'event_year']
        missing_cols = [col for col in expected_cols if col not in df.columns]
        if missing_cols:
            print(f"Error: Missing columns: {missing_cols}")
            return False
            
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def test_filtering():
    print("\nTesting filtering logic...")
    data_path = project_root / "data" / "gbif_cleaned.csv"
    df = load_and_clean_data(str(data_path))
    
    # Test Kingdom Filter
    kingdoms = df['kingdom_grouped'].unique()
    if len(kingdoms) > 0:
        target_kingdom = kingdoms[0]
        filtered_df = df[df["kingdom_grouped"] == target_kingdom]
        print(f"Filtered by Kingdom '{target_kingdom}': {len(filtered_df)} records")
        if not all(filtered_df['kingdom_grouped'] == target_kingdom):
             print("Error: Kingdom filter failed")
             return False

    # Test Year Filter
    if 'event_year' in df.columns:
        min_year = int(df['event_year'].min())
        max_year = int(df['event_year'].max())
        # Filter for first year only
        filtered_df = df[(df["event_year"] >= min_year) & (df["event_year"] <= min_year)]
        print(f"Filtered by Year {min_year}: {len(filtered_df)} records")
        if not all(filtered_df['event_year'] == min_year):
             print("Error: Year filter failed")
             return False
             
    return True

if __name__ == "__main__":
    if test_data_loading() and test_filtering():
        print("\nAll verification tests passed!")
    else:
        print("\nVerification failed.")
