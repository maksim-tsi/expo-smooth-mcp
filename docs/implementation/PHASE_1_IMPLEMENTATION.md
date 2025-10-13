# Phase 1: Decouple Business Logic - Implementation Guide

**Duration:** ~12 hours (8 tasks)  
**Status:** ✅ Completed  
**Complexity:** Medium

---

## Overview

This phase establishes the foundation for the FastMCP migration by separating business logic from UI code. We create a framework-agnostic `logic.py` module containing pure functions with no dependencies on Gradio, FastAPI, or other frameworks.

### Goals
- ✅ Extract all business logic from `app.py` into reusable functions
- ✅ Create framework-agnostic interfaces for forecasting operations
- ✅ Enable code reuse across Gradio UI, REST API, and MCP tools
- ✅ Maintain 100% backward compatibility with existing Gradio app
- ✅ Achieve >90% test coverage for business logic

### Prerequisites
- Existing Gradio app (`app.py`) functional
- Preprocessing and forecasting modules working
- Unit tests for preprocessing and forecasting passing

### Deliverables
1. `src/expo_smooth_mcp/logic.py` - Framework-agnostic business logic module
2. Refactored `app.py` - Thin UI layer delegating to logic module
3. `tests/test_logic.py` - Comprehensive test suite (>90% coverage)

---

## Tasks

### TASK-101: Create logic.py module structure
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:** 
Create `src/expo_smooth_mcp/logic.py` as a framework-agnostic business logic module. This module will contain pure functions with no dependencies on UI or web frameworks, enabling reuse across Gradio, FastAPI, and FastMCP interfaces.

**Implementation Steps:**
1. Create file: `src/expo_smooth_mcp/logic.py`
2. Add module-level docstring explaining purpose and design principles
3. Import required dependencies: `pandas`, `plotly.graph_objects`, `typing`
4. Import existing modules: `from .preprocessing import preprocess_data` and `from .forecasting import generate_forecast`
5. Define skeleton functions (implementation in subsequent tasks):
   - `get_forecast_data()` - Returns JSON-serializable forecast data
   - `get_available_skus()` - Returns list of available SKUs
   - `create_forecast_plot()` - Returns Plotly figure
   - `validate_forecast_request()` - Input validation
   - `get_processed_data()` - Singleton data loader

**File Structure:**
```python
"""
Framework-agnostic business logic for exponential smoothing forecasting.
Pure functions with no UI/web framework dependencies.
"""
from typing import Dict, List, Optional
import pandas as pd
import plotly.graph_objects as go
from .forecasting import generate_forecast
from .preprocessing import preprocess_data

# Module-level cache for preprocessed data
_cached_data: Optional[pd.DataFrame] = None

# Function skeletons (to be implemented)
def get_forecast_data(...) -> Dict[str, List]: pass
def get_available_skus(...) -> List[str]: pass
def create_forecast_plot(...) -> go.Figure: pass
def validate_forecast_request(...) -> None: pass
def get_processed_data(...) -> pd.DataFrame: pass
```

**Acceptance Criteria:**
- [ ] File `src/expo_smooth_mcp/logic.py` created
- [ ] Module docstring clearly explains framework-agnostic design
- [ ] All required imports present (pandas, plotly, typing, existing modules)
- [ ] Five skeleton functions defined with type hints
- [ ] Module-level cache variable declared
- [ ] File passes linting (no syntax errors)
- [ ] Can be imported: `from src.expo_smooth_mcp import logic`

---

### TASK-102: Extract forecast data generation function
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-101

**Description:** 
Implement `get_forecast_data()` function that transforms forecast output into a JSON-serializable format. This function bridges the existing `generate_forecast()` function and multiple consumer interfaces (REST API, MCP tools, Gradio UI).

**Implementation Steps:**
1. Analyze current `app.py` logic in `create_forecast_plot()` function (lines 19-81)
2. Extract data transformation logic (excluding Plotly visualization)
3. Implement function with comprehensive error handling
4. Add SKU validation against available data
5. Return structured dictionary suitable for JSON serialization
6. Add detailed docstring with type hints and examples

**Reference Current Code:**
```python
# From app.py lines 42-44 (to be extracted)
forecast_df = generate_forecast(PROCESSED_DF, sku, forecast_horizon=90)
# Result: DataFrame with index=dates, columns=['actuals', 'forecast']
```

**Function Signature:**
```python
def get_forecast_data(
    df: pd.DataFrame,
    sku: str,
    forecast_horizon: int = 90
) -> Dict[str, List]:
    """
    Generate forecast data for a specific SKU.
    
    Args:
        df: Preprocessed DataFrame with MultiIndex (date, sku)
        sku: Product SKU code (e.g., "PRODUCT_123")
        forecast_horizon: Number of days to forecast ahead
        
    Returns:
        {
            'dates': ['2025-01-01', '2025-01-02', ...],
            'actuals': [100.0, 105.0, None, None, ...],
            'forecast': [102.0, 107.0, 110.0, 115.0, ...],
            'metadata': {
                'sku': 'PRODUCT_123',
                'forecast_horizon': 90,
                'historical_points': 365,
                'forecast_points': 90
            }
        }
        
    Raises:
        ValueError: If SKU not found in DataFrame
    """
```

**Key Implementation Details:**
- Call existing `generate_forecast(df, sku, forecast_horizon)` from `forecasting.py`
- Convert DataFrame index (dates) to ISO format strings using `.strftime('%Y-%m-%d')`
- Handle NaN values in actuals column (convert to None for JSON compatibility)
- Include metadata dictionary for debugging and validation
- Raise descriptive ValueError if SKU doesn't exist

