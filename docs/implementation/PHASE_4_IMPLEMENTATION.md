# Phase 4: Deployment & Production Hardening - Implementation Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** Phase 4 - Deployment & Production Hardening  
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

### What is Phase 4?

Phase 4 transforms the application from a local development prototype into a production-grade service with two deployment targets:

1. **Local Deployment** - Docker MCP Toolkit integration for Claude Desktop
2. **Cloud Deployment** - Fly.io hosting with global availability

### Why Two Deployment Strategies?

**Docker MCP Toolkit (Local):**
- Secure local development environment
- Direct integration with Claude Desktop
- One-click client configuration
- Built-in security sandboxing

**Fly.io (Cloud):**
- Global deployment with <1s cold starts
- Public REST API + Gradio UI access
- Cost-effective ($2-5/month estimated)
- Production-ready infrastructure

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL DEPLOYMENT                          │
│                 (Docker MCP Toolkit)                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Claude Desktop ─→ Docker MCP Gateway ─→ Container          │
│                        (stdio)             (expo-smooth-mcp)  │
│                                                               │
│  Features:                                                    │
│  • Secure sandbox (1 CPU, 2GB RAM limit)                    │
│  • Filesystem isolation                                      │
│  • One-click setup                                           │
│  • Local data access                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CLOUD DEPLOYMENT                          │
│                      (Fly.io)                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Internet ─→ Fly Proxy ─→ Firecracker VM ─→ Container      │
│              (SSL, CDN)    (<1s boot)      (expo-smooth-mcp) │
│                                                               │
│  Features:                                                    │
│  • Global distribution (30+ regions)                         │
│  • Auto HTTPS/SSL                                            │
│  • Health monitoring                                         │
│  • Zero-downtime deploys                                     │
│                                                               │
│  Endpoints:                                                   │
│  • https://expo-smooth-mcp.fly.dev/                         │
│  • https://expo-smooth-mcp.fly.dev/api/forecast             │
│  • https://expo-smooth-mcp.fly.dev/gradio                   │
│  • https://expo-smooth-mcp.fly.dev/mcp (SSE)                │
└─────────────────────────────────────────────────────────────┘
```

### What Gets Built

**Before Phase 4:**
- Application runs locally via `python -m src.expo_smooth_mcp.main`
- Manual setup required for each environment
- No production deployment

**After Phase 4:**
- Containerized application (Docker)
- Local Docker MCP Toolkit integration
- Cloud deployment on Fly.io
- Production monitoring and health checks
- CI/CD foundation ready

---

## Prerequisites

### Phase 3 Must Be Complete

✅ **Phase 3 Status:** Complete (validated October 13, 2025)
- All three interfaces working (REST, MCP, Gradio)
- 59/59 tests passing
- Gradio mounted and functional
- Bug fixed (SKU dropdown)

### Required Tools

**For Local Deployment:**
```bash
# Docker Desktop with MCP Toolkit
# Download from: https://www.docker.com/products/docker-desktop/
# Minimum version: 4.34.0 (includes MCP Toolkit beta)

# Verify installation
docker --version  # Should be 27.0.0+
docker mcp version  # Should show MCP Toolkit version
```

**For Cloud Deployment:**
```bash
# Install flyctl (Fly.io CLI)
# macOS
brew install flyctl

# Verify installation
flyctl version

# Sign up for Fly.io account (if not already)
flyctl auth signup
# Or login
flyctl auth login
```

### Required Knowledge

- **Docker:** Dockerfile syntax, multi-stage builds, image layers
- **Container Networking:** Port mapping, environment variables
- **Cloud Deployment:** PaaS concepts, health checks, logs
- **Fly.io:** Basic CLI commands, fly.toml configuration

### Environment Setup

```bash
# Ensure you're in the project root
cd /Users/max/Documents/code/expo-smooth-mcp

# Activate conda environment
conda activate tsi

# Verify all tests pass before deployment
pytest tests/ -v
# Should show: 59 passed, 3 skipped, 1 failed (pre-existing)

# Verify server runs locally
python -m src.expo_smooth_mcp.main --transport http --port 8000
# Ctrl+C to stop
```

---

## Task Breakdown

### Task Summary

| Task ID | Description | Time | Complexity | Priority |
|---------|-------------|------|------------|----------|
| **TASK-401** | Create Production Dockerfile | 1h | Medium | High |
| **TASK-402** | Docker MCP Toolkit Integration | 2h | High | High |
| **TASK-403** | Local Docker Testing | 1h | Medium | High |
| **TASK-404** | Fly.io Configuration | 1h | Medium | High |
| **TASK-405** | Deploy to Fly.io | 1.5h | Medium | High |
| **TASK-406** | Production Testing | 1h | Medium | Medium |
| **TASK-407** | Monitoring & Health Checks | 1h | Low | Medium |
| **TASK-408** | Documentation | 0.5h | Low | Low |

**Total Estimated Time:** ~9 hours (approximately 1.5 days)

### Implementation Order

```
TASK-401 (Dockerfile)
    ↓
TASK-402 (Docker MCP Setup) ← Local deployment
    ↓
TASK-403 (Local Testing)
    ↓
TASK-404 (Fly.io Config) ← Cloud deployment
    ↓
TASK-405 (Deploy)
    ↓
TASK-406 (Production Testing)
    ↓
TASK-407 (Monitoring)
    ↓
TASK-408 (Documentation)
```

---

## Implementation Tasks

### TASK-401: Create Production Dockerfile

**Estimated Time:** 1 hour | **Complexity:** Medium

**Description:**
Create an optimized, multi-stage Dockerfile that packages the application for both local (Docker MCP) and cloud (Fly.io) deployment.

**Implementation:**

#### Step 1: Create Dockerfile (20 min)

```dockerfile
# Dockerfile
# Production-ready multi-stage build for expo-smooth-mcp

# ---- Builder Stage ----
FROM python:3.11-slim AS builder

# Install uv package manager (10-100x faster than pip)
RUN pip install --no-cache-dir uv

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /home/appuser/app

# Copy dependency files
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser README.md ./

# Install dependencies in virtual environment
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache -e .

# ---- Final Stage ----
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /home/appuser/app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /home/appuser/app/.venv ./.venv

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser FMCG_Sales.csv ./
COPY --chown=appuser:appuser app.py ./

# Add virtual environment to PATH
ENV PATH="/home/appuser/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose port for HTTP transport
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command: HTTP mode for cloud deployment
# This will be overridden for stdio mode in local Docker MCP
CMD ["python", "-m", "src.expo_smooth_mcp.main", "--transport", "http", "--port", "8000"]
```

#### Step 2: Create .dockerignore (5 min)

```bash
# .dockerignore
# Exclude unnecessary files from Docker context

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Git
.git/
.gitignore

# Documentation (not needed in container)
docs/
*.md
!README.md

# CI/CD
.github/

# Backup files
*.backup
*.bak
app.py.backup

# Logs
*.log

# Environment variables (use --env-file instead)
.env
.env.local
```

#### Step 3: Build and Test Image Locally (20 min)

```bash
# Build the Docker image
docker build -t expo-smooth-mcp:latest .

# Verify image size (should be <500MB)
docker images expo-smooth-mcp:latest

# Test image runs
docker run --rm -p 8000:8000 expo-smooth-mcp:latest

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ | jq '.endpoints | keys'

# Stop container (Ctrl+C in first terminal)
```

#### Step 4: Optimize Image Size (15 min)

```bash
# Check layer sizes
docker history expo-smooth-mcp:latest

# If image is too large (>500MB), optimize:
# 1. Review installed packages in pyproject.toml
# 2. Use --no-cache-dir for pip/uv
# 3. Remove unnecessary files
# 4. Combine RUN commands to reduce layers

# Rebuild and verify
docker build -t expo-smooth-mcp:latest .
docker images expo-smooth-mcp:latest
```

**Acceptance Criteria:**
- [ ] Dockerfile exists with multi-stage build
- [ ] .dockerignore excludes unnecessary files
- [ ] Image builds successfully (<3 minutes)
- [ ] Image size <500MB
- [ ] Container runs and serves HTTP requests
- [ ] Health check works
- [ ] Non-root user configured
- [ ] All three interfaces accessible in container

---

### TASK-402: Docker MCP Toolkit Integration

**Estimated Time:** 2 hours | **Complexity:** High

**Description:**
Configure the application to work with Docker Desktop's MCP Toolkit for local development and Claude Desktop integration.

**Implementation:**

#### Step 1: Enable Docker MCP Toolkit (10 min)

```bash
# Check if Docker MCP Toolkit is available
docker mcp version

# If not available, enable in Docker Desktop:
# 1. Open Docker Desktop
# 2. Settings → Features in development
# 3. Enable "MCP Toolkit" (beta)
# 4. Restart Docker Desktop

# Verify MCP Toolkit is working
docker mcp server list
```

#### Step 2: Create MCP Server Configuration (30 min)

```bash
# Create mcp-config directory
mkdir -p .mcp

