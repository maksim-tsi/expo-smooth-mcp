import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from src.expo_smooth_mcp import logic

# --- 1. Initialization: Load and preprocess data once at startup ---
try:
    PROCESSED_DF = logic.get_processed_data()
    SKU_LIST = logic.get_available_skus(PROCESSED_DF)
    print("Successfully loaded data via logic module.")
except Exception as e:
    print(f"ERROR: Failed to load data: {e}")
    # Create empty placeholders to allow the app to launch with an error message
    PROCESSED_DF = pd.DataFrame()
    SKU_LIST = []


# --- 2. Core Logic Function: Generate plot based on user input ---
def create_forecast_plot(sku: str) -> go.Figure:
    """
    Takes a SKU selected by the user, generates a forecast, and returns a Plotly figure.
    This function is now a thin wrapper that delegates to the logic module.
    """
    if not sku:
        # If no SKU is selected, return an empty plot with a message
        fig = go.Figure()
        fig.update_layout(
            title_text="Please select a product SKU to view its forecast",
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[{
                "text": "No data to display.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 20}
            }]
        )
        return fig

    if PROCESSED_DF.empty:
        # If data failed to load, show error
        fig = go.Figure()
        fig.update_layout(title_text="Error: Data failed to load. Please check FMCG_Sales.csv file.")
        return fig

    try:
        # Validate request using logic module
        validation_error = logic.validate_forecast_request(sku, 90, SKU_LIST)
        if validation_error:
            fig = go.Figure()
            fig.update_layout(title_text=f"Validation error: {validation_error}")
            return fig
        
        # Generate forecast data using logic module
        forecast_data = logic.get_forecast_data(PROCESSED_DF, sku, forecast_horizon=90)
        
        # Create visualization using logic module
        return logic.create_forecast_plot(forecast_data)
        
    except Exception as e:
        # Handle errors gracefully in the UI
        print(f"An error occurred: {e}")
        fig = go.Figure()
        fig.update_layout(title_text=f"Error generating forecast for {sku}: {e}")
        return fig


# --- 3. UI Definition: Create and launch the Gradio Interface ---
demo = gr.Interface(
    fn=create_forecast_plot,
    inputs=[
        gr.Dropdown(
            choices=SKU_LIST,
            label="Select Product SKU",
            info="Choose a product to forecast its sales for the next 90 days."
        )
    ],
    outputs=[
        gr.Plot(label="Forecast Visualization")
    ],
    title="📈 Supply Chain Demand Forecasting",
    description="An interactive demo of Exponential Smoothing for FMCG sales data. This application showcases a statistical model served via a Gradio interface.",
    allow_flagging="never"
)

if __name__ == "__main__":
    if PROCESSED_DF.empty:
        print("Could not start the app because the data failed to load.")
    else:
        # To enable the MCP server, we would add mcp_server=True
        # For now, we launch the UI only.
        demo.launch()