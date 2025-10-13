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

# Import column analysis module
from src.expo_smooth_mcp import column_analysis

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

def process_uploaded_file(file) -> tuple[Optional[pd.DataFrame], Optional[dict], str, list]:
    """
    Process uploaded file, analyze columns, and extract SKU list.
    
    Args:
        file: Gradio File object (can be None)
        
    Returns:
        Tuple of (DataFrame, analysis_dict, status_message, sku_list)
    """
    if file is None:
        return None, None, "No file uploaded. Using default dataset.", SKU_LIST
    
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
            return None, None, f"❌ Unsupported file type: {file_ext}", SKU_LIST
        
        # Analyze columns using the new column analysis module
        analysis = column_analysis.analyze_columns(df)
        
        # Create status message
        status = f"✅ Loaded {len(df)} rows, {len(df.columns)} columns from {os.path.basename(file_path)}"
        
        # Add smart suggestions to status
        if analysis['suggested_date'] and analysis['suggested_metric']:
            status += f"\n💡 Auto-detected: Date={analysis['suggested_date']}, Metric={analysis['suggested_metric']}"
            if analysis['suggested_product']:
                status += f", Product={analysis['suggested_product']}"
        else:
            status += "\n⚠️ Could not auto-detect columns. Please select manually."
        
        # Extract SKU list from uploaded data if product column detected
        sku_list = []
        if analysis['suggested_product']:
            product_col = analysis['suggested_product']
            if product_col in df.columns:
                sku_list = df[product_col].dropna().unique().tolist()
                sku_list = [str(sku) for sku in sku_list]  # Ensure string type
        
        return df, analysis, status, sku_list
        
    except Exception as e:
        return None, None, f"❌ Error processing file: {str(e)}", SKU_LIST

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

async def create_forecast_plot_with_mapping(
    df: Optional[pd.DataFrame],
    date_col: str,
    metric_col: str,
    product_col: Optional[str],
    sku: str,
    horizon: int
) -> go.Figure:
    """
    Generate forecast plot using custom column mapping.
    
    Args:
        df: Uploaded DataFrame (or None for default dataset)
        date_col: Name of date column in user's data
        metric_col: Name of metric column in user's data
        product_col: Optional name of product ID column (or "(None)")
        sku: Product SKU to forecast
        horizon: Forecast horizon in days
        
    Returns:
        Plotly figure with forecast visualization
    """
    if df is None:
        # Use default dataset via API
        return await create_forecast_plot(sku)
    
    try:
        # Handle "(None)" selection for product column
        if product_col == "(None)":
            product_col = None
        
        # Validate column mapping
        validation = column_analysis.validate_column_mapping(
            df, date_col, metric_col, product_col
        )
        
        if not validation["valid"]:
            error_msg = "❌ Invalid column mapping:\n" + "\n".join(validation["errors"])
            return _create_error_plot(error_msg)
        
        # Show warnings if any
        if validation["warnings"]:
            print("⚠️ Warnings:", validation["warnings"])
        
        # Rename columns to expected format
        df_mapped = df.copy()
        df_mapped = df_mapped.rename(columns={
            date_col: 'date',
            metric_col: 'sales'
        })
        
        if product_col:
            df_mapped = df_mapped.rename(columns={product_col: 'sku'})
        
        # Map 'sales' column to 'quantity' for preprocessing compatibility
        df_mapped['quantity'] = df_mapped['sales']
        df_mapped = df_mapped.drop('sales', axis=1)
        
        # Process with existing logic
        from src.expo_smooth_mcp import preprocessing, logic
        processed_df = preprocessing.preprocess_data(df_mapped)
        
        if processed_df is None or processed_df.empty:
            return _create_error_plot("❌ Data processing failed. Check data format.")
        
        # Validate SKU exists
        valid_skus = logic.get_available_skus(processed_df)
        if sku not in valid_skus:
            return _create_error_plot(
                f"❌ SKU '{sku}' not found.\nAvailable: {', '.join(valid_skus[:10])}"
            )
        
        # Generate forecast
        forecast_data = logic.get_forecast_data(processed_df, sku, horizon)
        return _create_forecast_plot_from_data(forecast_data)
        
    except Exception as e:
        return _create_error_plot(f"❌ Error generating forecast: {str(e)}")