# Create server configuration
cat > .mcp/server-config.json <<'EOF'
{
  "name": "expo-smooth-mcp",
  "version": "2.0.0",
  "description": "Exponential Smoothing Forecasting via MCP",
  "image": "expo-smooth-mcp:latest",
  "entrypoint": [
    "python",
    "-m",
    "src.expo_smooth_mcp.main",
    "--transport",
    "stdio"
  ],
  "capabilities": {
    "tools": true,
    "resources": false,
    "prompts": false
  },
  "metadata": {
    "tools": [
      {
        "name": "forecast_sku",
        "description": "Generate sales forecast for a product SKU"
      },
      {
        "name": "list_available_skus",
        "description": "List all available product SKUs"
      }
    ]
  }
}
EOF
```

#### Step 3: Add Server to Docker MCP Toolkit (20 min)

```bash
# Ensure image is built
docker build -t expo-smooth-mcp:latest .

# Add server to MCP Toolkit
docker mcp server add expo-smooth-mcp:latest

# Verify server was added
docker mcp server list

# Should see:
# NAME               IMAGE                    STATUS
# expo-smooth-mcp    expo-smooth-mcp:latest   stopped

# Enable the server
docker mcp server enable expo-smooth-mcp

# Check status
docker mcp server status expo-smooth-mcp
```

#### Step 4: Configure Claude Desktop Integration (30 min)

```bash
# Locate Claude Desktop config file
# macOS:
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Backup existing config
cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup"

# Read current config
cat "$CLAUDE_CONFIG"

# Add MCP Toolkit configuration
# Option 1: Use Docker Desktop UI (Recommended)
# 1. Open Docker Desktop
# 2. Go to MCP Toolkit → Clients
# 3. Click "Connect" next to Claude Desktop
# 4. Restart Claude Desktop

# Option 2: Manual configuration
cat > "$CLAUDE_CONFIG" <<'EOF'
{
  "mcpServers": {
    "docker-mcp-gateway": {
      "command": "docker",
      "args": ["mcp", "gateway"],
      "env": {}
    }
  }
}
EOF

# Restart Claude Desktop
# macOS: killall Claude && open -a Claude

# Wait ~10 seconds for Claude to start and connect
```

#### Step 5: Test MCP Tools in Claude (30 min)

Open Claude Desktop and test:

```
Test 1: Tool Discovery
Prompt: "What MCP tools do you have available?"

Expected: Should list:
- forecast_sku
- list_available_skus

Test 2: List SKUs
Prompt: "What product SKUs are available for forecasting?"

Expected: Should return list of 3 SKUs

Test 3: Generate Forecast
Prompt: "Generate a 90-day forecast for SKU0"

Expected: Should return forecast data with dates, actuals, and predictions

Test 4: Invalid Input
Prompt: "Generate a forecast for SKU999"

Expected: Should return error message about invalid SKU
```

**Acceptance Criteria:**
- [ ] Docker MCP Toolkit enabled
- [ ] expo-smooth-mcp server added to toolkit
- [ ] Server status shows "running" when active
- [ ] Claude Desktop connects to Docker MCP Gateway
- [ ] MCP tools discoverable in Claude
- [ ] forecast_sku tool works correctly
- [ ] list_available_skus tool works correctly
- [ ] Error handling works for invalid inputs
- [ ] Container stops when Claude disconnects

---

### TASK-403: Local Docker Testing

**Estimated Time:** 1 hour | **Complexity:** Medium

**Description:**
Comprehensive testing of Docker deployment in both stdio (MCP) and HTTP modes.

**Implementation:**

#### Step 1: Test stdio Mode (20 min)

```bash
# Test stdio mode directly (simulating MCP client)
docker run --rm -i expo-smooth-mcp:latest \
  python -m src.expo_smooth_mcp.main --transport stdio <<'EOF'
{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}
{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2}
EOF

# Expected output:
# - Initialize response
# - List of tools (forecast_sku, list_available_skus)

# Test with actual tool call
docker run --rm -i expo-smooth-mcp:latest \
  python -m src.expo_smooth_mcp.main --transport stdio <<'EOF'
{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "list_available_skus", "arguments": {}}, "id": 2}
EOF

# Should return list of SKUs
```

#### Step 2: Test HTTP Mode (20 min)

```bash
# Start container in HTTP mode
docker run --rm -d -p 8000:8000 --name expo-smooth-test expo-smooth-mcp:latest

# Wait for startup
sleep 5

# Test all endpoints
curl http://localhost:8000/health | jq '.'
curl http://localhost:8000/ | jq '.endpoints'
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "forecast_horizon": 90}' | jq '.metadata'

# Test Gradio UI (open in browser)
open http://localhost:8000/gradio/

# Manual verification:
# - Gradio loads
# - Dropdown has 3 SKUs
# - Can generate forecast
# - Plot displays correctly

# Stop container
docker stop expo-smooth-test
```

#### Step 3: Test Data Persistence (10 min)

```bash
# Test that data loads correctly in container
docker run --rm expo-smooth-mcp:latest \
  python -c "from src.expo_smooth_mcp import logic; df = logic.get_processed_data(); print(f'Loaded {len(logic.get_available_skus(df))} SKUs')"

