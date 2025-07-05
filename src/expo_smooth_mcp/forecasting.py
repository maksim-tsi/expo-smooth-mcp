import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def generate_forecast(
    processed_df: pd.DataFrame, 
    sku: str, 
    forecast_horizon: int = 30
) -> pd.DataFrame:
    """
    Generates a forecast for a given SKU using Holt-Winters Exponential Smoothing.

    Args:
        processed_df (pd.DataFrame): The preprocessed DataFrame from the preprocessing module.
                                     Must have a MultiIndex of ('sku', 'date').
        sku (str): The specific product SKU to forecast.
        forecast_horizon (int, optional): The number of days to forecast into the future. 
                                          Defaults to 30.

    Returns:
        pd.DataFrame: A DataFrame with a datetime index, and 'actuals' and 'forecast' columns,
                      ready for plotting.
    """
    if sku not in processed_df.index.get_level_values('sku'):
        raise ValueError(f"SKU '{sku}' not found in the dataset.")

    # Select the time series for the specified SKU
    time_series = processed_df.loc[sku]['quantity']
    
    # Define and fit the Holt-Winters Exponential Smoothing model
    # We assume an additive trend and additive weekly seasonality (7 days)
    model = ExponentialSmoothing(
        time_series, 
        trend='add', 
        seasonal='add', 
        seasonal_periods=7,
        initialization_method='estimated'
    )
    fitted_model = model.fit()

    # Generate the forecast
    forecast_values = fitted_model.forecast(steps=forecast_horizon)
    
    # Combine historical data and forecast into a single DataFrame for plotting
    history_df = pd.DataFrame({
        'actuals': time_series,
        'forecast': fitted_model.fittedvalues # In-sample forecast
    })
    
    forecast_df = pd.DataFrame({
        'actuals': None, # No actuals for future dates
        'forecast': forecast_values
    })

    plot_df = pd.concat([history_df, forecast_df])
    
    return plot_df