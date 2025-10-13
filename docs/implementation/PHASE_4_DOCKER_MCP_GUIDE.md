# Phase 4: Docker MCP Toolkit - Detailed Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Component:** Docker MCP Toolkit Local Deployment  
**Version:** 1.0.0  
**Created:** October 13, 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Docker MCP Toolkit Overview](#docker-mcp-toolkit-overview)
3. [Setup Instructions](#setup-instructions)
4. [Configuration Details](#configuration-details)
5. [Testing & Validation](#testing--validation)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

---

## Introduction

The Docker MCP Toolkit is a specialized feature within Docker Desktop designed to simplify the discovery, management, and secure execution of MCP (Model Context Protocol) servers. It provides a gateway architecture that enables:

- **Secure Sandboxing**: Resource limits (1 CPU, 2GB RAM) and filesystem isolation
- **Unified Management**: Single interface for multiple MCP servers
- **One-Click Integration**: Automatic client configuration
- **Enhanced Security**: Secret interception and permission management

### Why Docker MCP Toolkit?

**Compared to Classic Docker Containers:**

| Feature | Docker MCP Toolkit | Classic Container |
|---------|-------------------|-------------------|
| Setup Complexity | Low (one-click) | High (manual JSON) |
| Security | Built-in sandbox | Manual configuration |
| Client Integration | Automatic | Manual |
| Resource Limits | Automatic | Manual |
| Management | Centralized UI | Individual containers |

**Recommendation:** Docker MCP Toolkit is the **superior choice** for local MCP development.

---

## Docker MCP Toolkit Overview

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker MCP Toolkit                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│   Claude Desktop ─→ Docker MCP Gateway                      │
│   VS Code        ─→      (stdio)          ─→ expo-smooth-mcp│
│   Cursor         ─→                          (container)     │
│                                                               │
│   Gateway Features:                                           │
│   • Tool discovery                                           │
│   • Request routing                                          │
│   • Security enforcement                                     │
│   • Resource management                                      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Benefits

1. **Security by Default**
   - 1 CPU, 2GB RAM limits per container
   - No host filesystem access by default
   - Secret interception prevents API key leaks
   - Network isolation

2. **Simplified Management**
   - Single UI for all MCP servers
   - Enable/disable servers with one click
   - Centralized logging and monitoring
   - Version management

3. **Client Integration**
   - Automatic Claude Desktop configuration
   - VS Code integration
   - Cursor integration
   - No manual JSON editing

---

## Setup Instructions

### Prerequisites

```bash
# Required:
# - Docker Desktop 4.34.0+ for macOS
# - macOS 12.0+ (Monterey or later)
# - 4GB RAM minimum
# - 10GB disk space

# Verify Docker Desktop version
docker --version
# Should show: Docker version 27.0.0 or higher
```

### Step 1: Enable MCP Toolkit (5 minutes)

```bash
# 1. Open Docker Desktop
open -a "Docker Desktop"

# 2. Go to Settings → Features in development
# 3. Enable "MCP Toolkit" (beta feature)
# 4. Click "Apply & restart"
# 5. Wait for Docker Desktop to restart (~30 seconds)

# Verify MCP Toolkit is enabled
docker mcp version
# Should output: Docker MCP Toolkit version X.X.X
```

### Step 2: Build Application Image (10 minutes)

```bash
# Navigate to project directory
cd /Users/max/Documents/code/expo-smooth-mcp

# Ensure Dockerfile exists
ls -la Dockerfile

# Build Docker image
docker build -t expo-smooth-mcp:latest .

# Verify build
docker images expo-smooth-mcp:latest

# Expected output:
# REPOSITORY          TAG       IMAGE ID       SIZE
# expo-smooth-mcp     latest    <hash>         ~400MB
```

### Step 3: Add Server to Toolkit (5 minutes)

```bash
# Add server to Docker MCP Toolkit
docker mcp server add expo-smooth-mcp:latest

# Verify server was added
docker mcp server list

# Expected output:
# NAME              IMAGE                    STATUS
# expo-smooth-mcp   expo-smooth-mcp:latest   stopped

# Enable the server
docker mcp server enable expo-smooth-mcp

# Check server status
docker mcp server status expo-smooth-mcp
# Should show: enabled
```

### Step 4: Configure Claude Desktop (10 minutes)

#### Option A: Automatic Configuration (Recommended)

```bash
# 1. Open Docker Desktop
# 2. Navigate to MCP Toolkit → Clients tab
# 3. Find "Claude Desktop" in the list
# 4. Click "Connect" button
# 5. Click "Confirm" when prompted
# 6. Restart Claude Desktop

# Verify configuration was applied
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
cat "$CLAUDE_CONFIG"

# Should contain docker-mcp-gateway configuration
```

#### Option B: Manual Configuration

```bash
# Backup existing configuration
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup.$(date +%Y%m%d-%H%M%S)"

# Create or update configuration
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

# Verify configuration
jq '.' "$CLAUDE_CONFIG"
```

### Step 5: Test Integration (10 minutes)

```bash
# 1. Restart Claude Desktop
killall Claude 2>/dev/null || true
sleep 2
open -a Claude

# 2. Wait 10-15 seconds for Claude to fully start

# 3. In Claude, type: "What MCP tools do you have?"

# Expected response should list:
# - forecast_sku: Generate sales forecast for a product SKU
# - list_available_skus: List all available product SKUs

# 4. Test a tool
# Type in Claude: "List available SKUs for forecasting"

# Should return: ["SKU0", "SKU1", "SKU2"]

# 5. Test forecast generation
# Type in Claude: "Generate a 90-day forecast for SKU0"

# Should return forecast data with dates and predictions
```

---

## Configuration Details

### MCP Server Configuration

The Docker MCP Toolkit uses the container's entrypoint to configure the server mode. For expo-smooth-mcp:

```json
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
  }
}
```

### Resource Limits

The Docker MCP Toolkit automatically applies these limits:

```yaml
CPU: 1 core maximum
Memory: 2GB maximum
Disk: Ephemeral (no persistent storage by default)
Network: Isolated (no external network access by default)
Filesystem: Read-only host access (must be explicitly granted)
```

### Environment Variables

You can configure environment variables for the MCP server:

```bash
# Set environment variables
docker mcp server config expo-smooth-mcp \
  --env LOG_LEVEL=DEBUG \
  --env PYTHONUNBUFFERED=1

# Verify configuration
docker mcp server inspect expo-smooth-mcp
```

### Volume Mounts (Advanced)

To give the container access to local files:

```bash
# Mount a directory
docker mcp server config expo-smooth-mcp \
  --mount type=bind,source=/path/to/data,target=/data,readonly

# Example: Mount custom data directory
docker mcp server config expo-smooth-mcp \
  --mount type=bind,source=$HOME/Documents/mcp-data,target=/data
```

---

## Testing & Validation

### Smoke Tests

```bash
# Test 1: Server status
docker mcp server status expo-smooth-mcp
# Should show: enabled, running (when active)

# Test 2: Container logs
docker mcp server logs expo-smooth-mcp
# Should show:
# - Data loaded successfully
# - Found 3 unique SKUs
# - MCP server started

# Test 3: List servers
docker mcp server list
# Should show expo-smooth-mcp in the list

# Test 4: Server info
docker mcp server inspect expo-smooth-mcp
# Should show detailed configuration
```

### Integration Tests with Claude

Create a test plan and run through it:

```markdown
# Claude Desktop Integration Test Plan

## Test 1: Tool Discovery
Prompt: "What forecasting tools do you have available?"
Expected: Lists forecast_sku and list_available_skus
Status: [ ]

## Test 2: List SKUs
Prompt: "Show me all available product SKUs"
Expected: Returns ["SKU0", "SKU1", "SKU2"]
Status: [ ]

## Test 3: Valid Forecast
Prompt: "Generate a 90-day forecast for SKU0"
Expected: Returns forecast with dates, actuals, and predictions
Status: [ ]

## Test 4: Invalid SKU
Prompt: "Forecast for SKU999"
Expected: Returns error message about invalid SKU
Status: [ ]

## Test 5: Different Horizons
Prompt: "Give me a 30-day forecast for SKU1"
Expected: Returns forecast with 30-day horizon
Status: [ ]

## Test 6: Metadata Check
Prompt: "What's the forecast horizon and historical data size for SKU0?"
Expected: Returns metadata information
Status: [ ]
```

### Performance Validation

```bash
# Test startup time
time docker mcp server restart expo-smooth-mcp
# Should complete in <10 seconds

# Test memory usage
docker stats expo-smooth-mcp --no-stream
# Memory should be <500MB

# Test tool execution time (in Claude)
# Ask Claude: "Time how long it takes to list SKUs"
# Should respond in <1 second
```

---

## Advanced Usage

### Running Multiple MCP Servers

```bash
# Add another MCP server
docker mcp server add another-mcp:latest

# Enable it
docker mcp server enable another-mcp

# Both will be available in Claude
# Claude can discover and use tools from both servers
```

### Custom Entrypoints

For debugging or different modes:

```bash
# Configure custom entrypoint
docker mcp server config expo-smooth-mcp \
  --entrypoint "python -m src.expo_smooth_mcp.main --transport stdio --debug"

# Restart server to apply
docker mcp server restart expo-smooth-mcp
```

### Persistent Data with Volumes

```bash
# Create a named volume
docker volume create expo-smooth-data

# Configure server to use it
docker mcp server config expo-smooth-mcp \
  --mount type=volume,source=expo-smooth-data,target=/data

# Data will persist across container restarts
```

### Network Access (Use Carefully)

By default, MCP Toolkit isolates containers from the network. To enable:

```bash
# Enable network access (reduces security)
docker mcp server config expo-smooth-mcp --network-mode bridge

# Restart to apply
docker mcp server restart expo-smooth-mcp
```

⚠️ **Security Warning:** Only enable network access if absolutely necessary.

### Debugging

```bash
# Enable debug logging
docker mcp server config expo-smooth-mcp \
  --env LOG_LEVEL=DEBUG

# View live logs
docker mcp server logs expo-smooth-mcp --follow

# View last 100 lines
docker mcp server logs expo-smooth-mcp --tail 100

# Get detailed server state
docker mcp server inspect expo-smooth-mcp --format json | jq '.'
```

---

## Troubleshooting

### Issue: Docker MCP Command Not Found

**Symptom:**
```bash
$ docker mcp version
zsh: command not found: docker
```

**Solution:**
```bash
# 1. Verify Docker Desktop is installed
open -a "Docker Desktop"

# 2. Check Docker version
docker --version

# 3. Enable MCP Toolkit
# Docker Desktop → Settings → Features in development → MCP Toolkit

# 4. Restart Docker Desktop

# 5. Verify again
docker mcp version
```

### Issue: Server Won't Start

**Symptom:**
```bash
$ docker mcp server start expo-smooth-mcp
Error: failed to start server
```

**Solution:**
```bash
# Check server status
docker mcp server status expo-smooth-mcp

# View logs for errors
docker mcp server logs expo-smooth-mcp --tail 50

# Check Docker Desktop is running
docker info

# Rebuild image if corrupted
docker build -t expo-smooth-mcp:latest .

# Remove and re-add server
docker mcp server remove expo-smooth-mcp
docker mcp server add expo-smooth-mcp:latest
docker mcp server enable expo-smooth-mcp
```

### Issue: Claude Not Showing Tools

**Symptom:**
Claude doesn't show MCP tools or says no tools available.

**Solution:**
```bash
# 1. Verify gateway is running
docker ps | grep mcp-gateway

# 2. Check Claude config
cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Should contain docker-mcp-gateway

# 3. Restart Claude Desktop
killall Claude
sleep 5
open -a Claude

# 4. Check Docker MCP Gateway logs
docker logs $(docker ps | grep mcp-gateway | awk '{print $1}')

# 5. Verify server is enabled
docker mcp server list | grep expo-smooth-mcp
```

### Issue: Tools Execute Slowly

**Symptom:**
MCP tools take >5 seconds to respond.

**Solution:**
```bash
# Check container resource usage
docker stats expo-smooth-mcp --no-stream

# If memory is high (>1.5GB), there might be a memory leak
# Restart the server
docker mcp server restart expo-smooth-mcp

# Check for data loading issues
docker mcp server logs expo-smooth-mcp | grep "Data loaded"

# Should see: "✓ Data loaded successfully"
```

### Issue: "Permission Denied" Errors

**Symptom:**
```
Error: cannot read FMCG_Sales.csv: permission denied
```

**Solution:**
```bash
# Ensure file is readable in container
# Check Dockerfile COPY command uses --chown=appuser:appuser

# Rebuild image
docker build -t expo-smooth-mcp:latest .

# Update server
docker mcp server remove expo-smooth-mcp
docker mcp server add expo-smooth-mcp:latest
docker mcp server enable expo-smooth-mcp
```

### Issue: Container Keeps Restarting

**Symptom:**
Server status shows constant restarts.

**Solution:**
```bash
# Get detailed logs
docker mcp server logs expo-smooth-mcp --tail 200

# Common causes:
# 1. Missing dependencies → Check Dockerfile
# 2. Port conflict → Change port in Dockerfile
# 3. Out of memory → Check resource limits
# 4. Syntax error → Test locally first

# Test image locally without MCP Toolkit
docker run --rm -i expo-smooth-mcp:latest \
  python -m src.expo_smooth_mcp.main --transport stdio <<EOF
{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}
EOF

# Should return valid JSON-RPC response
```

### Getting Help

**Docker MCP Toolkit Issues:**
- Docker Desktop → Help → Report an issue
- Docker Community Forums: https://forums.docker.com/
- Docker MCP Documentation: https://docs.docker.com/desktop/mcp/

**Project-Specific Issues:**
- Check project documentation
- Review Phase 4 implementation guide
- Check application logs

---

## Summary

### Quick Reference

```bash
# Common Commands
docker mcp server list                    # List all servers
docker mcp server status <name>           # Check status
docker mcp server logs <name>             # View logs
docker mcp server restart <name>          # Restart server
docker mcp server enable <name>           # Enable server
docker mcp server disable <name>          # Disable server
docker mcp server remove <name>           # Remove server

# Claude Configuration
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
cat "$CLAUDE_CONFIG"                      # View config
```

### Best Practices

1. **Always test locally first** before adding to MCP Toolkit
2. **Use semantic versioning** for your images (e.g., v2.0.0)
3. **Monitor resource usage** to prevent memory issues
4. **Check logs regularly** for errors or warnings
5. **Keep Docker Desktop updated** for latest MCP Toolkit features

### Next Steps

After completing Docker MCP Toolkit setup:

1. ✅ Test all MCP tools in Claude Desktop
2. ✅ Document any custom configurations
3. → Proceed to Fly.io cloud deployment (TASK-404)
4. → Set up monitoring and alerts (TASK-407)

---

**Docker MCP Toolkit Guide Complete**  
**Local Deployment Ready**  
**Integration with Claude Desktop Validated**