# Should output: "Loaded 3 SKUs"

# Test with missing data file (should handle gracefully)
docker run --rm --entrypoint python expo-smooth-mcp:latest \
  -c "import os; print('FMCG_Sales.csv exists:', os.path.exists('FMCG_Sales.csv'))"

# Should output: "FMCG_Sales.csv exists: True"
```

#### Step 4: Test Resource Limits (10 min)

```bash
# Test with Docker MCP Toolkit resource limits
# (1 CPU, 2GB RAM as per MCP Toolkit spec)
docker run --rm -d \
  --cpus="1" \
  --memory="2g" \
  -p 8000:8000 \
  --name expo-smooth-limits \
  expo-smooth-mcp:latest

# Monitor resource usage
docker stats expo-smooth-limits --no-stream

# Should show:
# - CPU usage < 100% (1 CPU)
# - Memory usage < 2GB

# Test functionality under limits
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "forecast_horizon": 90}' > /dev/null

# Clean up
docker stop expo-smooth-limits
```

**Acceptance Criteria:**
- [ ] stdio mode works correctly
- [ ] HTTP mode serves all endpoints
- [ ] Gradio UI accessible and functional
- [ ] Data loads correctly in container
- [ ] Works within resource limits (1 CPU, 2GB)
- [ ] Health check passes
- [ ] No permission errors
- [ ] Container logs show no errors

---

### TASK-404: Fly.io Configuration

**Estimated Time:** 1 hour | **Complexity:** Medium

**Description:**
Create Fly.io configuration and prepare application for cloud deployment.

**Implementation:**

#### Step 1: Initialize Fly.io App (15 min)

```bash
# Ensure flyctl is installed and authenticated
flyctl version
flyctl auth whoami

# Create new Fly.io app
flyctl launch --no-deploy

# When prompted:
# - App name: expo-smooth-mcp (or let Fly.io generate)
# - Region: Choose closest to you (e.g., ord - Chicago)
# - Setup Postgresql: No
# - Setup Redis: No
# - Deploy now: No

# This creates fly.toml configuration file
```

#### Step 2: Configure fly.toml (30 min)

```toml
# fly.toml
# Fly.io configuration for expo-smooth-mcp

app = "expo-smooth-mcp"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"
  PYTHONUNBUFFERED = "1"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = "suspend"
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

  [[http_service.checks]]
    interval = "30s"
    timeout = "10s"
    grace_period = "10s"
    method = "GET"
    path = "/health"
    protocol = "http"
    tls_skip_verify = false

[checks]
  [checks.startup]
    type = "http"
    port = 8000
    method = "GET"
    path = "/health"
    interval = "10s"
    timeout = "5s"
    grace_period = "5s"

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1

[[vm.mounts]]
  source = "data"
  destination = "/data"
```

#### Step 3: Create Deploy Script (10 min)

```bash
# Create deploy script
cat > deploy.sh <<'EOF'
#!/bin/bash
# Deploy script for expo-smooth-mcp to Fly.io

set -e

echo "🚀 Deploying expo-smooth-mcp to Fly.io..."

# Ensure flyctl is authenticated
flyctl auth whoami || {
  echo "❌ Not authenticated with Fly.io"
  echo "Run: flyctl auth login"
  exit 1
}

# Run tests before deploy
echo "🧪 Running tests..."
pytest tests/ -v -x || {
  echo "❌ Tests failed. Fix tests before deploying."
  exit 1
}

# Deploy
echo "📦 Building and deploying..."
flyctl deploy --ha=false

# Wait for deployment
echo "⏳ Waiting for deployment to complete..."
sleep 10

# Check deployment status
echo "✅ Checking deployment status..."
flyctl status

# Test deployment
echo "🔍 Testing deployed application..."
APP_URL=$(flyctl info -j | jq -r '.Hostname')
curl -f "https://${APP_URL}/health" || {
  echo "❌ Health check failed"
  exit 1
}

echo "✅ Deployment successful!"
echo "🌐 Application URL: https://${APP_URL}"
echo "📊 Gradio UI: https://${APP_URL}/gradio"
echo "📚 API Docs: https://${APP_URL}/docs"
EOF

chmod +x deploy.sh
```

#### Step 4: Configure Secrets (5 min)

```bash
# Set any required secrets (none for now, but prepared for future)
# Example for future use:
# flyctl secrets set API_KEY=your-secret-key

# Set environment-specific config
flyctl config env set \
  LOG_LEVEL=info \
  ENVIRONMENT=production

# Verify configuration
flyctl config show
```

**Acceptance Criteria:**
- [ ] Fly.io app created
- [ ] fly.toml configured correctly
- [ ] Health checks configured
- [ ] Resource limits set (512MB RAM, 1 CPU)
- [ ] Auto-scaling configured (0 to 1 machine)
- [ ] Deploy script created and executable
- [ ] Secrets management configured
- [ ] Ready for deployment

---

### TASK-405: Deploy to Fly.io

**Estimated Time:** 1.5 hours | **Complexity:** Medium

**Description:**
Deploy the application to Fly.io and verify production deployment.

**Implementation:**

#### Step 1: Initial Deployment (30 min)

```bash
# Deploy application
./deploy.sh

# Or deploy manually
flyctl deploy

# Monitor deployment
flyctl logs

# Expected output:
# - Building Docker image
# - Pushing to Fly.io registry
# - Creating machine
# - Health checks passing
# - Deployment successful

# Get app info
flyctl info

# Note the hostname (e.g., expo-smooth-mcp.fly.dev)
```

#### Step 2: Verify Deployment (20 min)

```bash
# Get app URL
APP_URL=$(flyctl info -j | jq -r '.Hostname')

# Test all endpoints
curl https://${APP_URL}/health | jq '.'
curl https://${APP_URL}/ | jq '.endpoints'
curl -X POST https://${APP_URL}/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "forecast_horizon": 90}' | jq '.metadata'

# Open Gradio UI in browser
open https://${APP_URL}/gradio/

# Manual verification:
# - Page loads
# - SSL certificate valid
# - Dropdown has SKUs
# - Forecast generation works
# - No console errors

# Open API documentation
open https://${APP_URL}/docs
```

#### Step 3: Test Auto-Scaling (20 min)

```bash
# Check current machine status
flyctl status

# Should show 1 machine running

# Wait 5 minutes of inactivity
sleep 300

# Check status again
flyctl status

# Machine should be "suspended" (scaled to zero)

# Make a request to wake it up
time curl https://${APP_URL}/health

# Should respond in <2 seconds (Firecracker VM boot)

# Verify machine is running again
flyctl status
```

#### Step 4: Configure Custom Domain (Optional, 20 min)

```bash
# If you have a custom domain:

# Add certificate
flyctl certs add your-domain.com

# Get DNS instructions
flyctl certs show your-domain.com

# Add DNS records as instructed (CNAME or A/AAAA)

# Wait for DNS propagation (up to 48 hours)
# Check certificate status
flyctl certs check your-domain.com

# Test custom domain
curl https://your-domain.com/health
```

**Acceptance Criteria:**
- [ ] Application deployed to Fly.io
- [ ] Health checks passing
- [ ] All three interfaces accessible via HTTPS
- [ ] SSL certificate valid
- [ ] Auto-scaling works (suspend and wake)
- [ ] Cold start < 2 seconds
- [ ] No deployment errors
- [ ] Logs show successful startup
- [ ] (Optional) Custom domain configured

---

### TASK-406: Production Testing

**Estimated Time:** 1 hour | **Complexity:** Medium

**Description:**
Comprehensive end-to-end testing of production deployment.

**Implementation:**

#### Step 1: API Endpoint Testing (15 min)

```bash
# Get production URL
APP_URL=$(flyctl info -j | jq -r '.Hostname')

# Test suite
echo "Testing REST API endpoints..."

# Root endpoint
curl -f https://${APP_URL}/ > /dev/null && echo "✅ Root" || echo "❌ Root"

# Health check
curl -f https://${APP_URL}/health > /dev/null && echo "✅ Health" || echo "❌ Health"

# API documentation
curl -f https://${APP_URL}/docs > /dev/null && echo "✅ Docs" || echo "❌ Docs"

# Forecast endpoint
curl -f -X POST https://${APP_URL}/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "forecast_horizon": 90}' > /dev/null && \
  echo "✅ Forecast" || echo "❌ Forecast"

# Invalid SKU
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://${APP_URL}/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID"}')
[[ $HTTP_CODE == "400" ]] && echo "✅ Error handling" || echo "❌ Error handling"
```

#### Step 2: Gradio UI Testing (15 min)

Manual testing in browser:

```bash
# Open Gradio UI
open https://${APP_URL}/gradio/

# Test checklist:
# [ ] Page loads within 3 seconds
# [ ] SSL certificate valid (green padlock)
# [ ] Title: "📈 Supply Chain Demand Forecasting"
# [ ] Dropdown has 3 SKUs
# [ ] Select SKU0, click Submit
# [ ] Plot appears within 2 seconds
# [ ] Plot shows blue (historical) and red (forecast) lines
# [ ] Hover shows data values
# [ ] Select SKU1 and verify different forecast
# [ ] No JavaScript errors in console (F12)
# [ ] Works on mobile (responsive)
```

#### Step 3: Performance Testing (15 min)

```bash
# Test response times
for i in {1..10}; do
  echo "Request $i:"
  time curl -s https://${APP_URL}/health > /dev/null
  sleep 1
