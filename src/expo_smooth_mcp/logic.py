"""
Framework-agnostic business logic for exponential smoothing forecasting.

This module contains pure functions with no dependencies on UI frameworks
(Gradio, Streamlit) or web frameworks (FastAPI, Flask). It can be reused
across different interface layers.
"""
from typing import Dict, List, Optional
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
) -> Dict[str, List]:
    """
    Generate forecast data for a specific SKU.
    
    Args:
        df: Preprocessed DataFrame with time series data
        sku: Product SKU code (e.g., "PRODUCT_123")
        forecast_horizon: Number of days to forecast ahead
        
    Returns:
        Dictionary with keys: 'dates', 'actuals', 'forecast', 'metadata'
    """
    pass

def get_available_skus(df: pd.DataFrame) -> List[str]:
    """
    Get list of all product SKUs available for forecasting.
    
    Args:
        df: Preprocessed DataFrame
        
    Returns:
        Sorted list of unique SKU strings
    """
    pass

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