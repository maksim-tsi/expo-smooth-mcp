# app.py - Refactored for API communication
"""
Gradio UI for Exponential Smoothing Forecasting.

This version calls the FastAPI backend via HTTP instead of
using business logic directly. It can run standalone or be
mounted in the FastAPI application.
"""

import gradio as gr
import httpx
import os
import asyncio
import plotly.graph_objects as go
from typing import Optional
import pandas as pd
import io

# --- Configuration ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# --- Helper Functions ---

def _create_empty_plot(message: str) -> go.Figure:
    """Create empty plot with message."""
    fig = go.Figure()
    fig.update_layout(
        title_text=message,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": message,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 20}
        }]
    )
    return fig

def _create_error_plot(error_message: str) -> go.Figure:
    """Create error plot with message."""
    fig = go.Figure()
    fig.update_layout(
        title_text="Error",
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": error_message,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 16, "color": "red"}
        }]
    )
    return fig

def _create_forecast_plot_from_data(forecast_data: dict) -> go.Figure:
    """Create forecast plot from API response data."""
    # Extract data from API response
    dates = forecast_data["dates"]
    actuals = forecast_data["actuals"]
    forecast = forecast_data["forecast"]
    metadata = forecast_data["metadata"]

    # Create figure
    fig = go.Figure()

    # Add historical data (actuals that are not None)
    historical_dates = [d for d, a in zip(dates, actuals) if a is not None]
    historical_values = [a for a in actuals if a is not None]

    if historical_dates:
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=historical_values,
            mode='lines+markers',
            name='Historical Sales',
            line=dict(color='blue', width=2),
            marker=dict(size=5)
        ))

    # Add forecast data (where actuals are None)
    forecast_dates = [d for d, a in zip(dates, actuals) if a is None]
    forecast_values = forecast[len(historical_values):]  # Take remaining forecast values

    if forecast_dates:
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_values,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red', width=2, dash='dash'),
            marker=dict(size=5, symbol='x')
        ))

    # Update layout
    fig.update_layout(
        title_text=f"Sales Forecast for {metadata['sku']}",
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )

    return fig

# --- File Processing Function ---

def process_uploaded_file(file) -> tuple[Optional[pd.DataFrame], str, list]:
    """
    Process uploaded file and extract SKU list.
    
    Args:
        file: Gradio File object (can be None)
        
    Returns:
        Tuple of (DataFrame, status_message, sku_list)
    """
    if file is None:
        return None, "No file uploaded. Using default dataset.", SKU_LIST
    
    try:
        file_path = file.name
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Read file based on extension
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_ext == '.json':
            df = pd.read_json(file_path)
        else:
            return None, f"❌ Unsupported file type: {file_ext}", SKU_LIST
        
        # Validate required columns
        if 'date' not in df.columns or 'sales' not in df.columns:
            return None, "❌ File must contain 'date' and 'sales' columns", SKU_LIST
        
        # Map 'sales' column to 'quantity' for preprocessing compatibility
        df_processed = df.copy()
        df_processed['quantity'] = df_processed['sales']
        df_processed = df_processed.drop('sales', axis=1)
        
        # Process data using logic layer
        from src.expo_smooth_mcp import preprocessing, logic
        processed_df = preprocessing.preprocess_data(df_processed)
        
        if processed_df is None or processed_df.empty:
            return None, "❌ File processing failed. Check data format.", SKU_LIST
        
        # Extract SKU list
        skus = logic.get_available_skus(processed_df)
        
        status = f"✅ Loaded {len(processed_df)} rows, {len(skus)} SKUs from {os.path.basename(file_path)}"
        return processed_df, status, skus
        
    except Exception as e:
        return None, f"❌ Error processing file: {str(e)}", SKU_LIST

# --- Get SKU List ---

def get_sku_list() -> list:
    """
    Fetch SKU list for Gradio dropdown initialization.

    For Gradio initialization, we need the SKU list synchronously.
    When mounted in FastAPI, the API isn't listening yet during import,
    so we load data directly from the logic layer.
    """
    try:
        # When mounted in FastAPI, load data directly
        # (API isn't listening yet during import)
        from src.expo_smooth_mcp import logic
        df = logic.get_processed_data()
        if df is not None:
            skus = logic.get_available_skus(df)
            print(f"✓ Loaded {len(skus)} SKUs for Gradio dropdown")
            return skus
        else:
            print(f"⚠ Warning: No data available for SKU list")
            return []

    except Exception as e:
        print(f"⚠ Warning: Could not fetch SKU list: {e}")
        return []

# Initialize SKU list
SKU_LIST = get_sku_list()

# --- Main Forecast Function ---

