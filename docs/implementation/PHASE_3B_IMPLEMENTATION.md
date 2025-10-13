# Phase 3B: Intelligent Column Mapping - Implementation Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** 3B - Flexible Data Column Mapping  
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

Phase 3B extends Phase 3A by adding intelligent column detection and flexible mapping, enabling the application to work with diverse data formats commonly found in supply chain management without requiring users to rename their columns to match rigid requirements.

**Key Deliverables:**
1. Lightweight column analysis module with heuristic detection
2. Interactive column mapping UI in Gradio
3. Extended MCP tool with column mapping parameters
4. Refactored backend to support flexible column names
5. Comprehensive test coverage
6. Updated documentation with examples

### Prerequisites

- ✅ Phase 3A complete: Custom data upload working
- ✅ ADR 005 extended with Phase 3B decisions
- ✅ Understanding of common SCM data formats

### Deliverables

**Code Changes:**
- `src/expo_smooth_mcp/column_analysis.py`: New module for column detection
- `app.py`: Enhanced UI with column mapping interface
- `src/expo_smooth_mcp/main.py`: Extended MCP tool with mapping parameters
- `src/expo_smooth_mcp/logic.py`: Refactored to accept column parameters
- `tests/test_column_mapping.py`: New comprehensive test suite

**Documentation Updates:**
- `README.md`: Column mapping usage examples
- `docs/DATA_PREPROCESSING.md`: Extended with mapping guidance
- ADR 005: Extended with Phase 3B decisions (✅ Complete)

**Quality Gates:**
- All new tests passing (target: 15+ tests)
- Zero regressions in existing tests (94 tests must pass)
- Heuristic accuracy >80% on standard SCM datasets
- Backward compatibility maintained

### Architecture Impact

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interfaces                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Gradio UI                           MCP Client                  │
│  ┌──────────────────┐               ┌──────────────────┐        │
│  │ File Upload      │               │ file_data_base64 │        │
│  └────────┬─────────┘               │ date_column      │        │
│           │                         │ metric_column    │        │
│           ▼                         │ product_column   │        │
│  ┌──────────────────┐               └────────┬─────────┘        │
│  │ Column Analyzer  │◄──────────────────────┘                  │
│  │ (Heuristics)     │                                            │
│  └────────┬─────────┘                                            │
│           │                                                       │
│           ▼                                                       │
│  ┌──────────────────┐                                            │
│  │ Mapping UI       │                                            │
│  │ - Date dropdown  │                                            │
│  │ - Metric dropdown│                                            │
│  │ - Product dropdown                                            │
│  │ - Smart hints    │                                            │
│  └────────┬─────────┘                                            │
│           │                                                       │
│           ▼                                                       │
│  ┌──────────────────────────────────┐                            │
│  │ Backend Logic (Column-Flexible)  │                            │
│  │ - Renames columns internally     │                            │
│  │ - Validates column types         │                            │
│  │ - Generates forecast             │                            │
│  └──────────────────────────────────┘                            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Key Design Decisions (from ADR 005 Extension):**
- **Approach:** Interactive mapping with heuristic suggestions
- **Heuristics:** Lightweight string matching on column names + type checking
- **UI Pattern:** Smart defaults + user confirmation
- **MCP Pattern:** Optional parameters with sensible defaults
- **Backward Compatibility:** Default values maintain Phase 3A behavior

---

## Tasks

### TASK-3B-01: Create Column Analysis Module

**Estimated Time:** 2 hours  
**Complexity:** Medium  
**Dependencies:** None  
**File:** `src/expo_smooth_mcp/column_analysis.py` (new file)

#### Description

Create a lightweight module that analyzes DataFrame columns and suggests appropriate mappings for date, metric, and product identifier columns using simple heuristics.

#### Implementation Steps

1. **Create the new module file:**
   ```bash
   touch src/expo_smooth_mcp/column_analysis.py
   ```

2. **Implement the column analyzer:**

