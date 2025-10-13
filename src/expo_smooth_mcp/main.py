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

from typing import List, Dict, Any, Optional
import sys
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastmcp import FastMCP
import uvicorn

# Import business logic layer
from . import logic

# --- Pydantic Models ---

class ForecastRequest(BaseModel):
    """Request model for forecast API."""
    sku: str = Field(
        ...,
        description="Product SKU code",
        json_schema_extra={"example": "PRODUCT_123"}
    )
    forecast_horizon: int = Field(
        90,
        ge=1,
        le=365,
        description="Days to forecast ahead"
    )

class ForecastResponse(BaseModel):
    """Response model for forecast API."""
    dates: List[str]
    actuals: List[Optional[float]]
    forecast: List[float]
    metadata: Dict[str, Any]

# --- Application Configuration ---

APP_VERSION = "2.0.0"
APP_NAME = "Expo Smooth MCP Server"
APP_DESCRIPTION = (
    "Production MCP server for exponential smoothing forecasting. "
    "Supports both stdio and HTTP/SSE transports."
)

# --- Global State ---

PROCESSED_DF = None  # Will be loaded on startup

# --- Lifespan Context Manager ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan: startup and shutdown.
    
    This replaces the deprecated @app.on_event("startup") pattern.
    """
    global PROCESSED_DF
    
    # Startup
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
    
    yield  # Application runs here
    
    # Shutdown (cleanup if needed)
    print(f"Shutting down {APP_NAME}")

# --- FastAPI Application ---

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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

@app.get("/")
async def root():
    """
    Service information and API documentation.

    Returns metadata about the Expo Smooth MCP Server including
    available endpoints, version, and usage instructions.
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "status": "operational",
        "endpoints": {
            "health": {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint"
            },
            "mcp_tools": {
                "path": "/mcp",
                "method": "POST",
                "description": "MCP protocol endpoint (SSE transport)",
                "tools": ["forecast_sku", "list_available_skus"]
            },
            "rest_api": {
                "path": "/api/forecast",
                "method": "POST",
                "description": "REST API for forecasting"
            },
            "documentation": {
                "path": "/docs",
                "method": "GET",
                "description": "OpenAPI/Swagger documentation"
            }
        },
        "usage": {
            "mcp_clients": "Connect via MCP protocol at /mcp endpoint",
            "rest_clients": "POST to /api/forecast with JSON payload",
            "web_ui": "Visit /gradio for interactive interface (Phase 3)"
        },
        "data_status": "loaded" if PROCESSED_DF is not None else "not_loaded",
        "sku_count": len(logic.get_available_skus(PROCESSED_DF)) if PROCESSED_DF is not None else 0
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns health status of the service including data loading status.
    Used by monitoring systems, load balancers, and container orchestrators.

    Returns:
        200 OK: Service is healthy (data loaded)
        503 Service Unavailable: Service unhealthy (data not loaded)

    Response format:
        {
            "status": "healthy" | "unhealthy",
            "timestamp": "2024-01-15T10:30:00Z",
            "version": "2.0.0",
            "data_loaded": true | false,
            "sku_count": 3
        }
    """
    from datetime import datetime

    # Check if data is loaded
    data_loaded = PROCESSED_DF is not None
    
    # Get SKU count safely
    if data_loaded and PROCESSED_DF is not None:
        sku_count = len(logic.get_available_skus(PROCESSED_DF))
    else:
        sku_count = 0

    # Determine health status
    is_healthy = data_loaded
    status_code = 200 if is_healthy else 503

    # Prepare response
    response = {
        "status": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": APP_VERSION,
        "data_loaded": data_loaded,
        "sku_count": sku_count
    }

    # Return appropriate HTTP status
    return JSONResponse(
        content=response,
        status_code=status_code
    )

@app.post("/api/forecast", response_model=ForecastResponse)
async def api_forecast(request: ForecastRequest):
    """
    Generate sales forecast via REST API.
    
    Alternative to MCP tools for clients that prefer REST.
    Accepts JSON request body with SKU and horizon.
    """
    if PROCESSED_DF is None:
        raise HTTPException(
            status_code=503,
            detail="Data not loaded. Server not ready."
        )
    
    try:
        # Get valid SKUs for validation
        valid_skus = logic.get_available_skus(PROCESSED_DF)
        
        # Validate and generate forecast
        logic.validate_forecast_request(
            request.sku,
            request.forecast_horizon,
            valid_skus
        )
        
        forecast_data = logic.get_forecast_data(
            PROCESSED_DF,
            request.sku,
            request.forecast_horizon
        )
        
        return forecast_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Mount MCP Server ---

# Mount MCP server as ASGI sub-application at /mcp endpoint
# This exposes MCP tools via HTTP/SSE transport for remote clients
# Local stdio transport is handled separately in main block
app.mount("/mcp", mcp.http_app())

print(f"✓ Mounted MCP server at /mcp with HTTP transport")

# --- Main Entry Point ---

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} - Dual-transport MCP server"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="http",
        help="Transport mode: stdio for local MCP clients, http for production server (default: http)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP server (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development (HTTP mode only)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        # --- stdio Transport (Local MCP Clients) ---
        print(f"{APP_NAME} v{APP_VERSION} - stdio mode", file=sys.stderr)
        print("Ready for MCP communication via stdin/stdout", file=sys.stderr)
        
        # Load data synchronously for stdio mode
        try:
            PROCESSED_DF = logic.get_processed_data()
            sku_count = len(logic.get_available_skus(PROCESSED_DF))
            print(f"✓ Loaded data: {sku_count} SKUs", file=sys.stderr)
        except Exception as e:
            print(f"✗ ERROR: Failed to load data: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Run MCP server in stdio mode
        import asyncio
        asyncio.run(mcp.run_stdio_async(show_banner=False))
        
    else:
        # --- HTTP Transport (Production Server) ---
        print(f"{APP_NAME} v{APP_VERSION} - HTTP mode")
        print(f"Starting server at http://{args.host}:{args.port}")
        print(f"MCP endpoint: http://{args.host}:{args.port}/mcp")
        print(f"API docs: http://{args.host}:{args.port}/docs")
        
        # Run FastAPI server with uvicorn
        uvicorn.run(
            "src.expo_smooth_mcp.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )