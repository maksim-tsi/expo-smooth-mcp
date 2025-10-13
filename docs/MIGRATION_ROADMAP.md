# Migration Roadmap: Gradio → FastMCP + FastAPI + Fly.io

**Status:** Planning  
**Target Completion:** TBD  
**Owner:** Development Team  
**Last Updated:** 2025-10-12

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Migration Rationale](#migration-rationale)
3. [Target Architecture](#target-architecture)
4. [Phased Implementation Plan](#phased-implementation-plan)
5. [Technical Specifications](#technical-specifications)
6. [Risk Assessment & Mitigation](#risk-assessment--mitigation)
7. [Success Metrics](#success-metrics)
8. [Timeline & Resources](#timeline--resources)

---

## Executive Summary

### Current State
- **Framework:** Gradio 5.x with built-in MCP support
- **Deployment:** Hugging Face Spaces (free tier)
- **Performance:**
  - 600ms overhead per MCP tool call
  - 2-minute cold start on Hugging Face Spaces
  - Limited to SSE transport only

### Target State
- **Framework:** FastMCP 2.0 + FastAPI
- **Deployment:** Fly.io (Container-as-a-Service)
- **Expected Performance:**
  - <10ms overhead per tool call (60x improvement)
  - <1s cold start (120x improvement)
  - Dual transport support (stdio + HTTP/SSE)

### Migration Strategy
**Phased, zero-downtime migration** with backward compatibility throughout all phases.

---

## Migration Rationale

### Quantified Performance Issues

| Issue | Current Impact | Root Cause | Solution |
|-------|----------------|------------|----------|
| **600ms tool overhead** | Unacceptable latency for fast forecasting model | Gradio's queuing system for ML demos | Replace with FastMCP direct execution |
| **2-minute cold start** | Non-viable for production use | HF Spaces container provisioning | Migrate to Fly.io Firecracker VMs |
| **No stdio support** | Cannot integrate with Claude Desktop | Gradio MCP limited to SSE only | FastMCP native dual-transport |
| **Framework mismatch** | Coupling UI framework to API layer | Gradio is UI-first, not API-first | Decouple with FastAPI + mounted Gradio |

### Strategic Benefits

1. **Performance**: 60-120x improvement in critical metrics
2. **Scalability**: Global distribution with Fly.io (30+ regions)
3. **Flexibility**: Support both local (stdio) and remote (HTTP/SSE) clients
4. **Maintainability**: Clean separation of concerns (UI vs. API vs. business logic)
5. **Production-readiness**: Built-in auth, rate limiting, observability

### References
- [research-Lightweight-MCP-Server.md](./research-Lightweight-MCP-Server.md) - Framework analysis
- [research-Gradio-FastMCP-Migration.md](./research-Gradio-FastMCP-Migration.md) - Migration strategy

---

## Target Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Fly.io Global Network                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Docker Container (Python 3.12-slim)          │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │           Uvicorn ASGI Server (Port 8000)          │  │  │
│  │  │  ┌──────────────────────────────────────────────┐  │  │  │
│  │  │  │             FastAPI Application              │  │  │  │
│  │  │  │                                              │  │  │  │
│  │  │  │  ┌────────────────────────────────────────┐ │  │  │  │
│  │  │  │  │  FastMCP Server (mounted at /mcp)      │ │  │  │  │
│  │  │  │  │  • Streamable HTTP (SSE) transport     │ │  │  │  │
│  │  │  │  │  • @mcp.tool decorators                │ │  │  │  │
│  │  │  │  └────────────────────────────────────────┘ │  │  │  │
│  │  │  │                                              │  │  │  │
│  │  │  │  ┌────────────────────────────────────────┐ │  │  │  │
│  │  │  │  │  Gradio UI (mounted at /gradio)        │ │  │  │  │
│  │  │  │  │  • Backward compatibility layer        │ │  │  │  │
│  │  │  │  │  • Calls FastAPI endpoints             │ │  │  │  │
│  │  │  │  └────────────────────────────────────────┘ │  │  │  │
│  │  │  │                                              │  │  │  │
│  │  │  │  REST Endpoints:                             │  │  │  │
│  │  │  │  • GET  /health                              │  │  │  │
│  │  │  │  • POST /token (OAuth2)                      │  │  │  │
│  │  │  │  • GET  /api/forecast                        │  │  │  │
│  │  │  │  • GET  /docs (OpenAPI)                      │  │  │  │
│  │  │  └──────────────────────────────────────────────┘  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                           │                               │  │
│  │                           ▼                               │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         Core Business Logic (logic.py)             │  │  │
│  │  │  • generate_forecast()                             │  │  │
│  │  │  • preprocess_data()                               │  │  │
│  │  │  • Framework-agnostic pure functions              │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Local Development (stdio)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Claude Desktop / Cursor / VS Code                        │  │
│  │  └──────────────┬────────────────────────────────────────┘  │
│  │                 │ stdio (stdin/stdout)                       │
│  │                 ▼                                            │
│  │  ┌──────────────────────────────────────────────────────┐  │
│  │  │  FastMCP Server Process                              │  │
│  │  │  $ fastmcp run main.py:mcp --transport stdio         │  │
│  │  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Monolithic Design**: Single service (not microservices) for minimal overhead
2. **ASGI Foundation**: FastAPI + Uvicorn for high-performance async I/O
3. **Dual-Transport**: Runtime flag switches between stdio and HTTP/SSE
4. **Backward Compatibility**: Gradio mounted as sub-application, not replaced
5. **Stateful Model**: In-memory model storage (suitable for single-instance deployment)

---

## Phased Implementation Plan

### Phase 1: Decouple Business Logic (2-3 days)

**Objective:** Extract all forecasting logic into framework-agnostic module.

#### Tasks

1. **Create `src/expo_smooth_mcp/logic.py`**
   ```python
   # Pure business logic functions
   from typing import Dict, List
   import pandas as pd
   
   def generate_forecast_data(
       df: pd.DataFrame, 
       sku: str, 
       horizon: int = 90
   ) -> Dict[str, List]:
       """
       Generate forecast for a specific SKU.
       
       Returns dict with 'dates', 'actuals', 'forecast' keys.
       Framework-agnostic - works with any UI or API.
       """
       # Move existing logic from app.py
       pass
   ```

2. **Refactor `app.py`**
   - Import functions from `logic.py`
   - Simplify event handlers to call logic functions
   - Remove any business logic from UI layer

3. **Validate**
   - Run existing app: `python app.py`
   - Verify all functionality works identically
   - Run unit tests to confirm no regression

#### Acceptance Criteria
- ✅ Gradio app functions exactly as before
- ✅ All business logic in `logic.py` with no Gradio dependencies
- ✅ Unit tests pass
- ✅ Code review approved

---

### Phase 2: Build FastMCP Backend (3-4 days)

**Objective:** Create new FastAPI + FastMCP service exposing forecasting tools.

#### Tasks

1. **Install Dependencies**
   ```bash
   uv add fastapi fastmcp uvicorn python-multipart
   ```

2. **Create `src/expo_smooth_mcp/main.py`**
   ```python
   import sys
   from fastapi import FastAPI
   from fastmcp import FastMCP
   from .logic import generate_forecast_data
   from .preprocessing import load_and_preprocess_data
   
   # Initialize frameworks
   app = FastAPI(title="Exponential Smoothing MCP Server")
   mcp = FastMCP(name="ExpoSmoothForecaster")
   
   # Load data once at startup
   PROCESSED_DF = load_and_preprocess_data()
   
   @mcp.tool
   async def forecast_sku(
       sku: str,
       forecast_horizon: int = 90
   ) -> dict:
       """
       Generate a sales forecast for a specific product SKU.
       
       Uses Exponential Smoothing (Holt-Winters) with 7-day seasonality.
       
       Args:
           sku (str): Product SKU code (e.g., "PRODUCT_123")
           forecast_horizon (int): Number of days to forecast (default: 90)
       
       Returns:
           dict: Contains 'dates', 'actuals', 'forecast' arrays
       """
       return generate_forecast_data(PROCESSED_DF, sku, forecast_horizon)
   
   @mcp.tool
   async def list_available_skus() -> list:
       """
       Get list of all product SKUs available for forecasting.
       
       Returns:
           list: Array of SKU strings
       """
       return sorted(PROCESSED_DF['SKU'].unique().tolist())
   
   # Mount FastMCP server at /mcp endpoint
   app.mount("/mcp", mcp.as_asgi())
   
   # Standard REST endpoints
   @app.get("/")
   async def root():
       return {
           "service": "Exponential Smoothing MCP Server",
           "version": "2.0",
           "endpoints": {
               "mcp": "/mcp (Streamable HTTP)",
               "health": "/health",
               "docs": "/docs"
           }
       }
   
   @app.get("/health")
   async def health_check():
       return {
           "status": "healthy",
           "data_loaded": not PROCESSED_DF.empty,
           "sku_count": len(PROCESSED_DF['SKU'].unique())
       }
   
   # Dual-transport entrypoint
   if __name__ == "__main__":
       if "--transport" in sys.argv and sys.argv[sys.argv.index("--transport") + 1] == "stdio":
           # Local stdio mode for Claude Desktop
           mcp.run(transport="stdio")
       else:
           # HTTP/SSE mode for cloud deployment
           import uvicorn
           uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

3. **Test Locally**
   ```bash
   # Test HTTP/SSE transport
   uvicorn src.expo_smooth_mcp.main:app --reload
   # Visit http://localhost:8000/docs
   
   # Test stdio transport
   fastmcp run src/expo_smooth_mcp/main.py:mcp --transport stdio
   ```

4. **Create Integration Tests**
   ```python
   # tests/test_mcp_integration.py
   import pytest
   from fastapi.testclient import TestClient
   from src.expo_smooth_mcp.main import app
   
   @pytest.fixture
   def client():
       return TestClient(app)
   
   def test_health_endpoint(client):
       response = client.get("/health")
       assert response.status_code == 200
       assert response.json()["status"] == "healthy"
   
   def test_mcp_endpoint_exists(client):
       response = client.get("/mcp")
       assert response.status_code in [200, 405]  # 405 if GET not allowed
   ```

#### Acceptance Criteria
- ✅ FastMCP server runs on `http://localhost:8000`
- ✅ OpenAPI docs visible at `/docs`
- ✅ MCP tools accessible via MCP Inspector
- ✅ stdio transport works with test client
- ✅ All integration tests pass

---

### Phase 3: Mount Gradio for Backward Compatibility (1-2 days)

**Objective:** Preserve existing Gradio UI by mounting it into FastAPI.

#### Tasks

1. **Update `app.py` to be mountable**
   ```python
   import gradio as gr
   import httpx
   from typing import Optional
   
   # Update functions to call FastAPI backend
   async def create_forecast_plot_wrapper(sku: str, horizon: int):
       async with httpx.AsyncClient() as client:
           # Call the new FastAPI backend
           response = await client.post(
               "http://localhost:8000/api/forecast",
               json={"sku": sku, "horizon": horizon}
           )
           data = response.json()
           # Convert to Plotly figure as before
           return create_plotly_figure(data)
   
   # Create Gradio interface
   demo = gr.Blocks(title="Exponential Smoothing Forecaster")
   
   with demo:
       # ... existing UI code ...
       pass
   
   # Make demo object available for mounting
   # Don't call demo.launch() here anymore
   ```

2. **Mount Gradio in `main.py`**
   ```python
   import gradio as gr
   from app import demo as gradio_ui
   
   # ... existing FastAPI/FastMCP setup ...
   
   # Mount Gradio at /gradio path
   app = gr.mount_gradio_app(app, gradio_ui, path="/gradio")
   ```

3. **Add FastAPI REST endpoint for forecasting**
   ```python
   from pydantic import BaseModel
   
   class ForecastRequest(BaseModel):
       sku: str
       horizon: int = 90
   
   @app.post("/api/forecast")
   async def api_forecast(request: ForecastRequest):
       """REST endpoint for forecasting (used by Gradio UI)"""
       return generate_forecast_data(PROCESSED_DF, request.sku, request.horizon)
   ```

4. **Test both interfaces**
   ```bash
   uvicorn src.expo_smooth_mcp.main:app --reload
   
   # Test FastAPI: http://localhost:8000/docs
   # Test Gradio: http://localhost:8000/gradio
   # Test MCP: http://localhost:8000/mcp
   ```

#### Acceptance Criteria
- ✅ All three interfaces accessible from single service
- ✅ Gradio UI fully functional at `/gradio`
- ✅ Gradio calls FastAPI backend successfully
- ✅ No code duplication between UI and API layers

---

### Phase 4: Dockerize and Deploy to Fly.io (2-3 days)

**Objective:** Package application and deploy to production infrastructure.

#### Tasks

1. **Create `Dockerfile`**
   ```dockerfile
   # Multi-stage build for minimal image size
   FROM python:3.12-slim AS builder
   
   WORKDIR /app
   
   # Install uv for fast dependency installation
   RUN pip install uv
   
   # Copy dependency files
   COPY requirements.txt .
   
   # Create virtual environment and install dependencies
   RUN uv venv && . .venv/bin/activate && uv pip install -r requirements.txt
   
   # Production stage
   FROM python:3.12-slim AS final
   
   WORKDIR /app
   
   # Copy virtual environment from builder
   COPY --from=builder /app/.venv ./.venv
   
   # Copy application code
   COPY src/ ./src/
   COPY data/ ./data/
   COPY app.py .
   
   # Activate virtual environment
   ENV PATH="/app/.venv/bin:$PATH"
   
   # Expose port
   EXPOSE 8000
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD python -c "import requests; requests.get('http://localhost:8000/health')"
   
   # Run application
   CMD ["uvicorn", "src.expo_smooth_mcp.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Create `fly.toml`**
   ```toml
   app = "expo-smooth-mcp"
   primary_region = "sjc"  # San Jose, CA - choose closest to users
   
   [build]
     dockerfile = "Dockerfile"
   
   [env]
     PORT = "8000"
     PYTHONUNBUFFERED = "1"
   
   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = false  # CRITICAL: Prevents cold starts
     auto_start_machines = true
     min_machines_running = 1    # CRITICAL: Always-on for low latency
   
   [[http_service.checks]]
     interval = "15s"
     timeout = "3s"
     grace_period = "10s"
     method = "GET"
     path = "/health"
   
   [[vm]]
     memory = '512mb'
     cpu_kind = 'shared'
     cpus = 1
   ```

3. **Deploy to Fly.io**
   ```bash
   # Install flyctl
   curl -L https://fly.io/install.sh | sh
   
   # Login to Fly.io
   flyctl auth login
   
   # Launch application (creates app and fly.toml)
   flyctl launch --no-deploy  # Review fly.toml first
   
   # Deploy
   flyctl deploy
   
   # Check status
   flyctl status
   flyctl logs
   
   # Test deployment
   curl https://expo-smooth-mcp.fly.dev/health
   ```

4. **Update Documentation**
   - Create `docs/FLY_IO_DEPLOYMENT.md`
   - Update `README.md` with new architecture
   - Add client configuration examples

#### Acceptance Criteria
- ✅ Docker image builds successfully (<500MB)
- ✅ Application deployed to Fly.io
- ✅ Health checks passing
- ✅ Cold start < 1 second (verified with `flyctl logs`)
- ✅ All endpoints accessible via public URL

---

### Phase 5: Production Hardening (3-4 days)

**Objective:** Add security, rate limiting, and observability.

#### Tasks

1. **Implement OAuth2 + JWT Authentication**
   ```bash
   uv add python-jose[cryptography] passlib[bcrypt]
   ```
   
   ```python
   # src/expo_smooth_mcp/security.py
   from datetime import datetime, timedelta
   from jose import JWTError, jwt
   from passlib.context import CryptContext
   from fastapi import Depends, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer
   
   SECRET_KEY = "your-secret-key-here"  # Use env var in production
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
   
   def create_access_token(data: dict):
       to_encode = data.copy()
       expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       to_encode.update({"exp": expire})
       return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   
   async def get_current_user(token: str = Depends(oauth2_scheme)):
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           username: str = payload.get("sub")
           if username is None:
               raise HTTPException(status_code=401, detail="Invalid token")
           return username
       except JWTError:
           raise HTTPException(status_code=401, detail="Invalid token")
   ```

2. **Add Rate Limiting**
   ```bash
   uv add fastapi-limiter redis
   ```
   
   ```python
   # In main.py
   from fastapi_limiter import FastAPILimiter
   from fastapi_limiter.depends import RateLimiter
   import redis.asyncio as redis
   
   @app.on_event("startup")
   async def startup():
       redis_client = await redis.from_url(
           "redis://localhost",
           encoding="utf-8",
           decode_responses=True
       )
       await FastAPILimiter.init(redis_client)
   
   # Apply to endpoints
   @app.get("/api/forecast", dependencies=[Depends(RateLimiter(times=60, seconds=60))])
   async def forecast_endpoint():
       pass
   ```

3. **Configure Structured Logging**
   ```python
   import logging
   import json
   from datetime import datetime
   
   class JSONFormatter(logging.Formatter):
       def format(self, record):
           log_obj = {
               "timestamp": datetime.utcnow().isoformat(),
               "level": record.levelname,
               "message": record.getMessage(),
               "module": record.module,
               "function": record.funcName
           }
           return json.dumps(log_obj)
   
   handler = logging.StreamHandler()
   handler.setFormatter(JSONFormatter())
   logger = logging.getLogger("expo_smooth_mcp")
   logger.addHandler(handler)
   logger.setLevel(logging.INFO)
   ```

4. **Add Monitoring Middleware**
   ```python
   from fastapi import Request
   import time
   
   @app.middleware("http")
   async def log_requests(request: Request, call_next):
       start_time = time.time()
       response = await call_next(request)
       duration = time.time() - start_time
       
       logger.info({
           "path": request.url.path,
           "method": request.method,
           "status_code": response.status_code,
           "duration_ms": round(duration * 1000, 2)
       })
       
       return response
   ```

5. **Create Comprehensive Tests**
   ```python
   # tests/test_security.py
   def test_protected_endpoint_requires_auth(client):
       response = client.get("/api/forecast")
       assert response.status_code == 401
   
   def test_valid_token_grants_access(client):
       # Get token
       response = client.post("/token", data={"username": "test", "password": "test"})
       token = response.json()["access_token"]
       
       # Use token
       response = client.get(
           "/api/forecast",
           headers={"Authorization": f"Bearer {token}"}
       )
       assert response.status_code == 200
   ```

#### Acceptance Criteria
- ✅ JWT authentication working on protected endpoints
- ✅ Rate limiting prevents abuse (verified with load tests)
- ✅ Structured JSON logs visible in Fly.io dashboard
- ✅ Prometheus metrics exposed at `/metrics`
- ✅ All security tests passing

---

## Technical Specifications

### Dependencies

**Production**
```
fastapi>=0.110.0
fastmcp>=2.0.0
uvicorn[standard]>=0.27.0
gradio>=5.0.0
pandas>=2.2.0
plotly>=5.18.0
statsmodels>=0.14.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
fastapi-limiter>=0.1.5
redis>=5.0.0
```

**Development**
```
pytest>=8.0.0
httpx>=0.27.0
pytest-asyncio>=0.23.0
```

### Environment Variables

```bash
# Required
SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://...  # If using Postgres for users

# Optional
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Infrastructure Requirements

**Fly.io Configuration**
- **Region:** Choose closest to primary users
- **Memory:** 512MB (minimum), 1GB (recommended)
- **CPU:** 1 shared CPU
- **Machines:** min=1, max=3 (for autoscaling)
- **Persistent Storage:** Not required (stateless app)

**Redis** (for rate limiting)
- **Provider:** Upstash (serverless Redis)
- **Memory:** 100MB sufficient
- **Region:** Same as Fly.io app

---

## Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| **Breaking changes for existing users** | Medium | High | Mount Gradio UI at `/gradio`, maintain URL backward compat |
| **Performance regression** | Low | High | Benchmark before/after, rollback plan ready |
| **Deployment issues** | Medium | Medium | Test on Fly.io staging environment first |
| **Data loss during migration** | Low | Critical | No database - stateless app, no data migration needed |
| **Cost overruns on Fly.io** | Low | Low | Start with free tier (512MB), monitor usage |
| **FastMCP bugs/instability** | Low | Medium | Use stable FastMCP 2.0 release, comprehensive testing |

### Rollback Plan

If critical issues arise during migration:

1. **Phase 1-2:** Easy rollback - keep `app.py` running on HF Spaces
2. **Phase 3:** Revert `main.py` changes, run original `app.py`
3. **Phase 4+:** Use Fly.io's instant rollback: `flyctl releases list && flyctl releases rollback <version>`

---

## Success Metrics

### Performance Metrics

| Metric | Baseline (Gradio/HF) | Target (FastMCP/Fly.io) | Measurement Method |
|--------|----------------------|-------------------------|-------------------|
| **Tool call latency (p50)** | ~650ms | <50ms | MCP Inspector benchmarks |
| **Tool call latency (p95)** | ~850ms | <100ms | Load testing with locust |
| **Cold start time** | ~120s | <1s | Fly.io logs after idle period |
| **Concurrent requests** | ~40 (worker limit) | 1000+ (async) | Load testing |
| **Container size** | N/A (HF managed) | <500MB | `docker images` |

### Functional Metrics

- ✅ Both stdio and HTTP/SSE transports operational
- ✅ Gradio UI functional at `/gradio`
- ✅ MCP tools discoverable by Claude Desktop
- ✅ OpenAPI docs accurate and complete
- ✅ Health checks passing with <5% false negatives

### Operational Metrics

- ✅ Deployment time < 5 minutes
- ✅ 99.9% uptime (tracked by Fly.io)
- ✅ Log searchability via Grafana
- ✅ Alert notifications configured

---

## Timeline & Resources

### Estimated Timeline

| Phase | Duration | Dependencies | Team Size |
|-------|----------|--------------|-----------|
| **Phase 1: Decouple** | 2-3 days | None | 1 developer |
| **Phase 2: Build FastMCP** | 3-4 days | Phase 1 complete | 1-2 developers |
| **Phase 3: Mount Gradio** | 1-2 days | Phase 2 complete | 1 developer |
| **Phase 4: Deploy** | 2-3 days | Phase 3 complete, Fly.io account | 1 developer |
| **Phase 5: Harden** | 3-4 days | Phase 4 complete, Redis setup | 1-2 developers |
| **Total** | **11-16 days** | | |

### Resource Requirements

**Infrastructure Costs** (Monthly)
- Fly.io (512MB, 1 machine): ~$0 (free tier) or ~$5/month
- Upstash Redis (100MB): $0 (free tier)
- **Total:** $0-5/month (vs. $0 on HF Spaces)

**Development Resources**
- 1 senior developer (primary)
- 1 developer for testing/review (part-time)
- DevOps support for Fly.io setup (1-2 hours)

---

## Next Steps

### Immediate Actions (This Week)

1. ✅ Review and approve this roadmap
2. ⏳ Create Phase 1 implementation branch
3. ⏳ Set up Fly.io account and test deployment
4. ⏳ Run benchmark of current Gradio implementation

### Preparation Tasks

- [ ] Provision Fly.io account
- [ ] Set up Upstash Redis account
- [ ] Create staging environment for testing
- [ ] Schedule migration kickoff meeting
- [ ] Update project board with migration tasks

### Documentation Tasks

- [ ] Create ADR-004: Migration to FastMCP
- [ ] Update README.md with new architecture
- [ ] Create client integration guides
- [ ] Document new API endpoints

---

## References

1. [research-Lightweight-MCP-Server.md](./research-Lightweight-MCP-Server.md) - Comprehensive framework analysis
2. [research-Gradio-FastMCP-Migration.md](./research-Gradio-FastMCP-Migration.md) - Migration strategy and benchmarks
3. [FastMCP Documentation](https://gofastmcp.com/)
4. [Fly.io Documentation](https://fly.io/docs/)
5. [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## Approval

**Prepared by:** Development Team  
**Date:** 2025-10-12  
**Status:** Awaiting approval

**Approvals Required:**
- [ ] Technical Lead
- [ ] Product Owner
- [ ] DevOps/Infrastructure

---

*This document is a living artifact and will be updated as the migration progresses.*