```python
"""
Column Analysis Module for Intelligent Data Mapping.

This module provides lightweight heuristic-based detection of column types
in user-provided datasets, specifically for time-series forecasting in
supply chain management contexts.
"""

import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


# Common column name patterns for different types
DATE_KEYWORDS = [
    'date', 'time', 'day', 'period', 'ds', 
    'timestamp', 'datetime', 'order_date', 'orderdate',
    'transaction_date', 'week', 'month', 'year'
]

METRIC_KEYWORDS = [
    'sales', 'quantity', 'demand', 'revenue', 
    'units', 'value', 'amount', 'y', 'units_sold',
    'order_quantity', 'qty', 'volume', 'orders'
]

PRODUCT_KEYWORDS = [
    'sku', 'product', 'item', 'id', 'code',
    'product_id', 'product_code', 'item_id', 'item_code',
    'productid', 'itemid', 'productcode', 'itemcode'
]


def analyze_columns(df: pd.DataFrame) -> Dict[str, any]:
    """
    Analyze DataFrame columns and suggest mappings for forecasting.
    
    Uses lightweight heuristics to detect:
    - Date/time columns (for time series index)
    - Metric columns (numeric values to forecast)
    - Product identifier columns (for grouping/filtering)
    
    Args:
        df: Input DataFrame to analyze
        
    Returns:
        Dictionary with analysis results:
        {
            "all_columns": List of all column names,
            "date_candidates": List of likely date columns,
            "metric_candidates": List of likely metric columns,
            "product_candidates": List of likely product ID columns,
            "suggested_date": Best guess for date column,
            "suggested_metric": Best guess for metric column,
            "suggested_product": Best guess for product column,
            "analysis_details": Detailed scoring information
        }
    
    Example:
        >>> df = pd.read_csv("sales.csv")
        >>> analysis = analyze_columns(df)
        >>> print(f"Suggested date: {analysis['suggested_date']}")
        >>> print(f"Suggested metric: {analysis['suggested_metric']}")
    """
    if df is None or df.empty:
        return _empty_analysis()
    
    analysis = {
        "all_columns": df.columns.tolist(),
        "date_candidates": [],
        "metric_candidates": [],
        "product_candidates": [],
        "suggested_date": None,
        "suggested_metric": None,
        "suggested_product": None,
        "analysis_details": {}
    }
    
    # Analyze each column
    for col in df.columns:
        col_lower = str(col).lower().strip()
        col_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "scores": {}
        }
        
        # Check for date column
        date_score = _score_date_column(df[col], col_lower)
        if date_score > 0:
            col_info["scores"]["date"] = date_score
            analysis["date_candidates"].append({
                "column": col,
                "score": date_score
            })
        
        # Check for metric column (must be numeric)
        if pd.api.types.is_numeric_dtype(df[col]):
            metric_score = _score_metric_column(df[col], col_lower)
            if metric_score > 0:
                col_info["scores"]["metric"] = metric_score
                analysis["metric_candidates"].append({
                    "column": col,
                    "score": metric_score
                })
        
        # Check for product identifier column
        product_score = _score_product_column(df[col], col_lower)
        if product_score > 0:
            col_info["scores"]["product"] = product_score
            analysis["product_candidates"].append({
                "column": col,
                "score": product_score
            })
        
        analysis["analysis_details"][col] = col_info
    
    # Sort candidates by score
    analysis["date_candidates"].sort(key=lambda x: x["score"], reverse=True)
    analysis["metric_candidates"].sort(key=lambda x: x["score"], reverse=True)
    analysis["product_candidates"].sort(key=lambda x: x["score"], reverse=True)
    
    # Pick best suggestions
    if analysis["date_candidates"]:
        analysis["suggested_date"] = analysis["date_candidates"][0]["column"]
    
    if analysis["metric_candidates"]:
        analysis["suggested_metric"] = analysis["metric_candidates"][0]["column"]
    
    if analysis["product_candidates"]:
        analysis["suggested_product"] = analysis["product_candidates"][0]["column"]
    
    logger.info(f"Column analysis complete: {len(df.columns)} columns analyzed")
    logger.info(f"Suggestions - Date: {analysis['suggested_date']}, "
                f"Metric: {analysis['suggested_metric']}, "
                f"Product: {analysis['suggested_product']}")
    
    return analysis


def _score_date_column(series: pd.Series, col_name_lower: str) -> float:
    """
    Score how likely a column is to be a date/time column.
    
    Returns score from 0.0 (definitely not) to 1.0 (definitely is).
    """
    score = 0.0
    
    # Check column name keywords (0.5 points)
    for keyword in DATE_KEYWORDS:
        if keyword in col_name_lower:
            score += 0.5
            break
    
    # Check if data is parseable as datetime (0.5 points)
    try:
        # Test on a sample to avoid processing large datasets
        sample_size = min(100, len(series))
        sample = series.head(sample_size)
        
        parsed = pd.to_datetime(sample, errors='coerce')
        valid_ratio = parsed.notna().sum() / len(sample)
        
        # If >80% of values parse successfully, add score
        if valid_ratio > 0.8:
            score += 0.5
    except Exception:
        pass
    
    return min(score, 1.0)


def _score_metric_column(series: pd.Series, col_name_lower: str) -> float:
    """
    Score how likely a numeric column is to be a metric to forecast.
    
    Returns score from 0.0 (definitely not) to 1.0 (definitely is).
    """
    score = 0.0
    
    # Check column name keywords
    for keyword in METRIC_KEYWORDS:
        if keyword in col_name_lower:
            # Higher score for exact matches
            if col_name_lower == keyword:
                score += 0.8
            else:
                score += 0.5
            break
    
    # Check if values are reasonable for metrics (0.2 points)
    # Most metrics should be non-negative
    if (series >= 0).mean() > 0.9:
        score += 0.2
    
    return min(score, 1.0)


def _score_product_column(series: pd.Series, col_name_lower: str) -> float:
    """
    Score how likely a column is to be a product identifier.
    
    Returns score from 0.0 (definitely not) to 1.0 (definitely is).
    """
    score = 0.0
    
    # Check column name keywords
    for keyword in PRODUCT_KEYWORDS:
        if keyword in col_name_lower:
            # Higher score for exact matches
            if col_name_lower == keyword or col_name_lower == f"{keyword}_id":
                score += 0.8
            else:
                score += 0.5
            break
    
    # Check cardinality (0.2 points)
    # Product IDs typically have moderate cardinality
    unique_ratio = series.nunique() / len(series) if len(series) > 0 else 0
    if 0.01 < unique_ratio < 0.5:
        score += 0.2
    
    return min(score, 1.0)


def _empty_analysis() -> Dict[str, any]:
    """Return empty analysis structure for edge cases."""
    return {
        "all_columns": [],
        "date_candidates": [],
        "metric_candidates": [],
        "product_candidates": [],
        "suggested_date": None,
        "suggested_metric": None,
        "suggested_product": None,
        "analysis_details": {}
    }


def validate_column_mapping(
    df: pd.DataFrame,
    date_column: str,
    metric_column: str,
    product_column: Optional[str] = None
) -> Dict[str, any]:
    """
    Validate that specified column mapping is valid for forecasting.
    
    Args:
        df: DataFrame to validate against
        date_column: Name of the date column
        metric_column: Name of the metric column
        product_column: Optional name of product ID column
        
    Returns:
        Dictionary with validation results:
        {
            "valid": True/False,
            "errors": List of error messages,
            "warnings": List of warning messages
        }
    
    Example:
        >>> validation = validate_column_mapping(df, "OrderDate", "Sales", "SKU")
        >>> if not validation["valid"]:
        >>>     print("Errors:", validation["errors"])
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check columns exist
    if date_column not in df.columns:
        result["valid"] = False
        result["errors"].append(f"Date column '{date_column}' not found in data")
    
    if metric_column not in df.columns:
        result["valid"] = False
        result["errors"].append(f"Metric column '{metric_column}' not found in data")
    
    if product_column and product_column not in df.columns:
        result["valid"] = False
        result["errors"].append(f"Product column '{product_column}' not found in data")
    
    if not result["valid"]:
        return result
    
    # Validate date column can be parsed
    try:
        parsed = pd.to_datetime(df[date_column], errors='coerce')
        valid_ratio = parsed.notna().sum() / len(df)
        
        if valid_ratio < 0.5:
            result["valid"] = False
            result["errors"].append(
                f"Date column '{date_column}' has too many invalid dates "
                f"({valid_ratio:.1%} valid)"
            )
        elif valid_ratio < 0.95:
            result["warnings"].append(
                f"Date column '{date_column}' has some invalid dates "
                f"({valid_ratio:.1%} valid)"
            )
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Cannot parse date column '{date_column}': {str(e)}")
    
    # Validate metric column is numeric
    if not pd.api.types.is_numeric_dtype(df[metric_column]):
        result["valid"] = False
        result["errors"].append(
            f"Metric column '{metric_column}' must be numeric, "
            f"got {df[metric_column].dtype}"
        )
    
    # Check for missing values
    if df[metric_column].isna().sum() > 0:
        missing_pct = df[metric_column].isna().mean() * 100
        result["warnings"].append(
            f"Metric column '{metric_column}' has {missing_pct:.1f}% missing values"
        )
    
    return result
```