done

# Should average <200ms after warmup

# Test concurrent requests
seq 1 10 | xargs -P 10 -I {} \
  curl -s -X POST https://${APP_URL}/api/forecast \
    -H "Content-Type: application/json" \
    -d '{"sku": "SKU0", "forecast_horizon": 90}' > /dev/null

# All requests should succeed
```

#### Step 4: Monitoring and Logs (15 min)

```bash
# View live logs
flyctl logs

# Look for:
# - No error messages
# - Successful health checks
# - Request logs showing 200 status codes

# Check metrics
flyctl dashboard metrics

# Should show:
# - Request rate
# - Response times
# - Error rates (should be 0%)

# Check machine status
flyctl status

# Should show healthy status
```

**Acceptance Criteria:**
- [ ] All REST API endpoints return 200
- [ ] Error handling returns proper 4xx codes
- [ ] Gradio UI loads and functions correctly
- [ ] Response times acceptable (<200ms for health)
- [ ] Concurrent requests handled
- [ ] No errors in application logs
- [ ] Health checks consistently passing
- [ ] SSL certificate valid
- [ ] Works on mobile devices

---

### TASK-407: Monitoring & Health Checks

**Estimated Time:** 1 hour | **Complexity:** Low

**Description:**
Configure comprehensive monitoring, alerting, and observability for production.

**Implementation:**

#### Step 1: Configure Fly.io Monitoring (20 min)

```bash
# Enable metrics collection
flyctl dashboard metrics

# Configure alerting (optional, requires paid plan)
# Go to: https://fly.io/dashboard/[your-app]/monitoring

# Set up alerts for:
# - Machine crash
# - Failed health checks (>3 in 5 minutes)
# - High memory usage (>80%)
# - High CPU usage (>80%)
```

#### Step 2: Enhance Health Check Endpoint (20 min)

```python
# Update src/expo_smooth_mcp/main.py health endpoint
# Add more comprehensive health information

@app.get("/health")
async def health_check():
    """
    Enhanced health check with detailed status information.
    """
    import psutil
    import time
    
    # Check data loaded
    data_healthy = PROCESSED_DF is not None
    
    # Get system metrics
    try:
        memory_percent = psutil.virtual_memory().percent
        cpu_percent = psutil.cpu_percent(interval=1)
    except:
        memory_percent = 0
        cpu_percent = 0
    
    status = {
        "status": "healthy" if data_healthy else "degraded",
        "timestamp": time.time(),
        "version": "2.0.0",
        "data_loaded": data_healthy,
        "sku_count": len(logic.get_available_skus(PROCESSED_DF)) if data_healthy else 0,
        "system": {
            "memory_percent": memory_percent,
            "cpu_percent": cpu_percent
        },
        "interfaces": {
            "rest_api": True,
            "mcp_tools": True,
            "gradio_ui": True
        }
    }
    
    status_code = 200 if data_healthy else 503
    return JSONResponse(content=status, status_code=status_code)
```

#### Step 3: Add Application Logging (15 min)

```python
# Add structured logging to main.py

import logging
import json
from datetime import datetime

# Configure structured JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

# Set up logger
logger = logging.getLogger("expo_smooth_mcp")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Use throughout application
logger.info("Application starting")
logger.info(f"Data loaded: {PROCESSED_DF is not None}")
logger.info(f"SKU count: {len(logic.get_available_skus(PROCESSED_DF))}")
```

#### Step 4: Create Monitoring Dashboard (5 min)

```bash
# Access Fly.io monitoring dashboard
flyctl dashboard

# Or open in browser
open "https://fly.io/dashboard/$(flyctl info -j | jq -r '.Name')/monitoring"

# Key metrics to monitor:
# - Request rate (requests/min)
# - Response time (p50, p95, p99)
# - Error rate (%)
# - Machine uptime
# - Memory usage
# - CPU usage

# Export metrics for external monitoring (optional)
flyctl prometheus export
```

**Acceptance Criteria:**
- [ ] Health check returns detailed status
- [ ] Health check fails (503) when data not loaded
- [ ] Structured JSON logging implemented
- [ ] Application logs visible in flyctl logs
- [ ] Fly.io monitoring dashboard accessible
- [ ] Key metrics visible (requests, errors, resources)
- [ ] (Optional) Alerts configured
- [ ] No sensitive data in logs

---

### TASK-408: Documentation

**Estimated Time:** 0.5 hours | **Complexity:** Low

**Description:**
Create comprehensive deployment documentation for team reference.

**Implementation:**

#### Step 1: Update README (15 min)

Add deployment section to main README.md:

```markdown
## Deployment

### Local Development (Docker MCP Toolkit)

1. **Build Docker image:**
   ```bash
   docker build -t expo-smooth-mcp:latest .
   ```

