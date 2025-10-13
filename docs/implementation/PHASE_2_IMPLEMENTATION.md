# Phase 2: Build FastMCP Backend - Implementation Guide

**Duration:** ~20 hours (12 tasks)  
**Status:** ⏳ Ready to Start  
**Complexity:** Medium

---

## Overview

This phase builds the production-grade FastMCP + FastAPI backend that serves as the primary interface for the forecasting service. We migrate from the Gradio prototype to a professional MCP server supporting multiple transport modes (stdio and HTTP/SSE) while maintaining backward compatibility.

### Goals
- ✅ Create production FastMCP server with dual-transport support
- ✅ Implement two MCP tools: `forecast_sku` and `list_available_skus`
- ✅ Build REST API endpoints for non-MCP clients
- ✅ Enable HTTP/SSE transport for remote MCP clients
- ✅ Maintain backward compatibility with Gradio UI
- ✅ Achieve comprehensive test coverage for MCP functionality

### Prerequisites
- ✅ Phase 1 completed: `logic.py` module implemented and tested
- ✅ Business logic fully decoupled from UI
- ✅ Test suite passing with >90% coverage
- ✅ Python environment configured with conda/venv

### Deliverables
1. `src/expo_smooth_mcp/main.py` - FastMCP + FastAPI production server
2. REST API endpoints with OpenAPI documentation
3. Dual-transport support (stdio for local, HTTP/SSE for remote)
4. `tests/test_mcp.py` - MCP tool test suite
5. `tests/test_api.py` - REST API test suite
6. Updated `requirements.txt` with FastMCP dependencies

---

## Architecture Overview

### Before Phase 2 (Gradio Only)
```
User → Gradio UI → Business Logic → Forecasting Engine
```

### After Phase 2 (Multi-Interface)
```
                    ┌─────────────────┐
                    │   FastAPI App   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐        ┌─────▼──────┐      ┌─────▼─────┐
   │   MCP   │        │  REST API  │      │  Gradio   │
   │  Tools  │        │ Endpoints  │      │    UI     │
   └────┬────┘        └─────┬──────┘      └─────┬─────┘
        │                   │                    │
        └───────────────────┼────────────────────┘
                            │
                    ┌───────▼────────┐
                    │  Business      │
                    │  Logic Layer   │
                    │  (logic.py)    │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  Forecasting   │
                    │  Engine        │
                    └────────────────┘
```

### Key Components

#### 1. FastMCP Server
- **Purpose:** MCP protocol implementation
- **Tools:** `forecast_sku`, `list_available_skus`
- **Transport:** stdio (local) and HTTP/SSE (remote)

#### 2. FastAPI Application
- **Purpose:** HTTP server and routing
- **Endpoints:** Root, health, API, docs
- **Mounting:** MCP server at `/mcp`

#### 3. Business Logic Layer
- **Purpose:** Framework-agnostic forecasting logic
- **Module:** `src/expo_smooth_mcp/logic.py`
- **Reuse:** Shared by all interfaces

---

## Tasks

### TASK-201: Install FastMCP and FastAPI dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:** 
Install FastMCP 2.0 and FastAPI framework dependencies required for building the production MCP server. Use `uv` package manager for fast, deterministic dependency resolution.

**Implementation Steps:**
1. Install uv package manager (if not already installed)
2. Add required packages using uv
3. Verify installations
4. Update requirements.txt

**Required Packages:**
```bash
# Core framework packages
uv add fastapi        # Modern web framework (ASGI)
uv add fastmcp        # FastMCP 2.0 for MCP protocol
uv add uvicorn[standard]  # ASGI server with websocket support
uv add python-multipart   # For form data parsing

# Additional dependencies
uv add httpx          # For testing and API calls
uv add pydantic       # Data validation
```

**Installation Commands:**
```bash
# Option 1: Using uv (recommended - 10-100x faster)
uv add fastapi fastmcp "uvicorn[standard]" python-multipart httpx

# Option 2: Using pip (fallback)
pip install fastapi fastmcp "uvicorn[standard]" python-multipart httpx

# Option 3: Using conda
conda install -c conda-forge fastapi uvicorn httpx
pip install fastmcp python-multipart  # Not in conda

# Verify installation
python -c "import fastapi, fastmcp, uvicorn; print('✓ All imports successful')"
```

**Version Requirements:**
```txt
# Add to requirements.txt
fastapi>=0.104.0
fastmcp>=2.0.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
httpx>=0.25.0
pydantic>=2.5.0
```

**Testing Installation:**
```python
# Quick import test
python -c "
from fastapi import FastAPI
from fastmcp import FastMCP
from uvicorn import Config
import httpx

app = FastAPI()
mcp = FastMCP()

print('✓ FastAPI version:', fastapi.__version__)
print('✓ FastMCP imported successfully')
print('✓ Uvicorn imported successfully')
print('✓ All dependencies ready')
"
```

**Acceptance Criteria:**
- [ ] All packages installed without errors
- [ ] Import test passes successfully
- [ ] requirements.txt updated with versions
- [ ] No dependency conflicts
- [ ] Installation works in clean virtual environment
- [ ] Both pip and uv methods documented

---

### TASK-202: Create main.py skeleton structure
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-201

**Description:** 
Create the foundational `main.py` file that serves as the entry point for the FastMCP + FastAPI production server. This file will eventually replace `app.py` as the primary application interface.

**Implementation Steps:**
1. Create file: `src/expo_smooth_mcp/main.py`
2. Add comprehensive module docstring
3. Import required dependencies
4. Initialize FastAPI application
5. Initialize FastMCP server
6. Add section markers for future code

**File Structure:**
```python
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
```

**Configuration Values:**
- **APP_VERSION**: "2.0.0" (major version for MCP migration)
- **APP_NAME**: "Expo Smooth MCP Server"
- **MCP name**: "expo-smooth-forecast"
- **Default port**: 8000

**Design Decisions:**
- Single file for now (not split into modules yet)
- Clear section markers with comments
- Startup event for initialization
- Dual-transport support in main block

**Testing:**
```bash
# Test file can be imported
python -c "from src.expo_smooth_mcp import main; print('✓ Import successful')"

# Test file can run (does nothing yet)
python -m src.expo_smooth_mcp.main
# Press Ctrl+C to stop

# Expected output:
# Starting Expo Smooth MCP Server v2.0.0
# INFO: Started server process [12345]
# INFO: Waiting for application startup.
# INFO: Application startup complete.
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**Acceptance Criteria:**
- [ ] File `src/expo_smooth_mcp/main.py` created
- [ ] Comprehensive module docstring with examples
- [ ] FastAPI app initialized with title and version
- [ ] FastMCP server initialized with name
- [ ] Section markers for future code
- [ ] Startup event handler defined
- [ ] Main entry point with uvicorn.run()
- [ ] File imports without errors
- [ ] Server starts and stops cleanly

---

### TASK-203: Implement data loading in main.py
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-202, TASK-106

**Description:** 
Integrate data loading into the FastAPI application using the singleton pattern from `logic.get_processed_data()`. This ensures the dataset is loaded once during application startup and available to all endpoints.

**Implementation Steps:**
1. Update global variable declaration
2. Implement data loading in startup event
3. Add error handling for missing file
4. Add logging for successful load
5. Handle graceful degradation

**Code Implementation:**
```python
# --- Startup Event ---
# Replace existing startup_event function

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
```

**Error Handling Strategy:**
- **FileNotFoundError**: Log error but don't crash (debugging)
- **Other exceptions**: Log error but continue (graceful degradation)
- **Server starts**: Even if data fails, health endpoint works

**Expected Output:**
```bash
# Success case
Starting Expo Smooth MCP Server v2.0.0
Successfully loaded and cached data from FMCG_Sales.csv
✓ Data loaded successfully
✓ Found 43 unique SKUs
✓ Ready to serve requests

# Failure case
Starting Expo Smooth MCP Server v2.0.0
✗ ERROR: Data file not found: FMCG_Sales.csv
✗ Server will start but forecast endpoints will fail
```

**Testing:**
```bash
# Test with data file present
python -m src.expo_smooth_mcp.main
# Should see success message

# Test without data file (simulate failure)
mv FMCG_Sales.csv FMCG_Sales.csv.bak
python -m src.expo_smooth_mcp.main
# Should see error but server still starts

# Restore data file
mv FMCG_Sales.csv.bak FMCG_Sales.csv
```

**Acceptance Criteria:**
- [ ] Global `PROCESSED_DF` variable declared
- [ ] `logic.get_processed_data()` called in startup
- [ ] Success message logs SKU count
- [ ] FileNotFoundError handled gracefully
- [ ] Generic exceptions handled gracefully
- [ ] Server starts even if data load fails
- [ ] Startup logs are clear and informative
- [ ] Data accessible via global variable

---

### TASK-204: Create forecast_sku MCP tool
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-203

**Description:** 
Implement the primary MCP tool for generating forecasts. This tool will be discoverable by MCP clients (Claude Desktop, Cursor, VS Code) and serves as the main forecasting interface.

**Implementation Steps:**
1. Define tool function with `@mcp.tool()` decorator
2. Add comprehensive docstring (visible to MCP clients)
3. Implement type hints for all parameters
4. Validate inputs using `logic.validate_forecast_request()`
5. Call `logic.get_forecast_data()` to generate forecast
6. Return structured dictionary
7. Handle errors with user-friendly messages

**Code Implementation:**
```python
# --- MCP Tools ---
# Add after "# --- MCP Tools ---" section

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
        logic.validate_forecast_request(PROCESSED_DF, sku, forecast_horizon)
        
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
```

**MCP Tool Best Practices:**
- **Comprehensive docstring**: MCP clients display this to users
- **Type hints**: Enable IDE autocomplete
- **Default values**: Common usage is simple (90 days)
- **Clear errors**: Help users fix problems
- **Async function**: Enable concurrent requests

**Client Experience in Claude Desktop:**
```
User: "Can you forecast sales for PRODUCT_123?"

Claude sees available tool:
┌───────────────────────────────────────┐
│ Tool: forecast_sku                    │
│ Generate sales forecast for product   │
│                                       │
│ Parameters:                           │
│ • sku (required): Product SKU         │
│ • forecast_horizon (optional): Days   │
└───────────────────────────────────────┘

Claude calls: forecast_sku("PRODUCT_123", 90)
```

**Testing:**
```python
# Test with Python
import asyncio
from src.expo_smooth_mcp.main import forecast_sku, PROCESSED_DF

# Manual test
result = asyncio.run(forecast_sku("PRODUCT_001", 90))
print(result.keys())  # Should show: dates, actuals, forecast, metadata
print(f"Forecast points: {len(result['forecast'])}")

# Test with MCP Inspector
# In terminal:
# npx @modelcontextprotocol/inspector uvicorn main:app
```

**Acceptance Criteria:**
- [ ] Function decorated with `@mcp.tool()`
- [ ] Comprehensive docstring (>10 lines)
- [ ] Type hints for parameters and return
- [ ] Default value for forecast_horizon (90)
- [ ] Validates inputs before processing
- [ ] Returns dict with all four keys
- [ ] Handles data-not-loaded case
- [ ] Catches and re-raises exceptions
- [ ] Function is async
- [ ] Tool appears in MCP Inspector

---

### TASK-205: Create list_available_skus MCP tool
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-203

**Description:** 
Implement a discovery MCP tool that returns all available product SKUs. This allows MCP clients to discover what products can be forecasted.

**Implementation Steps:**
1. Define tool function with `@mcp.tool()` decorator
2. Add clear docstring for MCP clients
3. Call `logic.get_available_skus()`
4. Return list of SKU strings
5. Handle data-not-loaded case

**Code Implementation:**
```python
# Add after forecast_sku tool

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
        
        # Forecast the first product
        first_sku = skus[0]
        forecast = await forecast_sku(first_sku, 90)
    
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
```

**Tool Behavior:**
- **Input:** None (no parameters)
- **Output:** List of strings
- **Use case:** Called before `forecast_sku` to discover products

**Client Experience:**
```
User: "What products can you forecast?"

Claude calls: list_available_skus()

Claude responds:
"I can forecast sales for 43 products including:
 • PRODUCT_001
 • PRODUCT_002
 • PRODUCT_123
 ... (and 40 more)"
```

**Testing:**
```python
# Test in Python
import asyncio
from src.expo_smooth_mcp.main import list_available_skus

skus = asyncio.run(list_available_skus())
assert isinstance(skus, list)
assert len(skus) > 0
assert all(isinstance(sku, str) for sku in skus)
print(f"✓ Found {len(skus)} SKUs")
```

**Acceptance Criteria:**
- [ ] Function decorated with `@mcp.tool()`
- [ ] Clear docstring explaining purpose
- [ ] Returns List[str] type
- [ ] Function is async
- [ ] Handles data-not-loaded case
- [ ] Calls `logic.get_available_skus()`
- [ ] Returns sorted list
- [ ] Tool appears in MCP Inspector
- [ ] Exception handling for errors

---

### TASK-206: Mount FastMCP server to FastAPI
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-204, TASK-205

**Description:** 
Mount the FastMCP server as a sub-application within FastAPI, exposing MCP tools at the `/mcp` endpoint for HTTP/SSE transport.

**Implementation Steps:**
1. Add mount statement after tool definitions
2. Configure SSE transport
3. Add confirmation log message
4. Verify endpoint appears in routes

**Code Implementation:**
```python
# --- Mount MCP Server ---
# Add after "# --- Mount MCP Server ---" section

# Mount MCP server as ASGI sub-application at /mcp endpoint
# This exposes MCP tools via HTTP/SSE transport for remote clients
# Local stdio transport is handled separately in main block
app.mount("/mcp", mcp.as_asgi(transport="sse"))

print(f"✓ Mounted MCP server at /mcp with SSE transport")
```

**Endpoint Structure After Mounting:**
```
FastAPI Application (/)
├── GET  /               (root endpoint)
├── GET  /health         (health check)
├── GET  /docs           (OpenAPI docs)
├── POST /api/forecast   (REST API)
└── /mcp                 (MCP sub-app)
    ├── POST /mcp/messages
    ├── GET  /mcp/sse
    └── Tools:
        • forecast_sku
        • list_available_skus
```

**Testing:**
```bash
# Start server
uvicorn src.expo_smooth_mcp.main:app --reload

# Check routes exist
curl http://localhost:8000/openapi.json | jq '.paths | keys'

# Test with MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
# Should show both tools discoverable
```

**Acceptance Criteria:**
- [ ] `app.mount()` statement added after tools
- [ ] Mounted at `/mcp` path
- [ ] Transport set to "sse"
- [ ] Confirmation message printed
- [ ] Server starts without errors
- [ ] `/mcp` endpoint responds (not 404)
- [ ] MCP Inspector connects successfully
- [ ] Both tools discoverable

---

### TASK-207: Create root endpoint
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-202

**Description:** 
Create a welcoming root endpoint providing service information and API documentation. This serves as the entry point for users discovering the service.

**Implementation Steps:**
1. Create GET endpoint at "/"
2. Return structured JSON with metadata
3. Include links to documentation
4. Add version information
5. Show data status

**Code Implementation:**
```python
# --- REST API Endpoints ---
# Add after "# --- REST API Endpoints ---" section

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
```

**Response Example:**
```json
{
  "name": "Expo Smooth MCP Server",
  "version": "2.0.0",
  "status": "operational",
  "endpoints": {...},
  "usage": {...},
  "data_status": "loaded",
  "sku_count": 43
}
```

**Testing:**
```bash
# Test endpoint
curl http://localhost:8000/ | jq

# Verify fields
curl http://localhost:8000/ | jq '.version'
curl http://localhost:8000/ | jq '.sku_count'

