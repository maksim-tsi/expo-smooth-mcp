# Phase 2: Build FastMCP Backend - Quick Reference

**Status:** ⏳ Ready to Start  
**Duration:** ~20 hours (12 tasks)  
**Complexity:** Medium  
**Full Guide:** [PHASE_2_IMPLEMENTATION.md](PHASE_2_IMPLEMENTATION.md)

---

## Quick Overview

Phase 2 builds a production-grade FastMCP + FastAPI backend that replaces the Gradio prototype with professional MCP server infrastructure.

### What We're Building

```
┌─────────────────────────────────────────┐
│       FastAPI Application               │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐   ┌───────────────┐  │
│  │  MCP Tools  │   │   REST API    │  │
│  │  (stdio +   │   │  (/api/...)   │  │
│  │   HTTP/SSE) │   │               │  │
│  └──────┬──────┘   └───────┬───────┘  │
│         │                   │           │
│         └──────────┬────────┘           │
│                    │                    │
│         ┌──────────▼─────────┐         │
│         │  Business Logic    │         │
│         │  (logic.py)        │         │
│         └────────────────────┘         │
└─────────────────────────────────────────┘
```

---

## Task Summary

| Task | Description | Time | Complexity |
|------|-------------|------|------------|
| **TASK-201** | Install FastMCP dependencies | 0.5h | Low |
| **TASK-202** | Create main.py skeleton | 1.0h | Low |
| **TASK-203** | Implement data loading | 0.5h | Low |
| **TASK-204** | Create forecast_sku tool | 1.5h | Medium |
| **TASK-205** | Create list_skus tool | 0.5h | Low |
| **TASK-206** | Mount MCP to FastAPI | 0.5h | Low |
| **TASK-207** | Create root endpoint | 0.5h | Low |
| **TASK-208** | Create health endpoint | 0.5h | Low |
| **TASK-209** | Dual-transport entrypoint | 1.5h | High |
| **TASK-210** | Create REST API endpoint | 1.0h | Medium |
| **TASK-211** | Unit tests for MCP tools | 2.0h | Medium |
| **TASK-212** | Integration tests for API | 2.0h | Medium |
| **Total** | | **~12h** | |

---

## Quick Start

### 1. Install Dependencies (TASK-201)
```bash
# Using uv (recommended)
uv add fastapi fastmcp "uvicorn[standard]" python-multipart httpx

# Or using pip
pip install fastapi fastmcp "uvicorn[standard]" python-multipart httpx

# Verify
python -c "import fastapi, fastmcp; print('✓ Ready')"
```

### 2. Create main.py (TASK-202)
```bash
# Create file
touch src/expo_smooth_mcp/main.py

# See PHASE_2_IMPLEMENTATION.md for full template
```

### 3. Test Your Progress
```bash
# After each task, test:
python -m src.expo_smooth_mcp.main --transport http

# Visit in browser:
open http://localhost:8000
open http://localhost:8000/docs
```

---

## Key Features

### MCP Tools (Tasks 204-205)
```python
# Tool 1: Generate forecast
@mcp.tool()
async def forecast_sku(sku: str, forecast_horizon: int = 90):
    """Generate sales forecast for a product."""
    ...

# Tool 2: List available products
@mcp.tool()
async def list_available_skus():
    """Get all product SKUs."""
    ...
```

### REST API Endpoints (Tasks 207-210)
```
GET  /              - Service information
GET  /health        - Health check (for monitoring)
POST /api/forecast  - REST forecast endpoint
GET  /docs          - OpenAPI documentation
/mcp                - MCP protocol endpoint
```

### Dual-Transport Support (TASK-209)
```bash
# Local development (Claude Desktop, Cursor)
python -m src.expo_smooth_mcp.main --transport stdio

# Production (remote clients via HTTP)
python -m src.expo_smooth_mcp.main --transport http --port 8000
```

---

## Testing Strategy

### Unit Tests (TASK-211)
```bash
# Test MCP tools
pytest tests/test_mcp.py -v

# Expected: 8+ tests passing
```

### Integration Tests (TASK-212)
```bash
# Test REST API
pytest tests/test_api.py -v

# Expected: 10+ tests passing
```

