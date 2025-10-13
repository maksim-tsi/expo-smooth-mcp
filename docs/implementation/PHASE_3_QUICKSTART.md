# Phase 3: Mount Gradio UI - Quick Reference

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** Phase 3 - Mount Gradio UI  
**Quick Start Guide**

---

## Overview

Mount Gradio web UI into FastAPI app to create unified service with **three interfaces**:
- REST API (existing)
- MCP Tools (existing)  
- Gradio UI (NEW - mounted at `/gradio`)

**Time:** ~7 hours | **Tasks:** 6

---

## Prerequisites

✅ Phase 2 complete (FastMCP + FastAPI backend)  
✅ All dependencies installed  
✅ 27/27 tests passing  
✅ Server runs successfully

---

## Task Summary

| Task | Description | Time | Key Actions |
|------|-------------|------|-------------|
| **301** | Verify Pydantic models | 0.5h | Check models exist, test validation |
| **302** | Refactor Gradio → API | 2h | Update app.py to use httpx, call REST API |
| **303** | Mount Gradio in FastAPI | 1h | Add gr.mount_gradio_app() in main.py |
| **304** | Test unified service | 1.5h | Test all 3 interfaces together |
| **305** | Handle CORS (optional) | 0.5h | Add CORS middleware if needed |
| **306** | Integration tests | 1.5h | Create test_gradio_integration.py |

---

## Quick Implementation

### TASK-301: Verify Models (30 min)

```bash
# Check models exist
grep "class ForecastRequest" src/expo_smooth_mcp/main.py
grep "class ForecastResponse" src/expo_smooth_mcp/main.py

# Test models
python -c "from src.expo_smooth_mcp.main import ForecastRequest; r = ForecastRequest(sku='TEST', forecast_horizon=90); print('✓ Models OK')"
```

**Expected:** Models exist with proper validation

---

### TASK-302: Refactor Gradio (2 hours)

**Backup first:**
```bash
cp app.py app.py.backup
```

**Key Changes to app.py:**

1. **Add imports:**
```python
import httpx
import os
import asyncio
```

2. **Add configuration:**
```python
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

3. **Refactor main function:**
```python
async def create_forecast_plot(sku: str) -> go.Figure:
    """Call FastAPI backend via HTTP."""
    if not sku:
        return _create_empty_plot("Please select a product SKU")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/api/forecast",
                json={"sku": sku, "forecast_horizon": 90}
            )
            response.raise_for_status()
            forecast_data = response.json()
            return _create_forecast_plot_from_data(forecast_data)
    
    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get("detail", str(e))
        return _create_error_plot(f"API Error: {error_detail}")
    
    except httpx.RequestError as e:
        return _create_error_plot(f"Cannot connect to API at {API_BASE_URL}")
    
    except Exception as e:
        return _create_error_plot(f"Error: {str(e)}")
```

4. **Add helper functions:**
```python
def _create_empty_plot(message: str) -> go.Figure:
    # Create empty Plotly figure

def _create_error_plot(error_message: str) -> go.Figure:
    # Create error Plotly figure

def _create_forecast_plot_from_data(forecast_data: dict) -> go.Figure:
    # Create forecast plot from API response data
```

5. **Ensure proper export:**
```python
demo = gr.Interface(
    fn=create_forecast_plot,
    inputs=[gr.Dropdown(choices=SKU_LIST, ...)],
    outputs=[gr.Plot(...)],
    # ... config ...
)

if __name__ == "__main__":
    demo.launch()
```

**Test standalone:**
```bash
# Terminal 1
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Terminal 2  
python app.py

# Browser
open http://localhost:7860
```

---

### TASK-303: Mount Gradio (1 hour)

**Add to main.py after all endpoints (~line 290):**

```python
# --- Mount Gradio UI (Backward Compatibility) ---

try:
    import gradio as gr
    
    print("📊 Loading Gradio UI...")
    
    # Set API_BASE_URL for Gradio (same origin when mounted)
    import os
    os.environ["API_BASE_URL"] = "http://localhost:8000"
    
    from app import demo as gradio_demo
    
    # Mount at /gradio
    app = gr.mount_gradio_app(app, gradio_demo, path="/gradio")
    
    print("✅ Mounted Gradio UI at /gradio")
    print("   Access at: http://localhost:8000/gradio")
    
except ImportError as e:
    print(f"⚠️  Warning: Could not import Gradio: {e}")
    
except Exception as e:
    print(f"⚠️  Warning: Failed to mount Gradio UI: {e}")
```

**Update root endpoint to list Gradio:**

```python
@app.get("/")
async def root():
    return {
        "name": "Expo Smooth MCP Server",
        "version": "2.0.0",
        # ... existing fields ...
        "endpoints": {
            # ... existing endpoints ...
            "gradio_ui": {
                "path": "/gradio",
                "method": "GET",
                "description": "Interactive Gradio web interface"
            }
        }
    }
```

**Test:**
```bash
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Check logs for:
# ✅ Mounted Gradio UI at /gradio

# Test in browser
open http://localhost:8000/gradio
```

---

### TASK-304: Test Unified Service (1.5 hours)

**Start server:**
```bash
python -m src.expo_smooth_mcp.main --transport http --port 8000
```

**Test all three interfaces:**

**1. REST API:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/forecast -H "Content-Type: application/json" -d '{"sku": "PRODUCT_001"}'
```

**2. MCP Tools:**
```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
# Or use Claude Desktop
```

**3. Gradio UI:**
```bash
open http://localhost:8000/gradio
# Test: Select SKU, generate forecast
```

**Cross-interface test:**
```bash
# In one terminal - REST API calls
while true; do curl -X POST http://localhost:8000/api/forecast -H "Content-Type: application/json" -d '{"sku":"PRODUCT_001"}' > /dev/null; sleep 1; done

# In browser - use Gradio simultaneously
# Verify no conflicts
```

---

### TASK-305: CORS (30 min - Optional)

**Test if needed:**
```bash
open http://localhost:8000/gradio
# Press F12, check console for CORS errors
```

**If NO errors:** Skip this task (CORS not needed for mounted Gradio)

**If errors exist:** Add CORS middleware

```python
# In main.py after app creation
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:7860,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

print(f"✅ CORS middleware configured")
```

---

### TASK-306: Integration Tests (1.5 hours)

**Create test file:**
```bash
cat > tests/test_gradio_integration.py << 'EOF'
"""Integration tests for Gradio UI mounted in FastAPI."""

import pytest
from fastapi.testclient import TestClient
from src.expo_smooth_mcp.main import app, PROCESSED_DF
from src.expo_smooth_mcp import logic

@pytest.fixture
def client():
    return TestClient(app)

class TestGradioMounting:
    def test_gradio_endpoint_accessible(self, client):
        response = client.get("/gradio")
        assert response.status_code in [200, 307, 308]
    
    def test_gradio_with_trailing_slash(self, client):
        response = client.get("/gradio/")
        assert response.status_code == 200

class TestGradioAPIIntegration:
    def test_gradio_backend_uses_same_data(self, client):
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        rest_response = client.get("/")
        rest_sku_count = rest_response.json()["sku_count"]
        
        gradio_sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        assert rest_sku_count == gradio_sku_count

class TestGradioEndpointListing:
    def test_root_endpoint_lists_gradio(self, client):
        response = client.get("/")
        data = response.json()
        
        assert "gradio_ui" in data["endpoints"]
        assert data["endpoints"]["gradio_ui"]["path"] == "/gradio"
EOF
```

**Run tests:**
```bash
pytest tests/test_gradio_integration.py -v

# Expected: 4+ tests passing
```

**Run full suite:**
```bash
pytest tests/ -v

# Expected: 37+ tests passing
```

---

## Verification Checklist

### Functionality
- [ ] Server starts without errors
- [ ] /gradio endpoint accessible
- [ ] Gradio UI loads in browser
- [ ] Dropdown has SKUs
- [ ] Can generate forecasts
- [ ] Plots display correctly
- [ ] REST API still works
- [ ] MCP tools still work
- [ ] No console errors (F12)

### Testing
- [ ] Gradio integration tests pass
- [ ] Full test suite passes (37+ tests)
- [ ] Manual testing complete
- [ ] Cross-interface testing done

### Performance
- [ ] Gradio loads in < 2s
- [ ] Forecasts generate in < 2s
- [ ] No performance degradation

### Documentation
- [ ] Root endpoint lists Gradio
- [ ] README updated
- [ ] Troubleshooting guide reviewed

---

## Common Commands

### Start Server
```bash
# HTTP mode (all interfaces)
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Stdio mode (MCP only - no Gradio)
python -m src.expo_smooth_mcp.main --transport stdio
```

### Test Endpoints
```bash
# REST API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/forecast -H "Content-Type: application/json" -d '{"sku":"PRODUCT_001"}'

# Gradio UI
open http://localhost:8000/gradio

# MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp

# OpenAPI Docs
open http://localhost:8000/docs
```

### Run Tests
```bash
# Gradio tests only
pytest tests/test_gradio_integration.py -v

# Full test suite
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Troubleshooting Quick Fixes

**Problem: Gradio won't mount**
```bash
pip install --upgrade gradio>=4.0.0
python -c "import gradio; print(gradio.__version__)"
```

**Problem: Blank Gradio page**
```bash
# Check data loaded
python -c "from src.expo_smooth_mcp.main import PROCESSED_DF; print('OK' if PROCESSED_DF is not None else 'FAIL')"

# Check browser console (F12) for errors
```

**Problem: "Cannot connect to API"**
```bash
# Verify API running
curl http://localhost:8000/health

# Check API_BASE_URL in mounted context
grep "API_BASE_URL" src/expo_smooth_mcp/main.py
```

**Problem: Import errors**
```bash
# Verify app.py exists and exports demo
ls -la app.py
grep "demo =" app.py
grep "if __name__" app.py
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Total Tests | 37+ passing |
| Gradio Load Time | < 2 seconds |
| Forecast Time | < 2 seconds |
| Code Coverage | > 90% |
| Console Errors | 0 |

---

## Next Phase

✅ **Phase 3 Complete** → Proceed to **Phase 4: Deployment**

**Phase 4A Options:**
- Docker MCP Toolkit deployment
- Fly.io cloud deployment
- Docker Compose setup

---

## Quick Links

- [Full Implementation Guide](PHASE_3_IMPLEMENTATION.md)
- [Phase 2 Code Review](../PHASE_2_CODE_REVIEW.md)
- [Project Roadmap](../PROJECT_ROADMAP.md)
- [Test Plan](../TEST_PLAN.md)

---

**Phase 3 Quick Reference Complete**  
**Time to Complete: ~7 hours**  
**Ready to Begin!** 🚀
