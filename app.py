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

# --- Gradio UI Definition ---

demo = gr.Interface(
    fn=create_forecast_plot,
    inputs=[
        gr.Dropdown(
            choices=SKU_LIST if SKU_LIST else ["No SKUs available"],
            label="Select Product SKU",
            info="Choose a product to forecast its sales for the next 90 days.",
            value=SKU_LIST[0] if SKU_LIST else None
        )
    ],
    outputs=[gr.Plot(label="Forecast Visualization")],
    title="📈 Supply Chain Demand Forecasting",
    description=(
        "An interactive demonstration of Exponential Smoothing for FMCG sales forecasting. "
        "This interface connects to the FastAPI backend to generate predictions."
    ),
    allow_flagging="never",
    theme=gr.themes.Soft()
)

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