async def create_forecast_plot(sku: str) -> go.Figure:
    """
    Generate forecast plot by calling FastAPI backend.

    This function makes HTTP requests to the REST API instead of
    calling business logic directly. This allows Gradio to work as a
    standalone client of the FastAPI service.

    Args:
        sku: Product SKU code to forecast

    Returns:
        Plotly figure with forecast visualization
    """
    if not sku:
        return _create_empty_plot("Please select a product SKU")

    try:
        # Call FastAPI forecast endpoint
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/api/forecast",
                json={"sku": sku, "forecast_horizon": 90}
            )
            response.raise_for_status()

            # Parse response
            forecast_data = response.json()

            # Create plot from data
            return _create_forecast_plot_from_data(forecast_data)

    except httpx.HTTPStatusError as e:
        # API returned error status (400, 404, 500, etc.)
        try:
            error_detail = e.response.json().get("detail", str(e))
        except:
            error_detail = str(e)
        return _create_error_plot(f"API Error: {error_detail}")

    except httpx.RequestError as e:
        # Network error (API not reachable)
        return _create_error_plot(
            f"Cannot connect to API at {API_BASE_URL}\n"
            f"Make sure the FastAPI server is running.\n"
            f"Error: {str(e)}"
        )

    except Exception as e:
        # Unexpected error
        return _create_error_plot(f"Unexpected error: {str(e)}")

# --- Custom Data Forecast Function ---

async def create_forecast_plot_with_custom_data(
    sku: str,
    horizon: int,
    custom_df: Optional[pd.DataFrame]
) -> go.Figure:
    """
    Generate forecast plot using custom data or default dataset.
    
    Args:
        sku: Product SKU code
        horizon: Forecast horizon in days
        custom_df: Optional custom DataFrame from file upload
        
    Returns:
        Plotly figure with forecast visualization
    """
    try:
        if custom_df is not None:
            # Use custom data directly with logic layer
            from src.expo_smooth_mcp import logic
            
            # Validate SKU exists
            valid_skus = logic.get_available_skus(custom_df)
            if sku not in valid_skus:
                return _create_error_plot(
                    f"SKU '{sku}' not found in uploaded data.\n"
                    f"Available SKUs: {', '.join(valid_skus)}"
                )
            
            # Generate forecast
            forecast_data = logic.get_forecast_data(custom_df, sku, horizon)
            return _create_forecast_plot_from_data(forecast_data)
        
        else:
            # Use existing API-based logic for default dataset
            return await create_forecast_plot(sku)
            
    except Exception as e:
        return _create_error_plot(f"Error generating forecast: {str(e)}")

# --- Gradio UI Definition ---

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    
    with gr.Blocks(title="Sales Forecasting") as interface:
        gr.Markdown("# 📊 Sales Forecasting Application")
        gr.Markdown("Upload your sales data or use the default dataset to generate forecasts.")
        
        # State to hold custom DataFrame
        custom_data_state = gr.State(None)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload Your Data (Optional)")
                file_upload = gr.File(
                    label="Upload CSV, Excel, or JSON",
                    file_types=[".csv", ".xlsx", ".xls", ".json"],
                    type="filepath"
                )
                upload_status = gr.Textbox(
                    label="Upload Status",
                    value="Using default dataset (FMCG_Sales.csv)",
                    interactive=False
                )
                
                gr.Markdown("### 2. Select SKU")
                sku_dropdown = gr.Dropdown(
                    choices=SKU_LIST,
                    label="Product SKU",
                    value=SKU_LIST[0] if SKU_LIST else None
                )
                
                gr.Markdown("### 3. Set Forecast Horizon")
                horizon_slider = gr.Slider(
                    minimum=7,
                    maximum=365,
                    value=90,
                    step=1,
                    label="Forecast Days"
                )
                
                forecast_button = gr.Button("Generate Forecast", variant="primary")
            
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Forecast Visualization")
        
        # File upload handler
        file_upload.change(
            fn=process_uploaded_file,
            inputs=[file_upload],
            outputs=[custom_data_state, upload_status, sku_dropdown]
        )
        
        # Forecast generation handler
        forecast_button.click(
            fn=create_forecast_plot_with_custom_data,
            inputs=[sku_dropdown, horizon_slider, custom_data_state],
            outputs=[plot_output]
        )
    
    return interface

# Create the interface
demo = create_gradio_interface()

# --- Main Entry Point ---

if __name__ == "__main__":
    # Standalone mode - launch Gradio on its own port
    print("=" * 60)
    print("🚀 Launching Gradio UI (Standalone Mode)")
    print("=" * 60)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"SKUs Available: {len(SKU_LIST)}")
    print()
    print("⚠️  Important: Make sure FastAPI server is running!")
    print("   Start it with: python -m src.expo_smooth_mcp.main --transport http --port 8000")
    print("=" * 60)

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )