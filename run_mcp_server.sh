#!/bin/bash
# MCP Server Launch Script for Claude Desktop
# This script ensures the conda environment is activated before running the server

# Activate conda environment
source /Users/max/miniconda3/bin/activate tsi

# Run the MCP server
cd /Users/max/Documents/code/expo-smooth-mcp
exec python -m src.expo_smooth_mcp.main --transport stdio