#### Acceptance Criteria

- [ ] Module created with all functions implemented
- [ ] Heuristics detect date columns with >80% accuracy on test datasets
- [ ] Heuristics detect metric columns with >80% accuracy on test datasets
- [ ] Scoring system properly prioritizes exact matches
- [ ] Validation function catches common errors
- [ ] Logging provides useful debugging information
- [ ] Code is well-documented with examples

---

### TASK-3B-02: Update Gradio UI with Column Mapping

**Estimated Time:** 2 hours  
**Complexity:** Medium  
**Dependencies:** TASK-3B-01  
**File:** `app.py`

#### Description

Enhance the Gradio interface to include an interactive column mapping section that appears after file upload, allowing users to confirm or adjust automatically detected column mappings.

#### Implementation Steps

1. **Import the column analysis module:**

```python
from src.expo_smooth_mcp import column_analysis
```

2. **Update the file upload handler:**

```python
def process_uploaded_file(file) -> tuple:
    """
    Process uploaded file and analyze columns.
    
    Returns:
        Tuple of (DataFrame, analysis_dict, status_message, sku_list)
    """
    if file is None:
        return None, None, "No file uploaded. Using default dataset.", SKU_LIST
    
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
            return None, None, f"❌ Unsupported file type: {file_ext}", SKU_LIST
        
        # Analyze columns
        analysis = column_analysis.analyze_columns(df)
        
        # Create status message
        status = f"✅ Loaded {len(df)} rows, {len(df.columns)} columns from {os.path.basename(file_path)}"
        
        # Add smart suggestions to status
        if analysis['suggested_date'] and analysis['suggested_metric']:
            status += f"\n💡 Auto-detected: Date={analysis['suggested_date']}, Metric={analysis['suggested_metric']}"
        else:
            status += "\n⚠️ Could not auto-detect columns. Please select manually."
        
        return df, analysis, status, []
        
    except Exception as e:
        return None, None, f"❌ Error processing file: {str(e)}", SKU_LIST
```

3. **Add function to generate forecast with mapping:**

```python
async def generate_forecast_with_mapping(
    df: Optional[pd.DataFrame],
    date_col: str,
    metric_col: str,
    product_col: Optional[str],
    sku: str,
    horizon: int
) -> go.Figure:
    """
    Generate forecast using custom column mapping.
    
    Args:
        df: Uploaded DataFrame (or None for default dataset)
        date_col: Name of date column in user's data
        metric_col: Name of metric column in user's data
        product_col: Optional name of product ID column
        sku: Product SKU to forecast
        horizon: Forecast horizon in days
        
    Returns:
        Plotly figure with forecast visualization
    """
    if df is None:
        # Use default dataset via API
        return await create_forecast_plot(sku)
    
    try:
        # Validate column mapping
        validation = column_analysis.validate_column_mapping(
            df, date_col, metric_col, product_col
        )
        
        if not validation["valid"]:
            error_msg = "❌ Invalid column mapping:\n" + "\n".join(validation["errors"])
            return _create_error_plot(error_msg)
        
        # Show warnings if any
        if validation["warnings"]:
            print("⚠️ Warnings:", validation["warnings"])
        
        # Rename columns to expected format
        df_mapped = df.copy()
        df_mapped = df_mapped.rename(columns={
            date_col: 'date',
            metric_col: 'sales'
        })
        
        if product_col:
            df_mapped = df_mapped.rename(columns={product_col: 'sku'})
        
        # Process with existing logic
        from src.expo_smooth_mcp import preprocessing, logic
        processed_df = preprocessing.preprocess_data(df_mapped)
        
        if processed_df is None or processed_df.empty:
            return _create_error_plot("❌ Data processing failed. Check data format.")
        
        # Validate SKU exists
        valid_skus = logic.get_available_skus(processed_df)
        if sku not in valid_skus:
            return _create_error_plot(
                f"❌ SKU '{sku}' not found.\nAvailable: {', '.join(valid_skus[:10])}"
            )
        
        # Generate forecast
        forecast_data = logic.get_forecast_data(processed_df, sku, horizon)
        return _create_forecast_plot_from_data(forecast_data)
        
    except Exception as e:
        return _create_error_plot(f"❌ Error generating forecast: {str(e)}")
```

4. **Update the Gradio interface:**

```python
def create_gradio_interface():
    """Create and configure the Gradio interface with column mapping."""
    
    with gr.Blocks(title="Sales Forecasting") as interface:
        gr.Markdown("# 📊 Sales Forecasting Application")
        gr.Markdown("Upload your sales data to generate forecasts with exponential smoothing.")
        
        # State variables
        df_state = gr.State(None)
        analysis_state = gr.State(None)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Step 1: File Upload
                gr.Markdown("### 1️⃣ Upload Your Data")
                file_upload = gr.File(
                    label="Upload CSV, Excel, or JSON",
                    file_types=[".csv", ".xlsx", ".xls", ".json"],
                    type="filepath"
                )
                upload_status = gr.Textbox(
                    label="Upload Status",
                    value="📁 No file uploaded. Using default dataset.",
                    interactive=False,
                    lines=3
                )
                
                # Step 2: Column Mapping (initially hidden)
                with gr.Group(visible=False) as mapping_section:
                    gr.Markdown("### 2️⃣ Map Your Data Columns")
                    gr.Markdown("*Select which columns contain your date, metric, and product data.*")
                    
                    date_column = gr.Dropdown(
                        label="📅 Date/Time Column",
                        choices=[],
                        info="Column containing dates or timestamps"
                    )
                    
                    metric_column = gr.Dropdown(
                        label="📈 Metric Column to Forecast",
                        choices=[],
                        info="Numeric column with values to forecast (sales, demand, quantity, etc.)"
                    )
                    
                    product_column = gr.Dropdown(
                        label="🏷️ Product ID Column (Optional)",
                        choices=[],
                        value=None,
                        info="Column for grouping by product (SKU, Product ID, etc.)"
                    )
                
                # Step 3: Select Product & Parameters
                gr.Markdown("### 3️⃣ Select Product & Forecast Settings")
                sku_dropdown = gr.Dropdown(
                    choices=SKU_LIST,
                    label="Product SKU",
                    value=SKU_LIST[0] if SKU_LIST else None
                )
                
                horizon_slider = gr.Slider(
                    minimum=7,
                    maximum=365,
                    value=90,
                    step=1,
                    label="Forecast Horizon (days)"
                )
                
                forecast_button = gr.Button("🚀 Generate Forecast", variant="primary")
            
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Forecast Visualization")
        
        # Event: File uploaded
        file_upload.upload(
            fn=process_uploaded_file,
            inputs=[file_upload],
            outputs=[df_state, analysis_state, upload_status, sku_dropdown]
        ).then(
            # Show mapping section and populate dropdowns
            fn=lambda analysis: (
                gr.update(visible=True),
                gr.update(
                    choices=analysis.get("all_columns", []) if analysis else [],
                    value=analysis.get("suggested_date") if analysis else None
                ),
                gr.update(
                    choices=analysis.get("all_columns", []) if analysis else [],
                    value=analysis.get("suggested_metric") if analysis else None
                ),
                gr.update(
                    choices=["(None)"] + (analysis.get("all_columns", []) if analysis else []),
                    value=analysis.get("suggested_product") if analysis else None
                )
            ),
            inputs=[analysis_state],
            outputs=[mapping_section, date_column, metric_column, product_column]
        )
        
        # Event: Generate forecast
        forecast_button.click(
            fn=generate_forecast_with_mapping,
            inputs=[
                df_state,
                date_column,
                metric_column,
                product_column,
                sku_dropdown,
                horizon_slider
            ],
            outputs=[plot_output]
        )
    
    return interface
```

#### Acceptance Criteria

- [ ] Column mapping section appears after file upload
- [ ] Dropdowns populated with column names from uploaded file
- [ ] Smart suggestions pre-selected based on heuristics
- [ ] User can override suggestions
- [ ] Validation errors shown clearly
- [ ] Forecast generates correctly with mapped columns
- [ ] Backward compatible with default dataset

---

### TASK-3B-03: Extend MCP Tool with Column Mapping

**Estimated Time:** 1.5 hours  
**Complexity:** Medium  
**Dependencies:** TASK-3B-01  
**File:** `src/expo_smooth_mcp/main.py`

#### Description

Extend the `forecast_with_custom_data` MCP tool to accept optional column mapping parameters, enabling MCP clients to specify which columns contain date, metric, and product data.

#### Implementation Steps

1. **Import column analysis module:**

```python
from . import column_analysis
```

2. **Update the MCP tool signature and implementation:**