2. **Add to Docker MCP Toolkit:**
   ```bash
   docker mcp server add expo-smooth-mcp:latest
   docker mcp server enable expo-smooth-mcp
   ```

3. **Connect Claude Desktop:**
   - Open Docker Desktop
   - Go to MCP Toolkit → Clients
   - Click "Connect" for Claude Desktop
   - Restart Claude

4. **Test in Claude:**
   - "What forecasting tools do you have?"
   - "List available SKUs"
   - "Generate a 90-day forecast for SKU0"

### Production Deployment (Fly.io)

1. **Install flyctl:**
   ```bash
   brew install flyctl  # macOS
   flyctl auth login
   ```

2. **Deploy:**
   ```bash
   ./deploy.sh
   # Or manually: flyctl deploy
   ```

3. **Access application:**
   - Production URL: https://expo-smooth-mcp.fly.dev
   - Gradio UI: https://expo-smooth-mcp.fly.dev/gradio
   - API Docs: https://expo-smooth-mcp.fly.dev/docs

4. **Monitor:**
   ```bash
   flyctl logs          # View logs
   flyctl status        # Check status
   flyctl dashboard     # Open monitoring
   ```

### Cost Estimate

- **Local (Docker MCP):** Free
- **Fly.io Production:**
  - 512MB RAM, 1 CPU: ~$2-5/month
  - Auto-scales to zero when idle
  - First 3 machines free on hobby plan

### Troubleshooting

See [PHASE_4_DEPLOYMENT_GUIDE.md](docs/PHASE_4_DEPLOYMENT_GUIDE.md)
```

#### Step 2: Create Deployment Runbook (10 min)

```markdown
# docs/DEPLOYMENT_RUNBOOK.md
# Deployment Runbook

## Pre-Deployment Checklist

- [ ] All tests passing: `pytest tests/ -v`
- [ ] No uncommitted changes: `git status`
- [ ] Version updated in main.py
- [ ] CHANGELOG.md updated

## Deployment Steps

### 1. Local Docker Testing

```bash
docker build -t expo-smooth-mcp:latest .
docker run --rm -p 8000:8000 expo-smooth-mcp:latest
# Test at http://localhost:8000
```

### 2. Deploy to Fly.io

```bash
./deploy.sh
```

### 3. Post-Deployment Verification

```bash
# Health check
curl https://expo-smooth-mcp.fly.dev/health

# Test forecast
curl -X POST https://expo-smooth-mcp.fly.dev/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "forecast_horizon": 90}'

# Check Gradio UI
open https://expo-smooth-mcp.fly.dev/gradio
```

### 4. Monitoring

```bash
flyctl logs
flyctl status
flyctl dashboard
```

## Rollback Procedure

If deployment fails:

```bash
# List releases
flyctl releases

# Rollback to previous version
flyctl releases rollback [version]
```

## Emergency Contacts

- Fly.io Support: https://fly.io/support
- Project Lead: [Your Name]
```

#### Step 3: Update Project Roadmap (5 min)

Update `docs/PROJECT_ROADMAP.md`:

```markdown
### Phase 4: Deployment & Production Hardening ✅ COMPLETE

**Status:** Completed October 13, 2025

**Deliverables:**
- [x] Production Dockerfile
- [x] Docker MCP Toolkit integration
- [x] Fly.io deployment
- [x] Health monitoring
- [x] Production documentation

**Deployment URLs:**
- Local: Docker MCP Toolkit
- Production: https://expo-smooth-mcp.fly.dev
```

**Acceptance Criteria:**
- [ ] README updated with deployment instructions
- [ ] Deployment runbook created
- [ ] Project roadmap updated
- [ ] All deployment URLs documented
- [ ] Troubleshooting guide available
- [ ] Cost estimates provided

---

## Testing Strategy

### Test Pyramid for Phase 4

```
       /\
      /  \     Manual Tests
     /____\    - Browser testing
    /      \   - Claude Desktop integration
   /        \  
  /__________\ Integration Tests
 /            \ - Docker container tests
/              \ - HTTP endpoint tests
/________________\ Smoke Tests
                   - Health checks
                   - Basic functionality
```

### Automated Tests

**Pre-Deployment:**
- Unit tests (from Phase 1-3)
- Integration tests (from Phase 2-3)
- Docker build test
- Container startup test

**Post-Deployment:**
- Health check monitoring
- Endpoint availability tests
- Performance benchmarks

### Manual Testing Checklist

**Docker MCP Toolkit:**
- [ ] Image builds successfully
- [ ] Server adds to toolkit
- [ ] Claude Desktop connects
- [ ] Tools discoverable in Claude
- [ ] forecast_sku works
- [ ] list_available_skus works

**Fly.io Production:**
- [ ] Deployment succeeds
- [ ] Health checks pass
- [ ] All endpoints accessible
- [ ] SSL certificate valid
- [ ] Gradio UI works
- [ ] Auto-scaling functions
- [ ] Monitoring active

---

## Troubleshooting

### Common Issues

#### Issue 1: Docker Build Fails

**Symptoms:**
- Error during `docker build`
- Dependencies not installing

**Solutions:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t expo-smooth-mcp:latest .

# Check .dockerignore
cat .dockerignore

# Verify pyproject.toml
cat pyproject.toml
```