### Manual Testing
```bash
# 1. Test with MCP Inspector
npx @modelcontextprotocol/inspector \
  python -m src.expo_smooth_mcp.main --transport stdio

# 2. Test with cURL
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}'

# 3. Test with browser
open http://localhost:8000/docs
```

---

## Claude Desktop Integration

After completing Phase 2, configure Claude Desktop:

```json
// ~/.config/claude/config.json (macOS/Linux)
// %APPDATA%\claude\config.json (Windows)
{
  "mcpServers": {
    "expo-smooth-forecast": {
      "command": "python",
      "args": [
        "-m",
        "src.expo_smooth_mcp.main",
        "--transport",
        "stdio"
      ],
      "cwd": "/Users/max/Documents/code/expo-smooth-mcp"
    }
  }
}
```

Then restart Claude Desktop and verify:
```
User: "List available products for forecasting"
Claude: [calls list_available_skus() tool]
```

---

## Success Criteria

### Code Complete
- [ ] `main.py` created with 12 tasks implemented
- [ ] 2 MCP tools functional
- [ ] 4 REST endpoints working
- [ ] Dual-transport support
- [ ] Test files created

### Functionality Verified
- [ ] Server starts in both modes
- [ ] MCP Inspector shows tools
- [ ] REST API responds
- [ ] Health check works
- [ ] OpenAPI docs generated

### Quality Gates
- [ ] All tests passing (30+ tests)
- [ ] Coverage >90%
- [ ] No linting errors
- [ ] Works with Claude Desktop
- [ ] Works with cURL

---

## Common Issues & Solutions

### "Import fastmcp not found"
```bash
pip install fastmcp>=2.0.0
```

### "Port 8000 already in use"
```bash
python -m src.expo_smooth_mcp.main --port 8001
```

### "stdio mode hangs"
This is normal - it's waiting for input. Test with:
```bash
echo '{"jsonrpc": "2.0"}' | \
  python -m src.expo_smooth_mcp.main --transport stdio
```

### "MCP tools not appearing"
Check mount statement comes AFTER tool definitions:
```python
@mcp.tool()
async def my_tool(): pass  # Define first

app.mount("/mcp", mcp.as_asgi())  # Mount after
```

---

## File Structure After Phase 2

```
expo-smooth-mcp/
├── src/
│   └── expo_smooth_mcp/
│       ├── __init__.py
│       ├── logic.py          ✅ Phase 1
│       ├── forecasting.py    ✅ Phase 1
│       ├── preprocessing.py  ✅ Phase 1
│       └── main.py           🆕 Phase 2 - NEW!
├── tests/
│   ├── test_logic.py         ✅ Phase 1
│   ├── test_forecasting.py   ✅ Phase 1
│   ├── test_preprocessing.py ✅ Phase 1
│   ├── test_mcp.py           🆕 Phase 2 - NEW!
│   └── test_api.py           🆕 Phase 2 - NEW!
├── app.py                    ✅ Phase 1 (Gradio UI)
├── requirements.txt          🔄 Updated
└── FMCG_Sales.csv
```

---

## Next Steps After Phase 2

1. ✅ Complete all 12 tasks
2. ✅ Run full test suite
3. ✅ Test with Claude Desktop
4. ✅ Create Phase 2 Code Review
5. ⏭️ Proceed to Phase 3: Integration & Deployment

---

## Resources

- **Full Implementation Guide:** [PHASE_2_IMPLEMENTATION.md](PHASE_2_IMPLEMENTATION.md)
- **Technical Specification:** [../SPECIFICATION.md](../SPECIFICATION.md)
- **Phase 1 Review:** [../PHASE_1_CODE_REVIEW.md](../PHASE_1_CODE_REVIEW.md)
- **FastMCP Docs:** https://github.com/jlowin/fastmcp
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **MCP Specification:** https://modelcontextprotocol.io

---

**Status:** Ready to begin TASK-201  
**Estimated Completion:** ~20 hours (2-3 days with breaks)  
**Confidence:** High (Phase 1 provides solid foundation)
