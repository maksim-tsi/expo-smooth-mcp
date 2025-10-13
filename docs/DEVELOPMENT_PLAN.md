
# Development Plan & Project Status

- **Version:** 2.0
- **Status:** Living
- **Last Updated:** 2025-10-13
- **Summary:** This document outlines the development phases, granular atomic tasks, and implementation roadmap for migrating `expo-smooth-mcp` from Gradio prototype to production-grade FastMCP + FastAPI architecture. Each task is designed to be completable by an experienced Python developer in ≤2 hours.

---

## 1. Overview

This development plan translates the strategic goals from our `PROJECT_CHARTER.md` into actionable phases and tasks. It is a living document that will be updated as the project progresses to reflect our current status and priorities.

## 2. Development Phases

The project is structured into three distinct phases:

### Phase 1: Foundation & Backend Logic (95% Complete)
**Objective:** To establish the project's documentation framework and build the core, non-visual components.
*   **Deliverables:**
    *   **[✓]** Core documentation (`PROJECT_CHARTER.md`, ADRs, Guides).
    *   **[✓]** Data preprocessing pipeline (`preprocessing.py`).
    *   **[✓]** Core forecasting engine (`forecasting.py`).
    *   **[✓]** Unit test suite for backend logic (`tests/`).

### Phase 2: UI, Integration & Core Functionality (In Progress)
**Objective:** To build the user-facing application, integrate all backend components, and enable the core MCP functionality.
*   **Deliverables:**
    *   **[✓]** Initial Gradio UI with basic functionality.
    *   **[ ]** File upload capability for custom datasets.
    *   **[ ]** Enablement and testing of the MCP server endpoint.
    *   **[ ]** Completion of the formal Test Plan.

### Phase 3: Finalization & Dissemination (Not Started)
**Objective:** To finalize the application, deploy it, and complete the research paper.
*   **Deliverables:**
    *   **[ ]** Final E2E testing of the completed application.
    *   **[ ]** Final, stable deployment on Hugging Face Spaces.
    *   **[ ]** Completed research paper draft for submission to RelStat.

## 3. Current Project Status (As of 2025-07-05)

| Component | Status | Notes |
| :--- | :--- | :--- |
| **Documentation** | **90% Complete** | Core documents and ADRs are complete. `TEST_PLAN.md` is written. Only minor updates might be needed. |
| **Data Preprocessing** | **Completed** | `preprocessing.py` module is implemented and fully covered by unit tests. |
| **Forecasting Engine** | **Completed** | `forecasting.py` module is implemented and fully covered by unit tests. |
| **Gradio Application** | **Partially Completed** | The base UI is functional with the default dataset. File upload and MCP server are not yet implemented. |
| **Unit Testing** | **Completed** | The backend logic in `src/` has a corresponding test suite in `tests/`. |
| **Integration & E2E Testing** | **Not Started** | The test plan is written, but execution against the final application has not yet occurred. |

## 4. Immediate Next Steps (Action Plan)

The following tasks are our immediate priority to complete Phase 2.

1.  **Implement File Upload Functionality:**
    *   **Action:** Modify `app.py` to include a `gr.File` component.
    *   **Logic:** Add a function that takes an uploaded file, runs it through `preprocess_data`, and updates the SKU dropdown and application state with the new data.
    *   **Goal:** Allow users to interact with their own data, fulfilling a key requirement from the `PROJECT_CHARTER.md`.

2.  **Enable and Test the MCP Server:**
    *   **Action:** Modify `demo.launch()` in `app.py` to include `mcp_server=True`.
    *   **Process:** Launch the application using `uvicorn app:demo --reload`.
    *   **Testing:** Use `curl` or an MCP client to execute the integration test cases defined in `docs/TEST_PLAN.md` (IT-001, IT-002).
    *   **Goal:** Validate the core research component of our project.

3.  **Execute Final End-to-End Testing:**
    *   **Action:** Manually execute all test cases listed in `docs/TEST_PLAN.md` under section 4.3, including those for file uploads.
    *   **Goal:** Ensure the application is stable, user-friendly, and bug-free before final deployment.

## 5. Development Tasks

This section provides a comprehensive, granular breakdown of all tasks required for the FastMCP migration. Each task is:
- **Atomic:** Can be completed independently by a single developer
- **Time-Boxed:** Designed for ≤2 hours of work by an experienced Python developer
- **Testable:** Has clear Definition of Done criteria
- **Assignable:** Can be distributed across multiple team members

### Task Structure Template

Each task follows this structure:

```
### TASK-XXX: Task Name
**Phase:** [Phase Number]
**Estimated Time:** [hours]
**Complexity:** [Low/Medium/High]
**Dependencies:** [List of prerequisite tasks]

**Description:**
[Brief description of what needs to be done]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Status:** [Not Started / In Progress / In Review / Completed / Blocked]
**Assignee:** [TBD]
**Actual Time:** [hours]
**Notes:** [Any relevant implementation notes]
```

