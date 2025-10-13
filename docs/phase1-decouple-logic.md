# Phase 1 Implementation Guide: Decoupling Business Logic

**Objective:** Extract all forecasting logic into a framework-agnostic module to enable reuse across different interfaces (Gradio UI, FastAPI endpoints, FastMCP tools).

**Time Estimate:** 2-3 days  
**Prerequisites:** None  
**Next Phase:** [Phase 2 - Build FastMCP Backend](./phase2-build-fastmcp.md)

---

## Step 1: Create the Logic Module

Create a new file for pure business logic:

```bash
touch src/expo_smooth_mcp/logic.py
```

### Implementation

```python
# src/expo_smooth_mcp/logic.py
"""
Framework-agnostic business logic for exponential smoothing forecasting.

This module contains pure functions with no dependencies on UI frameworks
(Gradio, Streamlit) or web frameworks (FastAPI, Flask). It can be reused
across different interface layers.
"""

from typing import Dict, List, Optional
import pandas as pd
import plotly.graph_objects as go
from .forecasting import generate_forecast
from .preprocessing import load_and_preprocess_data


def get_forecast_data(
    df: pd.DataFrame,
    sku: str,
    forecast_horizon: int = 90
) -> Dict[str, List]:
    """
    Generate forecast data for a specific SKU.
    
    This is a pure function that transforms data without side effects.
    Returns a dictionary that can be serialized to JSON for APIs or
    converted to plots for UIs.
    
    Args:
        df: Preprocessed DataFrame with time series data
        sku: Product SKU code (e.g., "PRODUCT_123")
        forecast_horizon: Number of days to forecast
        
    Returns:
        Dictionary with keys:
        - 'dates': List of date strings in ISO format
        - 'actuals': List of actual values (null for future dates)
        - 'forecast': List of forecasted values
        - 'metadata': Dict with SKU info and forecast parameters
        
    Raises:
        ValueError: If SKU not found in DataFrame
    """
    # Validate SKU exists
    if sku not in df['SKU'].unique():
        available_skus = df['SKU'].unique().tolist()
        raise ValueError(
            f"SKU '{sku}' not found. Available SKUs: {available_skus[:5]}..."
        )
    
    # Generate forecast using existing forecasting module
    forecast_df = generate_forecast(df, sku, forecast_horizon)
    
    # Convert to JSON-serializable format
    return {
        'dates': forecast_df.index.strftime('%Y-%m-%d').tolist(),
        'actuals': forecast_df['actuals'].where(
            forecast_df['actuals'].notna(), None
        ).tolist(),
        'forecast': forecast_df['forecast'].tolist(),
        'metadata': {
            'sku': sku,
            'forecast_horizon': forecast_horizon,
            'historical_points': forecast_df['actuals'].notna().sum(),
            'forecast_points': len(forecast_df['forecast'])
        }
    }


def get_available_skus(df: pd.DataFrame) -> List[str]:
    """
    Get list of all product SKUs available for forecasting.
    
    Args:
        df: Preprocessed DataFrame
        
    Returns:
        Sorted list of unique SKU strings
    """
    return sorted(df['SKU'].unique().tolist())


def create_forecast_plot(forecast_data: Dict[str, List]) -> go.Figure:
    """
    Create a Plotly figure from forecast data.
    
    This function is UI-specific (Plotly) but still decoupled from Gradio.
    It can be reused in any context that supports Plotly figures.
    
    Args:
        forecast_data: Output from get_forecast_data()
        
    Returns:
        Plotly Figure object ready for display
    """
    dates = forecast_data['dates']
    actuals = forecast_data['actuals']
    forecast = forecast_data['forecast']
    metadata = forecast_data['metadata']
    
    fig = go.Figure()
    
    # Historical actuals trace
    fig.add_trace(go.Scatter(
        x=dates,
        y=actuals,
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))
    
    # Forecast trace
    fig.add_trace(go.Scatter(
        x=dates,
        y=forecast,
        mode='lines',
        name='Forecast',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Styling
    fig.update_layout(
        title=f"Sales Forecast for {metadata['sku']}",
        xaxis_title="Date",
        yaxis_title="Sales Volume",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig


def validate_forecast_request(
    sku: str,
    forecast_horizon: int,
    available_skus: List[str]
) -> Optional[str]:
    """
    Validate forecast request parameters.
    
    Args:
        sku: Requested SKU
        forecast_horizon: Requested horizon
        available_skus: List of valid SKUs
        
    Returns:
        Error message string if validation fails, None if valid
    """
    if not sku:
        return "SKU parameter is required"
    
    if sku not in available_skus:
        return f"Invalid SKU '{sku}'. Use list_available_skus() to see options."
    
    if forecast_horizon < 1:
        return "Forecast horizon must be at least 1 day"
    
    if forecast_horizon > 365:
        return "Forecast horizon cannot exceed 365 days"
    
    return None


# Module-level data loading (singleton pattern)
_PROCESSED_DF: Optional[pd.DataFrame] = None


def get_processed_data() -> pd.DataFrame:
    """
    Get preprocessed data, loading it once and caching.
    
    This implements a simple singleton pattern to avoid reloading
    data on every request.
    
    Returns:
        Preprocessed DataFrame
        
    Raises:
        RuntimeError: If data fails to load
    """
    global _PROCESSED_DF
    
    if _PROCESSED_DF is None:
        _PROCESSED_DF = load_and_preprocess_data()
        
        if _PROCESSED_DF.empty:
            raise RuntimeError("Failed to load and preprocess data")
    
    return _PROCESSED_DF
```

