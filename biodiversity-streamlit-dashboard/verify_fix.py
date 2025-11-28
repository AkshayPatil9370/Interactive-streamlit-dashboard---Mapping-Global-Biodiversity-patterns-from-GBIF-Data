from src.data_loader import load_data
import pandas as pd
import sys

try:
    print("Loading data...")
    df = load_data("data/dataset_sample.csv")
    print("Data loaded successfully")
    print("Columns:", df.columns)
    print("Missing values per column:")
    print(df.isnull().sum())
    
    if df['species'].isnull().any():
        print("FAILURE: Species column has missing values")
        sys.exit(1)
    
    if df['kingdom'].isnull().any():
        print("FAILURE: Kingdom column has missing values")
        sys.exit(1)
        
    print("SUCCESS: Assertions passed")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