# Test in browser
open http://localhost:8000/
```

**Acceptance Criteria:**
- [ ] Endpoint registered at "/" path
- [ ] Returns JSON response
- [ ] Includes name, version, description
- [ ] Lists all endpoints with descriptions
- [ ] Shows data_status
- [ ] Shows sku_count when loaded
- [ ] Valid JSON format
- [ ] Accessible without authentication
- [ ] Documented in OpenAPI

---

### TASK-208: Create health check endpoint
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-203

**Description:** 
Implement health check endpoint for monitoring, load balancers, and container orchestration. Returns appropriate status codes based on service health.

**Implementation Steps:**
1. Create GET endpoint at "/health"
2. Check data loaded status
3. Return appropriate HTTP status codes
4. Include diagnostic information
5. Follow health check best practices

**Code Implementation:**
```python
# Add after root endpoint

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns 200 OK if service is healthy (data loaded successfully).
    Returns 503 Service Unavailable if data failed to load.
    
    Used by:
    - Docker HEALTHCHECK
    - Fly.io health checks
    - Kubernetes liveness/readiness probes
    - Monitoring systems
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "reason": "Data not loaded",
                "details": "FMCG_Sales.csv failed to load on startup",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    try:
        # Additional health checks
        sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        return {
            "status": "healthy",
            "version": APP_VERSION,
            "data_loaded": True,
            "sku_count": sku_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "reason": "Health check failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

**Health Check Standards:**
- **200 OK**: Service healthy and ready
- **503 Service Unavailable**: Service running but not ready
- Always return JSON
- Include timestamp
- Include diagnostic info

**Integration Examples:**

**Docker:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Kubernetes:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
```

**Testing:**
```bash
# Test healthy state
curl -i http://localhost:8000/health
# Expected: HTTP/1.1 200 OK

# Test response format
curl http://localhost:8000/health | jq '.status'
# Expected: "healthy"
```

**Acceptance Criteria:**
- [ ] Endpoint at "/health"
- [ ] Returns 200 when data loaded
- [ ] Returns 503 when data not loaded
- [ ] Valid JSON in both cases
- [ ] Includes status field
- [ ] Includes timestamp (ISO format)
- [ ] Includes sku_count when healthy
- [ ] Never raises unhandled exceptions
- [ ] Works with Docker HEALTHCHECK

---

### TASK-209: Implement dual-transport entrypoint
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-206

**Description:** 
Implement command-line argument parsing to enable both stdio (local) and HTTP/SSE (production) transports from a single codebase.

**Implementation Steps:**
1. Add argparse for CLI
2. Implement stdio mode handler
3. Implement HTTP mode handler
4. Add usage documentation
5. Test both modes

**Code Implementation:**
```python
# --- Main Entry Point ---
# Replace existing if __name__ == "__main__" block

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} - Dual-transport MCP server"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="http",
        help="Transport mode: stdio for local, http for remote (default: http)"
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
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        # --- stdio Transport (Local Development) ---
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
        asyncio.run(mcp.run_stdio())
        
    else:
        # --- HTTP Transport (Production) ---
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
```

**Usage Examples:**
```bash
# Local Development (stdio)
python -m src.expo_smooth_mcp.main --transport stdio

# Production HTTP
python -m src.expo_smooth_mcp.main --transport http

# Custom port
python -m src.expo_smooth_mcp.main --transport http --port 3000

# Development with auto-reload
python -m src.expo_smooth_mcp.main --transport http --reload
```

**Claude Desktop Configuration:**
```json
{
  "mcpServers": {
    "expo-smooth": {
      "command": "python",
      "args": [
        "-m",
        "src.expo_smooth_mcp.main",
        "--transport",
        "stdio"
      ],
      "cwd": "/path/to/expo-smooth-mcp"
    }
  }
}
```

**Testing Both Modes:**
```bash
# Test stdio
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | \
  python -m src.expo_smooth_mcp.main --transport stdio

# Test HTTP
python -m src.expo_smooth_mcp.main --transport http --port 8000
curl http://localhost:8000/health
```

**Acceptance Criteria:**
- [ ] argparse configured with 4 arguments
- [ ] stdio mode handler implemented
- [ ] HTTP mode handler implemented
- [ ] stdio logs to stderr
- [ ] Default transport is "http"
- [ ] --reload works in HTTP mode
- [ ] Both modes start successfully
- [ ] stdio works with Claude Desktop
- [ ] HTTP serves all endpoints
- [ ] Help text: `--help`

---

### TASK-210: Create REST API forecast endpoint
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-204

**Description:** 
Create REST API endpoint for forecasting non-MCP clients (cURL, Postman, web apps). Provides same functionality as MCP tool via standard HTTP POST.

**Implementation Steps:**
1. Define Pydantic request/response models
2. Implement POST endpoint at /api/forecast
3. Add validation and error handling
4. Add OpenAPI documentation
5. Test with cURL

**Pydantic Models:**
```python
# Add after imports

from pydantic import BaseModel, Field

