import pytest
import pandas as pd
import os
from src.expo_smooth_mcp.preprocessing import preprocess_data
from src.expo_smooth_mcp.forecasting import generate_forecast

@pytest.fixture
def processed_data_df() -> pd.DataFrame:
    """
    Fixture to provide a preprocessed DataFrame for testing the forecast function.
    """
    csv_path = 'FMCG_Sales.csv'
    if not os.path.exists(csv_path):
        pytest.skip(f"Test data file not found at {csv_path}")
    
    raw_df = pd.read_csv(csv_path)
    return preprocess_data(raw_df)

def test_generate_forecast_output_structure(processed_data_df):
    """
    Tests that the forecast function returns a DataFrame with the correct structure.
    """
    # GIVEN a sample SKU and a forecast horizon
    if processed_data_df.empty:
        pytest.skip("Preprocessed data is empty, cannot run forecast test.")
        
    sample_sku = processed_data_df.index.get_level_values('sku')[0]
    horizon = 15
    
    # WHEN the forecast function is called
    forecast_df = generate_forecast(processed_data_df, sample_sku, forecast_horizon=horizon)
    
    # THEN verify the output
    assert isinstance(forecast_df, pd.DataFrame), "Output should be a DataFrame"
    assert 'actuals' in forecast_df.columns, "Output should have an 'actuals' column"
    assert 'forecast' in forecast_df.columns, "Output should have a 'forecast' column"

def test_generate_forecast_output_length(processed_data_df):
    """
    Tests that the output DataFrame has the correct total length.
    """
    # GIVEN a sample SKU and a forecast horizon
    if processed_data_df.empty:
        pytest.skip("Preprocessed data is empty, cannot run forecast test.")
        
    sample_sku = processed_data_df.index.get_level_values('sku')[0]
    horizon = 15
    
    # Calculate expected length
    history_length = len(processed_data_df.loc[sample_sku])
    expected_length = history_length + horizon
    
    # WHEN the forecast function is called
    forecast_df = generate_forecast(processed_data_df, sample_sku, forecast_horizon=horizon)
    
    # THEN verify the length
    assert len(forecast_df) == expected_length, "Output DataFrame length should be history + horizon"

def test_generate_forecast_raises_error_for_invalid_sku(processed_data_df):
    """
    Tests that a ValueError is raised for a non-existent SKU.
    """
    # GIVEN an invalid SKU
    invalid_sku = "INVALID_SKU_12345"
    
    # WHEN & THEN calling the function with an invalid SKU should raise a ValueError
    with pytest.raises(ValueError):
        generate_forecast(processed_data_df, invalid_sku)