# Phase 4: Quick Start Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** 4 - Deployment & Production Hardening  
**Version:** 1.0.0  
**Estimated Time:** 9 hours (1.5 days)

---

## Overview

Phase 4 focuses on deploying the MCP server to production using:
- **Docker MCP Toolkit** for local development with secure sandboxing
- **Fly.io** for cloud deployment with global availability

This guide provides a streamlined path to get your MCP server running in both environments.

---

## Prerequisites

### Local Environment
- ✅ Docker Desktop 4.34.0+ with MCP Toolkit enabled
- ✅ macOS 12.0+ (Monterey or later)
- ✅ 4GB RAM minimum, 10GB disk space

### Cloud Deployment
- ✅ Fly.io account (free tier available)
- ✅ flyctl CLI installed (`brew install flyctl`)
- ✅ Payment method added (required for custom domains, volumes)

### Completed Phases
- ✅ Phase 1: Backend logic implemented
- ✅ Phase 2: FastMCP + FastAPI integration
- ✅ Phase 3: Gradio UI mounted

---

## Quick Start: Docker MCP Toolkit (30 minutes)

### 1. Enable MCP Toolkit (5 min)

```bash
# Open Docker Desktop
open -a "Docker Desktop"

# Navigate to: Settings → Features in development
# Enable: "MCP Toolkit" (beta)
# Click: "Apply & restart"

# Verify MCP Toolkit is enabled
docker mcp version
```

### 2. Build Docker Image (10 min)

```bash
cd /Users/max/Documents/code/expo-smooth-mcp

# Build production image
docker build -t expo-smooth-mcp:latest .

# Verify build
docker images expo-smooth-mcp:latest
```

### 3. Add to MCP Toolkit (5 min)

```bash
# Add server to Docker MCP Toolkit
docker mcp server add expo-smooth-mcp:latest

# Enable the server
docker mcp server enable expo-smooth-mcp

# Verify status
docker mcp server status expo-smooth-mcp
```

### 4. Configure Claude Desktop (10 min)

**Automatic Configuration (Recommended):**
1. Open Docker Desktop
2. Navigate to: MCP Toolkit → Clients tab
3. Find "Claude Desktop" → Click "Connect"
4. Restart Claude Desktop

**Or Manual Configuration:**
```bash
# Backup existing config
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup"

# Add docker-mcp-gateway
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
killall Claude && sleep 2 && open -a Claude
```

### 5. Test in Claude (5 min)

Open Claude Desktop and try:

```
What forecasting tools do you have available?
```

Expected response:
- `forecast_sku`: Generate sales forecast for a product SKU
- `list_available_skus`: List all available product SKUs

Then test:
```
List available SKUs for forecasting
```

Should return: `["SKU0", "SKU1", "SKU2"]`

✅ **Docker MCP Toolkit setup complete!**

---

## Quick Start: Fly.io Cloud Deployment (45 minutes)

### 1. Install flyctl (5 min)

```bash
# Install Fly.io CLI
brew install flyctl

# Authenticate
flyctl auth login

# Verify
flyctl auth whoami
```

### 2. Initialize Application (10 min)

```bash
cd /Users/max/Documents/code/expo-smooth-mcp

# Launch Fly.io app
flyctl launch

# Interactive prompts:
# - App name: expo-smooth-mcp (or unique name)
# - Region: sjc (or closest to you)
# - PostgreSQL: No
# - Redis: No
# - Deploy now: No

# Allocate IPv4 address
flyctl ips allocate-v4

# Verify IP
flyctl ips list
```

### 3. Configure fly.toml (5 min)

Ensure `fly.toml` has these settings:

```toml
app = "expo-smooth-mcp"
primary_region = "sjc"

[env]
  PORT = "8000"
  TRANSPORT = "sse"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  memory = '512mb'
  cpu_kind = 'shared'
  cpus = 1
```

### 4. Deploy to Fly.io (15 min)

```bash
# Deploy application
flyctl deploy

# Monitor deployment
flyctl status

# View logs
flyctl logs
```

### 5. Test Deployment (10 min)

```bash
# Get application URL
APP_URL=$(flyctl info | grep "URL:" | awk '{print $2}')

# Test health endpoint
curl "$APP_URL/health"

# Test REST API
curl -X POST "$APP_URL/api/forecast" \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "horizon": 90}'

# Open in browser
flyctl open
```

