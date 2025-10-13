# Phase 4: Fly.io Cloud Deployment Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Component:** Fly.io Cloud Deployment  
**Version:** 1.0.0  
**Created:** October 13, 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Fly.io Platform Overview](#flyio-platform-overview)
3. [Setup & Prerequisites](#setup--prerequisites)
4. [Deployment Configuration](#deployment-configuration)
5. [Deployment Process](#deployment-process)
6. [Post-Deployment Validation](#post-deployment-validation)
7. [Monitoring & Operations](#monitoring--operations)
8. [Cost Optimization](#cost-optimization)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

Fly.io is a modern Platform-as-a-Service (PaaS) that deploys applications globally using Firecracker microVMs. It's optimized for:

- **Ultra-fast cold starts**: <1 second from idle to running
- **Global distribution**: Deploy to 37+ regions worldwide
- **Cost-effective**: Pay only for resources used ($2-5/month for small apps)
- **Developer-friendly**: Simple CLI, no Kubernetes complexity

### Why Fly.io for MCP Servers?

**Compared to Other Platforms:**

| Feature | Fly.io | AWS Lambda | Heroku | Railway |
|---------|--------|------------|--------|---------|
| Cold Start | <1s | 1-5s | 30s+ | 5-10s |
| HTTP/SSE Support | ✅ Native | ❌ No | ✅ Yes | ✅ Yes |
| Cost (small) | $2-5/mo | $0-10/mo | $7/mo | $5/mo |
| Global CDN | ✅ Built-in | ⚠️ Add CloudFront | ❌ No | ❌ No |
| WebSocket | ✅ Yes | ⚠️ API Gateway | ✅ Yes | ✅ Yes |
| Persistent Storage | ✅ Volumes | ❌ S3 only | ⚠️ Ephemeral | ✅ Yes |

**Recommendation:** Fly.io is **ideal for MCP servers** due to its HTTP/SSE support, fast cold starts, and simple deployment model.

---

## Fly.io Platform Overview

### Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      Fly.io Global Network                      │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Client Request ─→ Global Anycast IP (TLS Termination)        │
│                     │                                           │
│                     ├→ [Region: sjc (San Francisco)]           │
│                     │   └─ expo-smooth-mcp (Firecracker VM)    │
│                     │                                           │
│                     ├→ [Region: lhr (London)] (if deployed)    │
│                     │   └─ expo-smooth-mcp (Firecracker VM)    │
│                     │                                           │
│                     └→ [Region: syd (Sydney)] (if deployed)    │
│                         └─ expo-smooth-mcp (Firecracker VM)    │
│                                                                  │
│   Features:                                                      │
│   • Automatic TLS certificates (Let's Encrypt)                 │
│   • Health check routing                                        │
│   • Zero-downtime deploys                                       │
│   • Auto-scaling (if configured)                               │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Key Features

1. **Firecracker MicroVMs**
   - Kernel-level isolation
   - 125ms to boot a VM
   - Lightweight alternative to containers

2. **Anycast Network**
   - Single IP routes to nearest region
   - Sub-10ms latency for most users
   - Automatic failover

3. **Integrated Services**
   - Fly Postgres (managed PostgreSQL)
   - Fly Volumes (persistent storage)
   - Fly Machines API (programmatic control)
   - Built-in Redis (upstash.io integration)

---

## Setup & Prerequisites

### Install flyctl CLI (5 minutes)

```bash
# macOS installation
brew install flyctl

# Verify installation
flyctl version
# Should show: flyctl v0.2.x or higher

# Alternative: Direct download
curl -L https://fly.io/install.sh | sh

# Add to PATH if needed
echo 'export PATH="$HOME/.fly/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Create Fly.io Account (5 minutes)

```bash
# Sign up for free account
flyctl auth signup

# Or log in if you have an account
flyctl auth login

# Verify authentication
flyctl auth whoami
# Should show: Email: your@email.com

# Check available regions
flyctl platform regions
```

### Set Up Payment Method (5 minutes)

```bash
# Add payment method via dashboard
flyctl dashboard billing

# Or use CLI to open billing page
open https://fly.io/dashboard/personal/billing

# Required for:
# - Persistent volumes
# - Custom domains
# - Production apps

# Free tier includes:
# - Up to 3 shared-cpu VMs (256MB RAM each)
# - 160GB outbound data transfer
# - Automatic TLS certificates
```

---

## Deployment Configuration

### fly.toml Configuration

Create `fly.toml` in project root:

```toml
# Application name (must be globally unique)
app = "expo-smooth-mcp"

# Primary region (choose closest to your users)
primary_region = "sjc"  # San Francisco

# Build configuration
[build]
  dockerfile = "Dockerfile"

# Environment variables
[env]
  PORT = "8000"
  PYTHONUNBUFFERED = "1"
  LOG_LEVEL = "INFO"
  TRANSPORT = "sse"  # Use SSE for remote clients

# HTTP service configuration
[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = "stop"    # Stop when idle
  auto_start_machines = true     # Auto-start on request
  min_machines_running = 0       # Scale to zero when idle
  processes = ["app"]

  # Health checks
  [http_service.checks]
    [http_service.checks.alive]
      type = "http"
      interval = "30s"
      timeout = "5s"
      grace_period = "10s"
      method = "GET"
      path = "/health"
      protocol = "http"
      tls_skip_verify = false
      
      # Restart unhealthy machines
      [http_service.checks.alive.headers]
        User-Agent = "Fly-Health-Check"

# Resource allocation
[[vm]]
  memory = '512mb'
  cpu_kind = 'shared'
  cpus = 1

# OPTIONAL: Persistent volume for data
# [[mounts]]
#   source = "data"
#   destination = "/data"
#   initial_size = "1gb"
```

### Dockerfile Optimization for Fly.io

Ensure your Dockerfile is optimized:

```dockerfile
# Multi-stage build for smaller image size
FROM python:3.11-slim AS builder

# Install uv for fast dependency installation
RUN pip install uv

# Copy dependency files
COPY requirements.txt .

# Install dependencies to a virtual environment
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

# Start server with SSE transport for remote clients
CMD ["python", "-m", "src.expo_smooth_mcp.main", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]
```

### Secrets Management

Store sensitive configuration as secrets:

```bash
# Set secrets (not visible in fly.toml or logs)
flyctl secrets set API_KEY="your-secret-api-key"

# View secret names (values hidden)
flyctl secrets list

# Remove a secret
flyctl secrets unset API_KEY

# Import secrets from .env file
flyctl secrets import < .env.production
```

---

## Deployment Process

### Step 1: Launch Application (10 minutes)

```bash
# Navigate to project directory
cd /Users/max/Documents/code/expo-smooth-mcp

# Initialize Fly.io app (creates fly.toml)
flyctl launch

# Interactive prompts:
# - App name: expo-smooth-mcp (or choose unique name)
# - Region: sjc (San Francisco) or closest to you
# - Setup PostgreSQL: No (not needed for this app)
# - Setup Redis: No (not needed for this app)
# - Deploy now: No (we'll deploy manually after configuration)

# Review generated fly.toml
cat fly.toml
```

### Step 2: Configure Application (5 minutes)

```bash
# Allocate IPv4 address (required for HTTP)
flyctl ips allocate-v4

# Verify IP allocation
flyctl ips list
# Should show both IPv4 and IPv6 addresses

# OPTIONAL: Allocate IPv6 (usually automatic)
flyctl ips allocate-v6

# Set up custom domain (if you have one)
flyctl certs add your-domain.com
# Follow DNS instructions to point domain to Fly.io
```

### Step 3: Deploy Application (15 minutes)

```bash
# Deploy to Fly.io
flyctl deploy

# Expected output:
# ==> Building image
# ==> Pushing image to fly
# ==> Deploying expo-smooth-mcp
# --> v0 deployed successfully

# Monitor deployment
flyctl status

# View logs during deployment
flyctl logs
```

### Step 4: Verify Deployment (5 minutes)

```bash
# Check application status
flyctl status

# Expected output:
# NAME     STATUS  MACHINE VERSION  REGION  HEALTH
# app      started 0.1.0            sjc     passing

# Test health endpoint
flyctl curl /health

# Should return:
# {"status": "healthy", "timestamp": "2025-10-13T..."}

# Open application in browser
flyctl open

# Test API endpoint
flyctl curl /api/forecast --data '{"sku": "SKU0", "horizon": 90}'
```

---

## Post-Deployment Validation

### Automated Tests

```bash
# Get application URL
APP_URL=$(flyctl info | grep "URL:" | awk '{print $2}')
echo "Testing: $APP_URL"

# Test 1: Health Check
curl -f "$APP_URL/health"
# Expected: {"status": "healthy", ...}

# Test 2: Root endpoint (service discovery)
curl -f "$APP_URL/"
# Should list available endpoints

# Test 3: List SKUs (REST API)
curl -X POST "$APP_URL/api/forecast" \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU0", "horizon": 30}'
# Should return forecast data

# Test 4: MCP SSE endpoint
curl -N "$APP_URL/sse" \
  -H "Accept: text/event-stream"
# Should establish SSE connection
```

### Manual Validation Checklist

```markdown
# Fly.io Deployment Validation Checklist

## Infrastructure
- [ ] Application deployed successfully
- [ ] Health checks passing
- [ ] IPv4 and IPv6 addresses allocated
- [ ] TLS certificate issued (https://)
- [ ] Metrics dashboard accessible

## Functionality
- [ ] Root endpoint returns service info
- [ ] REST API /api/forecast works
- [ ] MCP SSE endpoint /sse accessible
- [ ] Gradio UI loads at /gradio
- [ ] Data loading successful (check logs)

## Performance
- [ ] Cold start < 2 seconds
- [ ] API response time < 500ms
- [ ] Memory usage < 400MB
- [ ] CPU usage < 50% under load

## Security
- [ ] HTTPS enforced (no HTTP access)
- [ ] Secrets properly set
- [ ] Non-root user in container
- [ ] Health check endpoint public
- [ ] No sensitive data in logs
```

### Load Testing (Optional)

```bash
# Install hey (HTTP load testing tool)
brew install hey

# Test API performance
APP_URL=$(flyctl info | grep "URL:" | awk '{print $2}')
hey -n 100 -c 10 "$APP_URL/health"

# Expected results:
# - Success rate: 100%
# - Average response time: <100ms
# - Max response time: <500ms
```

---

## Monitoring & Operations

### Real-time Monitoring

```bash
# View live logs
flyctl logs

# Filter logs by level
flyctl logs --level error

# Follow logs (like tail -f)
flyctl logs -f

# View machine metrics
flyctl metrics

# Open Grafana dashboard
flyctl dashboard metrics
```

### Resource Monitoring

```bash
# Check resource usage
flyctl status

# View machine details
flyctl machine list

# Check memory and CPU
flyctl ssh console
# Then inside the VM:
top
free -h
df -h
```

### Alerts & Notifications

```bash
# Set up webhook for health check failures
# In fly.toml, add:

# [alerts]
#   [[alerts.rules]]
#     name = "health-check-failure"
#     query = "health_check_status == 'critical'"
#     severity = "critical"
#     notification = "webhook:https://your-webhook.com"

# Apply configuration
flyctl deploy --config fly.toml
```

### Automated Backups

```bash
# If using volumes, create snapshots
flyctl volumes list
flyctl volumes snapshot create <volume-id>

# List snapshots
flyctl volumes snapshots list

# Restore from snapshot
flyctl volumes restore <snapshot-id>
```

---

## Cost Optimization

### Pricing Breakdown

```
BASE COSTS (Free Tier):
- 3 shared-cpu VMs (256MB): FREE
- 160GB bandwidth/month: FREE
- Automatic TLS: FREE

UPGRADE COSTS:
- Additional VM (512MB): ~$2/month
- Persistent volume (1GB): ~$0.15/month
- Extra bandwidth (GB): ~$0.02/GB
- Dedicated CPU: ~$30/month
- Extra memory: ~$5/month per GB

EXAMPLE: MCP Server (low traffic)
- 1 shared-cpu VM (512MB): $2/month
- 1GB volume: $0.15/month
- 50GB bandwidth: FREE (within limit)
- TLS certificate: FREE
TOTAL: ~$2.15/month
```

### Cost Optimization Strategies

#### 1. Auto-scaling to Zero

```toml
# In fly.toml
[http_service]
  auto_stop_machines = "stop"    # Stop when idle
  auto_start_machines = true     # Auto-start on request
  min_machines_running = 0       # Scale to zero
```

**Savings:** Reduces cost by 70-90% for low-traffic apps

#### 2. Right-size Resources

```bash
# Start with minimum resources
flyctl scale memory 256  # 256MB (free tier)
flyctl scale count 1     # Single instance

# Monitor and adjust based on actual usage
flyctl metrics

# If memory is consistently <50%, you're over-provisioned
# If CPU is consistently <20%, you're over-provisioned
```

#### 3. Optimize Docker Image

```bash
# Reduce image size to speed up deploys and reduce storage
docker images expo-smooth-mcp:latest
# Target: <400MB

# Use multi-stage builds
# Remove dev dependencies
# Use alpine base images (if compatible)
```

#### 4. Bandwidth Optimization

```bash
# Enable HTTP compression in FastAPI
# Add to main.py:
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Reduces bandwidth by 60-80% for JSON responses
```

### Cost Monitoring

```bash
# View current month's usage
flyctl dashboard billing

# Set up budget alerts
# Go to: https://fly.io/dashboard/personal/billing/settings
# Set spending limit: $10/month (example)
# Enable email alerts at 50%, 75%, 90%
```

---

## Troubleshooting

### Issue: Deployment Fails

**Symptom:**
```bash
$ flyctl deploy
Error: failed to deploy: build failed
```

**Solution:**
```bash
# Check build logs
flyctl logs

# Test Docker build locally first
docker build -t expo-smooth-mcp:latest .

# If local build works, try:
flyctl deploy --local-only  # Build on your machine, not Fly.io

# Check for .dockerignore issues
cat .dockerignore

# Ensure required files aren't ignored
```

### Issue: Health Checks Failing

**Symptom:**
```bash
$ flyctl status
HEALTH: critical
```

**Solution:**
```bash
# Check logs for errors
flyctl logs --level error

# Test health endpoint manually
flyctl ssh console
curl http://localhost:8000/health

# Common causes:
# 1. Port mismatch (fly.toml vs Dockerfile)
# 2. App not binding to 0.0.0.0
# 3. Health check path incorrect
# 4. Timeout too short

# Fix port binding in Dockerfile CMD:
CMD ["python", "-m", "src.expo_smooth_mcp.main", "--host", "0.0.0.0", "--port", "8000"]
```

### Issue: Slow Cold Starts

**Symptom:**
First request after idle takes >5 seconds.

**Solution:**
```bash
# Keep minimum machines running
# In fly.toml:
[http_service]
  min_machines_running = 1  # Costs ~$2/month

# OR optimize container startup
# - Reduce image size
# - Lazy-load data
# - Use readiness checks

# Monitor cold start time
flyctl logs | grep "started"
```

### Issue: Out of Memory

**Symptom:**
```
Error: process killed due to OOM
```

**Solution:**
```bash
# Check current memory allocation
flyctl status

# Increase memory
flyctl scale memory 512  # or 1024

# Or optimize application:
# - Profile memory usage
# - Fix memory leaks
# - Stream large responses
# - Use pagination

# Monitor memory
flyctl ssh console
free -h
```

### Issue: Connection Timeouts

**Symptom:**
Requests to Fly.io app timeout after 30 seconds.

**Solution:**
```bash
# Fly.io has a 300-second request timeout
# For long-running tasks:

# 1. Return immediately with job ID
# 2. Poll separate status endpoint
# 3. Use WebSockets for real-time updates

# For SSE connections:
# - Send periodic keepalive messages
# - Client should reconnect on disconnect

# Check for network issues
flyctl ping
```

### Issue: SSL/TLS Certificate Not Issued

**Symptom:**
`https://` not working, certificate errors.

**Solution:**
```bash
# Check certificate status
flyctl certs list

# Should show: "issued"

# If pending:
# 1. Verify DNS points to Fly.io IP
dig your-app.fly.dev

# 2. Wait 5-10 minutes for Let's Encrypt
# 3. Check certificate logs
flyctl certs show your-app.fly.dev

# Force certificate renewal
flyctl certs add your-app.fly.dev --force
```

### Getting Help

**Fly.io Support:**
- Community Forum: https://community.fly.io
- Documentation: https://fly.io/docs
- Status Page: https://status.fly.io
- Support Email: support@fly.io (for paid accounts)

**Project-Specific:**
- Check logs: `flyctl logs`
- Check status: `flyctl status`
- SSH to debug: `flyctl ssh console`

---

## Summary

### Quick Reference

```bash
# Essential Commands
flyctl deploy                  # Deploy application
flyctl status                  # Check status
flyctl logs                    # View logs
flyctl ssh console             # SSH into VM
flyctl scale memory 512        # Adjust memory
flyctl scale count 2           # Scale instances
flyctl restart                 # Restart app
flyctl destroy                 # Delete app (careful!)

# Monitoring
flyctl metrics                 # View metrics
flyctl dashboard metrics       # Open Grafana
flyctl dashboard billing       # View costs

# Configuration
flyctl secrets set KEY=value   # Set secret
flyctl ips allocate-v4         # Add IPv4
flyctl certs add domain.com    # Add custom domain
```

### Best Practices

1. **Start small, scale up**: Begin with 256MB memory, scale based on actual usage
2. **Enable auto-scaling**: Scale to zero for cost savings
3. **Monitor regularly**: Check logs and metrics daily initially
4. **Set budget alerts**: Prevent surprise bills
5. **Use secrets**: Never put sensitive data in fly.toml
6. **Test locally first**: Validate Docker image before deploying
7. **Keep dependencies minimal**: Faster builds, lower costs

### Success Criteria

✅ **Deployment successful if:**
- Health checks pass consistently
- API responds in <500ms
- Cold starts <2 seconds
- Cost <$5/month for low traffic
- Uptime >99.9%
- No errors in logs

### Next Steps

After completing Fly.io deployment:

1. ✅ Validate all endpoints work
2. ✅ Set up monitoring and alerts
3. ✅ Configure auto-scaling
4. → Test with remote MCP clients
5. → Document production URLs
6. → Set up CI/CD pipeline (optional)

---

**Fly.io Deployment Guide Complete**  
**Cloud Deployment Ready**  
**Production Environment Operational**
