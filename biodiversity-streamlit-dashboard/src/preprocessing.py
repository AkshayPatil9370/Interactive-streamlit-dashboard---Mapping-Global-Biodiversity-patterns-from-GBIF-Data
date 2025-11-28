import pandas as pd

def load_data(file_path):
    """Load the biodiversity dataset from a CSV file."""
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    """Clean the biodiversity dataset by handling missing values and standardizing formats."""
    taxonomy_cols = ['phylum', 'class', 'order', 'family', 'genus', 'species']
    
    # Fill missing taxonomy values
    for col in taxonomy_cols:
        df[col] = df[col].fillna("Unknown")
        df[col] = df[col].str.capitalize()
    
    # Replace missing country/state with 'Unknown'
    df['countryCode'] = df['countryCode'].fillna("Unknown")
    df['stateProvince'] = df['stateProvince'].fillna("Unknown").replace("", "Unknown")
    
    # Drop rows with invalid latitude/longitude values
    df = df[
        (df['decimalLatitude'].between(-90, 90, inclusive='both')) &
        (df['decimalLongitude'].between(-180, 180, inclusive='both'))
    ]
    
    # Remove (0,0) coordinates
    df = df[(df['decimalLatitude'] != 0) & (df['decimalLongitude'] != 0)]
    
    return df

def preprocess_data(file_path):
    """Load and preprocess the biodiversity dataset."""
    df = load_data(file_path)
    df = clean_data(df)
    return df