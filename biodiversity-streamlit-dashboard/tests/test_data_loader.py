import pytest
import pandas as pd
from src.data_loader import load_data

def test_load_data():
    # Test loading the dataset
    df = load_data("data/dataset_sample.csv")
    assert isinstance(df, pd.DataFrame), "The loaded data should be a DataFrame"
    assert not df.empty, "The DataFrame should not be empty"
    assert "species" in df.columns, "The DataFrame should contain a 'species' column"
    assert "kingdom" in df.columns, "The DataFrame should contain a 'kingdom' column"

def test_load_data_invalid_file():
    # Test loading an invalid file
    with pytest.raises(FileNotFoundError):
        load_data("data/non_existent_file.csv")

def test_load_data_missing_values():
    # Test handling of missing values
    df = load_data("data/dataset_sample.csv")
    # We expect taxonomy columns to be filled, but numeric columns might still have NaNs
    assert not df['species'].isnull().any(), "Species column should not have missing values"
    assert not df['kingdom'].isnull().any(), "Kingdom column should not have missing values"