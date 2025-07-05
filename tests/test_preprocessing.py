import pytest
import pandas as pd
import os
from src.expo_smooth_mcp.preprocessing import preprocess_data

@pytest.fixture
def raw_data_df() -> pd.DataFrame:
    """
    Fixture to load the raw data from the CSV file for testing.
    Assumes the CSV is in the root of the project directory.
    """
    # Adjust path if your test runner runs from a different directory
    csv_path = 'FMCG_Sales.csv'
    if not os.path.exists(csv_path):
        pytest.skip(f"Test data file not found at {csv_path}")
    
    return pd.read_csv(csv_path)

def test_preprocess_data_output_schema(raw_data_df):
    """
    Tests the basic structure and schema of the preprocessed DataFrame.
    """
    # WHEN the preprocessing function is called
    processed_df = preprocess_data(raw_data_df)
    
    # THEN verify the output schema
    assert isinstance(processed_df, pd.DataFrame), "Output should be a DataFrame"
    assert isinstance(processed_df.index, pd.MultiIndex), "Index should be a MultiIndex"
    assert processed_df.index.names == ['sku', 'date'], "Index names should be ['sku', 'date']"
    assert processed_df.columns == ['quantity'], "There should be a single 'quantity' column"

def test_preprocess_data_no_nulls(raw_data_df):
    """
    Tests that there are no null values in the final quantity column.
    """
    # WHEN the preprocessing function is called
    processed_df = preprocess_data(raw_data_df)
    
    # THEN verify no nulls
    assert processed_df['quantity'].isnull().sum() == 0, "There should be no NaN values in the quantity column"

def test_preprocess_data_continuous_date_index(raw_data_df):
    """
    Tests that the date index is continuous for a sample SKU.
    """
    # WHEN the preprocessing function is called
    processed_df = preprocess_data(raw_data_df)
    
    # THEN check a sample SKU for continuous dates
    if not processed_df.empty:
        sample_sku_data = processed_df.loc[processed_df.index.get_level_values('sku')[0]]
        date_diffs = sample_sku_data.index.to_series().diff().dropna()
        all_one_day = all(diff == pd.Timedelta(days=1) for diff in date_diffs)
        assert all_one_day, "Date index should be continuous with daily frequency for each SKU"