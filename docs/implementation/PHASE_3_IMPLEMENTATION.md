# Phase 3: Mount Gradio UI - Implementation Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** Phase 3 - Mount Gradio UI  
**Version:** 1.0.0  
**Created:** October 13, 2025

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Task Breakdown](#task-breakdown)
4. [Implementation Tasks](#implementation-tasks)
5. [Testing Strategy](#testing-strategy)
6. [Troubleshooting](#troubleshooting)
7. [Success Criteria](#success-criteria)

---

## Overview

### What is Phase 3?

Phase 3 integrates the Gradio web UI with the FastMCP + FastAPI backend created in Phase 2. This creates a unified service offering **three interfaces**:

1. **REST API** - HTTP endpoints for traditional web clients
2. **MCP Tools** - Protocol integration for AI assistants (Claude, Cursor, etc.)
3. **Gradio UI** - Interactive web interface for end users

### Why Three Interfaces?

**Backward Compatibility:** Existing Gradio users can continue using the familiar web interface

**Modern Integration:** New users can leverage MCP tools in AI assistants

**API Access:** Developers can integrate via REST API programmatically

**Unified Service:** All three run in a single FastAPI application, sharing data and logic

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                   (http://localhost:8000)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  REST API    │  │  MCP Tools   │  │  Gradio UI   │      │
│  │              │  │              │  │              │      │
│  │ /api/forecast│  │ /mcp         │  │ /gradio      │      │
│  │ /health      │  │ (stdio/SSE)  │  │ (mounted)    │      │
│  │ /docs        │  │              │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │ Business     │                          │
│                    │ Logic Layer  │                          │
│                    │ (logic.py)   │                          │
│                    └──────┬───────┘                          │
│                           │                                  │
│                    ┌──────▼───────┐                          │
│                    │ Forecasting  │                          │
│                    │ Engine       │                          │
│                    │(forecasting.py)│                        │
│                    └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### What Gets Built

**Before Phase 3:**
- Separate Gradio app (`app.py`) running standalone
- FastAPI backend with REST and MCP interfaces

**After Phase 3:**
- Gradio mounted at `/gradio` in FastAPI app
- Single unified service with all three interfaces
- Shared data and business logic
- Simplified deployment

---

## Prerequisites

### Phase 2 Must Be Complete

✅ **Phase 2 Status:** Complete (validated October 13, 2025)
- FastMCP + FastAPI backend built
- REST API endpoints working
- MCP tools functional
- 27/27 tests passing
- Claude Desktop integration validated

### Required Knowledge

- **Python:** Async/await, decorators, imports
- **FastAPI:** Mounting applications, routing
- **Gradio:** Interface creation, component usage
- **HTTP:** Status codes, headers, CORS concepts

### Environment Setup

```bash
# Activate conda environment
conda activate tsi

# Verify Phase 2 code is working
cd /Users/max/Documents/code/expo-smooth-mcp
python -m src.expo_smooth_mcp.main --transport http --port 8000

# In another terminal, test REST API
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}

# Stop server (Ctrl+C)
```

### Dependencies Already Installed

From Phase 2, you should have:
```
fastapi>=0.104.0
fastmcp>=2.12.0
gradio>=4.0.0
uvicorn[standard]>=0.24.0
httpx>=0.25.0
pydantic>=2.0.0
```

---

## Task Breakdown

### Task Summary

| Task ID | Description | Time | Complexity | Dependencies |
|---------|-------------|------|------------|--------------|
| **TASK-301** | Create/Verify Pydantic models | 0.5h | Low | TASK-210 |
| **TASK-302** | Refactor Gradio to call REST API | 2h | High | TASK-301 |
| **TASK-303** | Mount Gradio app in FastAPI | 1h | Medium | TASK-302 |
| **TASK-304** | Test unified service locally | 1.5h | Medium | TASK-303 |
| **TASK-305** | Handle CORS (if needed) | 0.5h | Low | TASK-303 |
| **TASK-306** | Create integration tests | 1.5h | Medium | TASK-304 |

**Total Estimated Time:** ~7 hours (approximately 1 day)

### Implementation Order

```
TASK-301 (Verify Models)
    ↓
TASK-302 (Refactor Gradio) ← Main complexity
    ↓
TASK-303 (Mount in FastAPI)
    ↓
TASK-304 (Test Everything)
    ↓
TASK-305 (CORS if needed) ← Optional
    ↓
TASK-306 (Integration Tests)
```

---

## Implementation Tasks

### TASK-301: Create/Verify Pydantic Models for API

**Estimated Time:** 0.5 hours | **Complexity:** Low

**Description:**
Verify that Pydantic models from Phase 2 (TASK-210) are suitable for Gradio integration. These models ensure type safety between Gradio UI and FastAPI backend.

**Implementation:**

#### Step 1: Verify Existing Models (5 min)

```bash
# Check if models exist in main.py
grep -A 10 "class ForecastRequest" src/expo_smooth_mcp/main.py
grep -A 10 "class ForecastResponse" src/expo_smooth_mcp/main.py
```

**Expected:** Both models should exist with proper fields and validation.

#### Step 2: Review Model Structure (10 min)

```python
# src/expo_smooth_mcp/main.py (should already exist)

from pydantic import BaseModel, Field
from typing import List, Optional

class ForecastRequest(BaseModel):
    """Request model for forecast API endpoint."""
    sku: str = Field(
        ...,
        description="Product SKU code to forecast",
        json_schema_extra={"example": "PRODUCT_123"}
    )
    forecast_horizon: int = Field(
        default=90,
        ge=1,
        le=365,
        description="Number of days to forecast ahead",
        json_schema_extra={"example": 90}
    )

class ForecastMetadata(BaseModel):
    """Metadata about the forecast."""
    sku: str
    forecast_horizon: int
    historical_points: int
    forecast_points: int

class ForecastResponse(BaseModel):
    """Response model for forecast API endpoint."""
    dates: List[str] = Field(
        description="Date strings in ISO format (YYYY-MM-DD)"
    )
    actuals: List[Optional[float]] = Field(
        description="Historical sales values (null for future dates)"
    )
    forecast: List[float] = Field(
        description="Forecasted sales values"
    )
    metadata: ForecastMetadata = Field(
        description="Forecast metadata and statistics"
    )
```

#### Step 3: Test Models (5 min)

```python
# Test in Python REPL or create test_models.py
from src.expo_smooth_mcp.main import ForecastRequest, ForecastResponse, ForecastMetadata

# Test request validation
request = ForecastRequest(sku="PRODUCT_001", forecast_horizon=90)
assert request.sku == "PRODUCT_001"
assert request.forecast_horizon == 90

# Test invalid horizon
try:
    invalid = ForecastRequest(sku="TEST", forecast_horizon=500)
    assert False, "Should have raised validation error"
except Exception as e:
    print(f"✓ Validation works: {e}")

# Test response model
metadata = ForecastMetadata(
    sku="PRODUCT_001",
    forecast_horizon=90,
    historical_points=100,
    forecast_points=90
)
response = ForecastResponse(
    dates=["2025-01-01", "2025-01-02"],
    actuals=[100.0, None],
    forecast=[100.0, 105.0],
    metadata=metadata
)
assert len(response.dates) == 2
print("✓ Models working correctly")
```

#### Step 4: Optional - Refactor to Separate File (10 min)

**Note:** Only do this if you prefer better code organization. Not required.

```python
# Create src/expo_smooth_mcp/models.py
"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class ForecastRequest(BaseModel):
    """Request model for forecast API endpoint."""
    # ... (move from main.py)

class ForecastMetadata(BaseModel):
    """Metadata about the forecast."""
    # ... (move from main.py)

class ForecastResponse(BaseModel):
    """Response model for forecast API endpoint."""
    # ... (move from main.py)
```

```python
# Update src/expo_smooth_mcp/main.py imports
# Replace inline model definitions with:
from .models import ForecastRequest, ForecastResponse, ForecastMetadata
```

**Acceptance Criteria:**
- [ ] ForecastRequest model exists with sku and forecast_horizon
- [ ] ForecastResponse model exists with dates, actuals, forecast, metadata
- [ ] ForecastMetadata model exists with all required fields
- [ ] Models have proper validation (ge=1, le=365 for horizon)
- [ ] Models can be imported successfully
- [ ] Test validation passes
- [ ] REST API endpoint (from Phase 2) still works with models

---

### TASK-302: Refactor Gradio to Call REST API

**Estimated Time:** 2 hours | **Complexity:** High

**Description:**
Refactor `app.py` to communicate with FastAPI via HTTP instead of calling business logic directly. This decouples the UI from the backend.

**Why This Is Important:**
- Allows Gradio to run as independent client
- Prepares for mounting in FastAPI
- Enables separate deployment if needed
- Follows microservice architecture principles

#### Step 1: Backup Current app.py (2 min)

```bash
cp app.py app.py.backup
echo "✓ Backup created: app.py.backup"
```

#### Step 2: Add httpx Dependency (5 min)

```bash
# Should already be installed from Phase 2
pip list | grep httpx

# If not installed:
pip install httpx>=0.25.0
```

#### Step 3: Refactor app.py (60 min)

Replace the entire `app.py` with the refactored version:

```python
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
            "text": "No data to display.",
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
    """Create Plotly figure from forecast data."""
    import plotly.graph_objects as go
    from datetime import datetime
    
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
            name='Historical (Actual)',
            line=dict(color='blue', width=2),
            marker=dict(size=5)
        ))
    
    # Add forecast data
    forecast_dates = dates[-len([f for f in forecast if f is not None]):]
    forecast_values = [f for f in forecast if f is not None]
    
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
        title=f"Sales Forecast for {metadata['sku']} ({metadata['forecast_horizon']} days)",
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
    Fetch SKU list from API.
    
    For Gradio initialization, we need the SKU list synchronously.
    This function attempts to get it from the API, falls back to
    loading data directly if API is not available.
    """
    try:
        # Try to get SKU list from API root endpoint
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                data = response.json()
                
                # For now, we need to load locally for dropdown
                # TODO: Add GET /api/skus endpoint in future
                from src.expo_smooth_mcp import logic
                df = logic.get_processed_data()
                if df is not None:
                    return logic.get_available_skus(df)
        
        return []
    
    except Exception as e:
        print(f"⚠ Warning: Could not fetch SKU list: {e}")
        print(f"  Make sure API is running at {API_BASE_URL}")
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
            f"Cannot connect to API at {API_BASE_URL}\\n"
            f"Make sure the FastAPI server is running.\\n"
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
```

#### Step 4: Test Refactored Gradio Standalone (20 min)

**Terminal 1 - Start FastAPI:**
```bash
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Should see:
# ✓ Data loaded successfully
# ✓ Found 3 unique SKUs
# ✓ Starting Expo Smooth MCP Server v2.0.0 - HTTP mode
```

**Terminal 2 - Start Gradio:**
```bash
python app.py

# Should see:
# 🚀 Launching Gradio UI (Standalone Mode)
# API Base URL: http://localhost:8000
# SKUs Available: 3
# Running on local URL:  http://127.0.0.1:7860
```

**Browser Testing:**
1. Open http://localhost:7860
2. Verify dropdown has SKUs
3. Select a SKU
4. Verify plot generates
5. Try different SKUs

**Test Error Handling:**
1. Stop FastAPI server (Terminal 1: Ctrl+C)
2. Try generating a forecast in Gradio
3. Should see error message: "Cannot connect to API"
4. Restart FastAPI server
5. Try again - should work

#### Step 5: Verify No Regressions (10 min)

```bash
# Test that REST API still works
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' | jq '.metadata'

# Should return forecast metadata
```

**Acceptance Criteria:**
- [ ] app.py imports httpx
- [ ] create_forecast_plot() is async
- [ ] Calls /api/forecast endpoint via HTTP
- [ ] API_BASE_URL configurable via environment variable
- [ ] Handles API errors gracefully
- [ ] Handles network errors (API not running)
- [ ] Shows helpful error messages
- [ ] SKU dropdown populates correctly
- [ ] Works when FastAPI server running
- [ ] Shows error when API unavailable
- [ ] Can run standalone: `python app.py`
- [ ] Visual behavior matches original app

---

### TASK-303: Mount Gradio App in FastAPI

**Estimated Time:** 1 hour | **Complexity:** Medium

**Description:**
Mount the refactored Gradio application into FastAPI at `/gradio` path. This provides backward compatibility while centralizing services.

#### Step 1: Choose Implementation Approach (5 min)

**Option A: Import from app.py (Recommended)**
- Reuses existing app.py
- Easier to maintain
- Gradio can still run standalone

**Option B: Define inline in main.py**
- Simpler import structure
- All code in one place
- Cannot run Gradio standalone easily

**Decision:** Use Option A for flexibility

#### Step 2: Modify main.py to Mount Gradio (30 min)

Add this code to `src/expo_smooth_mcp/main.py` after all endpoints are defined (around line 290):

```python
# --- Mount Gradio UI (Backward Compatibility) ---

try:
    import gradio as gr
    
    # Import the Gradio demo from app.py
    # Note: This requires app.py to not auto-launch when imported
    print("📊 Loading Gradio UI...")
    
    # Temporarily set API_BASE_URL for Gradio
    # When mounted, Gradio should call same-origin APIs
    import os
    original_api_url = os.getenv("API_BASE_URL")
    os.environ["API_BASE_URL"] = "http://localhost:8000"  # Same origin
    
    from app import demo as gradio_demo
    
    # Restore original if it existed
    if original_api_url:
        os.environ["API_BASE_URL"] = original_api_url
    else:
        os.environ.pop("API_BASE_URL", None)
    
    # Mount Gradio at /gradio path
    app = gr.mount_gradio_app(
        app,                    # FastAPI app
        gradio_demo,            # Gradio Interface
        path="/gradio"          # Mount path
    )
    
    print("✅ Mounted Gradio UI at /gradio")
    print("   Access at: http://localhost:8000/gradio")
    
except ImportError as e:
    print(f"⚠️  Warning: Could not import Gradio: {e}")
    print("   Continuing without Gradio UI...")
    print("   Install with: pip install gradio")
    
except Exception as e:
    print(f"⚠️  Warning: Failed to mount Gradio UI: {e}")
    print("   Continuing without Gradio interface...")
    import traceback
    traceback.print_exc()
```

#### Step 3: Prevent app.py Auto-Launch (5 min)

Verify `app.py` has this at the end:

```python
# At end of app.py

if __name__ == "__main__":
    # Only launch if run directly, not when imported
    print("🚀 Launching Gradio UI (Standalone Mode)")
    demo.launch()
```

**Important:** The `if __name__ == "__main__":` guard prevents Gradio from launching when `main.py` imports it.

#### Step 4: Update Root Endpoint (10 min)

Update the root endpoint in `main.py` to include Gradio UI information:

```python
# In main.py, update GET / endpoint

@app.get("/")
async def root():
    """Service information and available endpoints."""
    return {
        "name": "Expo Smooth MCP Server",
        "version": "2.0.0",
        "description": "Exponential Smoothing forecasting via FastMCP",
        "data_status": "loaded" if PROCESSED_DF is not None else "not_loaded",
        "sku_count": len(logic.get_available_skus(PROCESSED_DF)) if PROCESSED_DF else 0,
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
                "description": "REST API forecast endpoint"
            },
            "gradio_ui": {  # NEW
                "path": "/gradio",
                "method": "GET",
                "description": "Interactive Gradio web interface"
            },
            "documentation": {
                "path": "/docs",
                "method": "GET",
                "description": "Interactive API documentation (OpenAPI/Swagger)"
            }
        },
        "usage": {
            "mcp_stdio": "python -m src.expo_smooth_mcp.main --transport stdio",
            "mcp_http": "python -m src.expo_smooth_mcp.main --transport http --port 8000",
            "rest_api": "curl -X POST http://localhost:8000/api/forecast -d '{...}'",
            "gradio_ui": "Open http://localhost:8000/gradio in browser",  # NEW
            "mcp_inspector": "npx @modelcontextprotocol/inspector http://localhost:8000/mcp"
        }
    }
```

#### Step 5: Test Mounted Gradio (10 min)

```bash
# Start unified server
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Should see:
# ✓ Data loaded successfully
# ✓ Found 3 unique SKUs
# ✓ Mounted MCP server at /mcp
# 📊 Loading Gradio UI...
# ✅ Mounted Gradio UI at /gradio
# ✓ Starting Expo Smooth MCP Server v2.0.0 - HTTP mode
```

**Browser Tests:**
```bash
# Test all endpoints
open http://localhost:8000/              # Root info
open http://localhost:8000/docs          # API docs
open http://localhost:8000/gradio        # Gradio UI ← NEW

# Verify in Gradio:
# 1. UI loads correctly
# 2. Dropdown has SKUs
# 3. Can generate forecasts
# 4. No console errors (F12)
```

**Acceptance Criteria:**
- [ ] Gradio imported successfully in main.py
- [ ] demo interface imported from app.py
- [ ] Mounted at /gradio using gr.mount_gradio_app()
- [ ] Server starts without errors
- [ ] /gradio endpoint accessible in browser
- [ ] Gradio UI loads correctly
- [ ] Dropdown populated with SKUs
- [ ] Can generate forecasts through UI
- [ ] No CORS errors in browser console
- [ ] Gradio doesn't interfere with other endpoints
- [ ] Root endpoint lists Gradio in endpoints
- [ ] Error handling if Gradio import fails

---

### TASK-304: Test Unified Service Locally

**Estimated Time:** 1.5 hours | **Complexity:** Medium

**Description:**
Comprehensive testing of all three interfaces (REST, MCP, Gradio) working together.

#### Step 1: Start Unified Server (5 min)

```bash
# Start in HTTP mode with all interfaces
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Verify startup logs:
# ✓ Data loaded successfully
# ✓ Found 3 unique SKUs  
# ✓ Mounted MCP server at /mcp
# ✓ Mounted Gradio UI at /gradio
# ✓ Starting Expo Smooth MCP Server v2.0.0 - HTTP mode
# ✓ Uvicorn running on http://0.0.0.0:8000
```

#### Step 2: Test REST API Interface (15 min)

```bash
# Test root endpoint
curl http://localhost:8000/ | jq '.endpoints | keys'
# Should show: ["documentation", "gradio_ui", "health", "mcp_tools", "rest_api"]

# Test health check
curl http://localhost:8000/health | jq '.status'
# Should return: "healthy"

# Test forecast API
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' | jq '.metadata'
# Should return forecast metadata

# Test error handling
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID"}' | jq '.detail'
# Should return: "Validation error: SKU 'INVALID' not found..."

# Test OpenAPI docs
open http://localhost:8000/docs
# ✓ Swagger UI loads
# ✓ Shows /api/forecast endpoint
# ✓ Can execute test requests
```

#### Step 3: Test MCP Interface (15 min)

```bash
# Option 1: Use Claude Desktop (if configured from Phase 2)
# Just ask Claude: "What forecasting tools do you have?"

# Option 2: Use MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp

# In Inspector:
# ✓ Connection successful
# ✓ Shows 2 tools: forecast_sku, list_available_skus
# ✓ Execute list_available_skus → Returns ["PRODUCT_001", "PRODUCT_002", "PRODUCT_003"]
# ✓ Execute forecast_sku(sku="PRODUCT_001", horizon=90) → Returns forecast data
```

#### Step 4: Test Gradio UI Interface (20 min)

```bash
# Open Gradio in browser
open http://localhost:8000/gradio
```

**Manual Testing Checklist:**
- [ ] Page loads without errors (< 2 seconds)
- [ ] Title shows: "📈 Supply Chain Demand Forecasting"
- [ ] Dropdown populated with 3 SKUs
- [ ] Select "PRODUCT_001" from dropdown
- [ ] Click Submit or wait for auto-update
- [ ] Plot appears showing historical (blue) and forecast (red dashed)
- [ ] Hover over plot shows values
- [ ] Select "PRODUCT_002" and verify new forecast
- [ ] Select "PRODUCT_003" and verify new forecast
- [ ] UI is responsive and smooth
- [ ] No JavaScript errors in browser console (F12)

#### Step 5: Cross-Interface Testing (20 min)

**Test 1: Concurrent Access**

Terminal 1:
```bash
# Make REST API calls in loop
while true; do
  curl -X POST http://localhost:8000/api/forecast \
    -H "Content-Type: application/json" \
    -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' > /dev/null
  echo "REST request sent"
  sleep 1
done
```

Terminal 2:
```bash
# Open Gradio and use it while REST API is being called
open http://localhost:8000/gradio
# Generate forecasts through UI
```

**Verify:**
- [ ] Both work simultaneously without conflicts
- [ ] No performance degradation
- [ ] No errors in either interface

**Test 2: Data Consistency**

```bash
# Get SKU count from REST API
curl http://localhost:8000/ | jq '.sku_count'
# Note the count (should be 3)

# Get SKU list from MCP (using Inspector or Claude)
# Count the returned SKUs (should be 3)

# Check Gradio dropdown
# Count options (should be 3)

# ✓ All three should show same number
```

**Test 3: Error Handling**

```bash
# Test invalid SKU in REST
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID_SKU"}' | jq '.detail'
# ✓ Should return 400 with helpful error message

# Test invalid SKU in Gradio
# Try selecting a SKU, then manually edit URL or dropdown
# ✓ Should show error plot with message

# Test server shutdown during request
# Stop server (Ctrl+C) while Gradio is generating forecast
# ✓ Should show connection error
```

#### Step 6: Performance Testing (10 min)

```bash
# Test response times
time curl http://localhost:8000/ > /dev/null
# ✓ Should be < 100ms

time curl http://localhost:8000/health > /dev/null
# ✓ Should be < 100ms

time curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' > /dev/null
# ✓ Should be < 1 second

# Test Gradio responsiveness
# Time from clicking Submit to plot appearing
# ✓ Should be < 2 seconds
```

#### Step 7: Browser Console Check (5 min)

```bash
# Open browser with developer tools
open http://localhost:8000/gradio
# Press F12 to open developer tools
```

**Console Tab:**
- [ ] No error messages (red text)
- [ ] No warnings about CORS
- [ ] No 404 errors for missing resources

**Network Tab:**
- [ ] POST to /api/forecast returns 200
- [ ] Response contains forecast data
- [ ] No failed requests

#### Step 8: Service Discovery (5 min)

```bash
# Verify all endpoints are discoverable
curl http://localhost:8000/ | jq '.endpoints'

# Should show all 5 endpoint categories:
# {
#   "health": {...},
#   "mcp_tools": {...},
#   "rest_api": {...},
#   "gradio_ui": {...},    ← NEW
#   "documentation": {...}
# }

# Verify Gradio UI path
curl http://localhost:8000/ | jq '.endpoints.gradio_ui.path'
# Should return: "/gradio"
```

**Acceptance Criteria:**
- [ ] Unified server starts successfully
- [ ] All three interfaces accessible
- [ ] REST API endpoints work correctly
- [ ] MCP tools work correctly
- [ ] Gradio UI works correctly
- [ ] No CORS or network errors
- [ ] Performance is acceptable (<1s for forecasts)
- [ ] All interfaces show consistent data
- [ ] Error handling works across all interfaces
- [ ] Can handle concurrent requests
- [ ] Ready for production deployment

---

### TASK-305: Handle CORS for Gradio

**Estimated Time:** 0.5 hours | **Complexity:** Low

**Description:**
Configure CORS middleware if needed. For mounted Gradio (same origin), CORS is usually NOT required.

#### Step 1: Test for CORS Issues (10 min)

```bash
# Start server
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Open Gradio in browser
open http://localhost:8000/gradio

# Open browser developer console (F12)
# Generate a forecast
# Check console for CORS errors
```

**Look for:**
- ❌ "Access-Control-Allow-Origin" header is missing
- ❌ CORS policy blocked the request
- ❌ Cross-origin request blocked

**Expected Result:** No CORS errors (because Gradio is mounted, same origin)

#### Step 2: Add CORS Middleware (if needed) (15 min)

**Only if you see CORS errors or plan separate deployment:**

```python
# In src/expo_smooth_mcp/main.py
# Add after FastAPI app creation (around line 85, after lifespan)

from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:7860,http://localhost:8000,http://127.0.0.1:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,  # Cache preflight for 10 minutes
)

print(f"✅ CORS middleware configured")
print(f"   Allowed origins: {ALLOWED_ORIGINS}")
```

#### Step 3: Test CORS Configuration (5 min)

```bash
# Test preflight request
curl -X OPTIONS http://localhost:8000/api/forecast \
  -H "Origin: http://localhost:7860" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" -i

# Should see in response headers:
# Access-Control-Allow-Origin: http://localhost:7860
# Access-Control-Allow-Methods: GET, POST, OPTIONS
# Access-Control-Allow-Headers: Content-Type, Authorization
```

**Acceptance Criteria:**
- [ ] Tested for CORS errors in browser console
- [ ] No CORS errors with mounted Gradio (expected)
- [ ] CORS middleware added only if needed
- [ ] Environment variable support for ALLOWED_ORIGINS
- [ ] Gradio UI works without CORS errors
- [ ] Security best practices followed (no wildcard "*")
- [ ] Configuration documented

---

### TASK-306: Create Integration Tests for Mounted UI

**Estimated Time:** 1.5 hours | **Complexity:** Medium

**Description:**
Create integration tests specifically for Gradio UI mounted in FastAPI.

#### Step 1: Create Test File (10 min)

```bash
# Create test file
touch tests/test_gradio_integration.py
```

#### Step 2: Write Integration Tests (60 min)

```python
# tests/test_gradio_integration.py
"""
Integration tests for Gradio UI mounted in FastAPI.

Tests verify that:
- Gradio UI is accessible at /gradio
- UI can communicate with FastAPI backend
- All functionality works end-to-end
"""

import pytest
from fastapi.testclient import TestClient
from src.expo_smooth_mcp.main import app, PROCESSED_DF
from src.expo_smooth_mcp import logic

# --- Fixtures ---

@pytest.fixture
def client():
    """Create FastAPI test client."""
    return TestClient(app)

# --- Gradio Endpoint Tests ---

class TestGradioMounting:
    """Tests for Gradio UI mounting."""
    
    def test_gradio_endpoint_accessible(self, client):
        """Should be able to access /gradio endpoint."""
        response = client.get("/gradio")
        
        # Gradio might redirect to /gradio/ (with trailing slash)
        assert response.status_code in [200, 307, 308], \
            f"Expected 200/307/308, got {response.status_code}"
    
    def test_gradio_with_trailing_slash(self, client):
        """Should be accessible with trailing slash."""
        response = client.get("/gradio/")
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
    
    def test_gradio_content_exists(self, client):
        """Gradio should return HTML content."""
        response = client.get("/gradio/")
        
        if response.status_code == 200:
            # Check response contains HTML
            assert len(response.text) > 0
            assert "<!DOCTYPE" in response.text or "<html" in response.text.lower()

class TestGradioFunctionality:
    """Tests for Gradio UI functionality."""
    
    def test_gradio_can_access_data(self, client):
        """Gradio should have access to SKU list."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        # The Gradio interface should be initialized with SKU list
        skus = logic.get_available_skus(PROCESSED_DF)
        assert len(skus) > 0, "No SKUs available for Gradio"
        
        # Verify SKUs are valid
        assert all(isinstance(sku, str) for sku in skus)
        assert len(skus) == 3, f"Expected 3 SKUs, got {len(skus)}"

class TestGradioAPIIntegration:
    """Tests for Gradio-FastAPI integration."""
    
    def test_gradio_backend_uses_same_data(self, client):
        """Gradio and REST API should use same data source."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        # Get SKU count from REST API
        rest_response = client.get("/")
        rest_data = rest_response.json()
        rest_sku_count = rest_data["sku_count"]
        
        # Get SKU count from logic (used by Gradio)
        gradio_sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        # Should be the same
        assert rest_sku_count == gradio_sku_count, \
            f"REST API shows {rest_sku_count} SKUs, Gradio has {gradio_sku_count}"
    
    def test_gradio_forecast_uses_same_logic(self, client):
        """Gradio forecast should produce same results as REST API."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        # Get forecast via REST API
        rest_response = client.post(
            "/api/forecast",
            json={"sku": test_sku, "forecast_horizon": 90}
        )
        assert rest_response.status_code == 200
        rest_data = rest_response.json()
        
        # Get forecast via logic (same as Gradio uses)
        gradio_data = logic.get_forecast_data(PROCESSED_DF, test_sku, 90)
        
        # Should produce identical results
        assert rest_data["metadata"]["sku"] == gradio_data["metadata"]["sku"]
        assert rest_data["metadata"]["forecast_horizon"] == \
               gradio_data["metadata"]["forecast_horizon"]
        assert len(rest_data["forecast"]) == len(gradio_data["forecast"])
        
        # First few forecast values should match
        for i in range(min(5, len(rest_data["forecast"]))):
            assert abs(rest_data["forecast"][i] - gradio_data["forecast"][i]) < 0.01, \
                f"Forecast mismatch at index {i}"

class TestGradioEndpointListing:
    """Tests for Gradio in service discovery."""
    
    def test_root_endpoint_lists_gradio(self, client):
        """Root endpoint should list Gradio UI in endpoints."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "endpoints" in data
        assert "gradio_ui" in data["endpoints"]
        assert data["endpoints"]["gradio_ui"]["path"] == "/gradio"
        assert data["endpoints"]["gradio_ui"]["method"] == "GET"
    
    def test_root_endpoint_usage_includes_gradio(self, client):
        """Root endpoint usage should mention Gradio."""
        response = client.get("/")
        data = response.json()
        
        assert "usage" in data
        assert "gradio_ui" in data["usage"]
        assert "/gradio" in data["usage"]["gradio_ui"]

class TestGradioErrorHandling:
    """Tests for Gradio error scenarios."""
    
    def test_gradio_accessible_even_if_data_not_loaded(self, client):
        """Gradio UI should be accessible even if data fails to load."""
        # The /gradio endpoint should return 200 regardless of data status
        response = client.get("/gradio/")
        
        # Should not return 503 or 500
        assert response.status_code in [200, 307, 308]

class TestGradioPerformance:
    """Performance tests for Gradio integration."""
    
    def test_gradio_page_load_time(self, client):
        """Gradio page should load quickly."""
        import time
        
        start = time.time()
        response = client.get("/gradio/")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 2.0, f"Gradio took {elapsed:.2f}s to load (should be < 2s)"

# Run tests with: pytest tests/test_gradio_integration.py -v
```

#### Step 3: Run Tests (15 min)

```bash
# Run all Gradio integration tests
pytest tests/test_gradio_integration.py -v

# Expected output:
# tests/test_gradio_integration.py::TestGradioMounting::test_gradio_endpoint_accessible PASSED
# tests/test_gradio_integration.py::TestGradioMounting::test_gradio_with_trailing_slash PASSED
# tests/test_gradio_integration.py::TestGradioMounting::test_gradio_content_exists PASSED
# tests/test_gradio_integration.py::TestGradioFunctionality::test_gradio_can_access_data PASSED
# tests/test_gradio_integration.py::TestGradioAPIIntegration::test_gradio_backend_uses_same_data PASSED
# tests/test_gradio_integration.py::TestGradioAPIIntegration::test_gradio_forecast_uses_same_logic PASSED
# tests/test_gradio_integration.py::TestGradioEndpointListing::test_root_endpoint_lists_gradio PASSED
# tests/test_gradio_integration.py::TestGradioEndpointListing::test_root_endpoint_usage_includes_gradio PASSED
# tests/test_gradio_integration.py::TestGradioErrorHandling::test_gradio_accessible_even_if_data_not_loaded PASSED
# tests/test_gradio_integration.py::TestGradioPerformance::test_gradio_page_load_time PASSED
#
# ========== 10 passed in X.XXs ==========
```

#### Step 4: Run Full Test Suite (5 min)

```bash
# Run ALL tests (Phase 1 + Phase 2 + Phase 3)
pytest tests/ -v

# Should see:
# tests/test_preprocessing.py .................... [ XX%]
# tests/test_forecasting.py ...................... [ XX%]
# tests/test_logic.py ............................ [ XX%]
# tests/test_api.py .............................. [ XX%]
# tests/test_mcp.py .............................. [ XX%]
# tests/test_gradio_integration.py ............... [100%]
#
# ========== XX passed in X.XXs ==========
```

**Target:** All tests passing (37+ tests total)

**Acceptance Criteria:**
- [ ] Test file created at tests/test_gradio_integration.py
- [ ] 10+ integration tests written
- [ ] Tests cover endpoint accessibility
- [ ] Tests cover data consistency
- [ ] Tests cover error handling
- [ ] Tests cover performance
- [ ] All Gradio tests pass
- [ ] Full test suite still passes
- [ ] No regressions from Phase 1 or Phase 2

---

## Testing Strategy

### Test Pyramid for Phase 3

```
       /\
      /  \     E2E Tests (Manual)
     /____\    - Browser testing
    /      \   - Cross-interface testing
   /        \  
  /__________\ Integration Tests (Automated)
 /            \ - test_gradio_integration.py
/              \ - test_api.py (updated)
/________________\ Unit Tests (Existing)
                   - test_logic.py
                   - test_preprocessing.py
                   - test_forecasting.py
```

### Automated Tests

**Unit Tests (From Phase 1):**
- Business logic validation
- Data preprocessing
- Forecasting algorithms

**Integration Tests (Phase 2 + Phase 3):**
- REST API endpoints
- MCP tools functionality
- Gradio UI mounting
- Cross-component data consistency

**Total Coverage Target:** >90%

### Manual Testing Checklist

**Before Each Commit:**
- [ ] Server starts without errors
- [ ] All three interfaces accessible
- [ ] No console errors in browser

**Before Pull Request:**
- [ ] All automated tests pass
- [ ] Manual test all three interfaces
- [ ] Cross-interface testing complete
- [ ] Performance acceptable
- [ ] Documentation updated

**Before Production:**
- [ ] Full regression test suite
- [ ] Load testing
- [ ] Security review
- [ ] Deployment dry-run

---

## Troubleshooting

### Common Issues

#### Issue 1: Gradio Won't Mount

**Symptoms:**
- Error: "Could not import Gradio"
- Error: "Failed to mount Gradio UI"

**Solutions:**
```bash
# Check Gradio installed
pip list | grep gradio

# Reinstall if needed
pip install --upgrade gradio>=4.0.0

# Check import works
python -c "import gradio; print(gradio.__version__)"
```

#### Issue 2: Gradio UI Blank or Not Loading

**Symptoms:**
- /gradio shows blank page
- JavaScript errors in console

**Solutions:**
```bash
# Check PROCESSED_DF loaded
python -c "from src.expo_smooth_mcp.main import PROCESSED_DF; print('Loaded' if PROCESSED_DF is not None else 'Not loaded')"

# Check SKU list populated
python -c "from app import SKU_LIST; print(f'SKUs: {len(SKU_LIST)}')"

# Check browser console (F12) for specific errors
```

#### Issue 3: "Cannot connect to API" Error

**Symptoms:**
- Gradio shows error: "Cannot connect to API at http://localhost:8000"
- Forecast generation fails

**Solutions:**
```bash
# Verify FastAPI server running
curl http://localhost:8000/health

# Check API_BASE_URL in app.py
grep "API_BASE_URL" app.py

# When mounted, should use same origin
# In main.py, verify os.environ["API_BASE_URL"] is set before importing app
```

#### Issue 4: CORS Errors

**Symptoms:**
- Browser console: "CORS policy blocked"
- Network requests fail

**Solutions:**
```bash
# For mounted Gradio (same origin), CORS should NOT be needed
# If you see CORS errors, check:

# 1. Verify Gradio is mounted (not running separately)
curl http://localhost:8000/ | jq '.endpoints.gradio_ui'

# 2. Check browser is accessing via same origin
# Should use: http://localhost:8000/gradio
# Not: http://localhost:7860

# 3. If still needed, add CORS middleware (see TASK-305)
```

#### Issue 5: Import Errors

**Symptoms:**
- "ModuleNotFoundError: No module named 'app'"
- "ImportError: cannot import name 'demo'"

**Solutions:**
```bash
# Verify app.py exists in project root
ls -la app.py

# Verify app.py exports 'demo'
grep "demo =" app.py

# Verify app.py doesn't auto-launch when imported
grep "if __name__" app.py

# Run from correct directory
cd /Users/max/Documents/code/expo-smooth-mcp
python -m src.expo_smooth_mcp.main --transport http
```

#### Issue 6: Performance Issues

**Symptoms:**
- Slow plot generation
- UI feels laggy

**Solutions:**
```bash
# Check data size
python -c "from src.expo_smooth_mcp.main import PROCESSED_DF; print(f'Rows: {len(PROCESSED_DF)}')"

# Profile forecast generation
python -m cProfile -s time -m src.expo_smooth_mcp.main --transport http

# Consider adding caching for repeated requests
# (future enhancement)
```

### Debug Mode

Enable detailed logging:

```python
# In main.py, add at top
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export LOG_LEVEL=DEBUG
python -m src.expo_smooth_mcp.main --transport http
```

---

## Success Criteria

### Phase 3 Complete When:

**Functionality:**
- [ ] Gradio UI mounted at /gradio
- [ ] All three interfaces work (REST, MCP, Gradio)
- [ ] Can generate forecasts through Gradio
- [ ] Forecasts match REST API results
- [ ] Error handling works across interfaces

**Testing:**
- [ ] 10+ new integration tests pass
- [ ] Full test suite passes (37+ tests)
- [ ] Manual testing complete
- [ ] Cross-interface testing complete
- [ ] Performance acceptable

**Documentation:**
- [ ] README updated with /gradio endpoint
- [ ] API docs show Gradio UI
- [ ] Troubleshooting guide complete
- [ ] Phase 3 code review created

**Quality:**
- [ ] No console errors
- [ ] No CORS issues
- [ ] No performance degradation
- [ ] Clean code (linted, formatted)
- [ ] Ready for Phase 4 (deployment)

### Metrics to Track

| Metric | Target | Actual |
|--------|--------|--------|
| Total Tests | 37+ | _____ |
| Test Pass Rate | 100% | _____ |
| Gradio Load Time | < 2s | _____ |
| Forecast Time | < 2s | _____ |
| Code Coverage | > 90% | _____ |

---

## Next Steps

After Phase 3 completion:

**Phase 4A: Docker MCP Toolkit Deployment**
- Containerize the application
- Deploy to Docker MCP Toolkit
- Configure for production

**Phase 4B: Cloud Deployment**
- Deploy to Fly.io or similar
- Configure environment variables
- Set up monitoring

**Future Enhancements:**
- Add authentication/authorization
- Implement caching for performance
- Add more forecasting models
- Create admin dashboard
- Add usage analytics

---

**Phase 3 Implementation Guide Complete**  
**Ready to Begin Implementation**  
**Estimated Total Time: ~7 hours**
