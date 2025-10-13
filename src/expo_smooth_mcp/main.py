"""
Expo Smooth MCP Server - Production FastAPI + FastMCP Application

This module implements a production-grade MCP server for exponential smoothing
forecasting. It provides three interfaces:

1. MCP Tools (stdio and HTTP/SSE transports)
   - forecast_sku: Generate forecast for a specific product
   - list_available_skus: Get all available product codes

2. REST API Endpoints
   - GET  /: Service information
   - GET  /health: Health check
   - POST /api/forecast: REST forecast endpoint
   - GET  /docs: OpenAPI documentation

3. Gradio UI (backward compatibility)
   - Mounted at /gradio for existing users

Architecture:
    Client (Claude/Cursor/API)
        ↓
    FastAPI (ASGI Framework)
        ↓
    FastMCP (MCP Protocol Layer)
        ↓
    Business Logic (logic.py)
        ↓
    Forecasting Engine (forecasting.py)

Usage:
    # HTTP/SSE transport (production)
    $ uvicorn main:app --host 0.0.0.0 --port 8000

    # stdio transport (local development)
    $ python -m src.expo_smooth_mcp.main --transport stdio
"""

from typing import List, Dict, Any
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
import uvicorn

# Import business logic layer
from . import logic

# --- Application Configuration ---

APP_VERSION = "2.0.0"
APP_NAME = "Expo Smooth MCP Server"
APP_DESCRIPTION = (
    "Production MCP server for exponential smoothing forecasting. "
    "Supports both stdio and HTTP/SSE transports."
)

# --- FastAPI Application ---

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- FastMCP Server ---

mcp = FastMCP(
    name="expo-smooth-forecast",
    version=APP_VERSION,
)

# --- Global State ---
# (Data loading will be added in TASK-203)

PROCESSED_DF = None  # Will be loaded on startup

# --- MCP Tools ---

@mcp.tool()
async def forecast_sku(
    sku: str,
    forecast_horizon: int = 90
) -> Dict[str, Any]:
    """
    Generate sales forecast for a specific product SKU.

    This tool uses Holt-Winters exponential smoothing to forecast future sales
    based on historical data. The forecast includes trend and seasonality patterns.

    Parameters:
        sku: Product SKU code (e.g., "PRODUCT_123")
             Use list_available_skus tool to see all valid SKUs
        forecast_horizon: Number of days to forecast ahead (default: 90)
                         Must be between 1 and 365 days

    Returns:
        Dictionary with forecast data:
        {
            "dates": ["2025-01-01", "2025-01-02", ...],
            "actuals": [100.0, 105.0, None, None, ...],
            "forecast": [102.0, 107.0, 110.0, 115.0, ...],
            "metadata": {
                "sku": "PRODUCT_123",
                "forecast_horizon": 90,
                "historical_points": 365,
                "forecast_points": 90
            }
        }

    Example:
        result = await forecast_sku("PRODUCT_123", 90)
        print(f"Generated {len(result['forecast'])} forecast points")

    Raises:
        ValueError: If SKU not found or horizon out of valid range
        RuntimeError: If data failed to load on startup
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        raise RuntimeError(
            "Data not loaded. Server started without valid dataset. "
            "Check server logs for startup errors."
        )

    try:
        # Validate inputs
        valid_skus = logic.get_available_skus(PROCESSED_DF)
        logic.validate_forecast_request(sku, forecast_horizon, valid_skus)

        # Generate forecast
        forecast_data = logic.get_forecast_data(
            PROCESSED_DF,
            sku,
            forecast_horizon
        )

        return forecast_data

    except ValueError as e:
        # Re-raise validation errors with context
        raise ValueError(f"Forecast validation failed: {str(e)}")

    except Exception as e:
        # Log unexpected errors
        print(f"ERROR in forecast_sku: {e}")
        raise RuntimeError(f"Forecast generation failed: {str(e)}")

@mcp.tool()
async def list_available_skus() -> List[str]:
    """
    List all product SKUs available for forecasting.

    Use this tool to discover what products exist in the dataset before
    requesting a forecast. Each SKU can be passed to the forecast_sku tool.

    Returns:
        List of product SKU codes, sorted alphabetically
        Example: ["PRODUCT_001", "PRODUCT_002", "PRODUCT_123", ...]

    Example:
        skus = await list_available_skus()
        print(f"Found {len(skus)} products")

    Raises:
        RuntimeError: If data failed to load on startup
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        raise RuntimeError(
            "Data not loaded. Server started without valid dataset. "
            "Check server logs for startup errors."
        )

    try:
        # Get sorted list of SKUs
        sku_list = logic.get_available_skus(PROCESSED_DF)
        return sku_list

    except Exception as e:
        print(f"ERROR in list_available_skus: {e}")
        raise RuntimeError(f"Failed to retrieve SKU list: {str(e)}")

# --- REST API Endpoints ---
# (Will be added in TASK-207, TASK-208, TASK-210)

# --- Mount MCP Server ---
# (Will be added in TASK-206)

# --- Startup Event ---

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    global PROCESSED_DF
    
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    
    try:
        # Load and cache data using singleton pattern
        PROCESSED_DF = logic.get_processed_data()
        sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        print(f"✓ Data loaded successfully")
        print(f"✓ Found {sku_count} unique SKUs")
        print(f"✓ Ready to serve requests")
        
    except FileNotFoundError as e:
        print(f"✗ ERROR: Data file not found: {e}")
        print("✗ Server will start but forecast endpoints will fail")
        # Don't crash - allow health checks to work
        
    except Exception as e:
        print(f"✗ ERROR: Failed to load data: {e}")
        print("✗ Server will start but forecast endpoints will fail")

# --- Main Entry Point ---

if __name__ == "__main__":
    # Dual-transport support will be added in TASK-209
    uvicorn.run(app, host="0.0.0.0", port=8000)