```python
@mcp.tool()
async def forecast_with_custom_data(
    file_data_base64: str,
    file_name: str,
    sku: str,
    forecast_horizon: int = 90,
    date_column: str = "date",
    metric_column: str = "sales",
    product_column: Optional[str] = None
) -> dict:
    """
    Generate sales forecast using user-provided data with flexible column mapping.

    This tool allows you to forecast on your own sales data by encoding
    the file content as Base64. You can specify which columns in your data
    contain the date, metric, and product identifier information.

    **SIZE LIMITATION:**
    Files must be under 100KB when Base64-encoded (~66KB raw data).
    For larger files, use the Gradio UI at /gradio.

    **COLUMN MAPPING:**
    Your data may have columns with any names. Use the column parameters to
    map your columns to the required roles:
    - date_column: The column containing dates/timestamps
    - metric_column: The column containing numeric values to forecast
    - product_column: The column containing product/SKU identifiers (optional)

    Args:
        file_data_base64: Base64-encoded file content (max 100KB)
        file_name: Original filename (used to detect format)
        sku: Product SKU code to forecast
        forecast_horizon: Number of days to forecast (default: 90, range: 7-365)
        date_column: Name of your date/time column (default: "date")
        metric_column: Name of your metric column to forecast (default: "sales")
        product_column: Name of your product ID column (default: None)

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
                "model_type": "ExponentialSmoothing",
                "column_mapping": {
                    "date": "OrderDate",
                    "metric": "Units_Sold",
                    "product": "Product_Code"
                }
            }
        }

    Example Usage with Custom Columns:
        # Python client example with non-standard column names
        import base64

        # Data has columns: "OrderDate", "Product_Code", "Units_Sold"
        with open("orders.csv", "rb") as f:
            file_bytes = f.read()
            file_base64 = base64.b64encode(file_bytes).decode('utf-8')

        result = await forecast_with_custom_data(
            file_data_base64=file_base64,
            file_name="orders.csv",
            sku="PROD_123",
            forecast_horizon=90,
            date_column="OrderDate",
            metric_column="Units_Sold",
            product_column="Product_Code"
        )

    Common Column Names in SCM:
        Date columns: date, timestamp, day, period, order_date, ds
        Metric columns: sales, quantity, demand, revenue, units_sold, orders
        Product columns: sku, product_id, item_id, product_code

    Raises:
        ValueError: If file too large, invalid format, columns not found, or SKU not found
        RuntimeError: If data processing fails
    """
    try:
        # Validate Base64 size (existing code)
        base64_size = len(file_data_base64)
        if base64_size > MAX_BASE64_SIZE:
            size_kb = base64_size / 1024
            max_kb = MAX_BASE64_SIZE / 1024
            raise ValueError(
                f"File too large: {size_kb:.1f}KB (max {max_kb:.0f}KB). "
                f"Original file should be <66KB. "
                f"For larger files, use the Gradio UI at /gradio"
            )

        # Decode Base64 (existing code)
        try:
            file_bytes = base64.b64decode(file_data_base64)
        except Exception as e:
            raise ValueError(f"Invalid Base64 encoding: {str(e)}")

        # Detect file format and read (existing code)
        file_ext = os.path.splitext(file_name)[1].lower()
        
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

        # NEW: Validate column mapping
        validation = column_analysis.validate_column_mapping(
            df, date_column, metric_column, product_column
        )
        
        if not validation["valid"]:
            error_details = "\n".join(validation["errors"])
            raise ValueError(
                f"Invalid column mapping:\n{error_details}\n\n"
                f"Available columns: {', '.join(df.columns.tolist())}"
            )
        
        # Log warnings if any
        if validation["warnings"]:
            for warning in validation["warnings"]:
                print(f"WARNING: {warning}")

        # NEW: Rename columns to expected format
        df_mapped = df.rename(columns={
            date_column: 'date',
            metric_column: 'sales'
        })
        
        if product_column:
            df_mapped = df_mapped.rename(columns={product_column: 'sku'})

        # Preprocess data (now using mapped columns)
        processed_df = preprocessing.preprocess_data(df_mapped)
        if processed_df is None or processed_df.empty:
            raise ValueError(
                "Data preprocessing failed. Ensure date column contains "
                "valid dates and metric column contains numeric values."
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
        
        # Add column mapping info to metadata
        forecast_data["metadata"]["column_mapping"] = {
            "date": date_column,
            "metric": metric_column,
            "product": product_column
        }

        return forecast_data

    except ValueError as e:
        raise ValueError(f"Custom data forecast failed: {str(e)}")

    except Exception as e:
        print(f"ERROR in forecast_with_custom_data: {e}")
        raise RuntimeError(f"Forecast generation failed: {str(e)}")
```

#### Acceptance Criteria

- [ ] Tool accepts new column mapping parameters
- [ ] Default values maintain backward compatibility
- [ ] Column validation works correctly
- [ ] Clear error messages for invalid mappings
- [ ] Documentation includes examples with custom columns
- [ ] Metadata includes column mapping information

---

### TASK-3B-04: Refactor Backend for Column Flexibility

**Estimated Time:** 1.5 hours  
**Complexity:** Low-Medium  
**Dependencies:** None  
**File:** `src/expo_smooth_mcp/logic.py`

#### Description

Refactor the backend forecasting functions to accept column names as parameters, making them flexible enough to work with any column naming convention.

#### Implementation Steps

1. **Update `get_forecast_data` function signature:**

```python
def get_forecast_data(
    df: pd.DataFrame,
    sku: str,
    forecast_horizon: int,
    date_col: str = 'date',
    metric_col: str = 'sales',
    product_col: str = 'sku'
) -> dict:
    """
    Generate forecast data for a specific product SKU with flexible column mapping.
    
    This function now accepts column names as parameters, allowing it to work
    with data that uses any column naming convention. Columns are internally
    renamed to the standard format expected by the forecasting logic.
    
    Args:
        df: Preprocessed DataFrame with time series data
        sku: Product SKU code to forecast
        forecast_horizon: Number of days to forecast ahead
        date_col: Name of the date column (default: 'date')
        metric_col: Name of the metric column (default: 'sales')
        product_col: Name of the product ID column (default: 'sku')
        
    Returns:
        Dictionary containing forecast data and metadata
        
    Raises:
        ValueError: If SKU not found or invalid horizon
        
    Example:
        # Standard column names
        forecast = get_forecast_data(df, "PROD_123", 90)
        
        # Custom column names
        forecast = get_forecast_data(
            df, "PROD_123", 90,
            date_col="OrderDate",
            metric_col="Units_Sold",
            product_col="Product_Code"
        )
    """
    # Make a working copy and rename columns to standard format
    df_work = df.copy()
    
    # Only rename if columns are different from expected
    if date_col != 'date' or metric_col != 'sales' or product_col != 'sku':
        rename_map = {}
        if date_col in df_work.columns:
            rename_map[date_col] = 'date'
        if metric_col in df_work.columns:
            rename_map[metric_col] = 'sales'
        if product_col in df_work.columns:
            rename_map[product_col] = 'sku'
        
        df_work = df_work.rename(columns=rename_map)
    
    # Rest of the function remains unchanged
    # (existing forecast generation logic)
    ...
```