---

## 6. Task Inventory

### Phase 1: Decouple Business Logic (8 tasks, ~12 hours)

#### TASK-101: Create logic.py module structure
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None
**Description:** Create `src/expo_smooth_mcp/logic.py` with module docstring, imports, and skeleton functions.

#### TASK-102: Extract forecast data generation function
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-101
**Description:** Move forecast generation logic from `app.py` to `logic.get_forecast_data()`. Ensure function accepts DataFrame, SKU, and horizon; returns JSON-serializable dict.

#### TASK-103: Extract SKU listing function
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-101
**Description:** Create `logic.get_available_skus()` function that returns sorted list of unique SKUs from DataFrame.

#### TASK-104: Extract Plotly visualization function
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-102
**Description:** Create `logic.create_forecast_plot()` that takes forecast data dict and returns Plotly Figure object.

#### TASK-105: Extract validation function
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-102
**Description:** Create `logic.validate_forecast_request()` with input validation logic (SKU existence, horizon range).

#### TASK-106: Implement data loading singleton
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-101
**Description:** Create `logic.get_processed_data()` with module-level caching to load data once.

#### TASK-107: Refactor app.py to use logic module
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-102, TASK-103, TASK-104, TASK-105, TASK-106
**Description:** Update `app.py` event handlers to import and call logic functions. Remove all business logic from UI layer.

#### TASK-108: Create unit tests for logic module
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-107
**Description:** Create `tests/test_logic.py` with comprehensive tests for all logic functions. Achieve >90% coverage.

---

### Phase 2: Build FastMCP Backend (12 tasks, ~20 hours)

#### TASK-201: Install FastMCP and FastAPI dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None
**Description:** Add `fastapi`, `fastmcp`, `uvicorn[standard]`, `python-multipart` to requirements. Test installation.

#### TASK-202: Create main.py skeleton structure
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-201
**Description:** Create `src/expo_smooth_mcp/main.py` with FastAPI and FastMCP initialization, basic imports, and module docstring.

#### TASK-203: Implement data loading in main.py
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-202, TASK-106
**Description:** Import and call `get_processed_data()` at module level in `main.py`. Handle loading errors.

#### TASK-204: Create forecast_sku MCP tool
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-203
**Description:** Implement `@mcp.tool` decorated `forecast_sku()` function with complete docstring, type hints, and logic integration.

#### TASK-205: Create list_available_skus MCP tool
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-203
**Description:** Implement `@mcp.tool` decorated `list_available_skus()` function.

#### TASK-206: Mount FastMCP server to FastAPI
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-204, TASK-205
**Description:** Use `app.mount("/mcp", mcp.as_asgi())` to expose MCP server at `/mcp` endpoint.

#### TASK-207: Create root endpoint
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-202
**Description:** Implement `@app.get("/")` with service info and available endpoints documentation.

#### TASK-208: Create health check endpoint
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-203
**Description:** Implement `@app.get("/health")` that validates data loaded and returns status.

#### TASK-209: Implement dual-transport entrypoint
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-206
**Description:** Add command-line argument parsing in `if __name__ == "__main__"` block to support both stdio and HTTP transports.

#### TASK-210: Create REST API forecast endpoint
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-204
**Description:** Implement `@app.post("/api/forecast")` with Pydantic request model for non-MCP clients.

#### TASK-211: Create integration tests for FastMCP
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-208, TASK-209
**Description:** Create `tests/test_mcp_integration.py` with tests for health endpoint, MCP tools, and dual-transport modes.

#### TASK-212: Manual testing of local server
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-211
**Description:** Start server locally, verify OpenAPI docs, test with MCP Inspector, validate stdio mode.

---

### Phase 3: Mount Gradio UI (6 tasks, ~8 hours)

#### TASK-301: Create Pydantic models for API
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-210
**Description:** Define `ForecastRequest` and `ForecastResponse` Pydantic models in `main.py` or separate `models.py`.

#### TASK-302: Refactor Gradio to call REST API
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-301
**Description:** Update Gradio event handlers to use `httpx.AsyncClient()` to call FastAPI `/api/forecast` endpoint instead of direct logic calls.

#### TASK-303: Mount Gradio app in FastAPI
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-302
**Description:** Import Gradio demo and use `gr.mount_gradio_app(app, demo, path="/gradio")` in `main.py`.

#### TASK-304: Test unified service locally
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-303
**Description:** Start unified server, verify all three interfaces work: `/docs` (FastAPI), `/gradio` (UI), `/mcp` (MCP tools).

