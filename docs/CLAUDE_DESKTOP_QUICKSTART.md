# Claude Desktop Quick Start Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Last Updated:** October 13, 2025  
**Version:** 1.0.0

---

## Overview

This guide walks you through setting up the Expo Smooth MCP Server with Claude Desktop. After setup, you'll be able to ask Claude to forecast sales for products using natural language.

**What you'll be able to do:**
- Ask Claude "What products are available for forecasting?"
- Request forecasts like "Show me a 30-day forecast for PRODUCT_002"
- Get intelligent analysis of forecast trends and patterns

**Time required:** ~5 minutes

---

## Prerequisites

✅ Claude Desktop installed (macOS, Windows, or Linux)  
✅ Conda or Miniconda installed  
✅ Git installed  
✅ Terminal/command line access  

---

## Step-by-Step Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/maksim-tsi/expo-smooth-mcp.git
cd expo-smooth-mcp

# Create conda environment
conda create -n tsi python=3.11
conda activate tsi

# Install package in editable mode
pip install -e .
```

**Verify installation:**
```bash
python -c "import expo_smooth_mcp; print('✅ Package installed correctly')"
```

---

### 2. Create Shell Script Wrapper

**For macOS/Linux:**

Create file: `run_mcp_server.sh`

```bash
#!/bin/bash
# Update paths to match your system
source /Users/YOUR_USERNAME/miniconda3/bin/activate tsi
cd /Users/YOUR_USERNAME/path/to/expo-smooth-mcp
exec python -m src.expo_smooth_mcp.main --transport stdio
```

**Important:** Replace `YOUR_USERNAME` and update paths to match your system!

**Make executable:**
```bash
chmod +x run_mcp_server.sh
```

**For Windows:**

Create file: `run_mcp_server.bat`

```batch
@echo off
call C:\Users\YOUR_USERNAME\miniconda3\Scripts\activate.bat tsi
cd C:\Users\YOUR_USERNAME\path\to\expo-smooth-mcp
python -m src.expo_smooth_mcp.main --transport stdio
```

---

### 3. Test Shell Script Independently

**Before configuring Claude Desktop, verify the script works:**

```bash
# Run the script
./run_mcp_server.sh

# You should see:
# INFO:     Application startup complete.
# MCP server running on stdio transport...
```

**Press Ctrl+C to stop the server.**

If you see errors, see [Troubleshooting](#troubleshooting) below.

---

### 4. Configure Claude Desktop

**Find your config file:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Edit the config file:**

```json
{
  "mcpServers": {
    "expo-smooth-forecast": {
      "command": "/absolute/path/to/expo-smooth-mcp/run_mcp_server.sh"
    }
  }
}
```

**⚠️ Critical:**
- Use **absolute paths** (no `~` or relative paths)
- For Windows, use forward slashes: `"C:/Users/..."`
- Verify JSON syntax (no trailing commas)

---

### 5. Restart Claude Desktop

1. Completely quit Claude Desktop
2. Relaunch Claude Desktop
3. Look for 🔨 (hammer icon) in the bottom-right corner
4. The icon indicates MCP tools are available!

---

### 6. Test It Out!

Try these queries in Claude Desktop:

**Test 1: Discovery**
```
What forecasting tools do you have available?
```

**Test 2: List products**
```
What products are available for forecasting?
```

**Test 3: Basic forecast**
```
Forecast sales for PRODUCT_001 for 90 days
```

**Test 4: Custom horizon**
```
Show me a 30-day forecast for PRODUCT_002
```

---

## Verification Checklist

- [ ] Shell script runs successfully when executed manually
- [ ] Claude Desktop config file has correct JSON syntax
- [ ] Absolute paths used (no `~` or relative paths)
- [ ] Claude Desktop fully restarted after config change
- [ ] 🔨 Hammer icon visible in Claude Desktop
- [ ] Tools appear when asking "What forecasting tools do you have?"
- [ ] Forecasts execute successfully

---

## Troubleshooting

### Problem: No hammer icon appears

**Solution:**
1. Check config file location is correct for your OS
2. Verify JSON syntax (use https://jsonlint.com)
3. Confirm absolute paths (run `pwd` in project directory)
4. Completely quit and restart Claude Desktop

### Problem: "spawn python ENOENT"

**Cause:** Python not found in PATH

**Solution:**
- Use shell script wrapper (not direct Python command)
- Verify conda activation line in script
- Test script independently: `./run_mcp_server.sh`

### Problem: "ModuleNotFoundError: No module named 'src'"

**Cause:** Working directory not set correctly

**Solution:**
- Ensure script includes `cd /path/to/expo-smooth-mcp`
- Verify package installed: `pip list | grep expo-smooth-mcp`
- Try reinstalling: `pip install -e .`

### Problem: Tools don't update after code changes

**Cause:** Claude Desktop caches server state

**Solution:**
1. Completely quit Claude Desktop
2. Kill any running server processes:
   ```bash
   ps aux | grep expo_smooth_mcp
   kill -9 <PID>
   ```
3. Restart Claude Desktop

### Problem: Conda environment not found

**Cause:** Environment name mismatch or not created

**Solution:**
```bash
# List all conda environments
conda env list