2. **Update any other functions that need column flexibility:**

Review `preprocessing.py` and other modules to ensure they can handle renamed columns correctly. Most functions should already work since we're renaming before processing.

#### Acceptance Criteria

- [ ] Functions accept column name parameters
- [ ] Default values maintain backward compatibility
- [ ] Column renaming works correctly
- [ ] All existing tests still pass
- [ ] Documentation updated with examples

---

### TASK-3B-05: Create Comprehensive Test Suite

**Estimated Time:** 1.5 hours  
**Complexity:** Medium  
**Dependencies:** TASK-3B-01, TASK-3B-02, TASK-3B-03, TASK-3B-04  
**File:** `tests/test_column_mapping.py` (new file)

#### Description

Create a comprehensive test suite covering column analysis, validation, and end-to-end forecasting with custom column mappings.

#### Implementation Steps

Create `tests/test_column_mapping.py`:

```python
"""
Test suite for intelligent column mapping functionality.

Tests cover:
- Column analysis and heuristic detection
- Column validation
- Gradio UI with column mapping
- MCP tool with custom columns
- End-to-end workflows
"""

import pytest
import pandas as pd
import base64
import io
from src.expo_smooth_mcp import column_analysis


# --- Test Fixtures ---

@pytest.fixture
def standard_scm_data():
    """Create DataFrame with standard SCM column names."""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30),
        'sku': ['PROD_001'] * 30,
        'sales': range(100, 130)
    })


@pytest.fixture
def custom_column_data():
    """Create DataFrame with non-standard column names."""
    return pd.DataFrame({
        'OrderDate': pd.date_range('2024-01-01', periods=30),
        'Product_Code': ['PROD_001'] * 30,
        'Units_Sold': range(100, 130),
        'Warehouse': ['WH_01'] * 30
    })


@pytest.fixture
def ambiguous_data():
    """Create DataFrame with multiple numeric columns."""
    return pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=30),
        'item_id': ['ITEM_A'] * 30,
        'quantity': range(100, 130),
        'price': range(10, 40),
        'revenue': range(1000, 1300, 10)
    })


# --- Column Analysis Tests ---

class TestColumnAnalysis:
    """Test column analysis and heuristic detection."""
    
    def test_analyze_standard_columns(self, standard_scm_data):
        """Test analysis with standard column names."""
        analysis = column_analysis.analyze_columns(standard_scm_data)
        
        assert analysis['suggested_date'] == 'date'
        assert analysis['suggested_metric'] == 'sales'
        assert analysis['suggested_product'] == 'sku'
    
    def test_analyze_custom_columns(self, custom_column_data):
        """Test analysis detects custom SCM column names."""
        analysis = column_analysis.analyze_columns(custom_column_data)
        
        assert analysis['suggested_date'] == 'OrderDate'
        assert analysis['suggested_metric'] == 'Units_Sold'
        assert analysis['suggested_product'] == 'Product_Code'
    
    def test_analyze_ambiguous_columns(self, ambiguous_data):
        """Test analysis prioritizes correct columns when multiple options exist."""
        analysis = column_analysis.analyze_columns(ambiguous_data)
        
        assert analysis['suggested_date'] == 'timestamp'
        # Should prefer 'quantity' over 'price' or 'revenue'
        assert analysis['suggested_metric'] == 'quantity'
        assert analysis['suggested_product'] == 'item_id'
    
    def test_analyze_empty_dataframe(self):
        """Test analysis handles empty DataFrame gracefully."""
        df = pd.DataFrame()
        analysis = column_analysis.analyze_columns(df)
        
        assert analysis['suggested_date'] is None
        assert analysis['suggested_metric'] is None
        assert len(analysis['all_columns']) == 0
    
    def test_date_column_scoring(self):
        """Test date column detection with various formats."""
        df = pd.DataFrame({
            'order_date': pd.date_range('2024-01-01', periods=10),
            'value': range(10)
        })
        
        analysis = column_analysis.analyze_columns(df)
        assert 'order_date' in [c['column'] for c in analysis['date_candidates']]
    
    def test_metric_column_scoring(self):
        """Test metric column detection favors common names."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'demand': range(10),
            'random_number': range(10, 20)
        })
        
        analysis = column_analysis.analyze_columns(df)
        # 'demand' should score higher than 'random_number'
        assert analysis['suggested_metric'] == 'demand'


class TestColumnValidation:
    """Test column mapping validation."""
    
    def test_validate_valid_mapping(self, custom_column_data):
        """Test validation passes for valid mapping."""
        validation = column_analysis.validate_column_mapping(
            custom_column_data,
            'OrderDate',
            'Units_Sold',
            'Product_Code'
        )
        
        assert validation['valid'] is True
        assert len(validation['errors']) == 0
    
    def test_validate_missing_date_column(self, custom_column_data):
        """Test validation fails when date column doesn't exist."""
        validation = column_analysis.validate_column_mapping(
            custom_column_data,
            'NonExistentDate',
            'Units_Sold'
        )
        
        assert validation['valid'] is False
        assert any('NonExistentDate' in err for err in validation['errors'])
    
    def test_validate_missing_metric_column(self, custom_column_data):
        """Test validation fails when metric column doesn't exist."""
        validation = column_analysis.validate_column_mapping(
            custom_column_data,
            'OrderDate',
            'NonExistentMetric'
        )
        
        assert validation['valid'] is False
        assert any('NonExistentMetric' in err for err in validation['errors'])
    
    def test_validate_non_numeric_metric(self):
        """Test validation fails when metric column is not numeric."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'text_column': ['abc'] * 10
        })
        
        validation = column_analysis.validate_column_mapping(
            df,
            'date',
            'text_column'
        )
        
        assert validation['valid'] is False
        assert any('numeric' in err.lower() for err in validation['errors'])
    
    def test_validate_unparseable_dates(self):
        """Test validation fails when date column has invalid dates."""
        df = pd.DataFrame({
            'bad_dates': ['not a date'] * 10,
            'values': range(10)
        })
        
        validation = column_analysis.validate_column_mapping(
            df,
            'bad_dates',
            'values'
        )
        
        assert validation['valid'] is False


# --- Integration Tests ---

class TestGradioColumnMapping:
    """Test Gradio interface with column mapping."""
    
    def test_process_file_with_custom_columns(self, tmp_path, custom_column_data):
        """Test file processing detects custom columns."""
        from app import process_uploaded_file
        
        # Save DataFrame to temporary CSV
        csv_file = tmp_path / "orders.csv"
        custom_column_data.to_csv(csv_file, index=False)
        
        # Mock Gradio File object
        class MockFile:
            def __init__(self, path):
                self.name = str(path)
        
        file_obj = MockFile(csv_file)
        df, analysis, status, skus = process_uploaded_file(file_obj)
        
        assert df is not None
        assert analysis is not None
        assert analysis['suggested_date'] == 'OrderDate'
        assert analysis['suggested_metric'] == 'Units_Sold'
        assert '✅' in status


class TestMCPColumnMapping:
    """Test MCP tool with custom column mapping."""
    
    def test_forecast_with_custom_columns(self, custom_column_data):
        """Test MCP tool accepts and uses custom column mapping."""
        import base64
        
        # Convert DataFrame to CSV bytes
        csv_buffer = io.StringIO()
        custom_column_data.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode()
        
        # Encode to Base64
        file_base64 = base64.b64encode(csv_bytes).decode()
        
        # Test the logic that the MCP tool uses
        from src.expo_smooth_mcp.main import MAX_BASE64_SIZE
        from src.expo_smooth_mcp import preprocessing, logic, column_analysis
        
        # Validate size
        assert len(file_base64) <= MAX_BASE64_SIZE
        
        # Decode
        file_bytes = base64.b64decode(file_base64)
        file_buffer = io.BytesIO(file_bytes)
        df = pd.read_csv(file_buffer)
        
        # Validate column mapping
        validation = column_analysis.validate_column_mapping(
            df, 'OrderDate', 'Units_Sold', 'Product_Code'
        )
        assert validation['valid']
        
        # Map columns
        df_mapped = df.rename(columns={
            'OrderDate': 'date',
            'Units_Sold': 'sales',
            'Product_Code': 'sku'
        })
        
        # Process
        processed_df = preprocessing.preprocess_data(df_mapped)
        assert processed_df is not None
        
        # Check SKU
        valid_skus = logic.get_available_skus(processed_df)
        assert 'PROD_001' in valid_skus
    
    def test_forecast_with_invalid_column_names(self, custom_column_data):
        """Test MCP tool rejects invalid column names."""
        validation = column_analysis.validate_column_mapping(
            custom_column_data,
            'InvalidDate',
            'Units_Sold'
        )
        
        assert not validation['valid']
        assert len(validation['errors']) > 0


# --- End-to-End Tests ---

class TestEndToEndColumnMapping:
    """Test complete workflows with column mapping."""
    
    def test_standard_to_custom_column_workflow(self, custom_column_data):
        """Test full workflow from upload to forecast with custom columns."""
        from src.expo_smooth_mcp import preprocessing, logic, column_analysis
        
        # Analyze
        analysis = column_analysis.analyze_columns(custom_column_data)
        assert analysis['suggested_date'] == 'OrderDate'
        assert analysis['suggested_metric'] == 'Units_Sold'
        
        # Validate
        validation = column_analysis.validate_column_mapping(
            custom_column_data,
            analysis['suggested_date'],
            analysis['suggested_metric'],
            analysis['suggested_product']
        )
        assert validation['valid']
        
        # Map
        df_mapped = custom_column_data.rename(columns={
            'OrderDate': 'date',
            'Units_Sold': 'sales',
            'Product_Code': 'sku'
        })
        
        # Process
        processed_df = preprocessing.preprocess_data(df_mapped)
        assert processed_df is not None
        
        # Forecast (may fail with small dataset, that's OK)
        try:
            forecast = logic.get_forecast_data(processed_df, 'PROD_001', 7)
            assert 'dates' in forecast
            assert 'forecast' in forecast
        except ValueError as e:
            # Expected for small test datasets
            assert 'seasonal' in str(e).lower() or 'cycle' in str(e).lower()
```