#### TASK-305: Handle CORS for Gradio
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-303
**Description:** Add FastAPI CORS middleware if needed for Gradio to communicate with FastAPI backend.

#### TASK-306: Create integration tests for mounted UI
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-304
**Description:** Add tests to verify Gradio UI accessible, can make requests to FastAPI, and returns correct responses.

---

### Phase 4A: Docker MCP Toolkit Setup (7 tasks, ~10 hours)

#### TASK-401: Create multi-stage Dockerfile
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-303
**Description:** Create production `Dockerfile` with builder stage (uv), final stage (python:3.12-slim), non-root user, optimized layers.

#### TASK-402: Add Docker-specific configurations
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-401
**Description:** Add `.dockerignore`, configure HEALTHCHECK, set optimal ENV variables for production.

#### TASK-403: Build and test Docker image
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-402
**Description:** Build image, verify size <500MB, test HTTP mode locally with `docker run -p 8000:8000`.

#### TASK-404: Test stdio transport in Docker
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-403
**Description:** Test `docker run -i` with stdio mode, verify MCP communication works.

#### TASK-405: Enable in Docker MCP Toolkit
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-404
**Description:** Run `docker mcp server enable expo-smooth-mcp:latest`, verify appears in Docker Desktop.

#### TASK-406: Connect Claude Desktop via Toolkit
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-405
**Description:** Use Docker Desktop UI to connect Claude Desktop, restart Claude, verify tools discoverable.

#### TASK-407: Create Docker MCP Toolkit documentation
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-406
**Description:** Write `docs/DOCKER_MCP_TOOLKIT.md` with setup instructions, screenshots, troubleshooting.

---

### Phase 4B: Fly.io Cloud Deployment (8 tasks, ~12 hours)

#### TASK-408: Create fly.toml configuration
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-403
**Description:** Create `fly.toml` with 512MB memory, health checks, proper scaling config (`min_machines_running=1`).

#### TASK-409: Set up Fly.io account and CLI
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None
**Description:** Install `flyctl`, authenticate, verify account access.

#### TASK-410: Configure environment variables
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-408
**Description:** Set up Fly.io secrets for any required environment variables (SECRET_KEY, etc.).

#### TASK-411: Initial Fly.io deployment
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-409, TASK-410
**Description:** Run `flyctl launch`, review config, deploy with `flyctl deploy`, monitor logs.

#### TASK-412: Verify deployment and health checks
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-411
**Description:** Test public URL, verify health endpoint, check Fly.io dashboard metrics, validate cold start time.

#### TASK-413: Test all endpoints on production
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-412
**Description:** Test `/docs`, `/health`, `/mcp`, `/gradio` from public URL. Verify MCP tools work via remote client.

#### TASK-414: Configure custom domain (optional)
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-412
**Description:** Set up custom domain in Fly.io, configure DNS, verify SSL certificate.

#### TASK-415: Create Fly.io deployment documentation
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-413
**Description:** Write `docs/FLY_IO_DEPLOYMENT.md` with step-by-step deployment guide, CI/CD setup, rollback procedures.

---

### Phase 5: Production Hardening (14 tasks, ~22 hours)

#### TASK-501: Create security module skeleton
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None
**Description:** Create `src/expo_smooth_mcp/security.py` with imports and module structure.

#### TASK-502: Install security dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None
**Description:** Add `python-jose[cryptography]`, `passlib[bcrypt]` to requirements.

#### TASK-503: Implement password hashing utilities
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-502
**Description:** Create password hashing functions using bcrypt in `security.py`.

#### TASK-504: Implement JWT token creation
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-502
**Description:** Create `create_access_token()` function with expiration handling.

#### TASK-505: Implement token validation dependency
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-504
**Description:** Create `get_current_user()` FastAPI dependency for JWT validation.

#### TASK-506: Create /token authentication endpoint
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-505
**Description:** Implement OAuth2 password flow `/token` endpoint with user authentication.

#### TASK-507: Protect API endpoints with auth
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-506
**Description:** Add authentication dependencies to protected endpoints (`/api/forecast`, etc.).

#### TASK-508: Install rate limiting dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None
**Description:** Add `fastapi-limiter`, `redis` to requirements. Document Redis setup.

#### TASK-509: Set up Redis connection
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-508
**Description:** Configure Redis connection in startup event, handle connection errors gracefully.

#### TASK-510: Implement rate limiting middleware
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-509
**Description:** Initialize FastAPILimiter, configure rate limits per endpoint (global and per-user).

#### TASK-511: Create structured logging formatter
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** None
**Description:** Implement JSON logging formatter with timestamp, level, module, request ID fields.

#### TASK-512: Add request logging middleware
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-511
**Description:** Create FastAPI middleware to log all requests with method, path, status, duration.