class ForecastRequest(BaseModel):
    """Request model for forecast API."""
    sku: str = Field(
        ...,
        description="Product SKU code",
        example="PRODUCT_123"
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
```

**Endpoint Implementation:**
```python
# Add after health endpoint

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
        # Validate and generate forecast
        logic.validate_forecast_request(
            PROCESSED_DF,
            request.sku,
            request.forecast_horizon
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
```

**Testing:**
```bash
# Test with cURL
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' \
  | jq

# Test OpenAPI docs
open http://localhost:8000/docs
```

**Acceptance Criteria:**
- [ ] Pydantic models defined
- [ ] POST endpoint at /api/forecast
- [ ] Validates request body
- [ ] Returns ForecastResponse model
- [ ] HTTP 400 for validation errors
- [ ] HTTP 503 if data not loaded
- [ ] Documented in OpenAPI
- [ ] Works with cURL

---

### TASK-211: Create unit tests for MCP tools
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-204, TASK-205

**Description:** 
Create comprehensive test suite for MCP tools to ensure they work correctly in isolation.

**Implementation Steps:**
1. Create `tests/test_mcp.py`
2. Set up test fixtures
3. Write tests for both MCP tools
4. Test error cases
5. Use pytest-asyncio

**Test File Structure:**
```python
# tests/test_mcp.py
import pytest
import pytest_asyncio
from src.expo_smooth_mcp import main

@pytest.fixture
def setup_data():
    """Ensure data is loaded before tests."""
    main.PROCESSED_DF = main.logic.get_processed_data()
    yield
    # Cleanup if needed

@pytest.mark.asyncio
class TestForecastSkuTool:
    """Tests for forecast_sku MCP tool."""
    
    async def test_valid_forecast(self, setup_data):
        """Should generate forecast for valid SKU."""
        result = await main.forecast_sku("PRODUCT_001", 90)
        assert "dates" in result
        assert "actuals" in result
        assert "forecast" in result
        assert "metadata" in result
    
    async def test_invalid_sku_raises_error(self, setup_data):
        """Should raise ValueError for invalid SKU."""
        with pytest.raises(ValueError, match="not found"):
            await main.forecast_sku("INVALID", 90)
    
    async def test_invalid_horizon_raises_error(self, setup_data):
        """Should raise ValueError for out-of-range horizon."""
        with pytest.raises(ValueError, match="between 1 and 365"):
            await main.forecast_sku("PRODUCT_001", 500)
    
    async def test_data_not_loaded_raises_error(self):
        """Should raise RuntimeError if data not loaded."""
        main.PROCESSED_DF = None
        with pytest.raises(RuntimeError, match="Data not loaded"):
            await main.forecast_sku("PRODUCT_001", 90)

@pytest.mark.asyncio
class TestListAvailableSkusTool:
    """Tests for list_available_skus MCP tool."""
    
    async def test_returns_list_of_skus(self, setup_data):
        """Should return sorted list of SKUs."""
        result = await main.list_available_skus()
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(sku, str) for sku in result)
    
    async def test_data_not_loaded_raises_error(self):
        """Should raise RuntimeError if data not loaded."""
        main.PROCESSED_DF = None
        with pytest.raises(RuntimeError):
            await main.list_available_skus()
```

**Run Tests:**
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Run MCP tests
pytest tests/test_mcp.py -v
```

**Acceptance Criteria:**
- [ ] File `tests/test_mcp.py` created
- [ ] Tests for both MCP tools
- [ ] Tests happy paths
- [ ] Tests error cases
- [ ] Uses pytest-asyncio
- [ ] All tests pass
- [ ] >90% coverage for MCP tools

---

### TASK-212: Create integration tests for FastAPI
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-207, TASK-208, TASK-210

**Description:** 
Create integration tests for FastAPI endpoints using TestClient.

**Implementation Steps:**
1. Create `tests/test_api.py`
2. Use FastAPI TestClient
3. Test all REST endpoints
4. Test OpenAPI docs
5. Test error cases

**Test File:**
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.expo_smooth_mcp.main import app

client = TestClient(app)

class TestRootEndpoint:
    """Tests for / endpoint."""
    
    def test_root_returns_service_info(self):
        """Should return service metadata."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Expo Smooth MCP Server"
        assert data["version"] == "2.0.0"
        assert "endpoints" in data

class TestHealthEndpoint:
    """Tests for /health endpoint."""
    
    def test_health_when_data_loaded(self):
        """Should return 200 when healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "sku_count" in data

class TestForecastAPI:
    """Tests for /api/forecast endpoint."""
    
    def test_forecast_with_valid_request(self):
        """Should return forecast for valid request."""
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 90}
        )
        assert response.status_code == 200
        data = response.json()
        assert "dates" in data
        assert "forecast" in data
    
    def test_forecast_with_invalid_sku(self):
        """Should return 400 for invalid SKU."""
        response = client.post(
            "/api/forecast",
            json={"sku": "INVALID", "forecast_horizon": 90}
        )
        assert response.status_code == 400
    
    def test_forecast_with_invalid_horizon(self):
        """Should return 400 for invalid horizon."""
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 500}
        )
        assert response.status_code == 400
