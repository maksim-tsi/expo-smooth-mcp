"""
Framework-agnostic business logic for exponential smoothing forecasting.

This module contains pure functions with no dependencies on UI frameworks
(Gradio, Streamlit) or web frameworks (FastAPI, Flask). It can be reused
across different interface layers.
"""
from typing import Dict, List, Optional, Any
import pandas as pd
import plotly.graph_objects as go
from .forecasting import generate_forecast
from .preprocessing import preprocess_data

# Module-level cache for preprocessed data
_cached_data: Optional[pd.DataFrame] = None

# Function skeletons (to be implemented in subsequent tasks)
def get_forecast_data(
    df: pd.DataFrame,
    sku: str,
    forecast_horizon: int = 90
) -> Dict[str, Any]:
    """
    Generate forecast data for a specific SKU.
    
    Args:
        df: Preprocessed DataFrame with time series data
        sku: Product SKU code (e.g., "PRODUCT_123")
        forecast_horizon: Number of days to forecast ahead
        
    Returns:
        Dictionary with keys: 'dates', 'actuals', 'forecast', 'metadata'
    """
    # Generate forecast using existing function
    forecast_df = generate_forecast(df, sku, forecast_horizon)
    
    # Convert dates to ISO format strings
    dates = [d.strftime('%Y-%m-%d') for d in forecast_df.index]
    
    # Convert actuals and forecast to lists, handling NaN values
    actuals = forecast_df['actuals'].tolist()
    forecast = forecast_df['forecast'].tolist()
    
    # Convert NaN to None for JSON compatibility
    actuals = [None if pd.isna(x) else x for x in actuals]
    
    # Calculate metadata
    historical_points = sum(1 for x in actuals if x is not None)
    forecast_points = len(forecast) - historical_points
    
    metadata = {
        'sku': sku,
        'forecast_horizon': forecast_horizon,
        'historical_points': historical_points,
        'forecast_points': forecast_points
    }
    
    return {
        'dates': dates,
        'actuals': actuals,
        'forecast': forecast,
        'metadata': metadata
    }

def get_available_skus(df: pd.DataFrame) -> List[str]:
    """
    Get list of all product SKUs available for forecasting.
    
    Args:
        df: Preprocessed DataFrame with MultiIndex (date, sku)
        
    Returns:
        Sorted list of unique SKU strings
        Example: ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_123', ...]
        
    Raises:
        ValueError: If DataFrame is empty or doesn't have 'sku' level in index
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if not isinstance(df.index, pd.MultiIndex) or 'sku' not in df.index.names:
        raise ValueError("DataFrame must have MultiIndex with 'sku' level")
    
    return sorted(df.index.get_level_values('sku').unique().tolist())

def create_forecast_plot(forecast_data: Dict[str, List]) -> go.Figure:
    """
    Create a Plotly figure from forecast data.
    
    Args:
        forecast_data: Output from get_forecast_data()
        
    Returns:
        Plotly Figure object ready for display
    """
    pass

def validate_forecast_request(
    sku: str,
    forecast_horizon: int,
    valid_skus: List[str]
) -> Optional[str]:
    """
    Validate forecast request parameters.
    
    Args:
        sku: Requested SKU
        forecast_horizon: Requested horizon
        valid_skus: List of available SKUs
        
    Returns:
        Error message string if invalid, None if valid
    """
    pass

def get_processed_data() -> pd.DataFrame:
    """
    Get preprocessed data, loading it once and caching.
    
    Returns:
        Preprocessed DataFrame
        
    Raises:
        RuntimeError: If data fails to load
    """
    pass