# If 'tsi' missing, create it
conda create -n tsi python=3.11
conda activate tsi
pip install -e /path/to/expo-smooth-mcp
```

### Still having issues?

1. Check logs in Claude Desktop Developer Tools
2. Test server manually: `./run_mcp_server.sh`
3. Verify all paths are absolute and correct
4. See [CLAUDE_DESKTOP_TEST_REPORT.md](CLAUDE_DESKTOP_TEST_REPORT.md) for detailed troubleshooting

---

## Understanding the Setup

### Why Shell Script Wrapper?

Claude Desktop runs MCP servers in an isolated environment that doesn't have access to:
- Your shell configuration (`.zshrc`, `.bashrc`)
- Conda environments
- Environment variables

**The shell script wrapper solves this by:**
1. Explicitly activating the conda environment
2. Setting the correct working directory
3. Running Python with proper module paths

### Architecture Overview

```
┌─────────────────┐
│ Claude Desktop  │
└────────┬────────┘
         │ Invokes
         │
         ▼
┌──────────────────────┐
│ run_mcp_server.sh    │  ← Shell wrapper
│ - Activates conda    │
│ - Sets working dir   │
│ - Runs Python        │
└────────┬─────────────┘
         │ Executes
         │
         ▼
┌──────────────────────┐
│ main.py              │  ← MCP Server
│ - stdio transport    │
│ - FastMCP protocol   │
│ - Forecasting tools  │
└────────┬─────────────┘
         │ Uses
         │
         ▼
┌──────────────────────┐
│ Business Logic       │  ← Core algorithms
│ - Holt-Winters       │
│ - Data preprocessing │
│ - Forecasting engine │
└──────────────────────┘
```

---

## Usage Examples

### Basic Usage

**Query:** "What products can I forecast?"

**Claude Response:**
```
There are 3 products available:
- PRODUCT_001
- PRODUCT_002
- PRODUCT_003
```

### Forecasting

**Query:** "Forecast sales for PRODUCT_002 for 30 days"

**Claude Response:**
```
Here's the 30-day forecast for PRODUCT_002:

Historical Data: Jan 1-20, 2024 (200-290 units)
Forecast: Jan 21 - Feb 19, 2024 (295-441 units)

Key Observations:
- Strong upward trend (~5 units/day)
- Seasonality detected
- Continued growth trajectory
```

### Error Handling

**Query:** "Forecast PRODUCT_999"

**Claude Response:**
```
PRODUCT_999 isn't available. Only these products exist:
- PRODUCT_001
- PRODUCT_002
- PRODUCT_003

Would you like to forecast one of these instead?
```

---

## Advanced Configuration

### Custom Port (HTTP mode)

If you want to run in HTTP mode instead of stdio:

**Update shell script:**
```bash
#!/bin/bash
source /path/to/miniconda3/bin/activate tsi
cd /path/to/expo-smooth-mcp
exec python -m src.expo_smooth_mcp.main --transport http --port 8000
```

**Update Claude config:**
```json
{
  "mcpServers": {
    "expo-smooth-forecast": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Multiple MCP Servers

You can run multiple MCP servers simultaneously:

```json
{
  "mcpServers": {
    "expo-smooth-forecast": {
      "command": "/path/to/expo-smooth-mcp/run_mcp_server.sh"
    },
    "another-server": {
      "command": "/path/to/another-server/run.sh"
    }
  }
}
```

### Logging

Add logging to your shell script:

```bash
#!/bin/bash
source /path/to/miniconda3/bin/activate tsi
cd /path/to/expo-smooth-mcp
exec python -m src.expo_smooth_mcp.main --transport stdio 2>&1 | tee server.log
```

Logs will be written to `server.log` in the project directory.

---

## Next Steps

✅ **Setup complete!** Your MCP server is now integrated with Claude Desktop.

**What's next:**
1. Explore forecasting different products and time horizons
2. Try the REST API: `python -m src.expo_smooth_mcp.main --transport http`
3. Access OpenAPI docs: http://localhost:8000/docs
4. Wait for Phase 3: Gradio UI integration

**Learn more:**
- [Full Test Report](CLAUDE_DESKTOP_TEST_REPORT.md) - Detailed validation results
- [Phase 2 Code Review](PHASE_2_CODE_REVIEW.md) - Complete implementation analysis
- [Project Roadmap](PROJECT_ROADMAP.md) - Future development plans

---

## Support

**Issues or questions?**
- Check [Troubleshooting](#troubleshooting) section above
- Review [CLAUDE_DESKTOP_TEST_REPORT.md](CLAUDE_DESKTOP_TEST_REPORT.md)
- Open an issue on GitHub

**Contributing:**
- Fork the repository
- Create a feature branch
- Submit a Pull Request

---

**Happy Forecasting! 📈**