```

**Run Tests:**
```bash
pytest tests/test_api.py -v
```

**Acceptance Criteria:**
- [ ] File `tests/test_api.py` created
- [ ] Tests for all REST endpoints
- [ ] Uses FastAPI TestClient
- [ ] Tests happy paths
- [ ] Tests error cases
- [ ] All tests pass
- [ ] >90% coverage for API endpoints

---

## Phase 2 Summary

### Completion Checklist

**Code Deliverables:**
- [ ] `src/expo_smooth_mcp/main.py` - Complete FastMCP server
- [ ] Two MCP tools implemented and tested
- [ ] Four REST API endpoints functional
- [ ] Dual-transport support (stdio + HTTP/SSE)
- [ ] `tests/test_mcp.py` - MCP tool tests
- [ ] `tests/test_api.py` - API integration tests

**Functionality Verification:**
- [ ] Server starts in both stdio and HTTP modes
- [ ] MCP tools discoverable by clients
- [ ] REST API endpoints accessible
- [ ] Health check returns correct status
- [ ] OpenAPI documentation generated
- [ ] All tests passing

**Quality Gates:**
- [ ] All tests pass (>30 total)
- [ ] Coverage >90% for new code
- [ ] No linting errors
- [ ] Type checking passes
- [ ] MCP Inspector shows both tools
- [ ] cURL tests successful

**Documentation:**
- [ ] Module docstrings complete
- [ ] Function docstrings complete
- [ ] OpenAPI auto-generated
- [ ] README updated with new usage
- [ ] Claude Desktop config example

---

## Testing Guide

### Manual Testing Steps

1. **Test stdio mode:**
   ```bash
   python -m src.expo_smooth_mcp.main --transport stdio
   # Should start and wait for input
   ```

2. **Test HTTP mode:**
   ```bash
   python -m src.expo_smooth_mcp.main --transport http
   # Open browser: http://localhost:8000
   ```

3. **Test MCP tools:**
   ```bash
   npx @modelcontextprotocol/inspector \
     python -m src.expo_smooth_mcp.main --transport stdio
   ```

4. **Test REST API:**
   ```bash
   curl http://localhost:8000/
   curl http://localhost:8000/health
   curl -X POST http://localhost:8000/api/forecast \
     -H "Content-Type: application/json" \
     -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}'
   ```

5. **Test OpenAPI docs:**
   ```bash
   open http://localhost:8000/docs
   ```

---

## Troubleshooting

### Issue: Import errors for FastMCP
**Solution:**
```bash
pip install fastmcp>=2.0.0
python -c "import fastmcp; print('OK')"
```

### Issue: MCP tools not appearing
**Solution:**
Check mount is after tool definitions:
```python
# Tools first
@mcp.tool()
async def forecast_sku(...): pass

# Then mount
app.mount("/mcp", mcp.as_asgi())
```

### Issue: stdio mode hangs
**Solution:**
This is normal - stdio waits for input. Test with:
```bash
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | \
  python -m src.expo_smooth_mcp.main --transport stdio
```

---

## Next Steps

After completing Phase 2:
1. Verify all acceptance criteria met
2. Run full test suite
3. Test with real MCP clients (Claude Desktop)
4. Commit changes with detailed message
5. Proceed to Phase 3: Integration & Deployment

---

**Reference:** See [SPECIFICATION.md](../SPECIFICATION.md) for complete technical details.