✅ **Fly.io deployment complete!**

---

## Validation Checklist

### Docker MCP Toolkit
- [ ] Docker Desktop MCP Toolkit enabled
- [ ] expo-smooth-mcp image built successfully
- [ ] Server added and enabled in MCP Toolkit
- [ ] Claude Desktop configured and restarted
- [ ] MCP tools visible in Claude
- [ ] `list_available_skus` returns 3 SKUs
- [ ] `forecast_sku` generates forecast data

### Fly.io Cloud
- [ ] flyctl installed and authenticated
- [ ] Application launched with unique name
- [ ] IPv4 address allocated
- [ ] fly.toml configured correctly
- [ ] Deployment successful
- [ ] Health checks passing
- [ ] HTTPS working (TLS certificate issued)
- [ ] REST API responding
- [ ] Gradio UI accessible at /gradio
- [ ] Cold start < 2 seconds

---

## Common Issues & Solutions

### Docker MCP: "command not found: docker"
```bash
# Enable MCP Toolkit in Docker Desktop
# Settings → Features in development → MCP Toolkit
# Restart Docker Desktop
```

### Docker MCP: Claude not showing tools
```bash
# Verify gateway is running
docker ps | grep mcp-gateway

# Restart Claude Desktop
killall Claude && sleep 5 && open -a Claude

# Check server logs
docker mcp server logs expo-smooth-mcp
```

### Fly.io: Deployment fails
```bash
# Test Docker build locally first
docker build -t expo-smooth-mcp:latest .

# Deploy with local build
flyctl deploy --local-only

# Check logs for errors
flyctl logs --level error
```

### Fly.io: Health checks failing
```bash
# Check logs
flyctl logs

# Verify port binding in Dockerfile CMD
# Should include: --host 0.0.0.0 --port 8000

# Test health endpoint
flyctl ssh console
curl http://localhost:8000/health
```

---

## Cost Estimate

### Fly.io Monthly Costs

**Development (Free Tier):**
- 3 shared-cpu VMs (256MB): $0/month
- 160GB bandwidth: $0/month
- **Total: FREE**

**Production (Low Traffic):**
- 1 shared-cpu VM (512MB): $2/month
- 50GB bandwidth: $0/month (within free limit)
- Auto-scaling enabled
- **Total: ~$2-3/month**

**Production (Medium Traffic):**
- 2 shared-cpu VMs (512MB): $4/month
- 100GB bandwidth: $0/month
- **Total: ~$4-5/month**

---

## Next Steps

After completing Phase 4:

### Immediate Actions
1. ✅ Test all endpoints thoroughly
2. ✅ Document production URLs
3. ✅ Set up monitoring and alerts

### Optional Enhancements
4. Configure custom domain (if needed)
5. Set up CI/CD pipeline for automated deploys
6. Add log aggregation (e.g., Datadog, Sentry)
7. Implement rate limiting for API
8. Add authentication for sensitive endpoints

### Proceed to Phase 5: Monitoring & Observability
- Metrics collection (Prometheus)
- Log aggregation (Loki)
- Distributed tracing (Jaeger)
- Alerting (PagerDuty, Slack)
- SLO/SLA definitions

---

## Support & Resources

### Documentation
- **Phase 4 Implementation**: `docs/implementation/PHASE_4_IMPLEMENTATION.md`
- **Docker MCP Guide**: `docs/implementation/PHASE_4_DOCKER_MCP_GUIDE.md`
- **Fly.io Guide**: `docs/implementation/PHASE_4_FLYIO_GUIDE.md`

### External Resources
- Docker MCP Toolkit: https://docs.docker.com/desktop/mcp/
- Fly.io Docs: https://fly.io/docs
- FastMCP: https://github.com/jlowin/fastmcp

### Getting Help
- Docker MCP: Docker Community Forums
- Fly.io: community.fly.io
- Project Issues: GitHub repository

---

**Phase 4 Quick Start Complete**  
**Total Time: 75 minutes**  
**Both Environments Ready**

Need detailed instructions? See:
- `PHASE_4_DOCKER_MCP_GUIDE.md` for Docker MCP Toolkit
- `PHASE_4_FLYIO_GUIDE.md` for Fly.io cloud deployment