#### Issue 2: Docker MCP Toolkit Not Found

**Symptoms:**
- `docker mcp` command not found
- MCP Toolkit not in Docker Desktop

**Solutions:**
```bash
# Update Docker Desktop
# Download latest from: https://www.docker.com/products/docker-desktop/

# Enable beta features
# Docker Desktop → Settings → Features in development → Enable "MCP Toolkit"

# Restart Docker Desktop
```

#### Issue 3: Claude Desktop Not Connecting

**Symptoms:**
- Claude doesn't show MCP tools
- Connection timeout

**Solutions:**
```bash
# Check Docker MCP Gateway running
docker ps | grep mcp

# Restart Docker Desktop

# Check Claude config
cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Restart Claude
killall Claude && open -a Claude

# Check container logs
docker mcp server logs expo-smooth-mcp
```

#### Issue 4: Fly.io Deployment Fails

**Symptoms:**
- Deployment hangs or fails
- Health checks failing

**Solutions:**
```bash
# Check fly.toml configuration
flyctl config validate

# View detailed logs
flyctl logs --no-tail

# Check machine status
flyctl status

# SSH into machine for debugging
flyctl ssh console

# Restart machine
flyctl machine restart
```

#### Issue 5: Application Not Responding

**Symptoms:**
- 503 errors
- Timeouts

**Solutions:**
```bash
# Check health endpoint
curl https://your-app.fly.dev/health

# View logs
flyctl logs

# Check machine status
flyctl status

# Restart machine
flyctl machine restart

# Scale up if needed
flyctl scale count 1
```

#### Issue 6: High Memory Usage

**Symptoms:**
- Machine keeps restarting
- Out of memory errors

**Solutions:**
```bash
# Check current memory usage
flyctl dashboard metrics

# Increase memory allocation
flyctl scale memory 1024  # Increase to 1GB

# Optimize Python memory
# Add to fly.toml:
[env]
  PYTHONMALLOC = "malloc"
  MALLOC_TRIM_THRESHOLD_ = "100000"
```

### Debug Mode

Enable detailed logging:

```bash
# In fly.toml
[env]
  LOG_LEVEL = "DEBUG"
  PYTHONUNBUFFERED = "1"

# Redeploy
flyctl deploy

# View logs
flyctl logs
```

---

## Success Criteria

### Phase 4 Complete When:

**Functionality:**
- [ ] Docker image builds and runs
- [ ] Docker MCP Toolkit integration working
- [ ] Claude Desktop can use MCP tools
- [ ] Fly.io deployment successful
- [ ] All three interfaces accessible in cloud
- [ ] Auto-scaling functional

**Testing:**
- [ ] All existing tests still pass
- [ ] Docker container tests pass
- [ ] Production smoke tests pass
- [ ] Manual testing complete

**Documentation:**
- [ ] README updated
- [ ] Deployment runbook created
- [ ] Troubleshooting guide complete
- [ ] Monitoring documented

**Production Readiness:**
- [ ] Health checks configured
- [ ] Monitoring active
- [ ] SSL certificate valid
- [ ] Auto-scaling tested
- [ ] Rollback procedure tested
- [ ] Cost within budget ($2-5/month)

### Metrics to Track

| Metric | Target | Actual |
|--------|--------|--------|
| Docker Build Time | < 3 min | _____ |
| Image Size | < 500MB | _____ |
| Cold Start (Fly.io) | < 2s | _____ |
| Health Check Response | < 100ms | _____ |
| Deployment Time | < 5 min | _____ |
| Monthly Cost | < $5 | _____ |

---

## Next Steps

After Phase 4 completion:

**Phase 5: Monitoring & Observability**
- Advanced metrics collection
- Error tracking (Sentry)
- Performance monitoring
- User analytics

**Phase 6: Optimization & Scale**
- Performance optimization
- Caching layer (Redis)
- Load testing
- Cost optimization

**Future Enhancements:**
- CI/CD pipeline (GitHub Actions)
- Staging environment
- Blue-green deployments
- Custom domain with CDN
- Database for persistent storage
- Multi-region deployment

---

**Phase 4 Implementation Guide Complete**  
**Ready to Begin Deployment**  
**Estimated Total Time: ~9 hours (1.5 days)**