---

## Step 2: Refactor Gradio App

Update `app.py` to use the new logic module:

```python
# app.py (refactored)
import gradio as gr
from src.expo_smooth_mcp.logic import (
    get_processed_data,
    get_available_skus,
    get_forecast_data,
    create_forecast_plot,
    validate_forecast_request
)

# Load data once at module level
try:
    PROCESSED_DF = get_processed_data()
    AVAILABLE_SKUS = get_available_skus(PROCESSED_DF)
except RuntimeError as e:
    print(f"Error loading data: {e}")
    PROCESSED_DF = None
    AVAILABLE_SKUS = []


def create_forecast_plot_wrapper(sku: str, forecast_horizon: int):
    """
    Gradio event handler - thin wrapper around business logic.
    
    This function only handles Gradio-specific concerns:
    - Input extraction from UI components
    - Error message formatting for UI display
    - Return type conversion for Gradio components
    """
    # Validate inputs
    error = validate_forecast_request(sku, forecast_horizon, AVAILABLE_SKUS)
    if error:
        # Return error in a format Gradio can display
        return gr.Plot(), f"❌ Error: {error}"
    
    try:
        # Call business logic
        forecast_data = get_forecast_data(PROCESSED_DF, sku, forecast_horizon)
        plot = create_forecast_plot(forecast_data)
        
        # Format success message
        metadata = forecast_data['metadata']
        message = (
            f"✅ Forecast generated successfully\n"
            f"Historical points: {metadata['historical_points']}\n"
            f"Forecast points: {metadata['forecast_points']}"
        )
        
        return plot, message
        
    except Exception as e:
        return gr.Plot(), f"❌ Error generating forecast: {str(e)}"


# Gradio UI definition
with gr.Blocks(title="Exponential Smoothing Forecaster") as demo:
    gr.Markdown("# 📈 Supply Chain Forecasting with Exponential Smoothing")
    
    if not PROCESSED_DF.empty:
        with gr.Row():
            with gr.Column(scale=1):
                sku_dropdown = gr.Dropdown(
                    choices=AVAILABLE_SKUS,
                    label="Select Product SKU",
                    value=AVAILABLE_SKUS[0] if AVAILABLE_SKUS else None
                )
                
                horizon_slider = gr.Slider(
                    minimum=7,
                    maximum=365,
                    value=90,
                    step=1,
                    label="Forecast Horizon (days)"
                )
                
                forecast_btn = gr.Button("Generate Forecast", variant="primary")
            
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Forecast Visualization")
                status_output = gr.Textbox(label="Status", lines=3)
        
        # Event binding
        forecast_btn.click(
            fn=create_forecast_plot_wrapper,
            inputs=[sku_dropdown, horizon_slider],
            outputs=[plot_output, status_output]
        )
    else:
        gr.Markdown("⚠️ **Error:** Failed to load data. Please check data files.")


if __name__ == "__main__":
    if PROCESSED_DF is not None and not PROCESSED_DF.empty:
        demo.launch()
    else:
        print("Cannot start app: data failed to load.")
```

---

## Step 3: Update Unit Tests

Create tests for the new logic module:

```python
# tests/test_logic.py
import pytest
import pandas as pd
from src.expo_smooth_mcp.logic import (
    get_forecast_data,
    get_available_skus,
    validate_forecast_request,
    create_forecast_plot
)


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    dates = pd.date_range('2024-01-01', periods=100)
    return pd.DataFrame({
        'Date': dates,
        'SKU': ['PRODUCT_001'] * 50 + ['PRODUCT_002'] * 50,
        'Sales': range(100)
    })


def test_get_available_skus(sample_df):
    skus = get_available_skus(sample_df)
    assert len(skus) == 2
    assert 'PRODUCT_001' in skus
    assert 'PRODUCT_002' in skus


def test_get_forecast_data_returns_correct_structure(sample_df):
    result = get_forecast_data(sample_df, 'PRODUCT_001', forecast_horizon=30)
    
    assert 'dates' in result
    assert 'actuals' in result
    assert 'forecast' in result
    assert 'metadata' in result
    
    assert len(result['dates']) > 0
    assert result['metadata']['sku'] == 'PRODUCT_001'
    assert result['metadata']['forecast_horizon'] == 30


def test_get_forecast_data_raises_on_invalid_sku(sample_df):
    with pytest.raises(ValueError, match="SKU 'INVALID' not found"):
        get_forecast_data(sample_df, 'INVALID', forecast_horizon=30)


def test_validate_forecast_request():
    valid_skus = ['PRODUCT_001', 'PRODUCT_002']
    
    # Valid request
    assert validate_forecast_request('PRODUCT_001', 30, valid_skus) is None
    
    # Invalid SKU
    error = validate_forecast_request('INVALID', 30, valid_skus)
    assert error is not None
    assert 'Invalid SKU' in error
    
    # Invalid horizon
    error = validate_forecast_request('PRODUCT_001', 0, valid_skus)
    assert error is not None
    assert 'at least 1 day' in error


def test_create_forecast_plot():
    forecast_data = {
        'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'actuals': [10, 20, None],
        'forecast': [10, 20, 30],
        'metadata': {'sku': 'TEST_SKU', 'forecast_horizon': 1}
    }
    
    fig = create_forecast_plot(forecast_data)
    
    assert fig is not None
    assert len(fig.data) == 2  # Two traces: actuals and forecast
    assert 'TEST_SKU' in fig.layout.title.text
```

---

## Step 4: Validation Checklist

Before proceeding to Phase 2, verify:

### Functional Tests
- [ ] Run `python app.py` - Gradio app starts successfully
- [ ] Select an SKU and generate forecast - plot appears correctly
- [ ] Try invalid inputs (empty SKU, negative horizon) - errors display properly
- [ ] Change forecast horizon - plot updates correctly

### Code Quality
- [ ] Run `pytest tests/test_logic.py` - all tests pass
- [ ] Run `pytest tests/` - no existing tests broken
- [ ] Check `logic.py` has no imports of `gradio`, `fastapi`, or other UI/web frameworks
- [ ] Verify type hints on all public functions

### Architecture Verification
```bash
# Verify no circular dependencies
python -c "from src.expo_smooth_mcp.logic import get_forecast_data; print('✅ Import successful')"

# Verify module can be used without Gradio
python -c "
from src.expo_smooth_mcp.logic import get_processed_data, get_forecast_data
df = get_processed_data()
result = get_forecast_data(df, df['SKU'].iloc[0], 30)
print(f'✅ Generated forecast with {len(result[\"forecast\"])} points')
"
```

---

## Step 5: Commit Changes

```bash
git checkout -b phase1-decouple-logic
git add src/expo_smooth_mcp/logic.py
git add app.py
git add tests/test_logic.py
git commit -m "Phase 1: Decouple business logic from Gradio UI

- Created logic.py with framework-agnostic functions
- Refactored app.py to use logic module
- Added comprehensive unit tests for logic layer
- Verified backward compatibility with existing UI"

git push origin phase1-decouple-logic
```

---

## Common Issues & Solutions

### Issue 1: Import Errors
**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:** Ensure you're running from project root, or add to PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue 2: Data Loading Fails
**Error:** `RuntimeError: Failed to load and preprocess data`

**Solution:** Check that data files exist in expected location:
```bash
ls -la data/  # Verify CSV files present
```

### Issue 3: Tests Fail with Fixture Issues
**Error:** `pytest.fixture not found`

**Solution:** Install pytest and ensure test files start with `test_`:
```bash
uv add --dev pytest pytest-asyncio
```

---

## Next Steps

Once Phase 1 is complete and validated:

1. **Create Pull Request** for code review
2. **Proceed to Phase 2:** [Build FastMCP Backend](./phase2-build-fastmcp.md)
3. **Update Project Board** - Move Phase 1 tasks to "Done"

---

## Estimated Time Breakdown

| Task | Time | Notes |
|------|------|-------|
| Create logic.py | 2-3 hours | Extract and refactor existing code |
| Refactor app.py | 1-2 hours | Simplify to use logic functions |
| Write unit tests | 2-3 hours | Comprehensive test coverage |
| Manual testing | 1 hour | Verify UI still works |
| Code review & fixes | 1-2 hours | Address review comments |
| **Total** | **7-11 hours** | ~1-2 days with context switching |

---

## Success Criteria

✅ **Phase 1 Complete When:**
- All business logic extracted to `logic.py`
- `logic.py` has zero UI/web framework dependencies
- Gradio app functions identically to before refactoring
- All unit tests pass
- Code review approved
- Changes merged to main branch

🎯 **Ready for Phase 2 When:**
- Can import and use `logic.py` functions standalone
- Functions accept standard Python types (no Gradio components)
- Functions return JSON-serializable data structures