#### TASK-513: Add Prometheus metrics endpoint
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** None
**Description:** Install and configure `prometheus-fastapi-instrumentator`, expose `/metrics` endpoint.

#### TASK-514: Create comprehensive security tests
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-507, TASK-510
**Description:** Write tests for authentication, rate limiting, protected endpoints in `tests/test_security.py`.

---

### Phase 6: Documentation & Testing (10 tasks, ~16 hours)

#### TASK-601: Update README.md
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-415
**Description:** Rewrite README with new architecture diagram, installation instructions, both deployment options.

#### TASK-602: Update DEPLOYMENT_GUIDE.md
**Estimated Time:** 1.5 hours | **Complexity:** Low | **Dependencies:** TASK-407, TASK-415
**Description:** Replace HF Spaces guide with dual deployment guide (Docker MCP Toolkit + Fly.io).

#### TASK-603: Create client integration guide
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-406
**Description:** Write guide for configuring MCP clients (Claude Desktop, Cursor, VS Code) for both stdio and HTTP.

#### TASK-604: Document API endpoints
**Estimated Time:** 1.5 hours | **Complexity:** Low | **Dependencies:** TASK-413
**Description:** Create comprehensive API documentation with examples for all REST and MCP endpoints.

#### TASK-605: Create troubleshooting guide
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-413
**Description:** Document common issues, solutions, debugging steps for both local and cloud deployments.

#### TASK-606: Create benchmark script
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-413
**Description:** Create `benchmark.py` to measure latency (p50, p95, p99) for both Gradio and FastMCP implementations.

#### TASK-607: Run performance benchmarks
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-606
**Description:** Execute benchmarks against local and production deployments, document results.

#### TASK-608: Create load testing suite
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-606
**Description:** Create `locustfile.py` for load testing, define realistic user scenarios.

#### TASK-609: Update all ADRs
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-607
**Description:** Update ADR-004 status to "Accepted", add actual benchmark results, update revision history.

#### TASK-610: Final E2E testing checklist
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-607
**Description:** Execute comprehensive E2E test plan, document results, verify all acceptance criteria met.

---

## 7. Task Summary by Phase

| Phase | Task Count | Total Hours | Parallelization Potential |
|-------|------------|-------------|--------------------------|
| Phase 1: Decouple Logic | 8 | ~12h | Low (sequential dependencies) |
| Phase 2: FastMCP Backend | 12 | ~20h | Medium (some parallel tracks) |
| Phase 3: Mount Gradio | 6 | ~8h | Low (sequential) |
| Phase 4A: Docker MCP Toolkit | 7 | ~10h | Medium (docs parallel to testing) |
| Phase 4B: Fly.io Deployment | 8 | ~12h | Medium (after 4A complete) |
| Phase 5: Production Hardening | 14 | ~22h | High (auth, rate limit, logging parallel) |
| Phase 6: Documentation | 10 | ~16h | High (most tasks independent) |
| **TOTAL** | **65 tasks** | **~100h** | **Potential: 60-70h with 2-3 devs** |

---

## 8. Task Assignment Guidelines

### For Solo Developer
- Work sequentially through phases
- Estimated timeline: 12-15 working days
- Focus on completing each phase before moving to next

### For 2 Developers
**Developer 1 (Backend Focus):**
- Phase 1: All logic tasks
- Phase 2: MCP implementation
- Phase 5: Security & rate limiting

**Developer 2 (Integration Focus):**
- Phase 3: Gradio mounting
- Phase 4: Docker & deployment
- Phase 6: Documentation & testing

**Estimated timeline: 7-10 working days**

### For 3 Developers
**Developer 1 (Core):**
- Phase 1: Business logic
- Phase 2: FastMCP backend

**Developer 2 (Infrastructure):**
- Phase 4A: Docker MCP Toolkit
- Phase 4B: Fly.io deployment

**Developer 3 (Quality):**
- Phase 3: Gradio integration
- Phase 5: Production hardening
- Phase 6: Documentation

**Estimated timeline: 5-7 working days**

---

## 9. Future Enhancements (Post-v2.0 Backlog)

These are ideas for future iterations of the project:

*   **Model Parameter Tuning:** Add API endpoints to adjust Holt-Winters parameters (`alpha`, `beta`, `gamma`).
*   **Display Accuracy Metrics:** Calculate and return forecast accuracy metrics (MAPE, RMSE) in API responses.
*   **Comparative Model Visualization:** Support multiple forecasting models via MCP tools.
*   **Multi-tenancy:** Add organization/workspace support with isolated data.
*   **Caching Layer:** Implement Redis caching for frequently requested forecasts.
*   **Async Forecasting:** Support long-running forecasts with job queue (Celery/Redis).
*   **Custom UI:** Replace Gradio with React/Vue.js frontend.