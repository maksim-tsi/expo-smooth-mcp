# Phase 3A: User-Provided Data Support - Implementation Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** 3A - Custom Data Input Enhancement  
**Version:** 1.0.0  
**Created:** October 13, 2025  
**Status:** Ready for Implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Tasks](#tasks)
4. [Phase Completion Checklist](#phase-completion-checklist)
5. [Testing Strategy](#testing-strategy)
6. [Troubleshooting](#troubleshooting)
7. [Time Tracking](#time-tracking)
8. [Next Steps](#next-steps)

---

## Overview

### Goals

Phase 3A enhances the application to accept user-provided data instead of relying solely on the hard-coded `FMCG_Sales.csv` dataset. This makes the application practically useful for real-world forecasting scenarios.

**Key Deliverables:**
1. Gradio UI file upload capability with dynamic SKU detection
2. New MCP tool for custom data forecasting with Base64 encoding
3. Comprehensive test coverage for both interfaces
4. Updated documentation

### Prerequisites

- ✅ Phase 1 complete: Backend logic decoupled
- ✅ Phase 2 complete: FastMCP + FastAPI integration
- ✅ Phase 3 complete: Gradio UI mounted and functional
- ✅ ADR 005 reviewed and approved

### Deliverables

**Code Changes:**
- `app.py`: Enhanced Gradio UI with file upload
- `src/expo_smooth_mcp/main.py`: New MCP tool `forecast_with_custom_data`
- `tests/test_custom_data.py`: New test file

**Documentation Updates:**
- `README.md`: Usage examples for custom data
- `docs/DATA_PREPROCESSING.md`: Data format requirements
- ADR 005: Status updated to "Accepted"

**Quality Gates:**
- All new tests passing (target: 15+ tests)
- Zero regressions in existing tests
- File size limits enforced and documented
- Error messages clear and actionable

### Architecture Impact

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│   Gradio UI (app.py)                 MCP Client              │
│   ┌──────────────────┐              ┌──────────────────┐    │
│   │ gr.File()        │              │ Base64 Encoder   │    │
│   │ Upload CSV/XLS   │              │ (Client-side)    │    │
│   └────────┬─────────┘              └────────┬─────────┘    │
│            │                                  │              │
│            ▼                                  ▼              │
│   ┌──────────────────┐              ┌──────────────────┐    │
│   │ Session State    │              │ MCP Tool:        │    │
│   │ (DataFrame)      │              │ forecast_with_   │    │
│   └────────┬─────────┘              │ custom_data      │    │
│            │                        └────────┬─────────┘    │
│            │                                  │              │
│            └──────────┬───────────────────────┘              │
│                       ▼                                      │
│              ┌─────────────────┐                             │
│              │ Logic Layer     │                             │
│              │ (preprocessing, │                             │
│              │  forecasting)   │                             │
│              └─────────────────┘                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Decisions (from ADR 005):**
- **Gradio**: Native file upload component (best UX)
- **MCP**: Base64 encoding with strict size limits (simple, atomic)
- **Size Limit**: 100KB Base64 (~66KB original file)
- **Future**: Pattern B (two-step upload) for larger files

---

## Tasks

### TASK-3A-01: Add File Upload to Gradio UI

**Estimated Time:** 1.5 hours  
**Complexity:** Medium  
**Dependencies:** None  
**File:** `app.py`

#### Description

Add a `gr.File()` component to the Gradio interface to allow users to upload CSV, Excel, or JSON files containing their sales data.

#### Implementation Steps

1. **Import required modules** at the top of `app.py`:
   ```python
   import pandas as pd
   import io
   from typing import Optional, Tuple
   ```

2. **Create file processing function** (add after `get_sku_list()`):
   ```python
   def process_uploaded_file(file) -> Tuple[Optional[pd.DataFrame], str, list]:
       """
       Process uploaded file and extract SKU list.
       
       Args:
           file: Gradio File object (can be None)
           
       Returns:
           Tuple of (DataFrame, status_message, sku_list)
       """
       if file is None:
           return None, "No file uploaded. Using default dataset.", SKU_LIST
       
       try:
           file_path = file.name
           file_ext = os.path.splitext(file_path)[1].lower()
           
           # Read file based on extension
           if file_ext == '.csv':
               df = pd.read_csv(file_path)
           elif file_ext in ['.xlsx', '.xls']:
               df = pd.read_excel(file_path)
           elif file_ext == '.json':
               df = pd.read_json(file_path)
           else:
               return None, f"❌ Unsupported file type: {file_ext}", SKU_LIST
           
           # Validate required columns
           if 'date' not in df.columns or 'sales' not in df.columns:
               return None, "❌ File must contain 'date' and 'sales' columns", SKU_LIST
           
           # Process data using logic layer
           from src.expo_smooth_mcp import preprocessing, logic
           processed_df = preprocessing.preprocess_data(df)
           
           if processed_df is None or processed_df.empty:
               return None, "❌ File processing failed. Check data format.", SKU_LIST
           
           # Extract SKU list
           skus = logic.get_available_skus(processed_df)
           
           status = f"✅ Loaded {len(processed_df)} rows, {len(skus)} SKUs from {os.path.basename(file_path)}"
           return processed_df, status, skus
           
       except Exception as e:
           return None, f"❌ Error processing file: {str(e)}", SKU_LIST
   ```

3. **Update the Gradio interface** in `create_gradio_interface()`:
   ```python
   def create_gradio_interface():
       """Create and configure the Gradio interface."""
       
       with gr.Blocks(title="Sales Forecasting") as interface:
           gr.Markdown("# 📊 Sales Forecasting Application")
           gr.Markdown("Upload your sales data or use the default dataset to generate forecasts.")
           
           # State to hold custom DataFrame
           custom_data_state = gr.State(None)
           
           with gr.Row():
               with gr.Column(scale=1):
                   gr.Markdown("### 1. Upload Your Data (Optional)")
                   file_upload = gr.File(
                       label="Upload CSV, Excel, or JSON",
                       file_types=[".csv", ".xlsx", ".xls", ".json"],
                       type="filepath"
                   )
                   upload_status = gr.Textbox(
                       label="Upload Status",
                       value="Using default dataset (FMCG_Sales.csv)",
                       interactive=False
                   )
                   
                   gr.Markdown("### 2. Select SKU")
                   sku_dropdown = gr.Dropdown(
                       choices=SKU_LIST,
                       label="Product SKU",
                       value=SKU_LIST[0] if SKU_LIST else None
                   )
                   
                   gr.Markdown("### 3. Set Forecast Horizon")
                   horizon_slider = gr.Slider(
                       minimum=7,
                       maximum=365,
                       value=90,
                       step=1,
                       label="Forecast Days"
                   )
                   
                   forecast_button = gr.Button("Generate Forecast", variant="primary")
               
               with gr.Column(scale=2):
                   plot_output = gr.Plot(label="Forecast Visualization")
           
           # File upload handler
           file_upload.change(
               fn=process_uploaded_file,
               inputs=[file_upload],
               outputs=[custom_data_state, upload_status, sku_dropdown]
           )
           
           # Forecast generation handler
           forecast_button.click(
               fn=create_forecast_plot_with_custom_data,
               inputs=[sku_dropdown, horizon_slider, custom_data_state],
               outputs=[plot_output]
           )
       
       return interface
   ```

4. **Create forecast function with custom data support**:
   ```python
   async def create_forecast_plot_with_custom_data(
       sku: str,
       horizon: int,
       custom_df: Optional[pd.DataFrame]
   ) -> go.Figure:
       """
       Generate forecast plot using custom data or default dataset.
       
       Args:
           sku: Product SKU code
           horizon: Forecast horizon in days
           custom_df: Optional custom DataFrame from file upload
           
       Returns:
           Plotly figure with forecast visualization
       """
       try:
           if custom_df is not None:
               # Use custom data directly with logic layer
               from src.expo_smooth_mcp import logic
               
               # Validate SKU exists
               valid_skus = logic.get_available_skus(custom_df)
               if sku not in valid_skus:
                   return _create_error_plot(
                       f"SKU '{sku}' not found in uploaded data.\n"
                       f"Available SKUs: {', '.join(valid_skus)}"
                   )
               
               # Generate forecast
               forecast_data = logic.get_forecast_data(custom_df, sku, horizon)
               return _create_forecast_plot_from_data(forecast_data)
           
           else:
               # Use existing API-based logic for default dataset
               return await create_forecast_plot(sku, horizon)
               
       except Exception as e:
           return _create_error_plot(f"Error generating forecast: {str(e)}")
   ```

#### Acceptance Criteria

- [ ] File upload component renders correctly in UI
- [ ] Supports CSV, Excel (.xlsx, .xls), and JSON formats
- [ ] Validates required columns ('date', 'sales')
- [ ] Dynamically updates SKU dropdown after upload
- [ ] Shows clear status messages (success, error)
- [ ] Falls back to default dataset if no file uploaded
- [ ] Session state properly maintains uploaded DataFrame
- [ ] UI remains responsive during file processing

---

### TASK-3A-02: Create MCP Tool for Custom Data

**Estimated Time:** 2 hours  
**Complexity:** Medium-High  
**Dependencies:** None  
**File:** `src/expo_smooth_mcp/main.py`

#### Description

Implement a new MCP tool `forecast_with_custom_data` that accepts Base64-encoded file data and generates forecasts on the custom dataset.

#### Implementation Steps

1. **Add imports** at the top of `main.py`:
   ```python
   import base64
   import io
   ```

2. **Define size limit constant** (add after existing constants):
   ```python
   # Maximum Base64 string size for custom data (100KB = ~66KB original file)
   MAX_BASE64_SIZE = 100 * 1024  # 100KB
   ```

3. **Implement the new MCP tool** (add after `list_available_skus` tool):
   ```python
   @mcp.tool()
   async def forecast_with_custom_data(
       file_data_base64: str,
       file_name: str,
       sku: str,
       forecast_horizon: int = 90
   ) -> dict:
       """
       Generate sales forecast using user-provided data.
       
       This tool allows you to forecast on your own sales data by encoding
       the file content as Base64 and passing it directly in the request.
       
       **IMPORTANT SIZE LIMITATION:**
       Due to client payload constraints, this tool supports files up to ~66KB
       (100KB Base64-encoded). For larger files, use the Gradio UI or wait for
       the two-step upload feature in a future release.
       
       **Required Data Format:**
       Your data must contain at minimum:
       - 'date' column: Date/timestamp for each observation
       - 'sales' column: Sales values (numeric)
       - 'sku' column: Product identifier (if multiple products)
       
       Supported formats: CSV, Excel (.xlsx, .xls), JSON
       
       Args:
           file_data_base64: Base64-encoded file content (max 100KB)
           file_name: Original filename (used to detect format)
           sku: Product SKU code to forecast
           forecast_horizon: Number of days to forecast (default: 90, range: 7-365)
       
       Returns:
           Forecast data with historical and predicted values:
           {
               "sku": "PRODUCT_123",
               "dates": ["2024-01-01", ...],
               "actuals": [100.5, 105.2, ...],
               "forecast": [110.1, 112.3, ...],
               "metadata": {
                   "forecast_horizon": 90,
                   "data_points": 365,
                   "model_type": "ExponentialSmoothing"
               }
           }
       
       Example Usage:
           # Python client example
           import base64
           
           with open("my_sales.csv", "rb") as f:
               file_bytes = f.read()
               file_base64 = base64.b64encode(file_bytes).decode('utf-8')
           
           result = await forecast_with_custom_data(
               file_data_base64=file_base64,
               file_name="my_sales.csv",
               sku="PRODUCT_001",
               forecast_horizon=90
           )
       
       Raises:
           ValueError: If file too large, invalid format, or SKU not found
           RuntimeError: If data processing fails
       """
       try:
           # Validate Base64 size
           base64_size = len(file_data_base64)
           if base64_size > MAX_BASE64_SIZE:
               size_kb = base64_size / 1024
               max_kb = MAX_BASE64_SIZE / 1024
               raise ValueError(
                   f"File too large: {size_kb:.1f}KB (max {max_kb:.0f}KB). "
                   f"Original file should be <66KB. "
                   f"For larger files, use the Gradio UI at /gradio"
               )
           
           # Decode Base64
           try:
               file_bytes = base64.b64decode(file_data_base64)
           except Exception as e:
               raise ValueError(f"Invalid Base64 encoding: {str(e)}")
           
           # Detect file format from filename
           file_ext = os.path.splitext(file_name)[1].lower()
           
           # Read data into DataFrame
           try:
               file_buffer = io.BytesIO(file_bytes)
               
               if file_ext == '.csv':
                   df = pd.read_csv(file_buffer)
               elif file_ext in ['.xlsx', '.xls']:
                   df = pd.read_excel(file_buffer)
               elif file_ext == '.json':
                   df = pd.read_json(file_buffer)
               else:
                   raise ValueError(
                       f"Unsupported file format: {file_ext}. "
                       f"Supported: .csv, .xlsx, .xls, .json"
                   )
           except Exception as e:
               raise ValueError(f"Failed to parse file: {str(e)}")
           
           # Validate required columns
           required_cols = ['date', 'sales']
           missing_cols = [col for col in required_cols if col not in df.columns]
           if missing_cols:
               raise ValueError(
                   f"Missing required columns: {missing_cols}. "
                   f"File must contain: {required_cols}"
               )
           
           # Preprocess data
           processed_df = preprocessing.preprocess_data(df)
           if processed_df is None or processed_df.empty:
               raise ValueError(
                   "Data preprocessing failed. Check that 'date' column contains "
                   "valid dates and 'sales' column contains numeric values."
               )
           
           # Validate SKU exists
           valid_skus = logic.get_available_skus(processed_df)
           if sku not in valid_skus:
               raise ValueError(
                   f"SKU '{sku}' not found in data. "
                   f"Available SKUs: {', '.join(valid_skus[:10])}"
                   f"{'...' if len(valid_skus) > 10 else ''}"
               )
           
           # Validate forecast horizon
           logic.validate_forecast_request(sku, forecast_horizon, valid_skus)
           
           # Generate forecast
           forecast_data = logic.get_forecast_data(
               processed_df,
               sku,
               forecast_horizon
           )
           
           return forecast_data
           
       except ValueError as e:
           # Re-raise validation errors
           raise ValueError(f"Custom data forecast failed: {str(e)}")
       
       except Exception as e:
           # Log unexpected errors
           print(f"ERROR in forecast_with_custom_data: {e}")
           raise RuntimeError(f"Forecast generation failed: {str(e)}")
   ```

4. **Update tool list in docstring** (update the module docstring at top of file):
   ```python
   """
   FastMCP Server for Exponential Smoothing Forecasting.
   
   Available MCP Tools:
   - forecast_sku: Generate forecast using default dataset
   - forecast_with_custom_data: Generate forecast using user-provided data (Base64)
   - list_available_skus: List product SKUs in dataset
   """
   ```

#### Acceptance Criteria

- [ ] New tool registered with FastMCP
- [ ] Enforces 100KB Base64 size limit
- [ ] Supports CSV, Excel, and JSON formats
- [ ] Validates required columns ('date', 'sales')
- [ ] Returns clear error for oversized files
- [ ] Returns clear error for missing SKU
- [ ] Returns clear error for invalid data format
- [ ] Tool docstring includes usage examples
- [ ] Size limitation clearly documented

---

### TASK-3A-03: Create Comprehensive Tests

**Estimated Time:** 2.5 hours  
**Complexity:** Medium  
**Dependencies:** TASK-3A-01, TASK-3A-02  
**File:** `tests/test_custom_data.py`

#### Description

Create a comprehensive test suite covering both the Gradio file upload functionality and the new MCP tool with various scenarios.

#### Implementation Steps

Create `tests/test_custom_data.py`:

```python
"""
Test suite for custom data upload functionality.

Tests both Gradio UI file upload and MCP tool for custom data forecasting.
"""

import pytest
import pandas as pd
import base64
import io
import os
from fastapi.testclient import TestClient

# Import the application
from src.expo_smooth_mcp.main import app

# Import Gradio functions to test
from app import process_uploaded_file, create_forecast_plot_with_custom_data


# --- Test Fixtures ---

@pytest.fixture
def sample_csv_data():
    """Create sample CSV data as string."""
    return """date,sku,sales
2024-01-01,SKU_TEST_001,100
2024-01-02,SKU_TEST_001,105
2024-01-03,SKU_TEST_001,110
2024-01-04,SKU_TEST_001,115
2024-01-05,SKU_TEST_001,120
2024-01-06,SKU_TEST_001,125
2024-01-07,SKU_TEST_001,130
2024-01-08,SKU_TEST_001,135"""


@pytest.fixture
def sample_csv_base64(sample_csv_data):
    """Encode sample CSV as Base64."""
    return base64.b64encode(sample_csv_data.encode()).decode()


@pytest.fixture
def large_csv_base64():
    """Create Base64 data exceeding size limit (101KB)."""
    large_data = "date,sku,sales\n" + "2024-01-01,SKU001,100\n" * 10000
    return base64.b64encode(large_data.encode()).decode()


@pytest.fixture
def invalid_csv_base64():
    """Create CSV missing required columns."""
    invalid_data = "timestamp,product,value\n2024-01-01,SKU001,100\n"
    return base64.b64encode(invalid_data.encode()).decode()


@pytest.fixture
def client():
    """Create FastAPI test client."""
    return TestClient(app)


# --- Gradio UI Tests ---

class TestGradioFileUpload:
    """Test Gradio file upload functionality."""
    
    def test_process_no_file(self):
        """Test with no file uploaded."""
        df, status, skus = process_uploaded_file(None)
        
        assert df is None
        assert "No file uploaded" in status
        assert len(skus) > 0  # Should return default SKU list
    
    def test_process_valid_csv(self, tmp_path, sample_csv_data):
        """Test processing valid CSV file."""
        # Create temporary CSV file
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text(sample_csv_data)
        
        # Mock Gradio File object
        class MockFile:
            def __init__(self, path):
                self.name = str(path)
        
        file_obj = MockFile(csv_file)
        df, status, skus = process_uploaded_file(file_obj)
        
        assert df is not None
        assert "✅" in status
        assert "SKU_TEST_001" in skus
        assert len(df) == 8
    
    def test_process_unsupported_format(self, tmp_path):
        """Test with unsupported file format."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("random text")
        
        class MockFile:
            def __init__(self, path):
                self.name = str(path)
        
        file_obj = MockFile(txt_file)
        df, status, skus = process_uploaded_file(file_obj)
        
        assert df is None
        assert "Unsupported file type" in status
    
    def test_process_missing_columns(self, tmp_path):
        """Test CSV with missing required columns."""
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_text("timestamp,product,value\n2024-01-01,SKU001,100")
        
        class MockFile:
            def __init__(self, path):
                self.name = str(path)
        
        file_obj = MockFile(csv_file)
        df, status, skus = process_uploaded_file(file_obj)
        
        assert df is None
        assert "must contain 'date' and 'sales'" in status


class TestGradioForecastWithCustomData:
    """Test Gradio forecast generation with custom data."""
    
    @pytest.mark.asyncio
    async def test_forecast_with_custom_data(self, sample_csv_data):
        """Test forecast generation using custom DataFrame."""
        # Create DataFrame
        df = pd.read_csv(io.StringIO(sample_csv_data))
        from src.expo_smooth_mcp import preprocessing
        processed_df = preprocessing.preprocess_data(df)
        
        # Generate forecast
        fig = await create_forecast_plot_with_custom_data(
            sku="SKU_TEST_001",
            horizon=7,
            custom_df=processed_df
        )
        
        assert fig is not None
        assert len(fig.data) > 0  # Should have traces
    
    @pytest.mark.asyncio
    async def test_forecast_invalid_sku(self, sample_csv_data):
        """Test forecast with non-existent SKU."""
        df = pd.read_csv(io.StringIO(sample_csv_data))
        from src.expo_smooth_mcp import preprocessing
        processed_df = preprocessing.preprocess_data(df)
        
        fig = await create_forecast_plot_with_custom_data(
            sku="INVALID_SKU",
            horizon=7,
            custom_df=processed_df
        )
        
        # Should return error plot
        assert fig is not None
        # Check for error indication in plot


# --- MCP Tool Tests ---

class TestMCPCustomDataTool:
    """Test MCP forecast_with_custom_data tool."""
    
    def test_forecast_with_valid_data(self, client, sample_csv_base64):
        """Test successful forecast with valid Base64 data."""
        payload = {
            "file_data_base64": sample_csv_base64,
            "file_name": "test_data.csv",
            "sku": "SKU_TEST_001",
            "forecast_horizon": 7
        }
        
        # This would be called via MCP protocol
        # For now, test the function directly
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        result = asyncio.run(forecast_with_custom_data(**payload))
        
        assert result["sku"] == "SKU_TEST_001"
        assert len(result["forecast"]) > 0
        assert result["metadata"]["forecast_horizon"] == 7
    
    def test_forecast_file_too_large(self, large_csv_base64):
        """Test error when file exceeds size limit."""
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        payload = {
            "file_data_base64": large_csv_base64,
            "file_name": "large_data.csv",
            "sku": "SKU001",
            "forecast_horizon": 7
        }
        
        with pytest.raises(ValueError, match="File too large"):
            asyncio.run(forecast_with_custom_data(**payload))
    
    def test_forecast_invalid_base64(self):
        """Test error with invalid Base64 encoding."""
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        payload = {
            "file_data_base64": "not-valid-base64!!!",
            "file_name": "test.csv",
            "sku": "SKU001",
            "forecast_horizon": 7
        }
        
        with pytest.raises(ValueError, match="Invalid Base64"):
            asyncio.run(forecast_with_custom_data(**payload))
    
    def test_forecast_missing_required_columns(self, invalid_csv_base64):
        """Test error when CSV missing required columns."""
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        payload = {
            "file_data_base64": invalid_csv_base64,
            "file_name": "invalid.csv",
            "sku": "SKU001",
            "forecast_horizon": 7
        }
        
        with pytest.raises(ValueError, match="Missing required columns"):
            asyncio.run(forecast_with_custom_data(**payload))
    
    def test_forecast_unsupported_format(self):
        """Test error with unsupported file format."""
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        text_data = b"some random text"
        text_base64 = base64.b64encode(text_data).decode()
        
        payload = {
            "file_data_base64": text_base64,
            "file_name": "data.txt",
            "sku": "SKU001",
            "forecast_horizon": 7
        }
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            asyncio.run(forecast_with_custom_data(**payload))
    
    def test_forecast_sku_not_found(self, sample_csv_base64):
        """Test error when SKU not in custom data."""
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        payload = {
            "file_data_base64": sample_csv_base64,
            "file_name": "test.csv",
            "sku": "NONEXISTENT_SKU",
            "forecast_horizon": 7
        }
        
        with pytest.raises(ValueError, match="SKU .* not found"):
            asyncio.run(forecast_with_custom_data(**payload))


# --- Integration Tests ---

class TestCustomDataIntegration:
    """Integration tests for end-to-end custom data workflows."""
    
    def test_full_workflow_gradio(self, tmp_path, sample_csv_data):
        """Test complete Gradio workflow: upload -> process -> forecast."""
        # 1. Upload file
        csv_file = tmp_path / "sales.csv"
        csv_file.write_text(sample_csv_data)
        
        class MockFile:
            def __init__(self, path):
                self.name = str(path)
        
        file_obj = MockFile(csv_file)
        df, status, skus = process_uploaded_file(file_obj)
        
        assert df is not None
        assert "SKU_TEST_001" in skus
        
        # 2. Generate forecast
        import asyncio
        fig = asyncio.run(create_forecast_plot_with_custom_data(
            sku="SKU_TEST_001",
            horizon=7,
            custom_df=df
        ))
        
        assert fig is not None
        assert len(fig.data) > 0
    
    def test_full_workflow_mcp(self, sample_csv_base64):
        """Test complete MCP workflow: encode -> call tool -> get result."""
        from src.expo_smooth_mcp.main import forecast_with_custom_data
        import asyncio
        
        # Call tool with encoded data
        result = asyncio.run(forecast_with_custom_data(
            file_data_base64=sample_csv_base64,
            file_name="sales.csv",
            sku="SKU_TEST_001",
            forecast_horizon=7
        ))
        
        # Verify result structure
        assert "dates" in result
        assert "actuals" in result
        assert "forecast" in result
        assert "metadata" in result
        assert len(result["forecast"]) == 7
```

#### Acceptance Criteria

- [ ] All 15+ tests pass
- [ ] Tests cover happy path scenarios
- [ ] Tests cover all error conditions
- [ ] Tests for size limit enforcement
- [ ] Tests for format validation
- [ ] Tests for SKU validation
- [ ] Integration tests for full workflows
- [ ] Test fixtures properly isolated
- [ ] Tests run in <30 seconds

---

### TASK-3A-04: Update Documentation

**Estimated Time:** 1 hour  
**Complexity:** Low  
**Dependencies:** TASK-3A-01, TASK-3A-02, TASK-3A-03  
**Files:** Multiple documentation files

#### Description

Update project documentation to reflect the new custom data capabilities, including usage examples, data format requirements, and limitations.

#### Implementation Steps

1. **Update README.md** - Add "Using Custom Data" section:
   ```markdown
   ## Using Custom Data
   
   ### Via Gradio UI (Recommended)
   
   1. Open the Gradio UI at `http://localhost:8000/gradio`
   2. Click "Upload CSV, Excel, or JSON" and select your file
   3. Wait for processing (you'll see available SKUs update)
   4. Select a SKU and generate forecast
   
   **Supported Formats:**
   - CSV (.csv)
   - Excel (.xlsx, .xls)
   - JSON (.json)
   
   **Required Data Columns:**
   - `date`: Date/timestamp for each observation
   - `sales`: Sales values (numeric)
   - `sku`: Product identifier (if multiple products)
   
   ### Via MCP Tool
   
   For programmatic access, use the `forecast_with_custom_data` tool:
   
   ```python
   import base64
   
   # Read and encode your file
   with open("my_sales_data.csv", "rb") as f:
       file_base64 = base64.b64encode(f.read()).decode()
   
   # Call MCP tool
   result = await forecast_with_custom_data(
       file_data_base64=file_base64,
       file_name="my_sales_data.csv",
       sku="MY_PRODUCT_001",
       forecast_horizon=90
   )
   ```
   
   **Size Limitation:** Files must be <66KB (100KB Base64-encoded) due to client constraints.
   For larger files, use the Gradio UI.
   ```

2. **Update docs/DATA_PREPROCESSING.md** - Add data format section:
   ```markdown
   ## Custom Data Format Requirements
   
   ### Required Columns
   
   Your data file must contain these columns:
   
   | Column | Type | Description | Example |
   |--------|------|-------------|---------|
   | `date` | Date/String | Observation date | "2024-01-01" |
   | `sales` | Numeric | Sales value | 125.50 |
   | `sku` | String | Product identifier | "PRODUCT_001" |
   
   ### Supported File Formats
   
   - **CSV** (.csv): Comma-separated values
   - **Excel** (.xlsx, .xls): Microsoft Excel format
   - **JSON** (.json): JSON array of records
   
   ### Example Data Files
   
   **CSV Example:**
   ```csv
   date,sku,sales
   2024-01-01,SKU001,100.5
   2024-01-02,SKU001,105.2
   2024-01-03,SKU001,110.8
   ```
   
   **JSON Example:**
   ```json
   [
     {"date": "2024-01-01", "sku": "SKU001", "sales": 100.5},
     {"date": "2024-01-02", "sku": "SKU001", "sales": 105.2},
     {"date": "2024-01-03", "sku": "SKU001", "sales": 110.8}
   ]
   ```
   ```

3. **Update ADR 005 status**:
   ```markdown
   - **Status:** Accepted ✅
   - **Implemented:** 2025-10-13
   ```

4. **Create usage guide** in `docs/CUSTOM_DATA_GUIDE.md`:
   ```markdown
   # Custom Data Guide
   
   This guide explains how to use your own sales data with the forecasting application.
   
   ## Quick Start
   
   ### Method 1: Gradio UI (Best for Most Users)
   
   [Detailed steps...]
   
   ### Method 2: MCP Tool (For Developers)
   
   [Detailed steps with code examples...]
   
   ## Data Format Specifications
   
   [Detailed format requirements...]
   
   ## Limitations
   
   [Size limits, format restrictions...]
   
   ## Troubleshooting
   
   [Common issues and solutions...]
   ```

#### Acceptance Criteria

- [ ] README.md updated with usage examples
- [ ] DATA_PREPROCESSING.md includes format requirements
- [ ] New CUSTOM_DATA_GUIDE.md created
- [ ] ADR 005 marked as "Accepted"
- [ ] All code examples tested and working
- [ ] Documentation includes both Gradio and MCP methods
- [ ] Limitations clearly stated

---

## Phase Completion Checklist

### Code Deliverables
- [ ] `app.py` enhanced with file upload component
- [ ] `process_uploaded_file()` function implemented
- [ ] `create_forecast_plot_with_custom_data()` function implemented
- [ ] Gradio interface updated with file upload UI
- [ ] `src/expo_smooth_mcp/main.py` has new `forecast_with_custom_data` tool
- [ ] Size limit enforcement (100KB) implemented
- [ ] `tests/test_custom_data.py` created with 15+ tests

### Functionality Verification
- [ ] Gradio UI accepts CSV file upload
- [ ] Gradio UI accepts Excel file upload
- [ ] Gradio UI accepts JSON file upload
- [ ] SKU dropdown updates dynamically after upload
- [ ] Forecast generates correctly with custom data
- [ ] MCP tool processes Base64-encoded data
- [ ] MCP tool rejects oversized files with clear error
- [ ] MCP tool validates data format and columns
- [ ] Error messages are clear and actionable

### Quality Gates
- [ ] All new tests pass (15+)
- [ ] Zero regressions in existing tests (59 tests)
- [ ] Code follows project style guidelines
- [ ] Functions have docstrings with examples
- [ ] Error handling comprehensive
- [ ] Input validation thorough

### Documentation
- [ ] README.md updated
- [ ] DATA_PREPROCESSING.md updated
- [ ] CUSTOM_DATA_GUIDE.md created
- [ ] ADR 005 status updated to "Accepted"
- [ ] Code comments clear and helpful

---

## Testing Strategy

### Unit Tests (10 tests)
- File upload processing (valid/invalid formats)
- Column validation
- Base64 encoding/decoding
- Size limit enforcement
- SKU extraction from custom data

### Integration Tests (5 tests)
- Full Gradio workflow (upload → forecast)
- Full MCP workflow (encode → call → result)
- Error propagation through layers
- Session state management
- API fallback behavior

### Manual Testing Checklist
- [ ] Upload various file formats in Gradio
- [ ] Test with files near size limit
- [ ] Verify error messages are user-friendly
- [ ] Check UI responsiveness during processing
- [ ] Test MCP tool via Claude Desktop
- [ ] Verify size limit error in MCP client

---

## Troubleshooting

### Issue: File Upload Not Working in Gradio

**Symptom:** Upload button does nothing or shows error.

**Solution:**
```bash
# Check Gradio version
pip show gradio

# Ensure version is 4.0+
pip install --upgrade gradio

# Check file permissions
ls -la /path/to/upload/directory
```

### Issue: "File Too Large" Error in MCP

**Symptom:** MCP tool returns "File too large" error.

**Solution:**
- Check actual file size: should be <66KB
- Try compressing data (remove unnecessary columns)
- Use Gradio UI for larger files
- Or wait for Pattern B implementation (two-step upload)

### Issue: "Missing Required Columns" Error

**Symptom:** Error about missing 'date' or 'sales' columns.

**Solution:**
```python
# Check your data columns
import pandas as pd
df = pd.read_csv("your_file.csv")
print(df.columns.tolist())

# Rename columns if needed
df = df.rename(columns={
    'Date': 'date',
    'Sales': 'sales',
    'Product': 'sku'
})
```

### Issue: SKU Dropdown Not Updating

**Symptom:** After upload, dropdown still shows default SKUs.

**Solution:**
- Check that `file_upload.change()` event is wired correctly
- Verify `process_uploaded_file()` returns updated SKU list
- Check browser console for JavaScript errors
- Try refreshing the Gradio interface

---

## Time Tracking

| Task | Estimate | Actual | Notes |
|------|----------|--------|-------|
| TASK-3A-01: Gradio File Upload | 1.5h | | |
| TASK-3A-02: MCP Custom Data Tool | 2.0h | | |
| TASK-3A-03: Tests | 2.5h | | |
| TASK-3A-04: Documentation | 1.0h | | |
| **Total** | **7.0h** | | |

---

## Next Steps

After completing Phase 3A:

1. **Validate Phase Completion:**
   - [ ] Run full test suite: `pytest tests/`
   - [ ] Manual testing with various file formats
   - [ ] Test MCP tool via Claude Desktop
   - [ ] Review all documentation updates

2. **Phase 3A Code Review:**
   - Create code review document
   - Analyze implementation quality
   - Document lessons learned
   - Update project roadmap

3. **Proceed to Phase 4:**
   - Docker MCP Toolkit deployment
   - Fly.io cloud deployment
   - Production hardening
   - Monitoring setup

4. **Future Enhancement (Phase 5+):**
   - Implement Pattern B (two-step upload) for large files
   - Add data validation visualizations
   - Support more file formats (Parquet, Feather)
   - Add data quality checks

---

**Phase 3A Implementation Guide Complete**  
**Ready to Begin Custom Data Enhancement**  
**Estimated Time: 7 hours**