**Acceptance Criteria:**
- [ ] Function implemented in `logic.py` with complete docstring
- [ ] Handles valid SKU and returns correct data structure
- [ ] Raises ValueError with helpful message for invalid SKU
- [ ] Returns JSON-serializable dict (no NaN, only None for nulls)
- [ ] Metadata includes all four required fields
- [ ] Function is pure (no side effects, no global state modification)
- [ ] Can be tested independently without Gradio or FastAPI

---

### TASK-103: Extract SKU listing function
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-101

**Description:** 
Create `get_available_skus()` function to retrieve all unique product SKUs from the preprocessed dataset. This function will be used by Gradio dropdown, MCP `list_available_skus` tool, and API documentation.

**Implementation Steps:**
1. Extract unique SKUs from DataFrame MultiIndex
2. Sort alphabetically for consistent ordering
3. Return as Python list (JSON-serializable)
4. Add error handling for empty or malformed DataFrames

**Reference Current Code:**
```python
# From app.py line 8 (to be replaced)
SKU_LIST = PROCESSED_DF.index.get_level_values('sku').unique().tolist()
```

**Function Signature:**
```python
def get_available_skus(df: pd.DataFrame) -> List[str]:
    """
    Get list of all product SKUs available for forecasting.
    
    Args:
        df: Preprocessed DataFrame with MultiIndex (date, sku)
        
    Returns:
        Sorted list of unique SKU strings
        Example: ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_123', ...]
        
    Raises:
        ValueError: If DataFrame is empty or doesn't have 'sku' level in index
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if not isinstance(df.index, pd.MultiIndex) or 'sku' not in df.index.names:
        raise ValueError("DataFrame must have MultiIndex with 'sku' level")
    
    return sorted(df.index.get_level_values('sku').unique().tolist())
```

**Acceptance Criteria:**
- [ ] Function implemented in `logic.py`
- [ ] Returns sorted list of unique SKUs
- [ ] Handles empty DataFrame gracefully (raises ValueError)
- [ ] Validates MultiIndex structure
- [ ] Returns Python list (not pandas Index or array)
- [ ] Result matches current `SKU_LIST` from app.py
- [ ] Function is pure (no side effects)

---

### TASK-104: Extract Plotly visualization function
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-102

*[Full task content from SPECIFICATION.md - lines 307-432]*

---

### TASK-105: Extract validation function
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-102

*[Full task content from SPECIFICATION.md - lines 434-547]*

---

### TASK-106: Implement data loading singleton
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-101

*[Full task content from SPECIFICATION.md - lines 549-685]*

---

### TASK-107: Refactor app.py to use logic module
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-102, TASK-103, TASK-104, TASK-105, TASK-106

*[Full task content from SPECIFICATION.md - lines 687-823]*

---

### TASK-108: Create unit tests for logic module
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-107

*[Full task content from SPECIFICATION.md - lines 825-888]*

---

## Phase Completion Checklist

### Code Deliverables
- [ ] `src/expo_smooth_mcp/logic.py` created with all 5 functions
- [ ] `app.py` refactored to use logic module
- [ ] `tests/test_logic.py` created with comprehensive tests
- [ ] All existing unit tests still pass
- [ ] New tests achieve >90% coverage

### Functionality Verification
- [ ] Gradio app launches without errors
- [ ] All SKUs visible in dropdown
- [ ] Forecast visualization works for all SKUs
- [ ] Error handling works correctly
- [ ] No regression in app behavior

### Quality Gates
- [ ] All tests pass: `pytest tests/`
- [ ] Coverage >90%: `pytest --cov --cov-fail-under=90`
- [ ] No linting errors: `pylint src/`
- [ ] Type checking passes: `mypy src/`

### Documentation
- [ ] Module docstrings complete
- [ ] Function docstrings complete
- [ ] Code comments explain complex logic
- [ ] README updated if needed

---

## Troubleshooting This Phase

### Issue: Import errors for logic module
**Solution:**
```bash
# Ensure package structure is correct
cd /path/to/expo-smooth-mcp
python -c "from src.expo_smooth_mcp import logic; print('OK')"

# If fails, check __init__.py exists
touch src/expo_smooth_mcp/__init__.py
```

### Issue: Tests failing with import errors
**Solution:**
```bash
# Install package in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/expo-smooth-mcp"
```

### Issue: Coverage below 90%
**Solution:**
```bash
# Identify uncovered lines
pytest --cov=src.expo_smooth_mcp.logic --cov-report=term-missing

# Add tests for uncovered branches
# Focus on error handling and edge cases
```

### Issue: Gradio app behavior changed after refactor
**Solution:**
```bash
# Compare outputs before/after
# Use git to check what changed in app.py
git diff app.py

# Verify all logic functions return same types/formats
# Add integration tests comparing old vs new
```

---

## Next Steps

After completing Phase 1:
1. Verify all acceptance criteria met
2. Commit changes: `git commit -m "Phase 1: Decouple business logic"`
3. Run full test suite to ensure no regressions
4. Proceed to [Phase 2: FastMCP Backend](PHASE_2_IMPLEMENTATION.md)

---

## Time Tracking

| Task | Estimated | Actual | Notes |
|------|-----------|--------|-------|
| TASK-101 | 0.5h | ___h | _____ |
| TASK-102 | 1.5h | ___h | _____ |
| TASK-103 | 0.5h | ___h | _____ |
| TASK-104 | 1.0h | ___h | _____ |
| TASK-105 | 1.0h | ___h | _____ |
| TASK-106 | 1.0h | ___h | _____ |
| TASK-107 | 2.0h | ___h | _____ |
| TASK-108 | 2.0h | ___h | _____ |
| **Total** | **12h** | **___h** | **____** |

---

**Reference:** See [SPECIFICATION.md](../SPECIFICATION.md) for complete technical details.