# --- Gradio UI Definition ---

def create_gradio_interface():
    """Create and configure the Gradio interface with column mapping."""
    
    with gr.Blocks(title="Sales Forecasting") as interface:
        gr.Markdown("# 📊 Sales Forecasting Application")
        gr.Markdown("Upload your sales data to generate forecasts with exponential smoothing.")
        
        # State variables
        df_state = gr.State(None)
        analysis_state = gr.State(None)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Step 1: File Upload
                gr.Markdown("### 1️⃣ Upload Your Data")
                file_upload = gr.File(
                    label="Upload CSV, Excel, or JSON",
                    file_types=[".csv", ".xlsx", ".xls", ".json"],
                    type="filepath"
                )
                upload_status = gr.Textbox(
                    label="Upload Status",
                    value="📁 No file uploaded. Using default dataset.",
                    interactive=False,
                    lines=3
                )
                
                # Step 2: Column Mapping (initially hidden)
                with gr.Group(visible=False) as mapping_section:
                    gr.Markdown("### 2️⃣ Map Your Data Columns")
                    gr.Markdown("*Select which columns contain your date, metric, and product data.*")
                    
                    date_column = gr.Dropdown(
                        label="📅 Date/Time Column",
                        choices=[],
                        info="Column containing dates or timestamps"
                    )
                    
                    metric_column = gr.Dropdown(
                        label="📈 Metric Column to Forecast",
                        choices=[],
                        info="Numeric column with values to forecast (sales, demand, quantity, etc.)"
                    )
                    
                    product_column = gr.Dropdown(
                        label="🏷️ Product ID Column (Optional)",
                        choices=[],
                        value=None,
                        info="Column for grouping by product (SKU, Product ID, etc.)"
                    )
                
                # Step 3: Select Product & Parameters
                gr.Markdown("### 3️⃣ Select Product & Forecast Settings")
                sku_dropdown = gr.Dropdown(
                    choices=SKU_LIST,
                    label="Product SKU",
                    value=SKU_LIST[0] if SKU_LIST else None
                )
                
                horizon_slider = gr.Slider(
                    minimum=7,
                    maximum=365,
                    value=90,
                    step=1,
                    label="Forecast Horizon (days)"
                )
                
                forecast_button = gr.Button("🚀 Generate Forecast", variant="primary")
            
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Forecast Visualization")
        
        # Event: File uploaded
        file_upload.upload(
            fn=process_uploaded_file,
            inputs=[file_upload],
            outputs=[df_state, analysis_state, upload_status, sku_dropdown]
        ).then(
            # Show mapping section and populate dropdowns
            fn=lambda analysis: (
                gr.update(visible=True),
                gr.update(
                    choices=analysis.get("all_columns", []) if analysis else [],
                    value=analysis.get("suggested_date") if analysis else None
                ),
                gr.update(
                    choices=analysis.get("all_columns", []) if analysis else [],
                    value=analysis.get("suggested_metric") if analysis else None
                ),
                gr.update(
                    choices=["(None)"] + (analysis.get("all_columns", []) if analysis else []),
                    value=analysis.get("suggested_product") if analysis else None
                )
            ),
            inputs=[analysis_state],
            outputs=[mapping_section, date_column, metric_column, product_column]
        )
        
        # Event: Generate forecast
        forecast_button.click(
            fn=create_forecast_plot_with_mapping,
            inputs=[
                df_state,
                date_column,
                metric_column,
                product_column,
                sku_dropdown,
                horizon_slider
            ],
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