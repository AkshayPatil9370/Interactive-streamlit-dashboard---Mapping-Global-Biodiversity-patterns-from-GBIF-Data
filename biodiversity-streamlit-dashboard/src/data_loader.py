import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    """Load the biodiversity dataset from a CSV file."""
    # Read and perform cleaning to provide a ready-to-use DataFrame
    # Use low_memory=False to avoid mixed type warnings on large files if needed, 
    # or specify dtypes. For now, we'll stick to default.
    df = pd.read_csv(file_path)
    # Apply basic cleaning to taxonomy and location fields
    df = clean_data(df)
    return df

def clean_data(df):
    """Clean the dataset by handling missing values and duplicates."""
    # Fill missing values
    taxonomy_cols = ['phylum', 'class', 'order', 'family', 'genus', 'species']
    for col in taxonomy_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
            df[col] = df[col].str.capitalize()
    
    if 'countryCode' in df.columns:
        df['countryCode'] = df['countryCode'].fillna("Unknown")
    
    if 'stateProvince' in df.columns:
        df['stateProvince'] = df['stateProvince'].fillna("Unknown").replace("", "Unknown")
    
    # Drop duplicates
    if 'gbifID' in df.columns:
        df.drop_duplicates(subset=['gbifID'], inplace=True)
    
    # Convert eventDate to datetime if present
    if 'eventDate' in df.columns:
        df['eventDate'] = pd.to_datetime(df['eventDate'], errors='coerce')

    return df

def load_and_clean_data(file_path):
    """Load and clean the biodiversity dataset."""
    df = load_data(file_path)
    return df