#### Acceptance Criteria

- [ ] All tests pass (15+ tests)
- [ ] Column analysis tests cover various naming conventions
- [ ] Validation tests cover error cases
- [ ] Integration tests verify Gradio and MCP workflows
- [ ] End-to-end tests verify complete process
- [ ] No regressions in existing tests (94 tests must pass)

---

### TASK-3B-06: Update Documentation

**Estimated Time:** 1 hour  
**Complexity:** Low  
**Dependencies:** TASK-3B-01, TASK-3B-02, TASK-3B-03  
**Files:** `README.md`, `docs/DATA_PREPROCESSING.md`

#### Description

Update project documentation to explain column mapping feature, provide examples with various column naming conventions, and guide users on how to use the feature.

#### Implementation Steps

1. **Update README.md** - Add section on column mapping:

```markdown
### Flexible Column Mapping

The application automatically detects column types in your data using intelligent heuristics. If your data uses non-standard column names, the system will suggest mappings that you can confirm or adjust.

#### Supported Column Types

**Date/Time Columns (for time series):**
- Common names: `date`, `timestamp`, `day`, `period`, `order_date`, `ds`
- Must contain parseable date values

**Metric Columns (values to forecast):**
- Common names: `sales`, `quantity`, `demand`, `revenue`, `units_sold`, `orders`
- Must be numeric

**Product ID Columns (for grouping):**
- Common names: `sku`, `product_id`, `item_id`, `product_code`
- Used to filter/group data by product

#### Example: Custom Column Names

If your data has columns like `OrderDate`, `Product_Code`, and `Units_Sold`:

**Via Gradio UI:**
1. Upload your file
2. System auto-detects: "OrderDate" → Date, "Units_Sold" → Metric
3. Confirm or adjust selections
4. Generate forecast

**Via MCP Tool:**
```python
result = await forecast_with_custom_data(
    file_data_base64=data,
    file_name="orders.csv",
    sku="PROD_123",
    date_column="OrderDate",
    metric_column="Units_Sold",
    product_column="Product_Code"
)
```
```

