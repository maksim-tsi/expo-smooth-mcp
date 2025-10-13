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
# (Will be added in TASK-204 and TASK-205)

# --- REST API Endpoints ---
# (Will be added in TASK-207, TASK-208, TASK-210)

# --- Mount MCP Server ---
# (Will be added in TASK-206)

# --- Startup Event ---

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    # Data loading will be added in TASK-203

# --- Main Entry Point ---

if __name__ == "__main__":
    # Dual-transport support will be added in TASK-209
    uvicorn.run(app, host="0.0.0.0", port=8000)