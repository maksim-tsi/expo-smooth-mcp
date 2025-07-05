import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from src.expo_smooth_mcp.preprocessing import preprocess_data
from src.expo_smooth_mcp.forecasting import generate_forecast

# --- 1. Initialization: Load and preprocess data once at startup ---
try:
    RAW_DF = pd.read_csv('FMCG_Sales.csv')
    PROCESSED_DF = preprocess_data(RAW_DF.copy())
    SKU_LIST = PROCESSED_DF.index.get_level_values('sku').unique().tolist()
    print("Successfully loaded and preprocessed data.")
except FileNotFoundError:
    print("ERROR: FMCG_Sales.csv not found. Please ensure the dataset is in the root directory.")
    # Create empty placeholders to allow the app to launch with an error message
    PROCESSED_DF = pd.DataFrame()
    SKU_LIST = []


# --- 2. Core Logic Function: Generate plot based on user input ---
def create_forecast_plot(sku: str) -> go.Figure:
    """
    Takes a SKU selected by the user, generates a forecast, and returns a Plotly figure.
    This function is the core of the Gradio interface.
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

    try:
        # Generate the forecast data
        forecast_df = generate_forecast(PROCESSED_DF, sku, forecast_horizon=90)
        
        # Create an interactive plot with Plotly
        fig = go.Figure()

        # Add the historical actuals trace
        fig.add_trace(go.Scatter(
            x=forecast_df.index, 
            y=forecast_df['actuals'], 
            mode='lines', 
            name='Historical Sales',
            line=dict(color='blue')
        ))

        # Add the forecast trace
        fig.add_trace(go.Scatter(
            x=forecast_df.index, 
            y=forecast_df['forecast'], 
            mode='lines', 
            name='Forecasted Sales',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=f"Sales Forecast for SKU: {sku}",
            xaxis_title="Date",
            yaxis_title="Quantity Sold",
            legend_title="Series"
        )
        
        return fig

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