2. **Update DATA_PREPROCESSING.md** - Add column mapping guidance:

```markdown
## Column Mapping and Detection

### Automatic Column Detection

The system uses lightweight heuristics to automatically detect column types:

1. **Name Matching**: Checks if column names contain keywords like "date", "sales", "sku"
2. **Type Validation**: Verifies data types (numeric for metrics, parseable for dates)
3. **Scoring**: Assigns confidence scores to prioritize best matches

### Detection Accuracy

The heuristic system achieves >80% accuracy on standard SCM datasets with common naming conventions.

### Manual Override

If automatic detection is incorrect, users can manually select the correct columns via:
- Gradio UI: Dropdown selectors
- MCP Tool: Parameter specification

### Common Column Name Patterns

| Type | Common Names |
|------|--------------|
| Date | date, timestamp, day, order_date, period, ds |
| Metric | sales, quantity, demand, revenue, units_sold |
| Product | sku, product_id, item_id, product_code |
```

#### Acceptance Criteria

- [ ] README.md includes column mapping section
- [ ] Examples show various naming conventions
- [ ] MCP tool documentation updated
- [ ] DATA_PREPROCESSING.md explains detection logic
- [ ] Common column names listed

---

## Phase Completion Checklist

### Code Implementation
- [ ] TASK-3B-01: Column analysis module created
- [ ] TASK-3B-02: Gradio UI updated with mapping interface
- [ ] TASK-3B-03: MCP tool extended with mapping parameters
- [ ] TASK-3B-04: Backend refactored for column flexibility
- [ ] TASK-3B-05: Comprehensive test suite created
- [ ] TASK-3B-06: Documentation updated

### Quality Gates
- [ ] All new tests passing (15+ tests)
- [ ] No regressions (94 existing tests pass)
- [ ] Heuristic accuracy >80% on test datasets
- [ ] Backward compatibility maintained
- [ ] Code review completed
- [ ] Performance acceptable (<100ms for analysis)

### Documentation
- [ ] README.md updated
- [ ] DATA_PREPROCESSING.md updated
- [ ] ADR 005 extended (✅ Complete)
- [ ] Code comments comprehensive
- [ ] Examples provided

### User Experience
- [ ] Column mapping UI intuitive
- [ ] Smart suggestions work >80% of time
- [ ] Error messages clear and actionable
- [ ] Works with common SCM data formats

---

## Testing Strategy

### Unit Tests (8 tests)
- Column analysis with various naming conventions
- Scoring system accuracy
- Validation logic

### Integration Tests (4 tests)
- Gradio file processing with analysis
- MCP tool with custom columns
- Backend column renaming

### End-to-End Tests (3 tests)
- Complete Gradio workflow
- Complete MCP workflow
- Backward compatibility

**Total: 15 tests minimum**

---

## Troubleshooting

### Issue: Analysis doesn't detect columns

**Symptoms:**
- No suggestions shown
- All dropdowns empty

**Diagnosis:**
```python
from src.expo_smooth_mcp import column_analysis
analysis = column_analysis.analyze_columns(df)
print(analysis)
```

**Solutions:**
- Check if column names match any keywords
- Verify data types are correct
- Add custom keywords to detection lists

### Issue: Validation fails for valid data

**Symptoms:**
- "Invalid column mapping" errors
- Dates not parsing

**Diagnosis:**
```python
validation = column_analysis.validate_column_mapping(df, 'date_col', 'metric_col')
print(validation)
```

**Solutions:**
- Check date format compatibility
- Verify numeric columns are truly numeric
- Check for missing values

### Issue: Backward compatibility broken

**Symptoms:**
- Old code/tests failing
- Default dataset not working

**Solutions:**
- Verify default parameter values ('date', 'sales')
- Check column renaming logic
- Test with original FMCG dataset

---

## Time Tracking

| Task | Estimated | Actual | Notes |
|------|-----------|--------|-------|
| TASK-3B-01 | 2h | | |
| TASK-3B-02 | 2h | | |
| TASK-3B-03 | 1.5h | | |
| TASK-3B-04 | 1.5h | | |
| TASK-3B-05 | 1.5h | | |
| TASK-3B-06 | 1h | | |
| **TOTAL** | **9.5h** | | |

---

## Next Steps

After Phase 3B completion:

1. **Immediate:**
   - Run full test suite
   - Update PROJECT_ROADMAP.md
   - Create Phase 3B code review

2. **Phase 4:**
   - Docker MCP Toolkit deployment
   - Claude Desktop integration
   - Production optimization

3. **Future Enhancements:**
   - Pattern B (two-step upload) for large files
   - ML-based column detection
   - More sophisticated validation

---

**Phase Owner:** maksim-tsi  
**Reviewer:** GitHub Copilot  
**Status:** Ready for Implementation  
**Target Completion:** TBD
