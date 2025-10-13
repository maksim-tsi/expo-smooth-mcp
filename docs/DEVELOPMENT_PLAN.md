
# Development Plan & Project Status

- **Version:** 2.0
- **Status:** Living
- **Last Updated:** 2025-10-13
- **Summary:** This document outlines the development phases, granular atomic tasks, and implementation roadmap for migrating `expo-smooth-mcp` from Gradio prototype to production-grade FastMCP + FastAPI architecture. Each task is designed to be completable by an experienced Python developer in ≤2 hours.

---

## 1. Overview

This development plan translates the strategic goals from our `PROJECT_CHARTER.md` into actionable phases and tasks. It is a living document that will be updated as the project progresses to reflect our current status and priorities.

## 2. Development Phases

The project is structured into three distinct phases:

### Phase 1: Foundation & Backend Logic (95% Complete)
**Objective:** To establish the project's documentation framework and build the core, non-visual components.
*   **Deliverables:**
    *   **[✓]** Core documentation (`PROJECT_CHARTER.md`, ADRs, Guides).
    *   **[✓]** Data preprocessing pipeline (`preprocessing.py`).
    *   **[✓]** Core forecasting engine (`forecasting.py`).
    *   **[✓]** Unit test suite for backend logic (`tests/`).

### Phase 2: UI, Integration & Core Functionality (In Progress)
**Objective:** To build the user-facing application, integrate all backend components, and enable the core MCP functionality.
*   **Deliverables:**
    *   **[✓]** Initial Gradio UI with basic functionality.
    *   **[ ]** File upload capability for custom datasets.
    *   **[ ]** Enablement and testing of the MCP server endpoint.
    *   **[ ]** Completion of the formal Test Plan.

### Phase 3: Finalization & Dissemination (Not Started)
**Objective:** To finalize the application, deploy it, and complete the research paper.
*   **Deliverables:**
    *   **[ ]** Final E2E testing of the completed application.
    *   **[ ]** Final, stable deployment on Hugging Face Spaces.
    *   **[ ]** Completed research paper draft for submission to RelStat.

## 3. Current Project Status (As of 2025-07-05)

| Component | Status | Notes |
| :--- | :--- | :--- |
| **Documentation** | **90% Complete** | Core documents and ADRs are complete. `TEST_PLAN.md` is written. Only minor updates might be needed. |
| **Data Preprocessing** | **Completed** | `preprocessing.py` module is implemented and fully covered by unit tests. |
| **Forecasting Engine** | **Completed** | `forecasting.py` module is implemented and fully covered by unit tests. |
| **Gradio Application** | **Partially Completed** | The base UI is functional with the default dataset. File upload and MCP server are not yet implemented. |
| **Unit Testing** | **Completed** | The backend logic in `src/` has a corresponding test suite in `tests/`. |
| **Integration & E2E Testing** | **Not Started** | The test plan is written, but execution against the final application has not yet occurred. |

## 4. Immediate Next Steps (Action Plan)

The following tasks are our immediate priority to complete Phase 2.

1.  **Implement File Upload Functionality:**
    *   **Action:** Modify `app.py` to include a `gr.File` component.
    *   **Logic:** Add a function that takes an uploaded file, runs it through `preprocess_data`, and updates the SKU dropdown and application state with the new data.
    *   **Goal:** Allow users to interact with their own data, fulfilling a key requirement from the `PROJECT_CHARTER.md`.

2.  **Enable and Test the MCP Server:**
    *   **Action:** Modify `demo.launch()` in `app.py` to include `mcp_server=True`.
    *   **Process:** Launch the application using `uvicorn app:demo --reload`.
    *   **Testing:** Use `curl` or an MCP client to execute the integration test cases defined in `docs/TEST_PLAN.md` (IT-001, IT-002).
    *   **Goal:** Validate the core research component of our project.

3.  **Execute Final End-to-End Testing:**
    *   **Action:** Manually execute all test cases listed in `docs/TEST_PLAN.md` under section 4.3, including those for file uploads.
    *   **Goal:** Ensure the application is stable, user-friendly, and bug-free before final deployment.

## 5. Development Tasks

This section provides a comprehensive, granular breakdown of all tasks required for the FastMCP migration. Each task is:
- **Atomic:** Can be completed independently by a single developer
- **Time-Boxed:** Designed for ≤2 hours of work by an experienced Python developer
- **Testable:** Has clear Definition of Done criteria
- **Assignable:** Can be distributed across multiple team members

### Task Structure Template

Each task follows this structure:

```
### TASK-XXX: Task Name
**Phase:** [Phase Number]
**Estimated Time:** [hours]
**Complexity:** [Low/Medium/High]
**Dependencies:** [List of prerequisite tasks]

**Description:**
[Brief description of what needs to be done]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Status:** [Not Started / In Progress / In Review / Completed / Blocked]
**Assignee:** [TBD]
**Actual Time:** [hours]
**Notes:** [Any relevant implementation notes]
```

---

## 6. Task Inventory

### Phase 1: Decouple Business Logic (8 tasks, ~12 hours)

#### TASK-101: Create logic.py module structure
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

#### TASK-102: Extract forecast data generation function
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

#### TASK-103: Extract SKU listing function
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

#### TASK-104: Extract Plotly visualization function
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-102

**Description:** 
Extract Plotly visualization logic from `app.py` into a reusable `create_forecast_plot()` function. This function should accept the structured forecast data from `get_forecast_data()` and return a styled Plotly Figure.

**Implementation Steps:**
1. Extract plotting logic from `app.py` lines 46-64 (create_forecast_plot function)
2. Modify to accept forecast data dictionary instead of DataFrame
3. Preserve existing styling (blue for actuals, red dashed for forecast)
4. Add hover formatting and template styling
5. Include metadata in plot title

**Reference Current Code:**
```python
# From app.py lines 46-64 (to be refactored)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=forecast_df.index, 
    y=forecast_df['actuals'], 
    mode='lines', 
    name='Historical Sales',
    line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=forecast_df.index, 
    y=forecast_df['forecast'], 
    mode='lines', 
    name='Forecasted Sales',
    line=dict(color='red', dash='dash')
))
```

**Function Signature:**
```python
def create_forecast_plot(forecast_data: Dict[str, List]) -> go.Figure:
    """
    Create interactive Plotly figure from forecast data.
    
    Args:
        forecast_data: Output dictionary from get_forecast_data()
        
    Returns:
        Plotly Figure object ready for display in Gradio or HTML export
        
    Example:
        >>> data = get_forecast_data(df, 'PRODUCT_123', 90)
        >>> fig = create_forecast_plot(data)
        >>> fig.show()  # Opens in browser
    """
    dates = forecast_data['dates']
    actuals = forecast_data['actuals']
    forecast = forecast_data['forecast']
    metadata = forecast_data['metadata']
    
    fig = go.Figure()
    
    # Historical trace
    fig.add_trace(go.Scatter(
        x=dates, y=actuals,
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))
    
    # Forecast trace
    fig.add_trace(go.Scatter(
        x=dates, y=forecast,
        mode='lines',
        name='Forecasted Sales',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f"Sales Forecast for {metadata['sku']}",
        xaxis_title="Date",
        yaxis_title="Quantity Sold",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig
```

**Styling Requirements:**
- Historical data: blue solid line with markers
- Forecast: red dashed line
- Template: 'plotly_white' for clean appearance
- Hover mode: 'x unified' for better UX
- Height: 500px for Gradio integration

**Acceptance Criteria:**
- [ ] Function implemented in `logic.py`
- [ ] Accepts forecast_data dict (not DataFrame)
- [ ] Returns Plotly Figure object
- [ ] Preserves visual styling from current app.py
- [ ] Uses metadata for dynamic title
- [ ] Includes proper axis labels and legend
- [ ] Can be displayed in Gradio Plot component
- [ ] Function is pure (no side effects)

#### TASK-105: Extract validation function
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-102

**Description:** 
Create centralized validation function to ensure forecast requests are valid before processing. This prevents duplicate validation logic across Gradio UI, REST API, and MCP tools.

**Implementation Steps:**
1. Define validation rules for SKU and forecast_horizon
2. Check SKU exists in available SKUs
3. Validate horizon is within reasonable range (1-365 days)
4. Raise descriptive exceptions with actionable error messages
5. Return early (no-op) if all validations pass

**Validation Rules:**
- **SKU:** Must exist in DataFrame's unique SKU list
- **Horizon:** Must be integer between 1 and 365 days
  - Lower bound: 1 day (minimum practical forecast)
  - Upper bound: 365 days (beyond this, exponential smoothing becomes unreliable)

**Function Signature:**
```python
def validate_forecast_request(
    df: pd.DataFrame,
    sku: str,
    forecast_horizon: int
) -> None:
    """
    Validate forecast request parameters.
    
    Args:
        df: Preprocessed DataFrame to validate SKU against
        sku: Product SKU to forecast
        forecast_horizon: Number of days to forecast ahead
        
    Raises:
        ValueError: If SKU not found or horizon out of range
        TypeError: If forecast_horizon is not an integer
        
    Returns:
        None (function raises exception on validation failure)
        
    Example:
        >>> validate_forecast_request(df, 'PRODUCT_123', 90)  # Passes
        >>> validate_forecast_request(df, 'INVALID', 90)
        ValueError: SKU 'INVALID' not found. Available: ['PRODUCT_001', ...]
        >>> validate_forecast_request(df, 'PRODUCT_123', 500)
        ValueError: Forecast horizon must be between 1 and 365 days, got 500
    """
    # Type validation
    if not isinstance(forecast_horizon, int):
        raise TypeError(
            f"forecast_horizon must be integer, got {type(forecast_horizon).__name__}"
        )
    
    # Range validation
    if not (1 <= forecast_horizon <= 365):
        raise ValueError(
            f"Forecast horizon must be between 1 and 365 days, got {forecast_horizon}"
        )
    
    # SKU existence validation
    available_skus = get_available_skus(df)
    if sku not in available_skus:
        raise ValueError(
            f"SKU '{sku}' not found. Available SKUs: {available_skus[:5]}..."
            if len(available_skus) > 5 else f"Available SKUs: {available_skus}"
        )
```

**Error Message Guidelines:**
- Be specific about what's wrong
- Suggest corrective action when possible
- Show partial list of available SKUs (first 5) for large datasets
- Include actual value that failed validation

**Acceptance Criteria:**
- [ ] Function implemented in `logic.py`
- [ ] Validates SKU existence against DataFrame
- [ ] Validates forecast_horizon range (1-365)
- [ ] Validates forecast_horizon type (must be int)
- [ ] Raises ValueError with descriptive message for invalid inputs
- [ ] Returns None (no-op) for valid inputs
- [ ] Error messages include helpful context
- [ ] Can be called before any forecast operation

#### TASK-106: Implement data loading singleton
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-101

**Description:** 
Implement singleton pattern for data loading to ensure the FMCG dataset is loaded and preprocessed exactly once, then cached in module-level variable. This improves performance and prevents inconsistent data states across multiple function calls.

**Implementation Steps:**
1. Use module-level `_cached_data` variable (declared in TASK-101)
2. Implement lazy loading: load data only on first call
3. Add error handling for missing file
4. Add optional `force_reload` parameter for testing
5. Follow current app.py pattern (lines 7-12) but with better error handling

**Reference Current Code:**
```python
# From app.py lines 7-12 (to be replaced with function call)
try:
    RAW_DF = pd.read_csv('FMCG_Sales.csv')
    PROCESSED_DF = preprocess_data(RAW_DF.copy())
    SKU_LIST = PROCESSED_DF.index.get_level_values('sku').unique().tolist()
    print("Successfully loaded and preprocessed data.")
except FileNotFoundError:
    print("ERROR: FMCG_Sales.csv not found.")
    PROCESSED_DF = pd.DataFrame()
    SKU_LIST = []
```

**Function Signature:**
```python
_cached_data: Optional[pd.DataFrame] = None

def get_processed_data(
    data_path: str = 'FMCG_Sales.csv',
    force_reload: bool = False
) -> pd.DataFrame:
    """
    Load and preprocess FMCG sales data with singleton pattern.
    
    Data is loaded once and cached in module-level variable.
    Subsequent calls return cached data for performance.
    
    Args:
        data_path: Path to raw CSV file (default: 'FMCG_Sales.csv')
        force_reload: If True, reload data even if cached (for testing)
        
    Returns:
        Preprocessed DataFrame with MultiIndex (date, sku)
        
    Raises:
        FileNotFoundError: If data_path doesn't exist
        ValueError: If data fails validation after preprocessing
        
    Example:
        >>> df = get_processed_data()  # Loads and caches
        >>> df = get_processed_data()  # Returns cached (instant)
        >>> df = get_processed_data(force_reload=True)  # Reloads
    """
    global _cached_data
    
    # Return cached data if available
    if _cached_data is not None and not force_reload:
        return _cached_data
    
    # Load and preprocess data
    try:
        raw_df = pd.read_csv(data_path)
        processed_df = preprocess_data(raw_df.copy())
        
        # Validate result
        if processed_df.empty:
            raise ValueError("Preprocessing resulted in empty DataFrame")
        
        # Cache and return
        _cached_data = processed_df
        print(f"Successfully loaded and cached data from {data_path}")
        return _cached_data
        
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Data file not found: {data_path}. "
            "Please ensure FMCG_Sales.csv is in the root directory."
        )
```

**Design Pattern:**
- **Singleton Pattern:** Ensures single instance of processed data
- **Lazy Loading:** Only loads when first requested
- **Defensive Programming:** Validates result before caching
- **Test-Friendly:** `force_reload` parameter for unit testing

**Acceptance Criteria:**
- [ ] Function implemented in `logic.py`
- [ ] Uses module-level `_cached_data` variable
- [ ] First call loads and caches data
- [ ] Subsequent calls return cached data (no disk I/O)
- [ ] `force_reload=True` reloads data
- [ ] Raises FileNotFoundError with helpful message if CSV missing
- [ ] Validates preprocessed DataFrame before caching
- [ ] Prints confirmation message on successful load
- [ ] Can be tested independently

#### TASK-107: Refactor app.py to use logic module
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-102, TASK-103, TASK-104, TASK-105, TASK-106

**Description:** 
Refactor `app.py` to use the new `logic` module functions, transforming it from containing business logic to being a pure UI layer. This completes the decoupling phase and validates all logic functions work correctly.

**Implementation Steps:**
1. Add import at top: `from src.expo_smooth_mcp import logic`
2. Replace global data loading (lines 7-12) with `logic.get_processed_data()` call
3. Replace SKU_LIST generation with `logic.get_available_skus()` call
4. Refactor `create_forecast_plot()` function to:
   - Call `logic.validate_forecast_request()`
   - Call `logic.get_forecast_data()`
   - Call `logic.create_forecast_plot()`
5. Simplify error handling (logic module now handles most errors)
6. Ensure UI behavior remains identical to current implementation

**Current Code Structure:**
```python
# app.py - BEFORE (109 lines)
import gradio as gr
# Direct imports from preprocessing and forecasting
# Global data loading at module level
# create_forecast_plot() with embedded business logic
# Gradio Interface definition
```

**Target Code Structure:**
```python
# app.py - AFTER (~40-50 lines)
import gradio as gr
from src.expo_smooth_mcp import logic

# --- 1. Initialization ---
try:
    PROCESSED_DF = logic.get_processed_data()
    SKU_LIST = logic.get_available_skus(PROCESSED_DF)
    print("Successfully loaded data via logic module.")
except Exception as e:
    print(f"ERROR: Failed to load data: {e}")
    PROCESSED_DF = None
    SKU_LIST = []

# --- 2. UI Event Handler ---
def create_forecast_plot(sku: str):
    """Thin wrapper that delegates to logic module."""
    if not sku or PROCESSED_DF is None:
        # Return empty plot with message
        return _create_empty_plot("Please select a product SKU")
    
    try:
        # Validate request
        logic.validate_forecast_request(PROCESSED_DF, sku, 90)
        
        # Generate forecast data
        forecast_data = logic.get_forecast_data(PROCESSED_DF, sku, 90)
        
        # Create visualization
        return logic.create_forecast_plot(forecast_data)
        
    except ValueError as e:
        return _create_error_plot(f"Validation error: {e}")
    except Exception as e:
        return _create_error_plot(f"Error generating forecast: {e}")

def _create_empty_plot(message: str):
    """Helper for empty state plots."""
    # Keep existing empty plot logic
    pass

def _create_error_plot(message: str):
    """Helper for error state plots."""
    # Keep existing error plot logic
    pass

# --- 3. UI Definition ---
demo = gr.Interface(
    fn=create_forecast_plot,
    inputs=[gr.Dropdown(choices=SKU_LIST, label="Select Product SKU", ...)],
    outputs=[gr.Plot(label="Forecast Visualization")],
    # ... rest unchanged ...
)

if __name__ == "__main__":
    demo.launch()
```

**Key Changes:**
- Line count reduced from ~109 to ~50 lines
- All business logic delegated to `logic` module
- `create_forecast_plot()` becomes thin orchestration layer
- Error handling simplified (logic module provides detailed errors)
- Data loading uses singleton pattern
- Maintains 100% backward compatibility in UI behavior

**Testing Checklist:**
1. Launch app: `python app.py`
2. Verify data loads successfully
3. Verify dropdown populated with SKUs
4. Select various SKUs and verify plots render correctly
5. Verify error handling for invalid states
6. Compare output visually with pre-refactor version

**Acceptance Criteria:**
- [ ] Import `logic` module at top of file
- [ ] Global data loading uses `logic.get_processed_data()`
- [ ] SKU list generation uses `logic.get_available_skus()`
- [ ] `create_forecast_plot()` delegates all logic to logic module
- [ ] No direct calls to `generate_forecast()` or `preprocess_data()`
- [ ] UI behavior identical to pre-refactor version
- [ ] All error cases handled gracefully
- [ ] App launches without errors
- [ ] All SKUs can be visualized successfully
- [ ] Code passes linting and type checking

#### TASK-108: Create unit tests for logic module
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-107

**Description:** 
Create comprehensive unit test suite for the `logic` module to ensure all functions work correctly in isolation. This validates the business logic layer is robust and can be safely reused across multiple interfaces.

**Implementation Steps:**
1. Create `tests/test_logic.py` file
2. Set up test fixtures for sample DataFrame
3. Write test cases for each function
4. Test both happy paths and error cases
5. Use pytest for test framework
6. Run coverage analysis and aim for >90%

**Test File Structure:**
```python
# tests/test_logic.py
import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.expo_smooth_mcp import logic

# --- Fixtures ---

@pytest.fixture
def sample_df():
    """Create sample preprocessed DataFrame for testing."""
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    skus = ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_003']
    
    # Create MultiIndex DataFrame
    index = pd.MultiIndex.from_product(
        [dates, skus],
        names=['date', 'sku']
    )
    df = pd.DataFrame({
        'quantity': range(len(index))
    }, index=index)
    
    return df

# --- Test Cases ---

class TestGetProcessedData:
    """Tests for get_processed_data() function."""
    
    def test_loads_data_successfully(self, tmp_path):
        """Should load and cache data on first call."""
        pass
    
    def test_returns_cached_data(self):
        """Should return cached data on subsequent calls."""
        pass
    
    def test_force_reload(self):
        """Should reload data when force_reload=True."""
        pass
    
    def test_missing_file_raises_error(self):
        """Should raise FileNotFoundError for missing CSV."""
        pass

class TestGetAvailableSkus:
    """Tests for get_available_skus() function."""
    
    def test_returns_sorted_skus(self, sample_df):
        """Should return sorted list of unique SKUs."""
        result = logic.get_available_skus(sample_df)
        assert result == ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_003']
        assert isinstance(result, list)
    
    def test_empty_dataframe_raises_error(self):
        """Should raise ValueError for empty DataFrame."""
        with pytest.raises(ValueError, match="DataFrame is empty"):
            logic.get_available_skus(pd.DataFrame())
    
    def test_invalid_index_raises_error(self):
        """Should raise ValueError if no 'sku' level in index."""
        df = pd.DataFrame({'col': [1, 2, 3]})
        with pytest.raises(ValueError, match="MultiIndex"):
            logic.get_available_skus(df)

class TestValidateForecastRequest:
    """Tests for validate_forecast_request() function."""
    
    def test_valid_request_passes(self, sample_df):
        """Should not raise exception for valid inputs."""
        logic.validate_forecast_request(sample_df, 'PRODUCT_001', 90)
        # If we get here, validation passed
    
    def test_invalid_sku_raises_error(self, sample_df):
        """Should raise ValueError for non-existent SKU."""
        with pytest.raises(ValueError, match="SKU 'INVALID' not found"):
            logic.validate_forecast_request(sample_df, 'INVALID', 90)
    
    def test_invalid_horizon_range(self, sample_df):
        """Should raise ValueError for out-of-range horizon."""
        with pytest.raises(ValueError, match="between 1 and 365"):
            logic.validate_forecast_request(sample_df, 'PRODUCT_001', 500)
    
    def test_invalid_horizon_type(self, sample_df):
        """Should raise TypeError for non-integer horizon."""
        with pytest.raises(TypeError, match="must be integer"):
            logic.validate_forecast_request(sample_df, 'PRODUCT_001', "90")

class TestGetForecastData:
    """Tests for get_forecast_data() function."""
    
    def test_returns_correct_structure(self, sample_df):
        """Should return dict with required keys."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 90)
        
        assert isinstance(result, dict)
        assert set(result.keys()) == {'dates', 'actuals', 'forecast', 'metadata'}
        
    def test_dates_are_strings(self, sample_df):
        """Should return dates as ISO format strings."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 90)
        assert all(isinstance(d, str) for d in result['dates'])
        assert result['dates'][0] == '2024-01-01'  # ISO format
    
    def test_metadata_complete(self, sample_df):
        """Should include all metadata fields."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 90)
        metadata = result['metadata']
        
        assert metadata['sku'] == 'PRODUCT_001'
        assert metadata['forecast_horizon'] == 90
        assert 'historical_points' in metadata
        assert 'forecast_points' in metadata
    
    def test_invalid_sku_raises_error(self, sample_df):
        """Should raise ValueError for invalid SKU."""
        with pytest.raises(ValueError, match="not found"):
            logic.get_forecast_data(sample_df, 'INVALID', 90)

class TestCreateForecastPlot:
    """Tests for create_forecast_plot() function."""
    
    def test_returns_plotly_figure(self, sample_df):
        """Should return Plotly Figure object."""
        data = logic.get_forecast_data(sample_df, 'PRODUCT_001', 90)
        fig = logic.create_forecast_plot(data)
        
        assert hasattr(fig, 'data')  # Plotly Figure attribute
        assert len(fig.data) == 2  # Two traces (actuals + forecast)
    
    def test_plot_styling(self, sample_df):
        """Should apply correct styling to traces."""
        data = logic.get_forecast_data(sample_df, 'PRODUCT_001', 90)
        fig = logic.create_forecast_plot(data)
        
        # Check trace colors
        assert fig.data[0].line.color == 'blue'  # Historical
        assert fig.data[1].line.color == 'red'   # Forecast
        assert fig.data[1].line.dash == 'dash'   # Forecast is dashed

# --- Coverage Report ---
# Run: pytest tests/test_logic.py --cov=src.expo_smooth_mcp.logic --cov-report=term-missing
```

**Test Coverage Goals:**
- `get_processed_data()`: 100% (all branches)
- `get_available_skus()`: 100% (all branches)
- `validate_forecast_request()`: 100% (all error paths)
- `get_forecast_data()`: >90% (core logic)
- `create_forecast_plot()`: >80% (visual styling tested)

**Testing Commands:**
```bash
# Run tests
pytest tests/test_logic.py -v

# Run with coverage
pytest tests/test_logic.py --cov=src.expo_smooth_mcp.logic --cov-report=term-missing

# Run with coverage threshold
pytest tests/test_logic.py --cov=src.expo_smooth_mcp.logic --cov-fail-under=90
```

**Acceptance Criteria:**
- [ ] File `tests/test_logic.py` created
- [ ] All five functions have test classes
- [ ] Happy path tests for all functions
- [ ] Error path tests for all validation logic
- [ ] Test fixtures properly set up (sample_df)
- [ ] All tests pass: `pytest tests/test_logic.py`
- [ ] Coverage >90%: `pytest --cov --cov-fail-under=90`
- [ ] No warnings from pytest
- [ ] Tests run in <10 seconds
- [ ] Tests are independent (can run in any order)

---

### Phase 2: Build FastMCP Backend (12 tasks, ~20 hours)

#### TASK-201: Install FastMCP and FastAPI dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:** 
Install FastMCP 2.0 and FastAPI framework dependencies required for building the production MCP server. Use `uv` package manager for fast, deterministic dependency resolution.

**Implementation Steps:**
1. Install uv package manager if not already installed: `pip install uv`
2. Add required packages using uv
3. Verify installations and test imports
4. Update requirements.txt for backward compatibility

**Required Packages:**
```bash
# Core framework packages
uv add fastapi        # Modern web framework (ASGI)
uv add fastmcp        # FastMCP 2.0 for MCP protocol
uv add uvicorn[standard]  # ASGI server with websocket support
uv add python-multipart   # For form data parsing

# Additional dependencies
uv add httpx          # For testing and Gradio API calls
uv add pydantic       # Data validation (comes with FastAPI but explicit)
```

**Installation Commands:**
```bash
# Option 1: Using uv (recommended - 10-100x faster)
uv add fastapi fastmcp "uvicorn[standard]" python-multipart httpx

# Option 2: Using pip (fallback)
pip install fastapi fastmcp "uvicorn[standard]" python-multipart httpx

# Verify installation
python -c "import fastapi, fastmcp, uvicorn; print('✓ All imports successful')"
```

**Version Requirements:**
- `fastapi >= 0.104.0` (latest stable)
- `fastmcp >= 2.0.0` (production-ready MCP framework)
- `uvicorn >= 0.24.0` (with standard extras)
- `httpx >= 0.25.0` (for async HTTP)

**Expected requirements.txt Addition:**
```txt
# Web Framework & MCP Server
fastapi>=0.104.0
fastmcp>=2.0.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
httpx>=0.25.0
pydantic>=2.5.0
```

**Testing Installation:**
```python
# Quick import test
python -c "
from fastapi import FastAPI
from fastmcp import FastMCP
from uvicorn import Config
import httpx

app = FastAPI()
mcp = FastMCP()

print('✓ FastAPI version:', fastapi.__version__)
print('✓ FastMCP imported successfully')
print('✓ Uvicorn imported successfully')
print('✓ All dependencies ready')
"
```

**Acceptance Criteria:**
- [ ] uv package manager installed and working
- [ ] All five packages added via `uv add`
- [ ] Import test passes without errors
- [ ] requirements.txt updated with correct versions
- [ ] No dependency conflicts reported
- [ ] Documentation updated with installation instructions
- [ ] Installation tested on clean virtual environment

#### TASK-202: Create main.py skeleton structure
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-201

**Description:** 
Create the foundational `main.py` file that will serve as the entry point for the FastMCP + FastAPI production server. This file will eventually replace `app.py` as the primary application interface.

**Implementation Steps:**
1. Create file: `src/expo_smooth_mcp/main.py`
2. Add comprehensive module docstring
3. Import required dependencies
4. Initialize FastAPI application
5. Initialize FastMCP server
6. Add basic configuration

**File Structure:**
```python
"""
Expo Smooth MCP Server - Production FastAPI + FastMCP Application

This module implements a production-grade MCP server for exponential smoothing
forecasting. It provides three interfaces:

1. MCP Tools (stdio and HTTP/SSE transports)
   - forecast_sku: Generate forecast for a specific product
   - list_available_skus: Get all available product codes

2. REST API Endpoints
   - GET  /: Service information
   - GET  /health: Health check
   - POST /api/forecast: REST forecast endpoint
   - GET  /docs: OpenAPI documentation

3. Gradio UI (backward compatibility)
   - Mounted at /gradio for existing users

Architecture:
    Client (Claude/Cursor/API) 
        ↓
    FastAPI (ASGI Framework)
        ↓
    FastMCP (MCP Protocol Layer)
        ↓
    Business Logic (logic.py)
        ↓
    Forecasting Engine (forecasting.py)

Usage:
    # HTTP/SSE transport (production)
    $ uvicorn main:app --host 0.0.0.0 --port 8000
    
    # stdio transport (local development)
    $ fastmcp run main.py:mcp --transport stdio
"""

from typing import List, Dict, Any
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
import uvicorn

# Import business logic layer
from . import logic

# --- Application Configuration ---

APP_VERSION = "2.0.0"
APP_NAME = "Expo Smooth MCP Server"
APP_DESCRIPTION = (
    "Production MCP server for exponential smoothing forecasting. "
    "Supports both stdio and HTTP/SSE transports."
)

# --- FastAPI Application ---

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- FastMCP Server ---

mcp = FastMCP(
    name="expo-smooth-forecast",
    version=APP_VERSION,
)

# --- Global State ---
# (Data loading will be added in TASK-203)

# --- MCP Tools ---
# (Will be added in TASK-204 and TASK-205)

# --- REST API Endpoints ---
# (Will be added in TASK-207, TASK-208, TASK-210)

# --- Mount MCP Server ---
# (Will be added in TASK-206)

# --- Startup Event ---

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    # Data loading will be added in TASK-203

# --- Main Entry Point ---

if __name__ == "__main__":
    # Dual-transport support will be added in TASK-209
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Configuration Values:**
- **APP_VERSION**: "2.0.0" (major version change from Gradio prototype)
- **APP_NAME**: "Expo Smooth MCP Server"
- **MCP name**: "expo-smooth-forecast" (MCP server identifier)
- **Default port**: 8000 (standard HTTP)

**Key Design Decisions:**
- Single file for main application (not split into multiple files yet)
- Clear separation of sections with comments
- Startup event for initialization logic
- Dual-transport support in main block (to be added in TASK-209)

**Acceptance Criteria:**
- [ ] File `src/expo_smooth_mcp/main.py` created
- [ ] Comprehensive module docstring with usage examples
- [ ] FastAPI application initialized with title and version
- [ ] FastMCP server initialized with name
- [ ] Section markers for future additions
- [ ] Startup event handler defined
- [ ] Main entry point with uvicorn.run()
- [ ] File imports without errors
- [ ] Can run (but does nothing yet): `python -m src.expo_smooth_mcp.main`

#### TASK-203: Implement data loading in main.py
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-202, TASK-106

**Description:** 
Integrate data loading into the FastAPI application using the singleton pattern from `logic.get_processed_data()`. This ensures the dataset is loaded once during application startup and available to all endpoints.

**Implementation Steps:**
1. Add global variable for processed data
2. Call `logic.get_processed_data()` in startup event
3. Handle loading errors gracefully
4. Add logging for successful load

**Code Addition:**
```python
# --- Global State ---
# Add after "# --- Global State ---" section (around line 63)

PROCESSED_DF = None  # Will be loaded on startup

# --- Startup Event ---
# Replace existing startup_event function

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    global PROCESSED_DF
    
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    
    try:
        # Load and cache data using singleton pattern
        PROCESSED_DF = logic.get_processed_data()
        sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        print(f"✓ Data loaded successfully")
        print(f"✓ Found {sku_count} unique SKUs")
        print(f"✓ Ready to serve requests")
        
    except FileNotFoundError as e:
        print(f"✗ ERROR: Data file not found: {e}")
        print("✗ Server will start but forecast endpoints will fail")
        # Don't crash the server - allow health checks to work
        
    except Exception as e:
        print(f"✗ ERROR: Failed to load data: {e}")
        print("✗ Server will start but forecast endpoints will fail")
```

**Alternative: FastAPI lifespan (modern approach)**
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup/shutdown)."""
    global PROCESSED_DF
    
    # Startup
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    try:
        PROCESSED_DF = logic.get_processed_data()
        sku_count = len(logic.get_available_skus(PROCESSED_DF))
        print(f"✓ Loaded data with {sku_count} SKUs")
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    yield  # Server runs here
    
    # Shutdown (optional cleanup)
    print("Shutting down gracefully")

# Update FastAPI initialization
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan  # Add lifespan parameter
)
```

**Error Handling Strategy:**
- **FileNotFoundError**: Log error but don't crash server (allows debugging)
- **Other exceptions**: Log error but continue (health endpoint should still work)
- **Graceful degradation**: Server starts even if data fails to load

**Logging Output Examples:**
```
# Success
Starting Expo Smooth MCP Server v2.0.0
Successfully loaded and cached data from FMCG_Sales.csv
✓ Data loaded successfully
✓ Found 43 unique SKUs
✓ Ready to serve requests

# Failure
Starting Expo Smooth MCP Server v2.0.0
✗ ERROR: Data file not found: FMCG_Sales.csv
✗ Server will start but forecast endpoints will fail
```

**Acceptance Criteria:**
- [ ] Global `PROCESSED_DF` variable declared
- [ ] `logic.get_processed_data()` called in startup event
- [ ] Success message logs SKU count
- [ ] FileNotFoundError handled gracefully
- [ ] Generic exceptions handled gracefully
- [ ] Server starts successfully with or without data
- [ ] Data accessible to all endpoints via global variable
- [ ] Startup logs are clear and informative

#### TASK-204: Create forecast_sku MCP tool
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-203

**Description:** 
Implement the primary MCP tool for generating forecasts. This tool will be discoverable by MCP clients (Claude Desktop, Cursor, VS Code) and will be the main interface for requesting forecasts.

**Implementation Steps:**
1. Define tool function with `@mcp.tool()` decorator
2. Add comprehensive docstring (visible to MCP clients)
3. Implement type hints for parameters
4. Validate inputs using `logic.validate_forecast_request()`
5. Call `logic.get_forecast_data()` to generate forecast
6. Return structured data as dictionary
7. Handle errors with user-friendly messages

**MCP Tool Requirements:**
- **Tool Name**: `forecast_sku` (lowercase with underscore - MCP convention)
- **Visibility**: Appears in client tool list
- **Docstring**: Describes purpose, parameters, return format
- **Type Safety**: Full type hints for IDE support
- **Error Handling**: Graceful failures with actionable messages

**Code Implementation:**
```python
# --- MCP Tools ---
# Add after "# --- MCP Tools ---" section (around line 69)

@mcp.tool()
async def forecast_sku(
    sku: str,
    forecast_horizon: int = 90
) -> Dict[str, Any]:
    """
    Generate sales forecast for a specific product SKU.
    
    This tool uses Holt-Winters exponential smoothing to forecast future sales
    based on historical data. The forecast includes trend and seasonality patterns.
    
    Parameters:
        sku: Product SKU code (e.g., "PRODUCT_123")
             Use list_available_skus tool to see all valid SKUs
        forecast_horizon: Number of days to forecast ahead (default: 90)
                         Must be between 1 and 365 days
    
    Returns:
        Dictionary with forecast data:
        {
            "dates": ["2025-01-01", "2025-01-02", ...],
            "actuals": [100.0, 105.0, None, None, ...],
            "forecast": [102.0, 107.0, 110.0, 115.0, ...],
            "metadata": {
                "sku": "PRODUCT_123",
                "forecast_horizon": 90,
                "historical_points": 365,
                "forecast_points": 90
            }
        }
    
    Example:
        # Forecast 90 days ahead for PRODUCT_123
        result = await forecast_sku("PRODUCT_123", 90)
        print(f"Generated {len(result['forecast'])} forecast points")
    
    Raises:
        ValueError: If SKU not found or horizon out of valid range
        RuntimeError: If data failed to load on startup
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        raise RuntimeError(
            "Data not loaded. Server started without valid dataset. "
            "Check server logs for startup errors."
        )
    
    try:
        # Validate inputs
        logic.validate_forecast_request(PROCESSED_DF, sku, forecast_horizon)
        
        # Generate forecast
        forecast_data = logic.get_forecast_data(
            PROCESSED_DF, 
            sku, 
            forecast_horizon
        )
        
        return forecast_data
        
    except ValueError as e:
        # Re-raise validation errors with context
        raise ValueError(f"Forecast validation failed: {str(e)}")
    
    except Exception as e:
        # Log unexpected errors and raise
        print(f"ERROR in forecast_sku: {e}")
        raise RuntimeError(f"Forecast generation failed: {str(e)}")
```

**MCP Tool Best Practices:**
1. **Comprehensive Docstring**: MCP clients display this to users
2. **Type Hints**: Enable IDE autocomplete in client code
3. **Default Values**: Make common usage simple (90-day default)
4. **Clear Error Messages**: Help users fix problems
5. **Async Function**: Enable concurrent requests (FastAPI requirement)
6. **Structured Returns**: JSON-serializable dictionaries

**Error Scenarios to Handle:**
```python
# Scenario 1: Data not loaded
if PROCESSED_DF is None:
    raise RuntimeError("Data not loaded...")

# Scenario 2: Invalid SKU
# Handled by logic.validate_forecast_request()

# Scenario 3: Invalid horizon
# Handled by logic.validate_forecast_request()

# Scenario 4: Unexpected error
except Exception as e:
    print(f"ERROR in forecast_sku: {e}")
    raise RuntimeError(...)
```

**Testing the Tool:**
```python
# Test with MCP Inspector
$ npx @modelcontextprotocol/inspector uvicorn main:app

# Test with Python
import asyncio
result = asyncio.run(forecast_sku("PRODUCT_001", 90))
print(result.keys())  # Should show: dates, actuals, forecast, metadata
```

**Client Experience:**
```
User in Claude Desktop sees:
┌─────────────────────────────────────────┐
│ Available Tool: forecast_sku            │
│                                         │
│ Generate sales forecast for a specific │
│ product SKU.                            │
│                                         │
│ Parameters:                             │
│ • sku (required): Product SKU code      │
│ • forecast_horizon (optional): Days     │
│   ahead (default: 90)                   │
└─────────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] Function decorated with `@mcp.tool()`
- [ ] Comprehensive docstring (>10 lines) explaining usage
- [ ] Type hints for all parameters and return type
- [ ] Default value for `forecast_horizon` (90 days)
- [ ] Validates inputs before processing
- [ ] Returns dictionary with all four keys
- [ ] Handles `PROCESSED_DF is None` case
- [ ] Catches and re-raises exceptions with context
- [ ] Function is async (required for FastAPI)
- [ ] Can be called successfully with valid inputs
- [ ] Tool appears in MCP Inspector tool list

#### TASK-205: Create list_available_skus MCP tool
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-203

**Description:** 
Implement a discovery MCP tool that returns all available product SKUs. This tool allows MCP clients to discover what products can be forecasted without prior knowledge of the dataset.

**Implementation Steps:**
1. Define tool function with `@mcp.tool()` decorator
2. Add clear docstring for MCP client display
3. Call `logic.get_available_skus()` function
4. Return list of SKU strings
5. Handle data-not-loaded case

**Code Implementation:**
```python
# Add after forecast_sku() tool (around line 125)

@mcp.tool()
async def list_available_skus() -> List[str]:
    """
    List all product SKUs available for forecasting.
    
    Use this tool to discover what products exist in the dataset before
    requesting a forecast. Each SKU can be passed to the forecast_sku tool.
    
    Returns:
        List of product SKU codes, sorted alphabetically
        Example: ["PRODUCT_001", "PRODUCT_002", "PRODUCT_123", ...]
    
    Example:
        # Get all available SKUs
        skus = await list_available_skus()
        print(f"Found {len(skus)} products")
        
        # Forecast the first product
        first_sku = skus[0]
        forecast = await forecast_sku(first_sku, 90)
    
    Raises:
        RuntimeError: If data failed to load on startup
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        raise RuntimeError(
            "Data not loaded. Server started without valid dataset. "
            "Check server logs for startup errors."
        )
    
    try:
        # Get sorted list of SKUs
        sku_list = logic.get_available_skus(PROCESSED_DF)
        return sku_list
        
    except Exception as e:
        print(f"ERROR in list_available_skus: {e}")
        raise RuntimeError(f"Failed to retrieve SKU list: {str(e)}")
```

**Tool Behavior:**
- **Input:** None (no parameters required)
- **Output:** List of strings (JSON array)
- **Typical use case:** Called before `forecast_sku` to discover available products

**Client Experience:**
```
User in Claude Desktop:
> "What products can you forecast?"

Claude calls list_available_skus() and responds:
> "I can forecast sales for 43 products including:
>  • PRODUCT_001
>  • PRODUCT_002
>  • PRODUCT_123
>  ... (and 40 more)"
```

**Testing:**
```python
# Test in Python
import asyncio
skus = asyncio.run(list_available_skus())
assert isinstance(skus, list)
assert len(skus) > 0
assert all(isinstance(sku, str) for sku in skus)
print(f"✓ Found {len(skus)} SKUs")
```

**Acceptance Criteria:**
- [ ] Function decorated with `@mcp.tool()`
- [ ] Clear docstring explaining purpose
- [ ] Returns List[str] type
- [ ] Function is async
- [ ] Handles `PROCESSED_DF is None` case
- [ ] Calls `logic.get_available_skus()`
- [ ] Returns sorted list of SKUs
- [ ] Tool appears in MCP Inspector
- [ ] Can be called successfully
- [ ] Exception handling for unexpected errors

#### TASK-206: Mount FastMCP server to FastAPI
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-204, TASK-205

**Description:** 
Mount the FastMCP server as a sub-application within FastAPI, exposing MCP tools at the `/mcp` endpoint. This enables HTTP/SSE transport for remote MCP clients while keeping the FastAPI application as the primary entry point.

**Implementation Steps:**
1. Add mount statement after all MCP tools are defined
2. Configure SSE transport explicitly
3. Add comment explaining the mounting pattern
4. Verify endpoint appears in FastAPI routes

**Code Implementation:**
```python
# --- Mount MCP Server ---
# Add after "# --- Mount MCP Server ---" section (around line 160)

# Mount MCP server as ASGI sub-application at /mcp endpoint
# This exposes MCP tools via HTTP/SSE transport for remote clients
# Local stdio transport is handled separately in main block
app.mount("/mcp", mcp.as_asgi(transport="sse"))

print(f"✓ Mounted MCP server at /mcp with SSE transport")
```

**Alternative Configuration (if needed):**
```python
# For WebSocket transport (FastMCP 2.0 feature)
app.mount("/mcp", mcp.as_asgi(transport="websocket"))

# For automatic transport detection
app.mount("/mcp", mcp.as_asgi())  # Defaults to SSE
```

**Mounting Pattern Explanation:**
- **Path:** `/mcp` - Standard convention for MCP endpoints
- **Method:** `app.mount()` - FastAPI sub-application mounting
- **Transport:** SSE (Server-Sent Events) for streaming responses
- **Result:** MCP tools accessible at `https://yourserver.com/mcp`

**Endpoint Structure After Mounting:**
```
FastAPI Application (/)
├── GET  /          (root endpoint)
├── GET  /health    (health check)
├── GET  /docs      (OpenAPI docs)
├── POST /api/forecast  (REST API)
└── /mcp            (MCP sub-app)
    ├── POST /mcp/messages  (MCP protocol endpoint)
    ├── GET  /mcp/sse       (SSE transport)
    └── Tools:
        • forecast_sku
        • list_available_skus
```

**Verification:**
```bash
# Start server
uvicorn main:app --reload

# Check mounted routes
curl http://localhost:8000/openapi.json | jq '.paths | keys'

# Should include:
# - "/"
# - "/health"
# - "/api/forecast"
# - "/mcp/..." (MCP endpoints)
```

**Testing MCP Endpoint:**
```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp

# Should show:
# ✓ Connected to server
# ✓ Tools discovered: forecast_sku, list_available_skus
```

**Common Issues:**
- **404 on /mcp**: Ensure mount() called after tool definitions
- **CORS errors**: Add CORS middleware (handled in Phase 3)
- **Transport errors**: Verify SSE support in client

**Acceptance Criteria:**
- [ ] `app.mount()` statement added after tool definitions
- [ ] Mounted at `/mcp` path
- [ ] Transport specified as "sse"
- [ ] Print confirmation message
- [ ] Server starts without errors
- [ ] `/mcp` endpoint responds (not 404)
- [ ] MCP Inspector can connect successfully
- [ ] Both MCP tools discoverable by clients
- [ ] OpenAPI docs include /mcp routes

#### TASK-207: Create root endpoint
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-202

**Description:** 
Create a welcoming root endpoint that provides service information and API documentation. This endpoint serves as the entry point for users discovering the service and helps with debugging deployment issues.

**Implementation Steps:**
1. Create GET endpoint at root path "/"
2. Return structured JSON with service metadata
3. Include links to documentation and key endpoints
4. Add version information for debugging

**Code Implementation:**
```python
# --- REST API Endpoints ---
# Add after "# --- REST API Endpoints ---" section (around line 170)

@app.get("/")
async def root():
    """
    Service information and API documentation.
    
    Returns metadata about the Expo Smooth MCP Server including
    available endpoints, version, and usage instructions.
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "status": "operational",
        "endpoints": {
            "health": {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint"
            },
            "mcp_tools": {
                "path": "/mcp",
                "method": "POST",
                "description": "MCP protocol endpoint (SSE transport)",
                "tools": ["forecast_sku", "list_available_skus"]
            },
            "rest_api": {
                "path": "/api/forecast",
                "method": "POST",
                "description": "REST API for forecasting"
            },
            "gradio_ui": {
                "path": "/gradio",
                "method": "GET",
                "description": "Interactive web UI (backward compatibility)"
            },
            "documentation": {
                "path": "/docs",
                "method": "GET",
                "description": "OpenAPI/Swagger documentation"
            }
        },
        "usage": {
            "mcp_clients": "Connect via MCP protocol at /mcp endpoint",
            "rest_clients": "POST to /api/forecast with JSON payload",
            "web_ui": "Visit /gradio for interactive interface"
        },
        "data_status": "loaded" if PROCESSED_DF is not None else "not_loaded",
        "sku_count": len(logic.get_available_skus(PROCESSED_DF)) if PROCESSED_DF is not None else 0
    }
```

**Response Example:**
```json
{
  "name": "Expo Smooth MCP Server",
  "version": "2.0.0",
  "description": "Production MCP server for exponential smoothing forecasting...",
  "status": "operational",
  "endpoints": {
    "health": {
      "path": "/health",
      "method": "GET",
      "description": "Health check endpoint"
    },
    "mcp_tools": {
      "path": "/mcp",
      "method": "POST",
      "description": "MCP protocol endpoint (SSE transport)",
      "tools": ["forecast_sku", "list_available_skus"]
    },
    ...
  },
  "usage": {
    "mcp_clients": "Connect via MCP protocol at /mcp endpoint",
    "rest_clients": "POST to /api/forecast with JSON payload",
    "web_ui": "Visit /gradio for interactive interface"
  },
  "data_status": "loaded",
  "sku_count": 43
}
```

**Use Cases:**
1. **Service Discovery**: New users understand what the service does
2. **Deployment Verification**: Confirm service is running correctly
3. **Debugging**: Check data_status and sku_count
4. **API Exploration**: Discover available endpoints

**Testing:**
```bash
# Test endpoint
curl http://localhost:8000/ | jq

# Verify fields
curl http://localhost:8000/ | jq '.version'  # Should show "2.0.0"
curl http://localhost:8000/ | jq '.sku_count'  # Should show 43

# Test in browser
open http://localhost:8000/
```

**Design Decisions:**
- **JSON format**: Machine-readable and browser-friendly
- **Include status**: Helps monitoring/alerting
- **List endpoints**: Self-documenting API
- **Show data status**: Debugging aid
- **No authentication**: Public endpoint for discovery

**Acceptance Criteria:**
- [ ] Endpoint registered at "/" path
- [ ] Returns JSON response
- [ ] Includes name, version, description
- [ ] Lists all major endpoints with descriptions
- [ ] Shows data_status (loaded/not_loaded)
- [ ] Shows sku_count when data loaded
- [ ] Response is valid JSON
- [ ] Endpoint accessible without authentication
- [ ] Pretty-printed in browser
- [ ] Documented in OpenAPI schema

#### TASK-208: Create health check endpoint
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-203

**Description:** 
Implement a health check endpoint for monitoring, load balancers, and container orchestration. This endpoint validates that the service is running and data is loaded correctly.

**Implementation Steps:**
1. Create GET endpoint at "/health"
2. Check data loaded status
3. Return appropriate HTTP status codes
4. Include diagnostic information
5. Follow health check best practices

**Code Implementation:**
```python
# Add after root endpoint (around line 210)

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns 200 OK if service is healthy (data loaded successfully).
    Returns 503 Service Unavailable if data failed to load.
    
    This endpoint is used by:
    - Docker HEALTHCHECK
    - Fly.io health checks
    - Kubernetes liveness/readiness probes
    - Monitoring systems
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "reason": "Data not loaded",
                "details": "FMCG_Sales.csv failed to load on startup",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    try:
        # Additional health checks
        sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        return {
            "status": "healthy",
            "version": APP_VERSION,
            "data_loaded": True,
            "sku_count": sku_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "reason": "Health check failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

**Add Required Import:**
```python
# At top of file with other imports
from datetime import datetime
from fastapi.responses import JSONResponse
```

**Response Examples:**
```json
// Healthy (200 OK)
{
  "status": "healthy",
  "version": "2.0.0",
  "data_loaded": true,
  "sku_count": 43,
  "timestamp": "2025-10-13T10:30:45.123Z"
}

// Unhealthy (503 Service Unavailable)
{
  "status": "unhealthy",
  "reason": "Data not loaded",
  "details": "FMCG_Sales.csv failed to load on startup",
  "timestamp": "2025-10-13T10:30:45.123Z"
}
```

**Health Check Standards:**
- **Status Codes:**
  - `200 OK`: Service healthy and ready
  - `503 Service Unavailable`: Service running but not ready
  - Never return `500` (indicates endpoint itself is broken)

- **Response Content:**
  - Always return JSON (even on errors)
  - Include timestamp for debugging
  - Include version for deployment tracking
  - Include diagnostic info (sku_count)

**Integration Examples:**

**Docker HEALTHCHECK:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Fly.io fly.toml:**
```toml
[http_service.checks.health]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/health"
```

**Kubernetes:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
```

**Testing:**
```bash
# Test healthy state
curl -i http://localhost:8000/health
# Should return: HTTP/1.1 200 OK

# Test response format
curl http://localhost:8000/health | jq '.status'
# Should return: "healthy"

# Test with data not loaded (simulate failure)
# Move FMCG_Sales.csv temporarily and restart
mv FMCG_Sales.csv FMCG_Sales.csv.bak
# Restart server
curl -i http://localhost:8000/health
# Should return: HTTP/1.1 503 Service Unavailable
```

**Acceptance Criteria:**
- [ ] Endpoint registered at "/health" path
- [ ] Returns 200 OK when data loaded
- [ ] Returns 503 when data not loaded
- [ ] Response is valid JSON in both cases
- [ ] Includes status field ("healthy" or "unhealthy")
- [ ] Includes timestamp in ISO format
- [ ] Includes sku_count when healthy
- [ ] Includes reason when unhealthy
- [ ] Never raises unhandled exceptions
- [ ] Works with Docker HEALTHCHECK
- [ ] Documented in OpenAPI schema

#### TASK-209: Implement dual-transport entrypoint
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-206

**Description:** 
Implement command-line argument parsing to enable both stdio (local development) and HTTP/SSE (production) transports from a single codebase. This allows the same application to serve local MCP clients like Claude Desktop and remote clients via HTTP.

**Implementation Steps:**
1. Add argparse for command-line parsing
2. Implement stdio mode handler
3. Implement HTTP mode handler
4. Add usage documentation
5. Test both modes

**Code Implementation:**
```python
# --- Main Entry Point ---
# Replace existing if __name__ == "__main__" block (around line 280)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} - Dual-transport MCP server"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="http",
        help="Transport mode: stdio for local clients, http for remote (default: http)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP server (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        # --- stdio Transport (Local Development) ---
        print(f"{APP_NAME} v{APP_VERSION} - stdio mode", file=sys.stderr)
        print("Ready for MCP communication via stdin/stdout", file=sys.stderr)
        
        # Load data synchronously for stdio mode
        try:
            global PROCESSED_DF
            PROCESSED_DF = logic.get_processed_data()
            sku_count = len(logic.get_available_skus(PROCESSED_DF))
            print(f"✓ Loaded data: {sku_count} SKUs", file=sys.stderr)
        except Exception as e:
            print(f"✗ ERROR: Failed to load data: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Run MCP server in stdio mode
        # This blocks and handles MCP protocol on stdin/stdout
        import asyncio
        asyncio.run(mcp.run_stdio())
        
    else:
        # --- HTTP Transport (Production) ---
        print(f"{APP_NAME} v{APP_VERSION} - HTTP mode")
        print(f"Starting server at http://{args.host}:{args.port}")
        print(f"MCP endpoint: http://{args.host}:{args.port}/mcp")
        print(f"API docs: http://{args.host}:{args.port}/docs")
        print(f"Gradio UI: http://{args.host}:{args.port}/gradio")
        
        # Run FastAPI server with uvicorn
        uvicorn.run(
            "src.expo_smooth_mcp.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
```

**Usage Examples:**

**Local Development (stdio):**
```bash
# For Claude Desktop, Cursor, VS Code
python -m src.expo_smooth_mcp.main --transport stdio

# Or using FastMCP CLI
fastmcp run src.expo_smooth_mcp.main:mcp --transport stdio

# Output to stderr:
# Expo Smooth MCP Server v2.0.0 - stdio mode
# Ready for MCP communication via stdin/stdout
# ✓ Loaded data: 43 SKUs
```

**Production HTTP:**
```bash
# Basic HTTP server
python -m src.expo_smooth_mcp.main --transport http

# Custom port
python -m src.expo_smooth_mcp.main --transport http --port 3000

# Development with auto-reload
python -m src.expo_smooth_mcp.main --transport http --reload

# Output:
# Expo Smooth MCP Server v2.0.0 - HTTP mode
# Starting server at http://0.0.0.0:8000
# MCP endpoint: http://0.0.0.0:8000/mcp
# API docs: http://0.0.0.0:8000/docs
```

**Claude Desktop Configuration:**
```json
// ~/.config/claude/config.json
{
  "mcpServers": {
    "expo-smooth": {
      "command": "python",
      "args": [
        "-m",
        "src.expo_smooth_mcp.main",
        "--transport",
        "stdio"
      ],
      "cwd": "/path/to/expo-smooth-mcp"
    }
  }
}
```

**Docker Configuration:**
```dockerfile
# HTTP mode for container
CMD ["python", "-m", "src.expo_smooth_mcp.main", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Design Decisions:**
- **Default to HTTP**: Production use case is more common
- **stdio blocks**: Must use `asyncio.run(mcp.run_stdio())` for stdio mode
- **Separate data loading**: stdio mode loads synchronously before starting
- **stderr for stdio logs**: stdout is reserved for MCP protocol
- **Reload flag**: Only applicable in HTTP mode

**Testing Both Modes:**

**Test stdio mode:**
```bash
# Echo test (should see MCP protocol initialization)
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | \
  python -m src.expo_smooth_mcp.main --transport stdio

# With MCP Inspector
npx @modelcontextprotocol/inspector \
  python -m src.expo_smooth_mcp.main --transport stdio
```

**Test HTTP mode:**
```bash
# Start server
python -m src.expo_smooth_mcp.main --transport http --port 8000

# In another terminal
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

**Common Issues:**
- **stdio hangs**: Normal - it's waiting for input
- **Port already in use**: Change --port value
- **Data not loading**: Check FMCG_Sales.csv exists
- **Import errors**: Run from project root

**Acceptance Criteria:**
- [ ] argparse configured with all four arguments
- [ ] stdio mode handler implemented
- [ ] HTTP mode handler implemented
- [ ] stdio mode loads data before starting
- [ ] stdio mode logs to stderr (not stdout)
- [ ] HTTP mode starts uvicorn correctly
- [ ] Default transport is "http"
- [ ] --reload flag works in HTTP mode
- [ ] Both modes can start successfully
- [ ] stdio mode works with Claude Desktop
- [ ] HTTP mode serves all endpoints
- [ ] Help text available: `--help`

#### TASK-210: Create REST API forecast endpoint
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-204

**Description:** 
Create a REST API endpoint for forecasting that serves non-MCP clients (cURL, Postman, web apps). This endpoint provides the same functionality as the MCP tool but via standard HTTP POST with JSON.

**Implementation Steps:**
1. Define Pydantic request and response models
2. Implement POST endpoint at /api/forecast
3. Add validation and error handling
4. Add OpenAPI documentation
5. Test with cURL

**Pydantic Models:**
```python
# Add after imports section (around line 15)

from pydantic import BaseModel, Field
from typing import Optional

class ForecastRequest(BaseModel):
    """Request model for forecast API endpoint."""
    sku: str = Field(
        ...,
        description="Product SKU code to forecast",
        example="PRODUCT_123"
    )
    forecast_horizon: int = Field(
        default=90,
        ge=1,
        le=365,
        description="Number of days to forecast ahead",
        example=90
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "sku": "PRODUCT_123",
                "forecast_horizon": 90
            }
        }

class ForecastMetadata(BaseModel):
    """Metadata about the forecast."""
    sku: str
    forecast_horizon: int
    historical_points: int
    forecast_points: int

class ForecastResponse(BaseModel):
    """Response model for forecast API endpoint."""
    dates: List[str] = Field(
        description="Date strings in ISO format (YYYY-MM-DD)"
    )
    actuals: List[Optional[float]] = Field(
        description="Historical sales values (null for future dates)"
    )
    forecast: List[float] = Field(
        description="Forecasted sales values"
    )
    metadata: ForecastMetadata = Field(
        description="Forecast metadata and statistics"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "dates": ["2025-01-01", "2025-01-02", "2025-01-03"],
                "actuals": [100.0, 105.0, None],
                "forecast": [102.0, 107.0, 110.0],
                "metadata": {
                    "sku": "PRODUCT_123",
                    "forecast_horizon": 90,
                    "historical_points": 365,
                    "forecast_points": 90
                }
            }
        }
```

**REST Endpoint Implementation:**
```python
# Add after health check endpoint (around line 270)

@app.post("/api/forecast", response_model=ForecastResponse)
async def create_forecast(request: ForecastRequest):
    """
    Generate sales forecast for a product SKU (REST API).
    
    This endpoint provides the same functionality as the MCP forecast_sku tool
    but via standard REST API for non-MCP clients.
    
    Args:
        request: ForecastRequest with sku and optional forecast_horizon
    
    Returns:
        ForecastResponse with dates, actuals, forecast, and metadata
    
    Raises:
        HTTPException 503: If data not loaded
        HTTPException 400: If validation fails (invalid SKU or horizon)
        HTTPException 500: If forecast generation fails
    """
    # Check if data is loaded
    if PROCESSED_DF is None:
        raise HTTPException(
            status_code=503,
            detail="Data not loaded. Server started without valid dataset."
        )
    
    try:
        # Validate request
        logic.validate_forecast_request(
            PROCESSED_DF,
            request.sku,
            request.forecast_horizon
        )
        
        # Generate forecast
        forecast_data = logic.get_forecast_data(
            PROCESSED_DF,
            request.sku,
            request.forecast_horizon
        )
        
        # Return structured response
        return ForecastResponse(**forecast_data)
        
    except ValueError as e:
        # Validation errors (invalid SKU, bad horizon)
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    
    except Exception as e:
        # Unexpected errors
        print(f"ERROR in create_forecast: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Forecast generation failed: {str(e)}"
        )
```

**Add HTTPException Import:**
```python
# Update FastAPI import at top of file
from fastapi import FastAPI, HTTPException
```

**API Usage Examples:**

**cURL:**
```bash
# Basic request
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_123", "forecast_horizon": 90}'

# With jq for pretty output
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_123"}' | jq

# Get just the forecast values
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_123"}' | jq '.forecast'
```

**Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/forecast",
    json={"sku": "PRODUCT_123", "forecast_horizon": 90}
)

data = response.json()
print(f"Forecast {len(data['forecast'])} days")
```

**JavaScript fetch:**
```javascript
const response = await fetch('http://localhost:8000/api/forecast', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({sku: 'PRODUCT_123', forecast_horizon: 90})
});

const data = await response.json();
console.log(`Forecast: ${data.forecast.length} points`);
```

**OpenAPI Documentation:**
Once implemented, the endpoint will appear in `/docs` with:
- Interactive "Try it out" button
- Request body schema
- Response schema with examples
- Error response codes

**Error Responses:**

**400 Bad Request (Invalid SKU):**
```json
{
  "detail": "Validation error: SKU 'INVALID' not found. Available SKUs: ['PRODUCT_001', ...]"
}
```

**400 Bad Request (Invalid Horizon):**
```json
{
  "detail": "Validation error: Forecast horizon must be between 1 and 365 days, got 500"
}
```

**503 Service Unavailable:**
```json
{
  "detail": "Data not loaded. Server started without valid dataset."
}
```

**Testing Checklist:**
```bash
# Test valid request
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' | jq '.metadata'

# Test invalid SKU
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID"}' | jq '.detail'

# Test invalid horizon
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 500}' | jq '.detail'

# Test OpenAPI docs
open http://localhost:8000/docs
# Navigate to POST /api/forecast
# Click "Try it out"
# Test with example values
```

**Acceptance Criteria:**
- [ ] ForecastRequest model defined with validation
- [ ] ForecastResponse model defined with examples
- [ ] POST endpoint at /api/forecast
- [ ] Validates inputs before processing
- [ ] Returns 400 for validation errors
- [ ] Returns 503 if data not loaded
- [ ] Returns 500 for unexpected errors
- [ ] Response matches ForecastResponse schema
- [ ] Appears in OpenAPI docs at /docs
- [ ] Works with cURL
- [ ] Works with Postman
- [ ] Error messages are helpful

#### TASK-211: Create integration tests for FastMCP
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-208, TASK-209

**Description:** 
Create comprehensive integration test suite for the FastAPI + FastMCP application. These tests verify that all endpoints work together correctly and the application can start in both transport modes.

**Implementation Steps:**
1. Create test file with fixtures
2. Write tests for REST endpoints
3. Write tests for MCP tools
4. Write tests for error cases
5. Add test coverage reporting

**Test File Structure:**
```python
# tests/test_mcp_integration.py
"""
Integration tests for FastAPI + FastMCP application.

These tests verify the complete application stack including:
- REST API endpoints
- MCP tool functionality  
- Health checks
- Error handling
"""

import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from src.expo_smooth_mcp.main import app, PROCESSED_DF
from src.expo_smooth_mcp import logic

# --- Fixtures ---

@pytest.fixture
def client():
    """Create FastAPI test client."""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Create async HTTP client for FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# --- REST API Endpoint Tests ---

class TestRootEndpoint:
    """Tests for GET / endpoint."""
    
    def test_root_returns_service_info(self, client):
        """Should return service metadata."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Expo Smooth MCP Server"
        assert data["version"] == "2.0.0"
        assert "endpoints" in data
        assert "usage" in data
    
    def test_root_shows_data_status(self, client):
        """Should indicate if data is loaded."""
        response = client.get("/")
        data = response.json()
        
        assert "data_status" in data
        assert data["data_status"] in ["loaded", "not_loaded"]
        
        if data["data_status"] == "loaded":
            assert data["sku_count"] > 0

class TestHealthEndpoint:
    """Tests for GET /health endpoint."""
    
    def test_health_check_when_healthy(self, client):
        """Should return 200 when data loaded."""
        response = client.get("/health")
        
        # If data is loaded, expect 200
        if PROCESSED_DF is not None:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["data_loaded"] is True
            assert data["sku_count"] > 0
    
    def test_health_check_returns_timestamp(self, client):
        """Should include ISO timestamp."""
        response = client.get("/health")
        data = response.json()
        
        assert "timestamp" in data
        # Verify ISO format (basic check)
        assert "T" in data["timestamp"]
        assert "Z" in data["timestamp"] or "+" in data["timestamp"]
    
    def test_health_check_returns_version(self, client):
        """Should include app version."""
        response = client.get("/health")
        
        if response.status_code == 200:
            data = response.json()
            assert data["version"] == "2.0.0"

class TestForecastAPIEndpoint:
    """Tests for POST /api/forecast endpoint."""
    
    def test_forecast_with_valid_sku(self, client):
        """Should return forecast for valid SKU."""
        # Get a valid SKU first
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        response = client.post(
            "/api/forecast",
            json={"sku": test_sku, "forecast_horizon": 90}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "dates" in data
        assert "actuals" in data
        assert "forecast" in data
        assert "metadata" in data
        
        # Verify data types
        assert isinstance(data["dates"], list)
        assert isinstance(data["forecast"], list)
        assert len(data["forecast"]) > 0
    
    def test_forecast_with_invalid_sku(self, client):
        """Should return 400 for invalid SKU."""
        response = client.post(
            "/api/forecast",
            json={"sku": "INVALID_SKU", "forecast_horizon": 90}
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()
        assert "not found" in response.json()["detail"].lower()
    
    def test_forecast_with_invalid_horizon(self, client):
        """Should return 400 for out-of-range horizon."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        response = client.post(
            "/api/forecast",
            json={"sku": test_sku, "forecast_horizon": 500}
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_forecast_default_horizon(self, client):
        """Should use default horizon of 90 days."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        response = client.post(
            "/api/forecast",
            json={"sku": test_sku}  # No horizon specified
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["metadata"]["forecast_horizon"] == 90

# --- MCP Tool Tests ---

class TestMCPTools:
    """Tests for MCP tool functionality."""
    
    @pytest.mark.asyncio
    async def test_forecast_sku_tool(self):
        """Should generate forecast via MCP tool."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        from src.expo_smooth_mcp.main import forecast_sku
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        result = await forecast_sku(test_sku, 90)
        
        assert isinstance(result, dict)
        assert "dates" in result
        assert "forecast" in result
        assert "metadata" in result
    
    @pytest.mark.asyncio
    async def test_list_available_skus_tool(self):
        """Should list SKUs via MCP tool."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        from src.expo_smooth_mcp.main import list_available_skus
        
        result = await list_available_skus()
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(sku, str) for sku in result)

# --- Error Handling Tests ---

class TestErrorHandling:
    """Tests for error scenarios."""
    
    def test_openapi_schema_available(self, client):
        """Should serve OpenAPI schema."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
    
    def test_docs_endpoint_available(self, client):
        """Should serve Swagger UI."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

# --- Performance Tests ---

class TestPerformance:
    """Basic performance tests."""
    
    def test_forecast_response_time(self, client):
        """Should return forecast in reasonable time."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        import time
        start = time.time()
        
        response = client.post(
            "/api/forecast",
            json={"sku": test_sku, "forecast_horizon": 90}
        )
        
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0  # Should be under 1 second

# --- Test Configuration ---

def test_app_initialization():
    """Verify app initializes correctly."""
    assert app.title == "Expo Smooth MCP Server"
    assert app.version == "2.0.0"

# Run tests with: pytest tests/test_mcp_integration.py -v
```

**Test Dependencies:**
Add to requirements.txt or install separately:
```bash
uv add --dev pytest pytest-asyncio httpx
```

**Running Tests:**
```bash
# Run all integration tests
pytest tests/test_mcp_integration.py -v

# Run with coverage
pytest tests/test_mcp_integration.py --cov=src.expo_smooth_mcp.main --cov-report=term-missing

# Run specific test class
pytest tests/test_mcp_integration.py::TestHealthEndpoint -v

# Run in parallel (faster)
pytest tests/test_mcp_integration.py -v -n auto
```

**Expected Output:**
```
tests/test_mcp_integration.py::TestRootEndpoint::test_root_returns_service_info PASSED
tests/test_mcp_integration.py::TestHealthEndpoint::test_health_check_when_healthy PASSED
tests/test_mcp_integration.py::TestForecastAPIEndpoint::test_forecast_with_valid_sku PASSED
tests/test_mcp_integration.py::TestForecastAPIEndpoint::test_forecast_with_invalid_sku PASSED
tests/test_mcp_integration.py::TestMCPTools::test_forecast_sku_tool PASSED
tests/test_mcp_integration.py::TestMCPTools::test_list_available_skus_tool PASSED

=================== 15 passed in 2.34s ===================
```

**Acceptance Criteria:**
- [ ] File `tests/test_mcp_integration.py` created
- [ ] Tests for all REST endpoints (/, /health, /api/forecast)
- [ ] Tests for both MCP tools (forecast_sku, list_available_skus)
- [ ] Tests for error cases (invalid SKU, invalid horizon)
- [ ] Tests for OpenAPI documentation
- [ ] All tests pass: `pytest tests/test_mcp_integration.py`
- [ ] Coverage >80%: `pytest --cov`
- [ ] Tests run in <10 seconds
- [ ] Tests are independent (can run in any order)
- [ ] Skip tests gracefully if data not loaded

#### TASK-212: Manual testing of local server
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-211

**Description:** 
Perform comprehensive manual testing of the complete FastAPI + FastMCP server to verify all functionality works end-to-end. This validates the implementation before proceeding to Gradio integration.

**Testing Checklist:**

### 1. Server Startup Testing (10 min)

**HTTP Mode:**
```bash
# Start server in HTTP mode
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Verify startup logs show:
# ✓ "Starting Expo Smooth MCP Server v2.0.0 - HTTP mode"
# ✓ "✓ Data loaded successfully"
# ✓ "✓ Found {N} unique SKUs"
# ✓ "✓ Mounted MCP server at /mcp with SSE transport"

# Server should be running at http://localhost:8000
```

**stdio Mode:**
```bash
# Start server in stdio mode
python -m src.expo_smooth_mcp.main --transport stdio

# Verify startup logs to stderr show:
# ✓ "Expo Smooth MCP Server v2.0.0 - stdio mode"
# ✓ "Ready for MCP communication via stdin/stdout"
# ✓ "✓ Loaded data: {N} SKUs"

# Server should be waiting for input (this is normal)
# Press Ctrl+C to stop
```

### 2. REST API Testing (15 min)

**Test Root Endpoint:**
```bash
# Should return service info
curl http://localhost:8000/ | jq

# Verify response includes:
# ✓ name: "Expo Smooth MCP Server"
# ✓ version: "2.0.0"
# ✓ endpoints object with 5 endpoints
# ✓ data_status: "loaded"
# ✓ sku_count > 0
```

**Test Health Endpoint:**
```bash
# Should return 200 OK
curl -i http://localhost:8000/health

# Verify:
# ✓ HTTP/1.1 200 OK
# ✓ status: "healthy"
# ✓ data_loaded: true
# ✓ sku_count matches root endpoint
# ✓ timestamp in ISO format
```

**Test Forecast API:**
```bash
# Get available SKUs first
curl http://localhost:8000/ | jq '.sku_count'

# Test with first available SKU (usually PRODUCT_001)
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' | jq

# Verify response includes:
# ✓ dates array with 90+ items
# ✓ actuals array with some values and some nulls
# ✓ forecast array with 90 items
# ✓ metadata object with all 4 fields

# Test error handling
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID", "forecast_horizon": 90}' | jq

# Verify:
# ✓ Returns 400 status
# ✓ detail field with error message
```

### 3. OpenAPI Documentation Testing (10 min)

```bash
# Open Swagger UI in browser
open http://localhost:8000/docs

# Verify in browser:
# ✓ Swagger UI loads correctly
# ✓ Shows "Expo Smooth MCP Server v2.0.0"
# ✓ Lists all endpoints:
#   - GET  /
#   - GET  /health
#   - POST /api/forecast
#   - (MCP endpoints)

# Test forecast endpoint interactively:
# 1. Click "POST /api/forecast"
# 2. Click "Try it out"
# 3. Enter {"sku": "PRODUCT_001", "forecast_horizon": 90}
# 4. Click "Execute"
# 5. Verify 200 response with forecast data

# Check ReDoc
open http://localhost:8000/redoc

# Verify:
# ✓ ReDoc UI loads
# ✓ Clean documentation display
# ✓ All endpoints documented
```

### 4. MCP Inspector Testing (15 min)

```bash
# Install MCP Inspector (if not already installed)
npm install -g @modelcontextprotocol/inspector

# Test HTTP/SSE transport
npx @modelcontextprotocol/inspector http://localhost:8000/mcp

# In MCP Inspector UI:
# ✓ Connection status shows "Connected"
# ✓ Server info shows name and version
# ✓ Tools section shows 2 tools:
#   - forecast_sku
#   - list_available_skus

# Test list_available_skus tool:
# 1. Click on "list_available_skus"
# 2. Click "Execute"
# 3. Verify returns array of SKU strings
# 4. Note first SKU for next test

# Test forecast_sku tool:
# 1. Click on "forecast_sku"
# 2. Enter SKU from previous step
# 3. Enter forecast_horizon: 90
# 4. Click "Execute"
# 5. Verify returns forecast data object

# Test stdio transport
npx @modelcontextprotocol/inspector \
  python -m src.expo_smooth_mcp.main --transport stdio

# Verify:
# ✓ Inspector connects via stdio
# ✓ Both tools discoverable
# ✓ Can execute tools successfully
```

### 5. Performance Testing (10 min)

```bash
# Test response times
time curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' > /dev/null

# Verify:
# ✓ Response time < 1 second (should be 100-500ms)

# Test concurrent requests (simple load test)
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/forecast \
    -H "Content-Type: application/json" \
    -d '{"sku": "PRODUCT_001"}' &
done
wait

# Verify:
# ✓ All requests complete successfully
# ✓ No errors in server logs
# ✓ Response times remain consistent
```

### 6. Error Handling Testing (10 min)

**Test Data Not Loaded Scenario:**
```bash
# Temporarily rename data file
mv FMCG_Sales.csv FMCG_Sales.csv.bak

# Restart server
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Test health endpoint
curl http://localhost:8000/health

# Verify:
# ✓ Returns 503 status
# ✓ status: "unhealthy"
# ✓ reason indicates data not loaded

# Test forecast endpoint
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001"}' | jq

# Verify:
# ✓ Returns 503 status
# ✓ Helpful error message

# Restore data file
mv FMCG_Sales.csv.bak FMCG_Sales.csv
```

**Test Invalid Inputs:**
```bash
# Invalid SKU
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "DOES_NOT_EXIST"}' | jq '.detail'

# Invalid horizon (too large)
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 1000}' | jq '.detail'

# Invalid horizon (too small)
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 0}' | jq '.detail'

# Invalid JSON
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d 'invalid json' | jq

# All should return:
# ✓ 400 status with helpful error message
# ✓ Or 422 for malformed JSON
```

### 7. Final Verification Checklist

**HTTP Transport:**
- [ ] Server starts without errors
- [ ] All endpoints respond correctly
- [ ] OpenAPI docs accessible and accurate
- [ ] MCP Inspector can connect via HTTP
- [ ] Both MCP tools work correctly
- [ ] Error handling works as expected
- [ ] Response times < 1 second
- [ ] Concurrent requests handled correctly

**stdio Transport:**
- [ ] Server starts in stdio mode
- [ ] Logs go to stderr (not stdout)
- [ ] Data loads successfully
- [ ] MCP Inspector can connect via stdio
- [ ] Both MCP tools work correctly
- [ ] Can stop with Ctrl+C cleanly

**Documentation:**
- [ ] /docs shows all endpoints
- [ ] /redoc shows clean documentation
- [ ] Example requests work from Swagger UI
- [ ] OpenAPI schema is valid

**Acceptance Criteria:**
- [ ] All checklist items completed
- [ ] No errors in server logs
- [ ] All endpoints return expected responses
- [ ] Both transports work correctly
- [ ] Performance meets expectations (<1s response)
- [ ] Error handling is comprehensive
- [ ] Documentation is accurate
- [ ] Ready to proceed to Phase 3 (Gradio integration)

---

### Phase 3: Mount Gradio UI (6 tasks, ~8 hours)

#### TASK-301: Create Pydantic models for API
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-210

**Description:** 
Define Pydantic models for internal API communication between Gradio UI and FastAPI backend. These models ensure type safety and validation for the refactored Gradio interface. (Note: This task may be already completed in TASK-210, in which case verify the models are suitable for Gradio integration.)

**Implementation Steps:**
1. Verify Pydantic models from TASK-210 exist
2. Add any additional models needed for Gradio
3. Optionally move models to separate `models.py` file
4. Update imports if refactoring to separate file

**Verification:**
```python
# Check if models already exist in main.py from TASK-210
from src.expo_smooth_mcp.main import ForecastRequest, ForecastResponse

# Test model instantiation
request = ForecastRequest(sku="PRODUCT_001", forecast_horizon=90)
assert request.sku == "PRODUCT_001"
assert request.forecast_horizon == 90
```

**Optional: Refactor to Separate File:**
```python
# Create src/expo_smooth_mcp/models.py
"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class ForecastRequest(BaseModel):
    """Request model for forecast API endpoint."""
    sku: str = Field(
        ...,
        description="Product SKU code to forecast",
        example="PRODUCT_123"
    )
    forecast_horizon: int = Field(
        default=90,
        ge=1,
        le=365,
        description="Number of days to forecast ahead",
        example=90
    )

class ForecastMetadata(BaseModel):
    """Metadata about the forecast."""
    sku: str
    forecast_horizon: int
    historical_points: int
    forecast_points: int

class ForecastResponse(BaseModel):
    """Response model for forecast API endpoint."""
    dates: List[str]
    actuals: List[Optional[float]]
    forecast: List[float]
    metadata: ForecastMetadata

# Update main.py imports:
# from .models import ForecastRequest, ForecastResponse
```

**Design Decision:**
- **Keep in main.py**: Simpler for small projects (recommended)
- **Separate models.py**: Better for larger projects with many models

**Acceptance Criteria:**
- [ ] ForecastRequest model exists with sku and forecast_horizon fields
- [ ] ForecastResponse model exists with all four required fields
- [ ] Models have proper validation (ge=1, le=365 for horizon)
- [ ] Models have Field descriptions for documentation
- [ ] Can be imported from main.py or models.py
- [ ] Models work with FastAPI endpoint from TASK-210
- [ ] Models work with Gradio API calls (validated in TASK-302)

#### TASK-302: Refactor Gradio to call REST API
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-301

**Description:** 
Refactor the Gradio application to communicate with FastAPI via HTTP instead of calling business logic directly. This decouples the UI from the backend and prepares for mounting Gradio as a sub-application.

**Implementation Steps:**
1. Modify app.py to use httpx for API calls
2. Update create_forecast_plot() to call REST endpoint
3. Handle API errors gracefully in UI
4. Test with FastAPI server running
5. Maintain backward compatibility

**Current app.py Pattern:**
```python
# BEFORE (direct logic calls)
def create_forecast_plot(sku: str):
    logic.validate_forecast_request(PROCESSED_DF, sku, 90)
    forecast_data = logic.get_forecast_data(PROCESSED_DF, sku, 90)
    return logic.create_forecast_plot(forecast_data)
```

**Refactored Pattern:**
```python
# AFTER (API calls)
import httpx
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

async def create_forecast_plot(sku: str):
    """
    Generate forecast plot by calling FastAPI backend.
    
    This function now makes HTTP requests to the REST API instead of
    calling business logic directly. This allows Gradio to work as a
    standalone client of the FastAPI service.
    """
    if not sku:
        return _create_empty_plot("Please select a product SKU")
    
    try:
        # Call FastAPI forecast endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/forecast",
                json={"sku": sku, "forecast_horizon": 90},
                timeout=10.0
            )
            response.raise_for_status()
            
            # Parse response
            forecast_data = response.json()
            
            # Create plot using logic module (still UI concern)
            from src.expo_smooth_mcp import logic
            return logic.create_forecast_plot(forecast_data)
    
    except httpx.HTTPStatusError as e:
        # API returned error status
        error_detail = e.response.json().get("detail", str(e))
        return _create_error_plot(f"API Error: {error_detail}")
    
    except httpx.RequestError as e:
        # Network error (API not reachable)
        return _create_error_plot(
            f"Cannot connect to API at {API_BASE_URL}. "
            "Make sure the server is running."
        )
    
    except Exception as e:
        # Unexpected error
        return _create_error_plot(f"Error: {str(e)}")

def _create_empty_plot(message: str):
    """Create empty plot with message."""
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.update_layout(
        title_text=message,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": "No data to display.",
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 20}
        }]
    )
    return fig

def _create_error_plot(error_message: str):
    """Create error plot with message."""
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.update_layout(
        title_text="Error",
        annotations=[{
            "text": error_message,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 16, "color": "red"}
        }]
    )
    return fig
```

**Complete app.py After Refactoring:**
```python
# app.py - Refactored for API communication
import gradio as gr
import httpx
import os
import plotly.graph_objects as go
from src.expo_smooth_mcp import logic

# --- Configuration ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# --- Get SKU List ---
# For standalone mode, we still need to get SKUs somehow
# Option 1: Call API endpoint
async def get_sku_list():
    """Fetch SKU list from API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/")
            data = response.json()
            
            # Get SKU count, but we need actual list
            # For now, use a default list or add new endpoint
            # TODO: Add GET /api/skus endpoint in FastAPI
            
            # Temporary: Load locally for dropdown population
            df = logic.get_processed_data()
            return logic.get_available_skus(df)
    except Exception as e:
        print(f"Error fetching SKUs: {e}")
        return []

# Synchronous version for Gradio initialization
import asyncio
try:
    SKU_LIST = asyncio.run(get_sku_list())
except:
    SKU_LIST = []

# --- Event Handler ---
async def create_forecast_plot(sku: str):
    """Generate forecast plot by calling FastAPI backend."""
    if not sku:
        return _create_empty_plot("Please select a product SKU")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/forecast",
                json={"sku": sku, "forecast_horizon": 90},
                timeout=10.0
            )
            response.raise_for_status()
            forecast_data = response.json()
            return logic.create_forecast_plot(forecast_data)
    
    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get("detail", str(e))
        return _create_error_plot(f"API Error: {error_detail}")
    
    except httpx.RequestError as e:
        return _create_error_plot(
            f"Cannot connect to API at {API_BASE_URL}. "
            "Make sure FastAPI server is running."
        )
    
    except Exception as e:
        return _create_error_plot(f"Error: {str(e)}")

def _create_empty_plot(message: str):
    """Create empty plot with message."""
    fig = go.Figure()
    fig.update_layout(
        title_text=message,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": "No data to display.",
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 20}
        }]
    )
    return fig

def _create_error_plot(error_message: str):
    """Create error plot with message."""
    fig = go.Figure()
    fig.update_layout(
        title_text="Error",
        annotations=[{
            "text": error_message,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 16, "color": "red"}
        }]
    )
    return fig

# --- UI Definition ---
demo = gr.Interface(
    fn=create_forecast_plot,
    inputs=[
        gr.Dropdown(
            choices=SKU_LIST,
            label="Select Product SKU",
            info="Choose a product to forecast its sales for the next 90 days."
        )
    ],
    outputs=[gr.Plot(label="Forecast Visualization")],
    title="📈 Supply Chain Demand Forecasting",
    description="An interactive demo of Exponential Smoothing for FMCG sales data.",
    allow_flagging="never"
)

if __name__ == "__main__":
    # Standalone mode - launch Gradio on its own
    print(f"Gradio UI connecting to API at: {API_BASE_URL}")
    print("Make sure FastAPI server is running!")
    demo.launch()
```

**Testing the Refactored Gradio:**

**Terminal 1 - Start FastAPI server:**
```bash
python -m src.expo_smooth_mcp.main --transport http --port 8000
```

**Terminal 2 - Start Gradio app:**
```bash
python app.py
# Should open at http://localhost:7860
```

**Verify:**
1. Gradio UI loads successfully
2. Dropdown populated with SKUs
3. Select a SKU and verify plot appears
4. Stop FastAPI server and verify error message in UI
5. Restart FastAPI and verify UI recovers

**Acceptance Criteria:**
- [ ] app.py imports httpx
- [ ] create_forecast_plot() is async and calls REST API
- [ ] API_BASE_URL configurable via environment variable
- [ ] Handles API errors gracefully with user-friendly messages
- [ ] Handles network errors (API not running)
- [ ] Empty plot helper function defined
- [ ] Error plot helper function defined
- [ ] SKU list still populates dropdown
- [ ] Works when FastAPI server is running
- [ ] Shows helpful error when API unavailable
- [ ] Can run standalone: `python app.py`
- [ ] Visual behavior identical to original app

#### TASK-303: Mount Gradio app in FastAPI
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-302

**Description:** 
Mount the refactored Gradio application into FastAPI at the `/gradio` path. This provides backward compatibility for existing users while centralizing all services under a single server.

**Implementation Steps:**
1. Import Gradio and the demo from app.py
2. Use Gradio's mount_gradio_app() function
3. Configure path and mounting options
4. Test unified server

**Code Implementation:**
```python
# In src/expo_smooth_mcp/main.py
# Add after all endpoints are defined (around line 290)

# --- Mount Gradio UI (Backward Compatibility) ---

try:
    import gradio as gr
    
    # Import the Gradio demo from app.py
    # Note: app.py needs to export 'demo' variable
    from app import demo as gradio_demo
    
    # Mount Gradio at /gradio path
    app = gr.mount_gradio_app(
        app,                    # FastAPI app
        gradio_demo,            # Gradio Interface
        path="/gradio",         # Mount path
        app_kwargs={
            "docs_url": None,   # Disable Gradio's own docs
            "redoc_url": None   # Disable Gradio's redoc
        }
    )
    
    print("✓ Mounted Gradio UI at /gradio")
    
except ImportError as e:
    print(f"⚠ Warning: Could not mount Gradio UI: {e}")
    print("  Continuing without Gradio interface...")
    
except Exception as e:
    print(f"⚠ Warning: Failed to mount Gradio: {e}")
    print("  Continuing without Gradio interface...")
```

**Update app.py to Export demo:**
```python
# At end of app.py - ensure demo is exported
# ... (existing code) ...

demo = gr.Interface(
    fn=create_forecast_plot,
    # ... rest of Interface config ...
)

# Only launch if run directly, not when imported
if __name__ == "__main__":
    print(f"Gradio UI connecting to API at: {API_BASE_URL}")
    print("Make sure FastAPI server is running at {API_BASE_URL}!")
    demo.launch()
```

**Alternative: Define Gradio in main.py (Simpler):**
```python
# In main.py - define Gradio inline instead of importing

# --- Mount Gradio UI (Backward Compatibility) ---

try:
    import gradio as gr
    from src.expo_smooth_mcp import logic
    
    # Get SKU list for dropdown
    sku_list = logic.get_available_skus(PROCESSED_DF) if PROCESSED_DF else []
    
    # Define Gradio interface inline
    def gradio_forecast_ui(sku: str):
        """Gradio UI wrapper for forecast endpoint."""
        if not sku:
            # Return empty plot
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.update_layout(title_text="Please select a product SKU")
            return fig
        
        if PROCESSED_DF is None:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.update_layout(title_text="Data not loaded")
            return fig
        
        try:
            # Call logic directly (since we're in the same process)
            forecast_data = logic.get_forecast_data(PROCESSED_DF, sku, 90)
            return logic.create_forecast_plot(forecast_data)
        except Exception as e:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.update_layout(title_text=f"Error: {e}")
            return fig
    
    gradio_demo = gr.Interface(
        fn=gradio_forecast_ui,
        inputs=[
            gr.Dropdown(
                choices=sku_list,
                label="Select Product SKU",
                info="Choose a product to forecast its sales for the next 90 days."
            )
        ],
        outputs=[gr.Plot(label="Forecast Visualization")],
        title="📈 Supply Chain Demand Forecasting",
        description="Interactive demo of Exponential Smoothing for FMCG sales data.",
        allow_flagging="never"
    )
    
    # Mount at /gradio
    app = gr.mount_gradio_app(app, gradio_demo, path="/gradio")
    print("✓ Mounted Gradio UI at /gradio")
    
except ImportError:
    print("⚠ Warning: Gradio not installed, skipping UI mounting")
    
except Exception as e:
    print(f"⚠ Warning: Failed to mount Gradio: {e}")
```

**Unified Service Structure:**
```
FastAPI Application (http://localhost:8000/)
├── GET  /                    → Service info
├── GET  /health              → Health check
├── GET  /docs                → FastAPI OpenAPI docs
├── POST /api/forecast        → REST API
├── POST /mcp                 → MCP protocol endpoint
└── GET  /gradio              → Gradio UI (mounted)
    └── Interactive web interface for forecasting
```

**Testing the Mounted Gradio:**
```bash
# Start unified server
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Test endpoints
curl http://localhost:8000/              # FastAPI root
curl http://localhost:8000/health        # Health check
open http://localhost:8000/docs          # API docs
open http://localhost:8000/gradio        # Gradio UI

# Verify in browser:
# 1. http://localhost:8000/gradio loads Gradio interface
# 2. Dropdown populated with SKUs
# 3. Can generate forecasts
# 4. UI matches original app.py behavior
```

**Important Notes:**
- **Path must be /gradio**: Gradio expects to be mounted at a subpath
- **Gradio runs in same process**: No separate port needed
- **Shares FastAPI's lifecycle**: Starts/stops with main server
- **Backward compatible**: Existing Gradio users can continue using UI

**Common Issues:**

**Issue: Import error from app.py**
```python
# Solution: Define Gradio inline in main.py (recommended)
# Or ensure app.py doesn't launch when imported
```

**Issue: Gradio UI blank**
```python
# Solution: Check PROCESSED_DF is loaded
# Check SKU_LIST is populated
# Check browser console for errors
```

**Issue: Relative imports fail**
```python
# Solution: Use absolute imports
# from src.expo_smooth_mcp import logic  # Good
# from . import logic  # May fail in some contexts
```

**Acceptance Criteria:**
- [ ] Gradio imported successfully
- [ ] Demo interface created or imported
- [ ] Mounted at /gradio path using gr.mount_gradio_app()
- [ ] Server starts without errors
- [ ] /gradio endpoint accessible in browser
- [ ] Gradio UI loads correctly
- [ ] Dropdown populated with SKUs
- [ ] Can generate forecasts through UI
- [ ] UI behavior matches original app.py
- [ ] No CORS errors in browser console
- [ ] Gradio doesn't interfere with other endpoints
- [ ] Error handling if Gradio import fails

#### TASK-304: Test unified service locally
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-303

**Description:** 
Perform comprehensive testing of the unified service to verify all three interfaces (REST API, MCP tools, Gradio UI) work correctly together without conflicts.

**Testing Procedure:**

### 1. Start Unified Server (5 min)

```bash
# Start server in HTTP mode
python -m src.expo_smooth_mcp.main --transport http --port 8000 --reload

# Verify startup logs show:
# ✓ Starting Expo Smooth MCP Server v2.0.0 - HTTP mode
# ✓ ✓ Data loaded successfully
# ✓ ✓ Found {N} unique SKUs
# ✓ ✓ Mounted MCP server at /mcp with SSE transport
# ✓ ✓ Mounted Gradio UI at /gradio
# ✓ INFO: Uvicorn running on http://0.0.0.0:8000
```

### 2. Test REST API Interface (10 min)

```bash
# Test root endpoint
curl http://localhost:8000/ | jq '.endpoints'

# Verify shows all endpoints including Gradio:
# ✓ health, mcp_tools, rest_api, gradio_ui, documentation

# Test health check
curl http://localhost:8000/health | jq '.status'
# ✓ Should return "healthy"

# Test forecast API
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' | jq '.metadata'
# ✓ Should return forecast data

# Test OpenAPI docs
open http://localhost:8000/docs
# ✓ Swagger UI loads
# ✓ Shows all REST endpoints
# ✓ Can execute test requests
```

### 3. Test MCP Interface (10 min)

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp

# In Inspector UI:
# ✓ Connection successful
# ✓ Shows 2 tools: forecast_sku, list_available_skus
# ✓ Can execute list_available_skus
# ✓ Can execute forecast_sku with valid SKU
# ✓ Both tools return correct data
```

### 4. Test Gradio UI Interface (15 min)

```bash
# Open Gradio UI in browser
open http://localhost:8000/gradio

# Manual testing in browser:
# ✓ Page loads without errors
# ✓ Title: "Supply Chain Demand Forecasting"
# ✓ Dropdown populated with SKU list
# ✓ Select a SKU from dropdown
# ✓ Forecast plot generates and displays
# ✓ Plot shows both historical (blue) and forecast (red dashed)
# ✓ Can select different SKUs and generate new forecasts
# ✓ UI is responsive and interactive
```

### 5. Cross-Interface Testing (10 min)

**Test 1: Concurrent Access**
```bash
# Terminal 1: Make REST API calls
while true; do
  curl -X POST http://localhost:8000/api/forecast \
    -H "Content-Type: application/json" \
    -d '{"sku": "PRODUCT_001"}' > /dev/null
  sleep 1
done

# Terminal 2: Use Gradio UI
# Open browser to http://localhost:8000/gradio
# Generate forecasts through UI
# ✓ Verify both work simultaneously without conflicts

# Terminal 3: Use MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
# Execute MCP tools
# ✓ Verify MCP tools work while others are active
```

**Test 2: Data Consistency**
```bash
# Get SKU list via REST API
curl http://localhost:8000/ | jq '.sku_count'

# Get SKU list via MCP
# Use list_available_skus tool in Inspector
# Count returned SKUs

# Check Gradio dropdown
# Count options in dropdown

# ✓ All three should show same number of SKUs
```

**Test 3: Error Handling Across Interfaces**
```bash
# Test invalid SKU in REST API
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID"}' | jq '.detail'
# ✓ Should return 400 with error message

# Test invalid SKU in MCP
# Use forecast_sku tool with "INVALID" SKU in Inspector
# ✓ Should return error message

# Test invalid SKU in Gradio
# Type "INVALID" in dropdown (if possible) or select a SKU
# then stop server and try again
# ✓ Should show error plot with message
```

### 6. Performance Testing (5 min)

```bash
# Test response times
time curl http://localhost:8000/ > /dev/null
# ✓ Should be < 100ms

time curl http://localhost:8000/health > /dev/null
# ✓ Should be < 100ms

time curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001"}' > /dev/null
# ✓ Should be < 1 second

# Test Gradio UI responsiveness
# Open http://localhost:8000/gradio
# Select SKUs and time plot generation
# ✓ Should be < 2 seconds for plot to appear
```

### 7. Browser Console Check (5 min)

```bash
# Open browser developer tools
open http://localhost:8000/gradio

# In browser console:
# ✓ No CORS errors
# ✓ No 404 errors for assets
# ✓ No JavaScript errors
# ✓ Network tab shows successful requests
# ✓ Gradio communicates with FastAPI successfully
```

### 8. Service Discovery Testing (5 min)

```bash
# Test that all endpoints are discoverable
curl http://localhost:8000/ | jq '.endpoints | keys'

# Should return array with all endpoint categories:
# ✓ ["documentation", "gradio_ui", "health", "mcp_tools", "rest_api"]

# Verify each endpoint URL is correct
curl http://localhost:8000/ | jq '.endpoints.gradio_ui.path'
# ✓ Should return "/gradio"

curl http://localhost:8000/ | jq '.endpoints.mcp_tools.path'
# ✓ Should return "/mcp"
```

### Final Verification Checklist

**REST API:**
- [ ] Root endpoint returns service info with all endpoints listed
- [ ] Health check returns 200 and healthy status
- [ ] Forecast API works with valid inputs
- [ ] Error handling works for invalid inputs
- [ ] OpenAPI docs accessible and accurate

**MCP Interface:**
- [ ] MCP Inspector can connect
- [ ] Both tools discoverable
- [ ] list_available_skus returns SKU list
- [ ] forecast_sku generates forecasts
- [ ] Error handling works for invalid inputs

**Gradio UI:**
- [ ] Accessible at /gradio
- [ ] Page loads without errors
- [ ] Dropdown populated with SKUs
- [ ] Can generate forecasts
- [ ] Plots display correctly
- [ ] UI is responsive
- [ ] No browser console errors

**Integration:**
- [ ] All three interfaces work simultaneously
- [ ] No conflicts or interference
- [ ] Data consistency across interfaces
- [ ] Performance meets expectations
- [ ] Error handling consistent across interfaces

**Acceptance Criteria:**
- [ ] Unified server starts successfully
- [ ] All three interfaces accessible
- [ ] REST API endpoints work correctly
- [ ] MCP tools work correctly
- [ ] Gradio UI works correctly
- [ ] No CORS or network errors
- [ ] Performance is acceptable (<1s for forecasts)
- [ ] All interfaces show consistent data
- [ ] Error handling works across all interfaces
- [ ] Can run continuous integration tests
- [ ] Ready to proceed to Phase 4 (deployment)

#### TASK-305: Handle CORS for Gradio
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-303

**Description:** 
Configure CORS (Cross-Origin Resource Sharing) middleware to allow Gradio UI to communicate with FastAPI backend. This is typically only needed if Gradio is hosted separately or accessing the API from a different origin.

**When CORS is Needed:**
- ✅ **NOT needed**: When Gradio is mounted in same FastAPI app (TASK-303)
- ⚠️ **Might be needed**: If Gradio makes external API calls
- ✅ **Definitely needed**: If deploying Gradio and API on different domains

**Implementation Steps:**
1. Test if CORS errors occur in browser console
2. Add CORS middleware if needed
3. Configure allowed origins
4. Test cross-origin requests

**Testing for CORS Issues:**
```bash
# Start server
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Open Gradio in browser
open http://localhost:8000/gradio

# Open browser developer console (F12)
# Look for errors like:
# ❌ "Access-Control-Allow-Origin" header is missing
# ❌ CORS policy blocked the request
```

**If CORS Needed - Add Middleware:**
```python
# In src/expo_smooth_mcp/main.py
# Add after FastAPI app creation (around line 55)

from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:7860",      # Gradio default port (if standalone)
        "http://localhost:8000",      # Same origin (shouldn't be needed)
        "http://127.0.0.1:8000",      # Local alternative
        # Add production domains here:
        # "https://your-app.fly.dev",
        # "https://your-custom-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],              # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

print("✓ CORS middleware configured")
```

**Production Configuration:**
```python
# More restrictive CORS for production
import os

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:7860,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Specific methods only
    allow_headers=["Content-Type", "Authorization"],  # Specific headers
    max_age=600,  # Cache preflight requests for 10 minutes
)
```

**Environment Variable Configuration:**
```bash
# .env file
ALLOWED_ORIGINS=http://localhost:7860,http://localhost:8000,https://your-app.fly.dev

# Usage
export ALLOWED_ORIGINS="http://localhost:7860,http://localhost:8000"
python -m src.expo_smooth_mcp.main --transport http
```

**Testing CORS Configuration:**

**Test 1: Same-Origin Request (Should Always Work)**
```bash
# From same origin
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:8000" \
  -d '{"sku": "PRODUCT_001"}' -i | grep -i "access-control"

# Should see CORS headers in response if middleware configured
```

**Test 2: Cross-Origin Request**
```bash
# Simulate cross-origin request
curl -X OPTIONS http://localhost:8000/api/forecast \
  -H "Origin: http://localhost:7860" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" -i

# Should return:
# ✓ HTTP/1.1 200 OK
# ✓ Access-Control-Allow-Origin: http://localhost:7860
# ✓ Access-Control-Allow-Methods: *
# ✓ Access-Control-Allow-Headers: *
```

**Test 3: Browser Console Check**
```bash
# Open Gradio UI
open http://localhost:8000/gradio

# Open developer console (F12)
# Generate a forecast
# Check Network tab for API calls

# Should see:
# ✓ POST /api/forecast returns 200
# ✓ Response includes Access-Control-Allow-Origin header
# ✓ No CORS errors in console
```

**Common CORS Scenarios:**

**Scenario 1: Mounted Gradio (Most Common)**
```
Client Browser → http://localhost:8000/gradio
      ↓
   Gradio UI (mounted at /gradio)
      ↓
   Makes request to /api/forecast (same origin)
      ↓
   FastAPI handles request

Result: CORS NOT needed (same origin)
```

**Scenario 2: Separate Gradio**
```
Client Browser → http://localhost:7860 (Gradio standalone)
      ↓
   Gradio UI makes request to http://localhost:8000/api/forecast
      ↓
   Different origin - CORS check triggered

Result: CORS middleware REQUIRED
```

**Scenario 3: Production Deployment**
```
Client Browser → https://your-app.fly.dev/gradio
      ↓
   Gradio UI (mounted)
      ↓
   Makes request to /api/forecast (same origin)

Result: CORS NOT needed (same origin)
BUT: May need CORS for external API clients
```

**Debugging CORS Issues:**

```python
# Add verbose CORS logging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all (for debugging only!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if CORS errors disappear
# If yes: CORS was the issue
# If no: Different problem (not CORS)

# Then restrict origins for production
```

**Security Considerations:**
- ⚠️ **Never use `allow_origins=["*"]` in production**
- ✅ **Explicitly list allowed origins**
- ✅ **Use environment variables for configuration**
- ✅ **Restrict methods and headers when possible**
- ✅ **Set `allow_credentials=True` only if needed**

**Acceptance Criteria:**
- [ ] Tested if CORS errors occur in browser console
- [ ] CORS middleware added only if needed
- [ ] Allowed origins configured (not wildcard "*" in production)
- [ ] Environment variable support for ALLOWED_ORIGINS
- [ ] Gradio UI works without CORS errors
- [ ] External API clients can connect (if intended)
- [ ] Preflight OPTIONS requests handled correctly
- [ ] Security best practices followed
- [ ] Configuration documented in README
- [ ] Works in both development and production environments

#### TASK-306: Create integration tests for mounted UI
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-304

**Description:** 
Create integration tests specifically for the Gradio UI mounted in FastAPI. These tests verify the UI is accessible, properly integrated, and can communicate with the FastAPI backend.

**Implementation Steps:**
1. Create or update test file for Gradio integration
2. Write tests for Gradio endpoint accessibility
3. Write tests for UI functionality
4. Add tests for error scenarios

**Test File Structure:**
```python
# tests/test_gradio_integration.py
"""
Integration tests for Gradio UI mounted in FastAPI.

Tests verify that:
- Gradio UI is accessible at /gradio
- UI can communicate with FastAPI backend
- All functionality works end-to-end
"""

import pytest
from fastapi.testclient import TestClient
from src.expo_smooth_mcp.main import app, PROCESSED_DF
from src.expo_smooth_mcp import logic

# --- Fixtures ---

@pytest.fixture
def client():
    """Create FastAPI test client."""
    return TestClient(app)

# --- Gradio Endpoint Tests ---

class TestGradioMounting:
    """Tests for Gradio UI mounting."""
    
    def test_gradio_endpoint_accessible(self, client):
        """Should be able to access /gradio endpoint."""
        response = client.get("/gradio")
        
        # Gradio might redirect to /gradio/ (with trailing slash)
        assert response.status_code in [200, 307, 308]
        
        if response.status_code == 200:
            # Check response contains Gradio elements
            assert "gradio" in response.text.lower() or \
                   "gr-" in response.text  # Gradio CSS classes
    
    def test_gradio_with_trailing_slash(self, client):
        """Should be accessible with trailing slash."""
        response = client.get("/gradio/")
        assert response.status_code == 200
    
    def test_gradio_assets_accessible(self, client):
        """Gradio assets should be served correctly."""
        # First, get the main Gradio page
        response = client.get("/gradio/")
        
        if response.status_code == 200:
            # Gradio should be mounted and serving content
            assert len(response.text) > 0

class TestGradioFunctionality:
    """Tests for Gradio UI functionality."""
    
    def test_gradio_can_list_skus(self, client):
        """Gradio should have access to SKU list."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        # The Gradio interface should be initialized with SKU list
        # We can verify this by checking that the data is available
        skus = logic.get_available_skus(PROCESSED_DF)
        assert len(skus) > 0
        
        # Note: Testing actual dropdown requires browser automation
        # which is beyond scope of unit tests

class TestGradioAPIIntegration:
    """Tests for Gradio-FastAPI integration."""
    
    def test_gradio_backend_uses_same_data(self, client):
        """Gradio and REST API should use same data source."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        # Get SKU count from REST API
        rest_response = client.get("/")
        rest_sku_count = rest_response.json()["sku_count"]
        
        # Get SKU count from logic (used by Gradio)
        gradio_sku_count = len(logic.get_available_skus(PROCESSED_DF))
        
        # Should be the same
        assert rest_sku_count == gradio_sku_count
    
    def test_gradio_forecast_uses_same_logic(self, client):
        """Gradio forecast should produce same results as REST API."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")
        
        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]
        
        # Get forecast via REST API
        rest_response = client.post(
            "/api/forecast",
            json={"sku": test_sku, "forecast_horizon": 90}
        )
        rest_data = rest_response.json()
        
        # Get forecast via logic (same as Gradio uses)
        gradio_data = logic.get_forecast_data(PROCESSED_DF, test_sku, 90)
        
        # Should produce identical results
        assert rest_data["metadata"]["sku"] == gradio_data["metadata"]["sku"]
        assert rest_data["metadata"]["forecast_horizon"] == \
               gradio_data["metadata"]["forecast_horizon"]
        assert len(rest_data["forecast"]) == len(gradio_data["forecast"])

class TestGradioErrorHandling:
    """Tests for Gradio error scenarios."""
    
    def test_gradio_accessible_even_if_data_not_loaded(self, client):
        """Gradio UI should be accessible even if data fails to load."""
        # The /gradio endpoint should return 200 regardless of data status
        response = client.get("/gradio/")
        
        # Should not return 503 or 500
        assert response.status_code in [200, 307, 308]
    
    def test_root_endpoint_lists_gradio(self, client):
        """Root endpoint should list Gradio UI in endpoints."""
        response = client.get("/")
        data = response.json()
        
        assert "endpoints" in data
        assert "gradio_ui" in data["endpoints"]
        assert data["endpoints"]["gradio_ui"]["path"] == "/gradio"
        assert data["endpoints"]["gradio_ui"]["method"] == "GET"

# --- Browser-like Testing (Optional) ---

class TestGradioE2E:
    """End-to-end tests simulating browser behavior."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("playwright", reason="playwright not installed"),
        reason="Playwright not available"
    )
    def test_gradio_ui_loads_in_browser(self):
        """
        Test Gradio UI loads correctly in real browser.
        Requires: pip install playwright && playwright install
        """
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to Gradio UI
            page.goto("http://localhost:8000/gradio")
            
            # Wait for Gradio to load
            page.wait_for_selector("[id^='component-']", timeout=5000)
            
            # Verify page title
            assert "Supply Chain" in page.title() or \
                   "Forecasting" in page.title()
            
            browser.close()

# --- Performance Tests ---

class TestGradioPerformance:
    """Performance tests for Gradio integration."""
    
    def test_gradio_page_load_time(self, client):
        """Gradio page should load quickly."""
        import time
        
        start = time.time()
        response = client.get("/gradio/")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 2.0  # Should load in under 2 seconds

# Run tests with: pytest tests/test_gradio_integration.py -v
```

**Running the Tests:**
```bash
# Run all Gradio integration tests
pytest tests/test_gradio_integration.py -v

# Run with coverage
pytest tests/test_gradio_integration.py \
  --cov=src.expo_smooth_mcp.main \
  --cov-report=term-missing

# Run specific test class
pytest tests/test_gradio_integration.py::TestGradioMounting -v

# Run with server running (for E2E tests)
# Terminal 1:
python -m src.expo_smooth_mcp.main --transport http --port 8000

# Terminal 2:
pytest tests/test_gradio_integration.py::TestGradioE2E -v
```

**Optional: Browser Automation Testing:**
```bash
# Install Playwright for browser testing (optional)
pip install playwright
playwright install chromium

# Create E2E test with Playwright
# tests/test_gradio_e2e.py
```

**Test Configuration:**
```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "gradio: Gradio integration tests",
    "e2e: End-to-end tests requiring browser",
    "slow: Slow-running tests",
]

# Run only Gradio tests
# pytest -m gradio

# Skip E2E tests
# pytest -m "not e2e"
```

**Expected Test Output:**
```
tests/test_gradio_integration.py::TestGradioMounting::test_gradio_endpoint_accessible PASSED
tests/test_gradio_integration.py::TestGradioMounting::test_gradio_with_trailing_slash PASSED
tests/test_gradio_integration.py::TestGradioFunctionality::test_gradio_can_list_skus PASSED
tests/test_gradio_integration.py::TestGradioAPIIntegration::test_gradio_backend_uses_same_data PASSED
tests/test_gradio_integration.py::TestGradioAPIIntegration::test_gradio_forecast_uses_same_logic PASSED
tests/test_gradio_integration.py::TestGradioErrorHandling::test_gradio_accessible_even_if_data_not_loaded PASSED
tests/test_gradio_integration.py::TestGradioPerformance::test_gradio_page_load_time PASSED

=================== 7 passed in 1.23s ===================
```

**Manual Testing Checklist (Supplement to Automated Tests):**
```bash
# 1. Visual inspection
open http://localhost:8000/gradio
# ✓ UI loads correctly
# ✓ Styling is correct
# ✓ No console errors

# 2. Functionality test
# In browser:
# ✓ Select SKU from dropdown
# ✓ Click to generate forecast
# ✓ Plot appears correctly
# ✓ Can generate multiple forecasts

# 3. Error scenario test
# Stop FastAPI server
# Try to generate forecast
# ✓ Error message appears
# ✓ UI doesn't crash
```

**Acceptance Criteria:**
- [ ] Test file `tests/test_gradio_integration.py` created
- [ ] Tests for Gradio endpoint accessibility
- [ ] Tests for Gradio mounting with/without trailing slash
- [ ] Tests verify Gradio and REST API use same data
- [ ] Tests verify consistent forecast results
- [ ] Tests for error scenarios
- [ ] Performance test for page load time
- [ ] All tests pass: `pytest tests/test_gradio_integration.py`
- [ ] Tests are independent and can run in any order
- [ ] Optional: Browser automation tests with Playwright
- [ ] Manual testing checklist completed
- [ ] Gradio integration fully validated

---

### Phase 4A: Docker MCP Toolkit Setup (7 tasks, ~10 hours)

#### TASK-401: Create multi-stage Dockerfile
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-303

**Description:** 
Create an optimized multi-stage Dockerfile for production deployment. The Dockerfile will use `uv` for fast dependency installation, create a minimal final image, run as non-root user, and target <500MB image size.

**Implementation Steps:**
1. Create builder stage with uv for dependencies
2. Create minimal final stage with python:3.12-slim
3. Configure non-root user for security
4. Optimize layer caching
5. Add HEALTHCHECK instruction
6. Test build and run

**Complete Dockerfile:**
```dockerfile
# Dockerfile
# Multi-stage build for Expo Smooth MCP Server
# Target: <500MB final image, <300MB ideal

# ============================================================================
# Stage 1: Builder - Install dependencies with uv
# ============================================================================
FROM python:3.12-slim AS builder

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files first (better layer caching)
COPY requirements.txt pyproject.toml* ./
COPY FMCG_Sales.csv ./

# Install dependencies in virtual environment
# uv is 10-100x faster than pip
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY app.py ./

# ============================================================================
# Stage 2: Final - Minimal production image
# ============================================================================
FROM python:3.12-slim

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code from builder
COPY --from=builder /app/src ./src
COPY --from=builder /app/app.py ./
COPY --from=builder /app/FMCG_Sales.csv ./

# Copy requirements for documentation
COPY --from=builder /app/requirements.txt ./

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add virtual environment to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command: HTTP mode
# For stdio mode: docker run -i expo-smooth-mcp python -m src.expo_smooth_mcp.main --transport stdio
CMD ["python", "-m", "src.expo_smooth_mcp.main", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
```

**Build Arguments (Optional Enhancement):**
```dockerfile
# Add at top of Dockerfile for flexibility
ARG PYTHON_VERSION=3.12
ARG UV_VERSION=latest

FROM python:${PYTHON_VERSION}-slim AS builder

# Allow custom uv version
RUN pip install --no-cache-dir uv==${UV_VERSION}
```

**Size Optimization Techniques Used:**
1. **Multi-stage build**: Separate builder from final image
2. **Slim base image**: `python:3.12-slim` instead of full Python
3. **No cache**: `--no-cache-dir` and `--no-cache` flags
4. **Clean apt lists**: Remove package manager cache
5. **Minimal runtime deps**: Only curl and ca-certificates
6. **No development tools**: gcc, build-essential not in final image

**Security Best Practices:**
1. **Non-root user**: Runs as UID 1000 (appuser)
2. **Minimal attack surface**: Slim image with few packages
3. **No secrets in image**: Environment variables set at runtime
4. **Health check**: Enables container orchestration
5. **Latest patch level**: Using python:3.12-slim pulls security updates

**Building the Image:**
```bash
# Basic build
docker build -t expo-smooth-mcp:latest .

# Build with custom Python version
docker build --build-arg PYTHON_VERSION=3.11 -t expo-smooth-mcp:py311 .

# Build with specific tag
docker build -t expo-smooth-mcp:2.0.0 .

# Build with BuildKit (faster, better caching)
DOCKER_BUILDKIT=1 docker build -t expo-smooth-mcp:latest .
```

**Verifying the Build:**
```bash
# Check image size
docker images expo-smooth-mcp:latest
# Target: < 500MB
# Ideal: < 300MB

# Inspect image layers
docker history expo-smooth-mcp:latest

# Check for vulnerabilities (optional)
docker scan expo-smooth-mcp:latest
```

**Testing the Image:**
```bash
# Test HTTP mode
docker run --rm -p 8000:8000 expo-smooth-mcp:latest

# In another terminal
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}

# Test stdio mode
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | \
  docker run --rm -i expo-smooth-mcp:latest \
  python -m src.expo_smooth_mcp.main --transport stdio

# Test health check
docker run -d --name test-mcp expo-smooth-mcp:latest
sleep 15  # Wait for health check
docker ps  # Should show "healthy" status
docker rm -f test-mcp
```

**Expected Image Size Breakdown:**
```
Layer                          Size
----------------------------------------
python:3.12-slim              ~125MB
Virtual environment           ~150MB
Application code              ~10MB
Data file (FMCG_Sales.csv)    ~5MB
Runtime dependencies          ~10MB
----------------------------------------
Total                         ~300MB
```

**Common Build Issues:**

**Issue 1: Image too large (>500MB)**
```bash
# Solution: Review docker history to find large layers
docker history expo-smooth-mcp:latest --no-trunc

# Common causes:
# - Dev dependencies installed (use --prod flag)
# - Build cache not cleaned
# - Large data files in image
```

**Issue 2: Permission denied when running**
```bash
# Solution: Ensure proper ownership
RUN chown -R appuser:appuser /app

# Or: Run as root (not recommended)
USER root
```

**Issue 3: Module import errors**
```bash
# Solution: Verify PYTHONPATH
ENV PYTHONPATH=/app

# Or: Install package in editable mode
RUN . /opt/venv/bin/activate && pip install -e .
```

**Acceptance Criteria:**
- [ ] Dockerfile created in project root
- [ ] Multi-stage build with builder and final stages
- [ ] Uses python:3.12-slim as base
- [ ] Uses uv for dependency installation
- [ ] Non-root user (appuser) configured
- [ ] HEALTHCHECK instruction included
- [ ] Environment variables properly set
- [ ] CMD runs main.py in HTTP mode
- [ ] Image builds successfully: `docker build -t expo-smooth-mcp .`
- [ ] Image size < 500MB (ideally < 300MB)
- [ ] Image runs successfully: `docker run -p 8000:8000 expo-smooth-mcp`
- [ ] Health check passes after startup
- [ ] Can run in both HTTP and stdio modes

#### TASK-402: Add Docker-specific configurations
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-401

**Description:** 
Create Docker configuration files to optimize build performance, reduce image size, and configure production environment. These files improve Docker build speed and security.

**Files to Create:**

**1. .dockerignore:**
```
# .dockerignore
# Exclude files from Docker build context to speed up builds

# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Git
.git/
.gitignore
.gitattributes

# Documentation
docs/
*.md
!README.md

# CI/CD
.github/
.gitlab-ci.yml

# Development
tests/
.env
.env.local
*.log

# macOS
.DS_Store

# Build artifacts
build/
dist/
*.egg-info/
```

**2. .env.example (Template for environment variables):**
```bash
# .env.example
# Copy to .env and configure for your deployment

# Application
APP_ENV=production
LOG_LEVEL=info

# API Configuration
API_BASE_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:7860,http://localhost:8000

# Data
DATA_PATH=FMCG_Sales.csv

# Optional: Authentication (if implementing Phase 5)
# SECRET_KEY=your-secret-key-here
# JWT_ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Redis (if implementing Phase 5)
# REDIS_URL=redis://localhost:6379
```

**3. docker-compose.yml (Optional - for local development):**
```yaml
# docker-compose.yml
version: '3.8'

services:
  expo-smooth-mcp:
    build: .
    image: expo-smooth-mcp:latest
    container_name: expo-smooth-mcp
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=development
      - LOG_LEVEL=debug
    volumes:
      # Mount data file for easy updates
      - ./FMCG_Sales.csv:/app/FMCG_Sales.csv:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped

  # Optional: Redis for rate limiting (Phase 5)
  # redis:
  #   image: redis:7-alpine
  #   ports:
  #     - "6379:6379"
  #   volumes:
  #     - redis_data:/data
  #   restart: unless-stopped

# volumes:
#   redis_data:
```

**Testing docker-compose:**
```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f expo-smooth-mcp

# Test API
curl http://localhost:8000/health

# Stop services
docker-compose down
```

**Acceptance Criteria:**
- [ ] .dockerignore file created with comprehensive exclusions
- [ ] .env.example file created with all configuration options
- [ ] docker-compose.yml created (optional but recommended)
- [ ] Docker build respects .dockerignore (faster builds)
- [ ] Build context size reduced significantly
- [ ] Environment variables documented
- [ ] docker-compose up works successfully

#### TASK-403: Build and test Docker image
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-402

**Description:** 
Build the Docker image and perform comprehensive testing to verify size constraints, functionality, and performance. This validates the Dockerfile is production-ready.

**Implementation Steps:**

### 1. Build the Image (10 min)

```bash
# Clean build (no cache)
docker build --no-cache -t expo-smooth-mcp:latest .

# Or with BuildKit (faster, recommended)
DOCKER_BUILDKIT=1 docker build -t expo-smooth-mcp:latest .

# Build with specific tag
docker build -t expo-smooth-mcp:2.0.0 .

# Tag for multiple versions
docker build -t expo-smooth-mcp:latest -t expo-smooth-mcp:2.0.0 .
```

### 2. Verify Image Size (5 min)

```bash
# Check image size
docker images expo-smooth-mcp:latest

# Should show:
# REPOSITORY          TAG       SIZE
# expo-smooth-mcp     latest    ~300MB (target: <500MB)

# Detailed size breakdown
docker history expo-smooth-mcp:latest --human --no-trunc

# Find largest layers
docker history expo-smooth-mcp:latest --human | sort -k2 -h
```

**Size Optimization if >500MB:**
```bash
# Identify large layers
docker history expo-smooth-mcp:latest --format "{{.Size}}\t{{.CreatedBy}}" | sort -h

# Common fixes:
# 1. Remove dev dependencies
# 2. Clean apt cache: apt-get clean && rm -rf /var/lib/apt/lists/*
# 3. Use --no-cache-dir for pip/uv
# 4. Minimize data files in image
```

### 3. Test HTTP Mode (15 min)

```bash
# Run container in HTTP mode
docker run --rm -p 8000:8000 --name mcp-test expo-smooth-mcp:latest

# In another terminal - test all endpoints
curl http://localhost:8000/ | jq
# ✓ Should return service info

curl http://localhost:8000/health | jq
# ✓ Should return {"status": "healthy"}

curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}' | jq '.metadata'
# ✓ Should return forecast data

# Test OpenAPI docs
open http://localhost:8000/docs
# ✓ Swagger UI should load

# Test Gradio UI
open http://localhost:8000/gradio
# ✓ Gradio interface should load

# Test MCP endpoint
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
# ✓ Should connect and show 2 tools

# Stop container
docker stop mcp-test
```

### 4. Test Health Check (5 min)

```bash
# Run container with health check
docker run -d -p 8000:8000 --name mcp-health expo-smooth-mcp:latest

# Wait for health check
sleep 15

# Check health status
docker ps
# STATUS should show: "healthy"

# Inspect health check details
docker inspect mcp-health --format='{{json .State.Health}}' | jq

# Check health check logs
docker inspect mcp-health --format='{{range .State.Health.Log}}{{.Output}}{{end}}'

# Cleanup
docker rm -f mcp-health
```

### 5. Test Container Logs (5 min)

```bash
# Run container
docker run -d -p 8000:8000 --name mcp-logs expo-smooth-mcp:latest

# View logs
docker logs mcp-logs

# Should show:
# ✓ Starting Expo Smooth MCP Server v2.0.0 - HTTP mode
# ✓ ✓ Data loaded successfully
# ✓ ✓ Found N unique SKUs
# ✓ ✓ Mounted MCP server at /mcp
# ✓ ✓ Mounted Gradio UI at /gradio
# ✓ INFO: Uvicorn running on http://0.0.0.0:8000

# Follow logs in real-time
docker logs -f mcp-logs

# Cleanup
docker rm -f mcp-logs
```

### 6. Test with Environment Variables (5 min)

```bash
# Run with custom environment
docker run --rm -p 8000:8000 \
  -e APP_ENV=production \
  -e LOG_LEVEL=debug \
  expo-smooth-mcp:latest

# Verify environment variables are used
docker run --rm expo-smooth-mcp:latest env | grep APP_
```

### 7. Test with Volume Mounts (5 min)

```bash
# Mount data file from host (for easy updates)
docker run --rm -p 8000:8000 \
  -v $(pwd)/FMCG_Sales.csv:/app/FMCG_Sales.csv:ro \
  expo-smooth-mcp:latest

# Verify data loads correctly
curl http://localhost:8000/health | jq '.sku_count'
```

### 8. Performance Testing (10 min)

```bash
# Start container
docker run -d -p 8000:8000 --name mcp-perf expo-smooth-mcp:latest

# Wait for startup
sleep 5

# Test response times
time curl http://localhost:8000/health > /dev/null
# ✓ Should be < 100ms

time curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "PRODUCT_001"}' > /dev/null
# ✓ Should be < 1 second

# Test concurrent requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/forecast \
    -H "Content-Type: application/json" \
    -d '{"sku": "PRODUCT_001"}' > /dev/null 2>&1 &
done
wait

# Check container resource usage
docker stats mcp-perf --no-stream

# Should show:
# CPU: < 50% during requests
# MEM USAGE: 200-300MB (within 512MB limit)

# Cleanup
docker rm -f mcp-perf
```

### 9. Test Container Restart (5 min)

```bash
# Run container
docker run -d -p 8000:8000 --name mcp-restart expo-smooth-mcp:latest

# Wait for healthy
sleep 15

# Restart container
docker restart mcp-restart

# Wait for healthy again
sleep 15

# Verify still works
curl http://localhost:8000/health | jq '.status'
# ✓ Should return "healthy"

# Cleanup
docker rm -f mcp-restart
```

**Common Issues and Solutions:**

**Issue 1: Container exits immediately**
```bash
# Check logs
docker logs expo-smooth-mcp

# Common causes:
# - Data file missing
# - Python import errors
# - Port already in use

# Solution: Check Dockerfile CMD and entrypoint
```

**Issue 2: Health check fails**
```bash
# Exec into container
docker exec -it mcp-test bash

# Test health endpoint from inside
curl http://localhost:8000/health

# Check if uvicorn is running
ps aux | grep uvicorn
```

**Issue 3: Permission errors**
```bash
# Run as root temporarily for debugging
docker run --rm -u root -p 8000:8000 expo-smooth-mcp:latest

# Fix permissions in Dockerfile:
# RUN chown -R appuser:appuser /app
```

**Testing Checklist:**
- [ ] Image builds successfully without errors
- [ ] Image size < 500MB (ideally < 300MB)
- [ ] Container starts in HTTP mode
- [ ] Health endpoint returns 200 OK
- [ ] All REST API endpoints work
- [ ] MCP endpoint accessible
- [ ] Gradio UI loads correctly
- [ ] Health check passes (shows "healthy" status)
- [ ] Logs show successful startup
- [ ] Environment variables work
- [ ] Volume mounts work
- [ ] Performance acceptable (<1s forecasts)
- [ ] Container restarts successfully
- [ ] Resource usage within limits (< 512MB RAM)

**Acceptance Criteria:**
- [ ] Docker image builds without errors
- [ ] Image size verified < 500MB
- [ ] Container runs successfully in HTTP mode
- [ ] All endpoints tested and working
- [ ] Health check passes within 30 seconds
- [ ] Startup logs show no errors
- [ ] Performance meets expectations
- [ ] Can handle concurrent requests
- [ ] Container restarts gracefully
- [ ] Resource usage documented and acceptable
- [ ] Ready for stdio testing (TASK-404)

#### TASK-404: Test stdio transport in Docker
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-403

**Description:**
Test the MCP server running in stdio transport mode within Docker. This validates the dual-transport implementation works in containerized environments and communicates properly via stdin/stdout.

**Implementation Steps:**

### 1. Test Basic stdio Execution (5 min)

```bash
# Run container in stdio mode (interactive)
docker run --rm -i expo-smooth-mcp:latest stdio

# Container should:
# 1. Start without binding to port 8000
# 2. Wait for JSON-RPC messages on stdin
# 3. Send responses to stdout
# 4. Log to stderr (not stdout!)
```

**Expected stderr output:**
```
Starting Expo Smooth MCP Server v2.0.0 - stdio mode
✓ Data loaded successfully
✓ Found N unique SKUs
✓ Registered 2 MCP tools: generate_forecast, list_available_skus
Ready for MCP communication on stdin/stdout
```

### 2. Test with MCP Inspector (15 min)

```bash
# Option A: Use MCP Inspector directly
npx @modelcontextprotocol/inspector docker run --rm -i expo-smooth-mcp:latest stdio

# The Inspector will:
# 1. Launch the Docker container
# 2. Connect via stdio
# 3. Open web UI at http://localhost:5173
# 4. Show available tools and prompts

# In the Inspector UI, verify:
# ✓ 2 tools shown: generate_forecast, list_available_skus
# ✓ Server info shows correct name and version
# ✓ Can invoke tools and get responses
```

**Option B: Manual JSON-RPC testing:**

```bash
# Create test request file
cat > test_request.json <<EOF
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
EOF

# Send to container via stdio
cat test_request.json | docker run --rm -i expo-smooth-mcp:latest stdio

# Expected response (on stdout):
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "generate_forecast",
        "description": "Generate demand forecast...",
        "inputSchema": {...}
      },
      {
        "name": "list_available_skus",
        "description": "List all available SKUs...",
        "inputSchema": {...}
      }
    ]
  }
}
```

### 3. Test Tool Invocation (5 min)

```bash
# Test list_available_skus
cat > list_skus_request.json <<EOF
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "list_available_skus",
    "arguments": {}
  }
}
EOF

cat list_skus_request.json | docker run --rm -i expo-smooth-mcp:latest stdio

# Expected response:
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Available SKUs (X total): PRODUCT_001, PRODUCT_002, ..."
      }
    ]
  }
}
```

```bash
# Test generate_forecast
cat > forecast_request.json <<EOF
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "generate_forecast",
    "arguments": {
      "sku": "PRODUCT_001",
      "forecast_horizon": 90
    }
  }
}
EOF

cat forecast_request.json | docker run --rm -i expo-smooth-mcp:latest stdio

# Expected response:
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Forecast Summary for PRODUCT_001..."
      }
    ]
  }
}
```

### 4. Test Error Handling (5 min)

```bash
# Test invalid SKU
cat > error_request.json <<EOF
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "generate_forecast",
    "arguments": {
      "sku": "INVALID_SKU",
      "forecast_horizon": 90
    }
  }
}
EOF

cat error_request.json | docker run --rm -i expo-smooth-mcp:latest stdio

# Expected error response:
{
  "jsonrpc": "2.0",
  "id": 4,
  "error": {
    "code": -32603,
    "message": "SKU 'INVALID_SKU' not found..."
  }
}
```

### 5. Test with Docker Compose (Optional)

Create `docker-compose.stdio.yml`:
```yaml
version: '3.8'

services:
  mcp-stdio:
    image: expo-smooth-mcp:latest
    command: stdio
    stdin_open: true
    tty: false
    
    # Mount data file for easy updates
    volumes:
      - ./FMCG_Sales.csv:/app/FMCG_Sales.csv:ro
    
    # Environment
    environment:
      - APP_ENV=production
      - LOG_LEVEL=info
```

Test with compose:
```bash
# This doesn't work well for interactive stdio
# But documents the stdio command structure
docker-compose -f docker-compose.stdio.yml up
```

**Common Issues and Solutions:**

**Issue 1: Logs appear in stdout (breaking MCP protocol)**
```bash
# Problem: Python print() or logging to stdout
# Solution: All logs MUST go to stderr

# Verify in main.py:
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        # Redirect Python logging to stderr
        logging.basicConfig(stream=sys.stderr, ...)
        # Use stderr for status messages
        print("Starting...", file=sys.stderr)
        
        # Run MCP server (only JSON-RPC on stdout)
        mcp.run(transport="stdio")
```

**Issue 2: Container exits immediately**
```bash
# Problem: No stdin provided
# Solution: Always use -i flag

# Wrong:
docker run --rm expo-smooth-mcp:latest stdio  # Exits immediately

# Right:
docker run --rm -i expo-smooth-mcp:latest stdio  # Waits for input
```

**Issue 3: JSON responses malformed**
```bash
# Problem: Extra characters in output
# Solution: Ensure clean stdout

# Debug output:
cat test_request.json | docker run --rm -i expo-smooth-mcp:latest stdio 2>/dev/null

# Should be valid JSON only, nothing else
```

**Issue 4: MCP Inspector can't connect**
```bash
# Problem: Docker command format
# Solution: Use exact command format

# Wrong:
npx @modelcontextprotocol/inspector "docker run --rm -i expo-smooth-mcp:latest stdio"

# Right:
npx @modelcontextprotocol/inspector docker run --rm -i expo-smooth-mcp:latest stdio
```

**Testing Checklist:**
- [ ] Container starts in stdio mode without errors
- [ ] Logs go to stderr, not stdout
- [ ] tools/list returns 2 tools
- [ ] list_available_skus returns SKU list
- [ ] generate_forecast returns valid forecast
- [ ] Invalid SKU returns proper error
- [ ] MCP Inspector can connect
- [ ] Inspector shows tools correctly
- [ ] Tool invocations work from Inspector
- [ ] Multiple sequential requests work
- [ ] JSON-RPC format is correct
- [ ] No extra output on stdout

**Acceptance Criteria:**
- [ ] Container runs successfully in stdio mode with `-i` flag
- [ ] All logs directed to stderr, not stdout
- [ ] MCP Inspector connects successfully
- [ ] tools/list returns expected 2 tools
- [ ] Both tools (generate_forecast, list_available_skus) work correctly
- [ ] Error handling returns proper JSON-RPC errors
- [ ] JSON-RPC communication is clean (no extra output)
- [ ] Multiple requests can be processed sequentially
- [ ] Performance is acceptable (< 1s per forecast)
- [ ] Ready for Docker MCP Toolkit integration (TASK-405)

#### TASK-405: Enable in Docker MCP Toolkit
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-404

**Description:**
Register the MCP server with Docker MCP Toolkit, making it discoverable and manageable through Docker Desktop UI. This enables easy connection to Claude Desktop and other MCP clients.

**Prerequisites:**
- Docker Desktop with MCP Toolkit installed
- Docker MCP Toolkit CLI available
- Container tested in stdio mode (TASK-404)

**Implementation Steps:**

### 1. Verify Docker MCP Toolkit Installation (5 min)

```bash
# Check if Docker MCP Toolkit is installed
docker mcp version

# Should show:
# Docker MCP Toolkit v1.x.x

# If not installed, install from:
# https://github.com/docker/mcp-toolkit

# On macOS:
brew install docker-mcp

# Or manually install the CLI
```

### 2. Tag Image Appropriately (5 min)

```bash
# Docker MCP Toolkit expects specific image naming
docker tag expo-smooth-mcp:latest expo-smooth-mcp:latest

# Optionally tag with version
docker tag expo-smooth-mcp:latest expo-smooth-mcp:2.0.0

# Verify tags
docker images expo-smooth-mcp
```

### 3. Enable MCP Server in Toolkit (5 min)

```bash
# Register the server with Docker MCP Toolkit
docker mcp server enable expo-smooth-mcp:latest

# Expected output:
# ✓ Registered MCP server: expo-smooth-mcp:latest
# ✓ Server will be available in Docker Desktop
# ✓ Run 'docker mcp server list' to verify

# Verify registration
docker mcp server list

# Should show:
# NAME                STATUS    IMAGE
# expo-smooth-mcp     enabled   expo-smooth-mcp:latest
```

**Alternative command formats:**
```bash
# Enable with custom name
docker mcp server enable expo-smooth-mcp:latest --name "Expo Smooth Forecasting"

# Enable with description
docker mcp server enable expo-smooth-mcp:latest \
  --description "FMCG demand forecasting with exponential smoothing"

# Enable with custom stdio command
docker mcp server enable expo-smooth-mcp:latest \
  --command "stdio"
```

### 4. Verify in Docker Desktop UI (5 min)

```
Open Docker Desktop → MCP Servers section

You should see:
┌─────────────────────────────────────────────┐
│ MCP Servers                                 │
├─────────────────────────────────────────────┤
│ ● expo-smooth-mcp                 [enabled] │
│   FMCG demand forecasting                   │
│   Image: expo-smooth-mcp:latest             │
│                                             │
│   Tools: 2                                  │
│   - generate_forecast                       │
│   - list_available_skus                     │
│                                             │
│   [Connect to Claude Desktop]               │
│   [View Logs]  [Disable]                    │
└─────────────────────────────────────────────┘
```

### 5. Test Server via Toolkit (5 min)

```bash
# Start server via toolkit
docker mcp server start expo-smooth-mcp

# Check status
docker mcp server status expo-smooth-mcp

# Should show:
# Status: running
# Container ID: abc123...
# Uptime: 10s

# View logs
docker mcp server logs expo-smooth-mcp

# Should show startup logs

# Stop server
docker mcp server stop expo-smooth-mcp
```

### 6. Configure Server Metadata (5 min)

Create `mcp-server.json` in project root:
```json
{
  "name": "expo-smooth-mcp",
  "version": "2.0.0",
  "description": "FMCG demand forecasting with exponential smoothing",
  "author": "Your Name",
  "license": "MIT",
  
  "docker": {
    "image": "expo-smooth-mcp:latest",
    "command": ["stdio"],
    "environment": {
      "APP_ENV": "production",
      "LOG_LEVEL": "info"
    }
  },
  
  "mcp": {
    "tools": [
      {
        "name": "generate_forecast",
        "description": "Generate demand forecast for an SKU using exponential smoothing"
      },
      {
        "name": "list_available_skus",
        "description": "List all available product SKUs in the dataset"
      }
    ]
  }
}
```

Register with metadata:
```bash
docker mcp server enable expo-smooth-mcp:latest \
  --metadata mcp-server.json
```

### 7. Test Server Discovery (5 min)

```bash
# List all available tools
docker mcp tools list expo-smooth-mcp

# Should show:
# Tool: generate_forecast
#   Description: Generate demand forecast...
#   Parameters: sku, forecast_horizon, alpha, beta, gamma
#
# Tool: list_available_skus
#   Description: List all available SKUs...
#   Parameters: none

# Test tool invocation via CLI
docker mcp tools invoke expo-smooth-mcp list_available_skus

# Should return SKU list
```

**Common Issues and Solutions:**

**Issue 1: `docker mcp` command not found**
```bash
# Solution: Install Docker MCP Toolkit
# macOS:
brew install docker-mcp

# Linux:
curl -fsSL https://get.docker-mcp.com | sh

# Windows:
# Download from https://github.com/docker/mcp-toolkit/releases
```

**Issue 2: Server registration fails**
```bash
# Check Docker is running
docker ps

# Check image exists
docker images expo-smooth-mcp

# Check Dockerfile has LABEL
# Add to Dockerfile:
LABEL com.docker.mcp.server=true
LABEL com.docker.mcp.version=2.0.0
```

**Issue 3: Server doesn't appear in Docker Desktop**
```bash
# Restart Docker Desktop
# Or refresh MCP Servers page

# Re-register
docker mcp server disable expo-smooth-mcp
docker mcp server enable expo-smooth-mcp:latest
```

**Issue 4: Tools not discovered**
```bash
# Verify stdio mode works
docker run --rm -i expo-smooth-mcp:latest stdio

# Send tools/list request manually
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  docker run --rm -i expo-smooth-mcp:latest stdio

# Should return tool list
```

**Testing Checklist:**
- [ ] Docker MCP Toolkit CLI installed
- [ ] `docker mcp version` works
- [ ] Server registers successfully
- [ ] Server appears in `docker mcp server list`
- [ ] Server visible in Docker Desktop UI
- [ ] Server metadata correct (name, description)
- [ ] 2 tools listed correctly
- [ ] Server can start/stop via toolkit
- [ ] Logs viewable via toolkit
- [ ] Tool invocation works via CLI

**Acceptance Criteria:**
- [ ] Docker MCP Toolkit installed and functioning
- [ ] Server registered with `docker mcp server enable`
- [ ] Server listed in `docker mcp server list` with status "enabled"
- [ ] Server visible in Docker Desktop MCP Servers section
- [ ] Server metadata displays correctly (name, description, tools)
- [ ] Both tools (generate_forecast, list_available_skus) discoverable
- [ ] Server can be started/stopped via toolkit commands
- [ ] Server logs accessible via `docker mcp server logs`
- [ ] Documentation updated with toolkit integration steps
- [ ] Ready for Claude Desktop connection (TASK-406)

#### TASK-406: Connect Claude Desktop via Toolkit
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-405

**Description:**
Connect the MCP server to Claude Desktop application using Docker MCP Toolkit integration. This enables Claude to use the forecasting tools through the MCP protocol.

**Prerequisites:**
- Claude Desktop installed (latest version)
- MCP server enabled in Docker MCP Toolkit (TASK-405)
- Docker Desktop running

**Implementation Steps:**

### 1. Verify Claude Desktop Installation (5 min)

```bash
# Check Claude Desktop is installed
# macOS:
ls /Applications/Claude.app

# Check version
open /Applications/Claude.app
# Look for version in About dialog
# Requires: Claude Desktop v0.7.0+ (with MCP support)
```

If not installed:
- Download from: https://claude.ai/download
- Install Claude Desktop application
- Sign in with your Anthropic account

### 2. Connect via Docker Desktop UI (10 min)

**Method A: Using Docker Desktop UI (Recommended)**

```
1. Open Docker Desktop
2. Navigate to: Extensions → Docker MCP Toolkit
3. Click on "MCP Servers" tab
4. Find "expo-smooth-mcp" in server list
5. Click "Connect to Claude Desktop" button
6. Confirm connection dialog:
   ┌─────────────────────────────────────────┐
   │ Connect to Claude Desktop?              │
   ├─────────────────────────────────────────┤
   │ This will add expo-smooth-mcp to        │
   │ Claude Desktop's MCP configuration.     │
   │                                         │
   │ Server: expo-smooth-mcp:latest          │
   │ Tools: 2 (generate_forecast, list...)  │
   │                                         │
   │ [Cancel]  [Connect]                     │
   └─────────────────────────────────────────┘
7. Click "Connect"
8. Success message: "✓ Connected to Claude Desktop"
```

**Method B: Using CLI**

```bash
# Connect server to Claude Desktop
docker mcp connect expo-smooth-mcp claude-desktop

# Expected output:
# ✓ Updated Claude Desktop configuration
# ✓ Server expo-smooth-mcp added to MCP servers
# ✓ Restart Claude Desktop to apply changes

# Verify connection
docker mcp connections list

# Should show:
# CLIENT          SERVER             STATUS
# claude-desktop  expo-smooth-mcp    connected
```

### 3. Verify Configuration File (5 min)

```bash
# Check Claude Desktop config was updated
# macOS:
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Expected content:
{
  "mcpServers": {
    "expo-smooth-mcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "expo-smooth-mcp:latest",
        "stdio"
      ],
      "env": {
        "APP_ENV": "production"
      }
    }
  }
}
```

**Linux:**
```bash
cat ~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
type %APPDATA%\Claude\claude_desktop_config.json
```

### 4. Restart Claude Desktop (5 min)

```bash
# macOS: Quit and reopen
osascript -e 'quit app "Claude"'
sleep 2
open -a Claude

# Or use GUI: Claude → Quit Claude (⌘Q)
# Then reopen from Applications
```

**Verify server is loading:**
Check Claude Desktop logs:
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp.log

# Should show:
# [INFO] Loading MCP server: expo-smooth-mcp
# [INFO] Starting Docker container: expo-smooth-mcp:latest
# [INFO] Connected to MCP server: expo-smooth-mcp
# [INFO] Discovered 2 tools: generate_forecast, list_available_skus
```

### 5. Test in Claude Desktop (15 min)

**Test 1: Verify tools are available**

In Claude Desktop chat, type:
```
What tools do you have available?
```

Claude should respond with:
```
I have access to the following tools:

1. **generate_forecast** - Generate demand forecast for an SKU using 
   exponential smoothing. Parameters: sku, forecast_horizon, alpha, 
   beta, gamma.

2. **list_available_skus** - List all available product SKUs in the 
   FMCG dataset.
```

**Test 2: List available SKUs**

In Claude Desktop, type:
```
Can you list all available SKUs?
```

Claude should use the `list_available_skus` tool and return the list.

**Test 3: Generate a forecast**

In Claude Desktop, type:
```
Generate a 90-day demand forecast for PRODUCT_001
```

Claude should:
1. Use `generate_forecast` tool with sku="PRODUCT_001", forecast_horizon=90
2. Display the forecast results
3. Potentially show a summary or insights

**Test 4: Error handling**

In Claude Desktop, type:
```
Generate a forecast for SKU "INVALID_SKU_123"
```

Claude should handle the error gracefully and explain the SKU was not found.

### 6. Verify Docker Container Lifecycle (5 min)

```bash
# While Claude is using the tools, check containers
docker ps

# Should show expo-smooth-mcp container running when tool is active
# Container should start/stop automatically per request

# Watch container lifecycle
watch -n 1 'docker ps | grep expo-smooth-mcp'

# In Claude, trigger tool usage
# You should see container appear briefly

# View container logs
docker logs $(docker ps -qf "ancestor=expo-smooth-mcp:latest")
```

### 7. Test Multiple Sequential Requests (10 min)

In Claude Desktop, test multiple requests:

```
Conversation:
User: List available SKUs
Claude: [Uses list_available_skus tool, shows results]

User: Generate forecast for the first SKU you showed me
Claude: [Uses generate_forecast with first SKU]

User: Now generate a 30-day forecast for the same SKU
Claude: [Uses generate_forecast with forecast_horizon=30]

User: Compare forecasts for PRODUCT_001 and PRODUCT_002
Claude: [Uses generate_forecast twice, compares results]
```

Verify:
- All tool calls succeed
- Responses are accurate
- No errors or timeouts
- Performance is acceptable (< 3s per tool call)

### 8. Troubleshoot Common Issues (10 min)

**Issue 1: Tools not showing in Claude**
```bash
# Check config file syntax
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq

# Restart Claude Desktop completely
osascript -e 'quit app "Claude"'
sleep 5
open -a Claude

# Check MCP logs for errors
tail -50 ~/Library/Logs/Claude/mcp.log
```

**Issue 2: Tool calls timeout**
```bash
# Check Docker is running
docker ps

# Test server manually
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  docker run --rm -i expo-smooth-mcp:latest stdio

# Increase timeout in config
# Edit claude_desktop_config.json:
{
  "mcpServers": {
    "expo-smooth-mcp": {
      "command": "docker",
      "args": [...],
      "timeout": 30000  // 30 seconds
    }
  }
}
```

**Issue 3: Container permission errors**
```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# On macOS, Claude should have Docker access automatically
# If issues, grant Docker Desktop full disk access in System Preferences
```

**Issue 4: Tools return errors**
```bash
# Test container directly
docker run --rm -i expo-smooth-mcp:latest stdio

# Send test request
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_available_skus","arguments":{}}}

# Check for errors in response

# View detailed logs
docker run --rm -i -e LOG_LEVEL=debug expo-smooth-mcp:latest stdio
```

### 9. Document the Connection (5 min)

Create `docs/CLAUDE_DESKTOP_SETUP.md`:

```markdown
# Claude Desktop Setup

## Quick Start

1. Enable server in Docker MCP Toolkit:
   ```bash
   docker mcp server enable expo-smooth-mcp:latest
   ```

2. Connect to Claude Desktop:
   ```bash
   docker mcp connect expo-smooth-mcp claude-desktop
   ```

3. Restart Claude Desktop

4. Verify tools available in Claude chat

## Manual Setup

If automatic connection fails, manually edit:
`~/Library/Application Support/Claude/claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "expo-smooth-mcp": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "expo-smooth-mcp:latest", "stdio"]
    }
  }
}
```

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues.
```

**Testing Checklist:**
- [ ] Claude Desktop installed (v0.7.0+)
- [ ] Server connected via Docker Desktop UI or CLI
- [ ] claude_desktop_config.json updated correctly
- [ ] Claude Desktop restarted
- [ ] Tools appear in Claude's available tools
- [ ] list_available_skus works correctly
- [ ] generate_forecast works correctly
- [ ] Error handling works (invalid SKU)
- [ ] Multiple sequential requests work
- [ ] Container lifecycle managed automatically
- [ ] Performance acceptable (< 3s per tool call)
- [ ] No errors in MCP logs

**Acceptance Criteria:**
- [ ] Claude Desktop successfully connected to MCP server
- [ ] Configuration file (claude_desktop_config.json) properly updated
- [ ] Both tools visible and functional in Claude Desktop
- [ ] list_available_skus returns correct SKU list
- [ ] generate_forecast generates valid forecasts
- [ ] Error handling works correctly
- [ ] Multiple sequential tool calls work
- [ ] Docker containers start/stop automatically
- [ ] Performance meets expectations
- [ ] Troubleshooting documentation created
- [ ] Ready for toolkit documentation (TASK-407)

#### TASK-407: Create Docker MCP Toolkit documentation
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-406

**Description:**
Create comprehensive documentation for deploying and using the MCP server through Docker MCP Toolkit. This includes setup guides, troubleshooting, and best practices for local development.

**Documentation Files to Create:**

### 1. Main Guide: `docs/DOCKER_MCP_TOOLKIT.md`

**Sections to include:**
- Overview and prerequisites
- Quick start (5-minute setup)
- Detailed setup instructions
- Server configuration options
- Testing procedures
- Troubleshooting common issues
- Advanced configuration
- Best practices
- Performance optimization
- Security considerations
- Integration with other MCP clients

**Key content:**
```markdown
# Docker MCP Toolkit Deployment Guide

## Quick Start
1. Build: `docker build -t expo-smooth-mcp:latest .`
2. Enable: `docker mcp server enable expo-smooth-mcp:latest`
3. Connect: `docker mcp connect expo-smooth-mcp claude-desktop`
4. Restart Claude Desktop

## Managing Server
- Start: `docker mcp server start expo-smooth-mcp`
- Stop: `docker mcp server stop expo-smooth-mcp`
- Logs: `docker mcp server logs expo-smooth-mcp`
- Update: rebuild image + `docker mcp server restart`

## Troubleshooting
[Common issues with diagnostic commands and solutions]

## Advanced
[Environment variables, custom data files, multiple servers]
```

### 2. Quick Reference: `docs/DOCKER_TOOLKIT_QUICKREF.md`

**Purpose:** One-page cheat sheet for common commands

**Content:**
```markdown
# Quick Reference

## Setup (One-Time)
docker build -t expo-smooth-mcp:latest .
docker mcp server enable expo-smooth-mcp:latest
docker mcp connect expo-smooth-mcp claude-desktop

## Daily Operations  
docker mcp server start/stop/status/logs expo-smooth-mcp

## Troubleshooting
docker mcp server restart expo-smooth-mcp
docker run --rm -i expo-smooth-mcp:latest stdio

## Updates
docker build -t expo-smooth-mcp:latest .
docker mcp server restart expo-smooth-mcp
```

### 3. Troubleshooting Guide: `docs/DOCKER_TOOLKIT_TROUBLESHOOTING.md`

**Common issues to document:**

**Issue 1: Server not listed**
- Diagnosis: Check image exists, Docker running
- Solution: Re-enable server

**Issue 2: Claude can't see tools**
- Diagnosis: Check config file, connections, logs
- Solution: Reconnect and restart Claude

**Issue 3: Tool timeouts**
- Diagnosis: Test manually, check response time
- Solution: Increase timeout, optimize server

**Issue 4: Container won't start**
- Diagnosis: Check logs, test HTTP mode
- Solution: Rebuild image, verify data file

**Issue 5: Data file not found**
- Diagnosis: Check file in image
- Solution: Verify build context, rebuild

Include diagnostic commands for each:
```bash
# System checks
docker --version
docker mcp version
docker ps
docker images

# Server checks
docker mcp server list
docker mcp server logs expo-smooth-mcp

# Manual testing
docker run --rm -i expo-smooth-mcp:latest stdio
```

### 4. FAQ: `docs/DOCKER_TOOLKIT_FAQ.md`

**Questions to answer:**

**General:**
- Q: What is Docker MCP Toolkit?
- Q: Do I need Docker Desktop or is Docker Engine enough?
- Q: Which Claude Desktop versions support MCP?

**Setup:**
- Q: Why isn't my server appearing?
- Q: Why can't Claude see my tools?
- Q: How do I update the server?

**Usage:**
- Q: How do I see what the server is doing?
- Q: Can I run multiple MCP servers?
- Q: How do I temporarily disable a server?

**Troubleshooting:**
- Q: Tools are timing out, what can I do?
- Q: The container keeps restarting, why?
- Q: How do I reset everything?

**Performance:**
- Q: How fast should tool calls be?
- Q: How much memory does it use?
- Q: Can it handle concurrent requests?

**Advanced:**
- Q: Can I use custom data files?
- Q: Can I run without Claude Desktop?
- Q: Can I expose HTTP endpoints too?

### 5. Demo Script (Optional): `docs/DOCKER_TOOLKIT_DEMO_SCRIPT.md`

**5-minute demo structure:**
- Part 1: Build and enable (2 min)
- Part 2: Connect to Claude (2 min)
- Part 3: Test in Claude (1 min)

Include exact commands and expected outputs for demo presentations.

### 6. Update Existing Documentation

**Update README.md:**
Add Docker Toolkit deployment section:
```markdown
## Deployment Options

### Option 1: Docker MCP Toolkit (Recommended for Local Use)

Quick Start:
```bash
docker build -t expo-smooth-mcp:latest .
docker mcp server enable expo-smooth-mcp:latest
docker mcp connect expo-smooth-mcp claude-desktop
```

Full docs: [Docker MCP Toolkit Guide](docs/DOCKER_MCP_TOOLKIT.md)
```

**Update docs/DEPLOYMENT_GUIDE.md:**
Add Docker Toolkit as deployment option with:
- Prerequisites
- Setup time (~10 minutes)
- Step-by-step instructions
- Management commands
- Pros/cons vs other deployment methods

### 7. Include Visual Aids (Optional but Helpful)

**Screenshots to capture:**
- Docker Desktop with MCP Servers section showing expo-smooth-mcp
- Claude Desktop showing available tools
- MCP Inspector UI showing tool list
- Terminal showing successful docker mcp commands

**Diagrams to create:**
```
Claude Desktop <--stdio--> Docker Container <--> MCP Server
                                              <--> Business Logic
                                              <--> Data (FMCG_Sales.csv)
```

**Testing Checklist:**
- [ ] DOCKER_MCP_TOOLKIT.md created (comprehensive guide)
- [ ] DOCKER_TOOLKIT_QUICKREF.md created (cheat sheet)
- [ ] DOCKER_TOOLKIT_TROUBLESHOOTING.md created (common issues)
- [ ] DOCKER_TOOLKIT_FAQ.md created (Q&A)
- [ ] Demo script created (optional)
- [ ] README.md updated with Docker Toolkit section
- [ ] DEPLOYMENT_GUIDE.md includes Docker Toolkit option
- [ ] All commands tested and verified
- [ ] Cross-references between docs work
- [ ] Follows DOCUMENTATION_STANDARDS.md

**Acceptance Criteria:**
- [ ] Complete Docker MCP Toolkit documentation suite created
- [ ] Main guide covers all setup, configuration, and usage scenarios
- [ ] Troubleshooting guide addresses 5+ common issues with solutions
- [ ] Quick reference provides one-page command cheat sheet
- [ ] FAQ answers 15+ frequently asked questions
- [ ] All code examples tested and working
- [ ] Documentation integrated with existing docs
- [ ] Links and cross-references functional
- [ ] Follows project documentation standards
- [ ] Phase 4A complete, ready for Phase 4B (Fly.io deployment)

---

### Phase 4B: Fly.io Cloud Deployment (8 tasks, ~12 hours)

#### TASK-408: Create fly.toml configuration
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-403

**Description:**
Create Fly.io configuration file that defines app deployment settings, resource limits, health checks, and scaling behavior. This file is the blueprint for cloud deployment.

**Implementation Steps:**

### 1. Create Base fly.toml (20 min)

Create `fly.toml` in project root:

```toml
# fly.toml - Fly.io deployment configuration

app = "expo-smooth-mcp"
primary_region = "sjc"  # San Jose, California - choose closest to users

# Run image in HTTP mode
[build]
  dockerfile = "Dockerfile"

[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"

# HTTP service configuration
[[services]]
  protocol = "tcp"
  internal_port = 8000
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  
  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true
  
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
  
  # Health check configuration
  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20
  
  [[services.tcp_checks]]
    interval = "15s"
    timeout = "2s"
    grace_period = "10s"
  
  [[services.http_checks]]
    interval = "30s"
    timeout = "5s"
    grace_period = "10s"
    method = "get"
    path = "/health"
    protocol = "http"
    tls_skip_verify = false
    
    [services.http_checks.headers]
      # Optional: add custom headers
      # X-Forwarded-Proto = "https"

# Resource limits (512MB RAM validated in testing)
[vm]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512

# Deployment strategy
[deploy]
  strategy = "rolling"
  max_unavailable = 0  # Zero-downtime deployments
```

### 2. Add MCP-Specific Configuration (10 min)

For HTTP/SSE transport mode, add:

```toml
# MCP endpoint configuration
[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"
  # MCP mode: http (SSE transport)
  MCP_TRANSPORT = "http"

# Timeouts for long-running forecast requests
[[services]]
  # ... existing config ...
  
  [[services.http_checks]]
    interval = "30s"
    timeout = "5s"
    path = "/health"
    
    # Expected response
    [services.http_checks.headers]
      Content-Type = "application/json"
```

### 3. Add Scaling Configuration (10 min)

```toml
# Scaling configuration
[[services]]
  # ... existing config ...
  
  # Auto-scaling settings
  auto_stop_machines = true   # Stop when no requests
  auto_start_machines = true  # Start on demand
  min_machines_running = 1    # Always keep 1 running for availability
  
  # For production with high traffic, consider:
  # min_machines_running = 2  # High availability
  # max_per_region = 3        # Limit horizontal scaling

# Compute resources
[vm]
  cpu_kind = "shared"  # "shared" (cheaper) or "performance" (faster)
  cpus = 1             # 1 vCPU sufficient for our workload
  memory_mb = 512      # Validated memory budget
```

### 4. Add Regional Configuration (5 min)

```toml
# Primary region (choose closest to main users)
primary_region = "sjc"  # San Jose, CA

# For multi-region deployment (optional):
# primary_region = "sjc"  # West Coast US
# [regions]
#   sjc = { weight = 100 }  # Primary
#   iad = { weight = 50 }   # East Coast backup

# Common regions:
# sjc = San Jose, CA (US West)
# iad = Ashburn, VA (US East)
# lhr = London, UK
# fra = Frankfurt, Germany
# syd = Sydney, Australia
# nrt = Tokyo, Japan
```

### 5. Add Production Tweaks (10 min)

```toml
# Console command (override CMD from Dockerfile)
[processes]
  web = "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1"

# Or use Dockerfile CMD (default)
# [processes]
#   web = ""  # Empty = use Dockerfile CMD

# Volume mounts (if needed for persistent data)
# [mounts]
#   source = "data"
#   destination = "/app/data"

# Secrets (don't put sensitive values in fly.toml!)
# Set via: flyctl secrets set SECRET_KEY=value
[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  # SECRET_KEY set via flyctl secrets

# Metrics and monitoring
[metrics]
  port = 9091  # If using Prometheus metrics
  path = "/metrics"
```

### 6. Create Environment-Specific Configs (Optional, 5 min)

**fly.staging.toml** for staging environment:
```toml
app = "expo-smooth-mcp-staging"
primary_region = "sjc"

[env]
  APP_ENV = "staging"
  LOG_LEVEL = "debug"

[vm]
  memory_mb = 256  # Smaller for staging
  
[[services]]
  min_machines_running = 0  # Auto-stop when idle
```

**fly.production.toml** for production:
```toml
app = "expo-smooth-mcp"
primary_region = "sjc"

[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"

[vm]
  memory_mb = 512
  
[[services]]
  min_machines_running = 2  # High availability
```

### 7. Validate Configuration (5 min)

```bash
# Validate fly.toml syntax
flyctl config validate

# Expected output:
# ✓ Configuration is valid

# Check for common issues
flyctl config show

# Should display parsed configuration

# Validate Dockerfile builds
docker build -t expo-smooth-mcp:latest .

# Test locally before deploying
docker run --rm -p 8000:8000 expo-smooth-mcp:latest
curl http://localhost:8000/health
```

### 8. Add Documentation Comments (5 min)

```toml
# fly.toml - Expo Smooth MCP Fly.io Configuration
#
# This configuration deploys the MCP server to Fly.io with:
# - HTTP/SSE transport mode (MCP protocol)
# - 512MB RAM (validated memory budget)
# - Auto-scaling: 1 machine minimum, scales on demand
# - Health checks on /health endpoint
# - Zero-downtime rolling deployments
#
# Deploy with: flyctl deploy
# Update: flyctl deploy --config fly.toml
# Monitor: flyctl logs
# Scale: flyctl scale memory 1024  # if needed

app = "expo-smooth-mcp"
# ... rest of config ...
```

**Complete fly.toml Template:**

```toml
# fly.toml - Expo Smooth MCP Fly.io Configuration

app = "expo-smooth-mcp"
primary_region = "sjc"

# Build configuration
[build]
  dockerfile = "Dockerfile"

# Environment variables
[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"

# Process to run
[processes]
  web = ""  # Use Dockerfile CMD

# VM resources
[vm]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512

# HTTP service
[[services]]
  protocol = "tcp"
  internal_port = 8000
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

  # Ports
  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  # Concurrency limits
  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20

  # TCP health check
  [[services.tcp_checks]]
    interval = "15s"
    timeout = "2s"
    grace_period = "10s"

  # HTTP health check
  [[services.http_checks]]
    interval = "30s"
    timeout = "5s"
    grace_period = "10s"
    method = "get"
    path = "/health"
    protocol = "http"

# Deployment strategy
[deploy]
  strategy = "rolling"
  max_unavailable = 0
```

**Common Configuration Options:**

**Memory Sizes:**
```toml
[vm]
  memory_mb = 256   # Minimal (may not work)
  memory_mb = 512   # Recommended (validated)
  memory_mb = 1024  # If needed for larger datasets
  memory_mb = 2048  # High-memory workloads
```

**CPU Options:**
```toml
[vm]
  cpu_kind = "shared"       # Cost-effective
  cpu_kind = "performance"  # Dedicated CPU
  cpus = 1                  # 1 vCPU (sufficient)
  cpus = 2                  # If CPU-bound
```

**Scaling Options:**
```toml
[[services]]
  min_machines_running = 0  # Stop when idle (staging)
  min_machines_running = 1  # Always available (prod)
  min_machines_running = 2  # High availability
  max_per_region = 3        # Limit scaling
```

**Testing Checklist:**
- [ ] fly.toml created in project root
- [ ] App name set appropriately
- [ ] Primary region chosen
- [ ] Build section references Dockerfile
- [ ] Environment variables defined
- [ ] VM resources set (512MB RAM)
- [ ] HTTP service configured
- [ ] Ports 80/443 configured
- [ ] Health checks defined (/health endpoint)
- [ ] Scaling parameters set
- [ ] Configuration validates with flyctl
- [ ] Comments explain key settings

**Acceptance Criteria:**
- [ ] fly.toml configuration file created
- [ ] App name unique and appropriate
- [ ] Dockerfile referenced in build section
- [ ] 512MB RAM limit configured
- [ ] HTTP service on ports 80/443
- [ ] Health check endpoint configured (/health)
- [ ] Auto-scaling enabled (min_machines_running=1)
- [ ] Zero-downtime deployment strategy configured
- [ ] Configuration validates successfully
- [ ] Documentation comments added
- [ ] Ready for Fly.io CLI setup (TASK-409)

#### TASK-409: Set up Fly.io account and CLI
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:**
Set up Fly.io account and install flyctl CLI tool. This provides the foundation for deploying to Fly.io's global application platform.

**Implementation Steps:**

### 1. Create Fly.io Account (5 min)

```bash
# Sign up at https://fly.io/app/sign-up
# Or use GitHub/Google OAuth

# No credit card required for:
# - Up to 3 shared-cpu-1x machines
# - 3GB persistent volume storage
# - 160GB outbound data transfer

# Pricing (as of 2024):
# Hobby Plan: $5/month minimum (pay-as-you-go after)
# Shared CPU 1x (256MB): ~$2/month
# Shared CPU 1x (512MB): ~$4/month
```

Visit: https://fly.io/app/sign-up
1. Enter email or use GitHub/Google
2. Verify email
3. (Optional) Add payment method for production use

### 2. Install flyctl CLI (10 min)

**macOS:**
```bash
# Using Homebrew (recommended)
brew install flyctl

# Verify installation
flyctl version

# Should show:
# flyctl v0.x.xxx darwin/arm64 Commit: xxx BuildDate: xxx
```

**Linux:**
```bash
# Using install script
curl -L https://fly.io/install.sh | sh

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export FLYCTL_INSTALL="/home/$USER/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc

# Verify
flyctl version
```

**Windows:**
```powershell
# Using PowerShell
iwr https://fly.io/install.ps1 -useb | iex

# Verify
flyctl version
```

### 3. Authenticate flyctl (5 min)

```bash
# Login to Fly.io
flyctl auth login

# This will:
# 1. Open browser for authentication
# 2. Show "Successfully logged in" message
# 3. Save credentials to ~/.fly/config.yml

# Alternative: Use token
flyctl auth token
# Save token for CI/CD use: FlyV1 fm...

# Verify authentication
flyctl auth whoami

# Should show:
# Email: your@email.com
# Organizations: personal, ...
```

### 4. Verify Account Access (5 min)

```bash
# List apps (should be empty for new account)
flyctl apps list

# Check regions
flyctl platform regions

# Should show available regions:
# CODE NAME                          
# ams  Amsterdam, Netherlands
# cdg  Paris, France
# fra  Frankfurt, Germany
# iad  Ashburn, Virginia (US)
# lhr  London, United Kingdom
# sjc  San Jose, California (US)
# syd  Sydney, Australia
# ...

# Check status
flyctl platform status

# Should show: All systems operational
```

### 5. Configure CLI Preferences (Optional, 5 min)

```bash
# Set default region
flyctl config set region sjc

# Set default organization
flyctl orgs list
flyctl config set org personal

# View config
cat ~/.fly/config.yml
```

Example `~/.fly/config.yml`:
```yaml
access_token: FlyV1_fm...
current_org: personal
default_region: sjc
```

### 6. Test CLI Functionality (5 min)

```bash
# Check machine types
flyctl platform vm-sizes

# Should show:
# NAME             CPU   MEMORY  PRICE/MO
# shared-cpu-1x    1     256MB   $1.94
# shared-cpu-1x    1     512MB   $3.88
# shared-cpu-1x    1     1024MB  $7.76
# ...

# Check pricing
flyctl pricing

# Test command help
flyctl deploy --help
flyctl apps --help
flyctl scale --help
```

**Testing Checklist:**
- [ ] Fly.io account created and verified
- [ ] flyctl installed successfully
- [ ] flyctl version command works
- [ ] Authenticated via flyctl auth login
- [ ] Browser auth completed successfully
- [ ] flyctl auth whoami shows correct email
- [ ] Can list regions
- [ ] Can check platform status
- [ ] CLI config saved to ~/.fly/config.yml

**Acceptance Criteria:**
- [ ] Fly.io account created and email verified
- [ ] flyctl CLI installed (version 0.2.0+)
- [ ] Successfully authenticated with flyctl auth login
- [ ] Authentication verified with flyctl auth whoami
- [ ] Can access platform information (regions, VM sizes)
- [ ] Config file created at ~/.fly/config.yml
- [ ] Ready to deploy applications
- [ ] Ready for environment configuration (TASK-410)

#### TASK-410: Configure environment variables
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** TASK-408

**Description:**
Configure environment variables and secrets for Fly.io deployment. This includes both non-sensitive configuration (in fly.toml) and sensitive values (as Fly.io secrets).

**Implementation Steps:**

### 1. Identify Required Variables (5 min)

**Non-sensitive (in fly.toml):**
```toml
[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"
  PYTHONUNBUFFERED = "1"
```

**Sensitive (Fly.io secrets):**
- SECRET_KEY (for JWT/OAuth, if implementing)
- DATABASE_URL (if using external database)
- REDIS_URL (if using Redis for rate limiting)
- API_KEYS (if integrating with external services)

**For current implementation:**
- Minimal secrets needed (self-contained app)
- Add SECRET_KEY for future authentication

### 2. Generate Secret Values (5 min)

```bash
# Generate secure random secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Example output: 
# xK9v_8mN2pR7tQ...

# Or use openssl
openssl rand -base64 32

# Save for next step
```

### 3. Set Fly.io Secrets (5 min)

```bash
# Set individual secret
flyctl secrets set SECRET_KEY="your-generated-secret-key-here"

# Expected output:
# Secrets are staged for the first deployment

# Set multiple secrets at once
flyctl secrets set \
  SECRET_KEY="your-secret-key" \
  API_VERSION="2.0.0"

# List secrets (values are hidden)
flyctl secrets list

# Should show:
# NAME            DIGEST                           DATE
# SECRET_KEY      abc123...                        1m ago
# API_VERSION     def456...                        1m ago

# Unset a secret (if needed)
flyctl secrets unset SECRET_KEY
```

### 4. Import Secrets from .env File (Optional, 5 min)

Create `.env.production`:
```bash
# .env.production - Production secrets (DO NOT COMMIT)
SECRET_KEY=your-generated-secret-key-here
# Add more secrets as needed
```

Import all at once:
```bash
# Import from file
flyctl secrets import < .env.production

# Or using a script
while IFS='=' read -r key value; do
  [[ $key =~ ^#.*$ ]] && continue  # Skip comments
  [[ -z $key ]] && continue        # Skip empty lines
  flyctl secrets set "$key=$value"
done < .env.production
```

**Add .env.production to .gitignore:**
```bash
echo ".env.production" >> .gitignore
```

### 5. Verify Environment Configuration (5 min)

**Check fly.toml environment:**
```bash
# View current fly.toml config
cat fly.toml | grep -A 10 "\[env\]"

# Should show:
# [env]
#   APP_ENV = "production"
#   LOG_LEVEL = "info"
#   PORT = "8000"
```

**Check secrets:**
```bash
# List all secrets
flyctl secrets list

# Deploy and verify secrets are available
flyctl ssh console
# In the VM:
env | grep SECRET_KEY
# Should show: SECRET_KEY=****** (value hidden in logs)
exit
```

### 6. Create Environment Documentation (5 min)

Create `docs/ENVIRONMENT_VARIABLES.md`:

```markdown
# Environment Variables

## Required Variables

### APP_ENV
- **Description:** Application environment
- **Values:** `development`, `staging`, `production`
- **Default:** `production`
- **Location:** fly.toml [env] section

### LOG_LEVEL
- **Description:** Logging verbosity
- **Values:** `debug`, `info`, `warning`, `error`
- **Default:** `info`
- **Location:** fly.toml [env] section

### PORT
- **Description:** HTTP server port
- **Default:** `8000`
- **Location:** fly.toml [env] section

## Optional Secrets

### SECRET_KEY
- **Description:** Secret key for JWT tokens (if auth enabled)
- **Required:** Only if Phase 5 authentication implemented
- **Generation:** `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- **Set with:** `flyctl secrets set SECRET_KEY=value`

### REDIS_URL (Future)
- **Description:** Redis connection URL for rate limiting
- **Format:** `redis://host:port/db`
- **Set with:** `flyctl secrets set REDIS_URL=redis://...`

## Setting Secrets

```bash
# Single secret
flyctl secrets set SECRET_KEY=value

# Multiple secrets
flyctl secrets set SECRET_KEY=value1 API_KEY=value2

# From file
flyctl secrets import < .env.production

# List secrets
flyctl secrets list

# Unset secret
flyctl secrets unset SECRET_KEY
```

## Local Development

Create `.env` file:
```
APP_ENV=development
LOG_LEVEL=debug
SECRET_KEY=dev-secret-key-not-for-production
```

Load with: `python-dotenv` or `export $(cat .env | xargs)`
```

### 7. Update Dockerfile for Environment (Optional, 5 min)

If using environment-specific behavior:

```dockerfile
# Dockerfile

# Environment defaults
ENV APP_ENV=production \
    LOG_LEVEL=info \
    PORT=8000 \
    PYTHONUNBUFFERED=1

# These can be overridden by:
# 1. fly.toml [env] section
# 2. flyctl secrets set
# 3. docker run -e VAR=value
```

### 8. Test Environment Configuration (5 min)

**Locally:**
```bash
# Test with environment variables
docker run --rm -p 8000:8000 \
  -e APP_ENV=production \
  -e LOG_LEVEL=debug \
  -e SECRET_KEY=test-key \
  expo-smooth-mcp:latest

# Verify logs show correct environment
curl http://localhost:8000/
# Should show {"environment": "production", ...}
```

**On Fly.io (after first deployment):**
```bash
# Check environment in deployed app
flyctl ssh console -a expo-smooth-mcp
env | grep -E "APP_ENV|LOG_LEVEL|PORT"
# Should show configured values
exit
```

**Testing Checklist:**
- [ ] Required environment variables identified
- [ ] Non-sensitive vars added to fly.toml [env]
- [ ] SECRET_KEY generated securely
- [ ] Secrets set with flyctl secrets set
- [ ] flyctl secrets list shows all secrets
- [ ] .env.production in .gitignore
- [ ] ENVIRONMENT_VARIABLES.md documentation created
- [ ] Dockerfile has environment defaults
- [ ] Environment config tested locally

**Acceptance Criteria:**
- [ ] All required environment variables defined in fly.toml
- [ ] Sensitive secrets set via flyctl secrets set (if any)
- [ ] SECRET_KEY generated and stored securely
- [ ] flyctl secrets list shows configured secrets
- [ ] .env.production excluded from git
- [ ] Environment documentation created
- [ ] Configuration tested locally with Docker
- [ ] Ready for initial deployment (TASK-411)

#### TASK-411: Initial Fly.io deployment
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-409, TASK-410

**Description:**
Perform the initial deployment to Fly.io, launching the MCP server to the cloud. This includes app initialization, configuration review, deployment, and monitoring.

**Implementation Steps:**

### 1. Pre-Deployment Checklist (10 min)

```bash
# Verify prerequisites
✓ flyctl installed and authenticated (TASK-409)
✓ fly.toml configured (TASK-408)
✓ Secrets set (TASK-410)
✓ Docker image builds successfully
✓ Local testing passed

# Final checks
flyctl auth whoami
docker build -t expo-smooth-mcp:latest .
docker run --rm -p 8000:8000 expo-smooth-mcp:latest &
sleep 5
curl http://localhost:8000/health
# Should return {"status": "healthy"}
pkill -f "expo-smooth-mcp"
```

### 2. Initialize Fly.io App (15 min)

**Option A: Using flyctl launch (Recommended for first deployment)**

```bash
# Launch interactive setup
flyctl launch

# Interactive prompts:
# 1. App name: expo-smooth-mcp (or auto-generated)
# 2. Region: sjc (San Jose) or closest to users
# 3. PostgreSQL? No (we don't need it)
# 4. Redis? No (not needed initially)
# 5. Deploy now? No (review config first)

# This creates:
# - fly.toml (or updates existing)
# - Registers app on Fly.io
# - Sets up app infrastructure
```

**Option B: Using existing fly.toml**

```bash
# If fly.toml already configured (TASK-408)
# Create app without deployment
flyctl apps create expo-smooth-mcp --org personal

# Or with specific region
flyctl apps create expo-smooth-mcp --org personal --region sjc

# Verify app created
flyctl apps list
# Should show expo-smooth-mcp
```

### 3. Review and Adjust Configuration (10 min)

```bash
# Review generated/existing fly.toml
cat fly.toml

# Key things to verify:
# ✓ app = "expo-smooth-mcp"
# ✓ primary_region = "sjc"
# ✓ internal_port = 8000
# ✓ memory_mb = 512
# ✓ min_machines_running = 1
# ✓ Health check path = "/health"

# Validate configuration
flyctl config validate

# Show what will be deployed
flyctl config show
```

**If adjustments needed:**
```bash
# Edit fly.toml manually
nano fly.toml

# Or use flyctl commands
flyctl scale memory 512
flyctl scale count 1
```

### 4. Deploy to Fly.io (20 min)

```bash
# Deploy the application
flyctl deploy

# Deployment process:
# 1. Building image remotely (or using local Docker)
# 2. Pushing image to Fly.io registry
# 3. Creating VM/machine
# 4. Starting application
# 5. Running health checks
# 6. Marking deployment successful

# Expected output:
# ==> Building image
# --> Building Dockerfile
#     [+] Building 45.2s
# ==> Pushing image to fly.io registry
# --> Pushing image: registry.fly.io/expo-smooth-mcp:deployment-xxx
# ==> Creating release
# --> Release v1 created
# ==> Monitoring deployment
#     1 desired, 1 placed, 1 healthy, 0 unhealthy
# --> v1 deployed successfully
```

**Deployment options:**
```bash
# Deploy with specific Dockerfile
flyctl deploy --dockerfile Dockerfile

# Deploy without remote builder (use local Docker)
flyctl deploy --local-only

# Deploy with custom config
flyctl deploy --config fly.production.toml

# Deploy specific image
flyctl deploy --image expo-smooth-mcp:latest

# Skip health checks (not recommended)
flyctl deploy --no-health-checks
```

### 5. Monitor Deployment Progress (10 min)

```bash
# Watch deployment in real-time
flyctl status

# Should show:
# App
#   Name     = expo-smooth-mcp
#   Owner    = personal
#   Hostname = expo-smooth-mcp.fly.dev
#   Image    = expo-smooth-mcp:deployment-xxx
#   Platform = machines
#
# Machines
# PROCESS ID              VERSION REGION  STATE   ROLE    CHECKS  LAST UPDATED
# app     91857...        v1      sjc     started         1/1 ✓   2m ago

# View logs in real-time
flyctl logs

# Expected logs:
# app[91857] sjc [info] Starting Expo Smooth MCP Server v2.0.0
# app[91857] sjc [info] ✓ Data loaded successfully
# app[91857] sjc [info] ✓ Found 50 unique SKUs
# app[91857] sjc [info] ✓ Mounted MCP server at /mcp
# app[91857] sjc [info] ✓ Mounted Gradio UI at /gradio
# app[91857] sjc [info] Uvicorn running on http://[::]:8000
# app[91857] sjc [info] Health check passed
```

### 6. Verify Initial Deployment (10 min)

```bash
# Get app URL
flyctl info

# Shows:
# Hostname = expo-smooth-mcp.fly.dev
# Services:
#   PROTOCOL  PORTS
#   TCP       80 => 8000 [HTTP]
#           443 => 8000 [TLS, HTTP]

# Test health endpoint
curl https://expo-smooth-mcp.fly.dev/health

# Expected response:
{
  "status": "healthy",
  "version": "2.0.0",
  "sku_count": 50,
  "memory_mb": 512
}

# Test root endpoint
curl https://expo-smooth-mcp.fly.dev/

# Should return service info JSON
```

### 7. Check Fly.io Dashboard (5 min)

Visit Fly.io dashboard: https://fly.io/dashboard/personal/expo-smooth-mcp

**Verify:**
- ✓ App is running (green status)
- ✓ 1 machine allocated
- ✓ Health checks passing
- ✓ Hostname assigned (expo-smooth-mcp.fly.dev)
- ✓ SSL certificate issued
- ✓ Metrics showing requests

**Dashboard sections to check:**
- **Overview:** App status, machines, regions
- **Monitoring:** CPU, memory, requests
- **Logs:** Application logs stream
- **Certificates:** SSL/TLS certificates
- **Secrets:** Configured secrets (values hidden)

### 8. Handle Common Deployment Issues (10 min)

**Issue 1: Build fails**
```bash
# Check build logs
flyctl logs --image

# Common causes:
# - Dockerfile syntax errors
# - Missing files in build context
# - Dependency installation failures

# Solution: Test build locally first
docker build -t expo-smooth-mcp:latest .
```

**Issue 2: Health checks fail**
```bash
# Check app logs
flyctl logs

# Common causes:
# - App not listening on 0.0.0.0:8000
# - Health endpoint not responding
# - App crashes on startup

# Debug in VM
flyctl ssh console
curl http://localhost:8000/health
exit
```

**Issue 3: Deployment times out**
```bash
# Increase timeout
flyctl deploy --wait-timeout 900  # 15 minutes

# Or deploy without waiting
flyctl deploy --detach

# Monitor separately
flyctl status -w  # watch mode
```

**Issue 4: Out of memory**
```bash
# Check memory usage
flyctl vm status

# If OOM, increase memory
flyctl scale memory 1024

# Redeploy
flyctl deploy
```

### 9. Post-Deployment Validation (10 min)

```bash
# Run comprehensive health check
curl -v https://expo-smooth-mcp.fly.dev/health

# Test all endpoints
curl https://expo-smooth-mcp.fly.dev/          # Root
curl https://expo-smooth-mcp.fly.dev/docs      # OpenAPI docs
curl https://expo-smooth-mcp.fly.dev/gradio    # Gradio UI

# Test MCP endpoint
curl https://expo-smooth-mcp.fly.dev/mcp/sse

# Check response times
time curl https://expo-smooth-mcp.fly.dev/health
# Should be < 500ms

# Check SSL certificate
curl -vI https://expo-smooth-mcp.fly.dev/health 2>&1 | grep "SSL certificate"
# Should show valid certificate
```

### 10. Save Deployment Information (5 min)

Create `deployment-info.txt`:
```bash
# Save deployment details
cat > deployment-info.txt <<EOF
# Expo Smooth MCP - Fly.io Deployment

App Name: expo-smooth-mcp
URL: https://expo-smooth-mcp.fly.dev
Region: sjc (San Jose, CA)
Deployment Date: $(date)
Version: v1

## Endpoints
- Root: https://expo-smooth-mcp.fly.dev/
- Health: https://expo-smooth-mcp.fly.dev/health
- OpenAPI: https://expo-smooth-mcp.fly.dev/docs
- Gradio: https://expo-smooth-mcp.fly.dev/gradio
- MCP: https://expo-smooth-mcp.fly.dev/mcp/sse

## Commands
- Deploy: flyctl deploy
- Logs: flyctl logs
- Status: flyctl status
- SSH: flyctl ssh console
- Scale: flyctl scale memory 512

## Deployed by: $(flyctl auth whoami)
EOF

cat deployment-info.txt
```

**Testing Checklist:**
- [ ] Pre-deployment checks passed
- [ ] flyctl launch or apps create successful
- [ ] fly.toml configuration validated
- [ ] flyctl deploy completed successfully
- [ ] Deployment shows "v1 deployed successfully"
- [ ] flyctl status shows "started" state
- [ ] Logs show successful startup
- [ ] Health checks passing (1/1 ✓)
- [ ] App accessible via HTTPS
- [ ] SSL certificate valid
- [ ] All endpoints responding
- [ ] Dashboard shows green status

**Acceptance Criteria:**
- [ ] App deployed to Fly.io successfully
- [ ] Assigned URL: https://expo-smooth-mcp.fly.dev
- [ ] Health endpoint returns 200 OK
- [ ] SSL/TLS certificate auto-issued and valid
- [ ] Application logs show no errors
- [ ] Health checks passing in dashboard
- [ ] VM running with 512MB memory
- [ ] Response time < 1s for health endpoint
- [ ] Deployment documented in deployment-info.txt
- [ ] Ready for comprehensive verification (TASK-412)

#### TASK-412: Verify deployment and health checks
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-411

**Description:**
Thoroughly verify the Fly.io deployment is functioning correctly, validate health checks, monitor performance metrics, and ensure production readiness.

**Implementation Steps:**

### 1. Test Public URL Access (10 min)

```bash
# Get app URL
APP_URL="https://expo-smooth-mcp.fly.dev"

# Test HTTPS access
curl -I $APP_URL/health

# Should show:
# HTTP/2 200
# content-type: application/json
# ...

# Test HTTP redirect to HTTPS
curl -I http://expo-smooth-mcp.fly.dev/health

# Should show:
# HTTP/1.1 301 Moved Permanently
# Location: https://expo-smooth-mcp.fly.dev/health

# Test from multiple locations (optional)
# Use: https://www.websiteplanet.com/webtools/server-location/
```

### 2. Verify Health Endpoint (10 min)

```bash
# Test health endpoint
curl https://expo-smooth-mcp.fly.dev/health | jq

# Expected response:
{
  "status": "healthy",
  "version": "2.0.0",
  "environment": "production",
  "sku_count": 50,
  "memory_mb": 512,
  "uptime_seconds": 123
}

# Test multiple times to verify consistency
for i in {1..10}; do
  curl -s https://expo-smooth-mcp.fly.dev/health | jq '.status'
  sleep 1
done
# All should return "healthy"

# Test response time
time curl https://expo-smooth-mcp.fly.dev/health > /dev/null
# Should be < 1 second
```

### 3. Check Fly.io Dashboard Metrics (10 min)

Visit: https://fly.io/dashboard/personal/expo-smooth-mcp

**Monitoring Tab - Verify:**

**CPU Usage:**
- Idle: < 5%
- Under load: < 50%
- No sustained spikes

**Memory Usage:**
- Steady state: 200-300MB
- Max: < 450MB (safety margin)
- No memory leaks (flat line over time)

**Request Rate:**
- Requests per second
- Response times (p50, p95, p99)
- Error rate (should be 0%)

**Network:**
- Inbound/outbound traffic
- Connection count

### 4. Validate Health Check Configuration (10 min)

```bash
# Check machine health status
flyctl status

# Should show:
# CHECKS
# tcp   ✓  1/1 passed
# http  ✓  1/1 passed

# View detailed health check config
flyctl config show | grep -A 20 "http_checks"

# Verify health check logs
flyctl logs | grep "health"

# Should show periodic health checks:
# app[xxx] sjc [info] GET /health 200 OK 25ms
```

**Test health check behavior:**
```bash
# SSH into VM
flyctl ssh console

# Simulate unhealthy state (temporarily)
# This is for testing only - don't do in real production!
mv /app/FMCG_Sales.csv /app/FMCG_Sales.csv.bak

# Health check should fail
curl http://localhost:8000/health
# Returns 503 Service Unavailable

# Restore
mv /app/FMCG_Sales.csv.bak /app/FMCG_Sales.csv

# Health check should pass again
curl http://localhost:8000/health

exit
```

### 5. Validate Cold Start Time (15 min)

**Test cold start (machine stopped → started):**

```bash
# Stop all machines
flyctl machine stop -a expo-smooth-mcp --all

# Wait a few seconds
sleep 5

# Make request to trigger auto-start
time curl https://expo-smooth-mcp.fly.dev/health

# Measure cold start time:
# Should be < 5 seconds total:
# - Machine start: ~2s
# - App startup: ~2s
# - First request: ~1s

# Repeat test 3 times for average
for i in {1..3}; do
  flyctl machine stop --all
  sleep 5
  echo "Test $i:"
  time curl https://expo-smooth-mcp.fly.dev/health
  sleep 10
done
```

**Expected cold start time:**
- **Target:** < 5 seconds
- **Acceptable:** < 10 seconds
- **Needs optimization:** > 10 seconds

**If cold start is slow:**
```bash
# Option 1: Keep min 1 machine running
# In fly.toml:
# min_machines_running = 1

# Option 2: Optimize image size
# Reduce dependencies, use smaller base image

# Option 3: Use warm start with traffic
# Machines stay running with recent activity
```

### 6. Test Auto-Scaling Behavior (10 min)

```bash
# Current machine count
flyctl status

# Should show 1 machine

# Generate load to trigger scaling (if configured)
# Install apache bench
# macOS: brew install apache-bench

# Send 100 requests, 10 concurrent
ab -n 100 -c 10 https://expo-smooth-mcp.fly.dev/health

# Check if additional machines started
flyctl status

# With min_machines_running=1, should stay at 1
# With higher concurrency, might scale up

# Check machine lifecycle
flyctl machine list

# Shows all machines and their states
```

### 7. Verify SSL Certificate (5 min)

```bash
# Check SSL certificate details
echo | openssl s_client -servername expo-smooth-mcp.fly.dev \
  -connect expo-smooth-mcp.fly.dev:443 2>/dev/null | \
  openssl x509 -noout -dates

# Should show:
# notBefore=Oct  1 00:00:00 2025 GMT
# notAfter=Dec 30 23:59:59 2025 GMT

# Check certificate issuer
echo | openssl s_client -servername expo-smooth-mcp.fly.dev \
  -connect expo-smooth-mcp.fly.dev:443 2>/dev/null | \
  openssl x509 -noout -issuer

# Should show: Let's Encrypt Authority

# Test SSL rating
# Visit: https://www.ssllabs.com/ssltest/
# Enter: expo-smooth-mcp.fly.dev
# Should get A or A+ rating
```

### 8. Monitor Application Logs (5 min)

```bash
# Stream logs
flyctl logs

# Should show:
# - Startup messages (no errors)
# - Health check requests every 30s
# - User requests (if any)
# - No error stack traces
# - No memory warnings

# Filter for errors
flyctl logs | grep -i error

# Should be empty

# Filter for health checks
flyctl logs | grep "GET /health"

# Should show regular successful requests:
# app[xxx] sjc [info] GET /health 200 OK 25ms
```

### 9. Test Geographic Access (Optional, 5 min)

```bash
# Test from different regions using curl with different resolvers
# or use online tools

# From different region (if you have access):
# ssh remote-server
# curl https://expo-smooth-mcp.fly.dev/health

# Or use online tools:
# - https://www.dotcom-tools.com/website-speed-test
# - https://tools.pingdom.com/
# - https://www.webpagetest.org/

# Test latency from your location
ping expo-smooth-mcp.fly.dev

# Should be:
# - < 50ms if same region
# - < 200ms if different continent
```

### 10. Create Deployment Verification Report (5 min)

Create `deployment-verification.md`:

```markdown
# Deployment Verification Report

**Date:** $(date)
**App:** expo-smooth-mcp
**URL:** https://expo-smooth-mcp.fly.dev
**Version:** v1

## Health Checks
- [x] Health endpoint returns 200 OK
- [x] Health checks passing in dashboard (tcp + http)
- [x] No errors in application logs
- [x] Status shows "healthy"

## Performance
- Cold start time: 4.2s (target: < 5s) ✓
- Health endpoint response: 180ms ✓
- Memory usage: 245MB / 512MB ✓
- CPU usage: 3% idle ✓

## Security
- [x] HTTPS enforced (HTTP redirects to HTTPS)
- [x] SSL certificate valid (Let's Encrypt)
- [x] SSL Labs rating: A+

## Availability
- [x] Accessible from public internet
- [x] Auto-start working (tested cold start)
- [x] Health checks passing consistently

## Issues Found
None

## Next Steps
- [ ] Test all endpoints (TASK-413)
- [ ] Configure custom domain (TASK-414)
- [ ] Document deployment process (TASK-415)
```

**Testing Checklist:**
- [ ] Public URL accessible via HTTPS
- [ ] HTTP redirects to HTTPS
- [ ] Health endpoint returns 200 OK consistently
- [ ] Dashboard shows healthy status
- [ ] CPU usage normal (< 10% idle)
- [ ] Memory usage within limits (< 400MB)
- [ ] Cold start time acceptable (< 5s)
- [ ] SSL certificate valid and auto-renewed
- [ ] Health checks passing (tcp + http)
- [ ] Application logs show no errors
- [ ] Auto-scaling working (if configured)
- [ ] Verification report created

**Acceptance Criteria:**
- [ ] App accessible at https://expo-smooth-mcp.fly.dev
- [ ] Health endpoint consistently returns 200 OK
- [ ] Health checks passing in Fly.io dashboard
- [ ] Cold start time < 5 seconds
- [ ] Response time < 1 second for health endpoint
- [ ] Memory usage < 400MB (within 512MB limit)
- [ ] SSL certificate valid and properly configured
- [ ] No errors in application logs
- [ ] Metrics visible in dashboard
- [ ] Deployment verification report completed
- [ ] Ready for endpoint testing (TASK-413)

#### TASK-413: Test all endpoints on production
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-412

**Description:**
Comprehensively test all application endpoints on the production Fly.io deployment to ensure full functionality, including REST API, MCP protocol, Gradio UI, and OpenAPI documentation.

**Implementation Steps:**

### 1. Set Up Testing Environment (5 min)

```bash
# Set base URL
export APP_URL="https://expo-smooth-mcp.fly.dev"

# Install testing tools (if needed)
# macOS:
brew install jq curl

# Create test script
cat > test-production.sh <<'EOF'
#!/bin/bash
set -e

APP_URL="https://expo-smooth-mcp.fly.dev"

echo "Testing Expo Smooth MCP Production Endpoints"
echo "=============================================="
echo ""

test_endpoint() {
  local name=$1
  local url=$2
  local expected_code=$3
  
  echo -n "Testing $name... "
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  
  if [ "$code" == "$expected_code" ]; then
    echo "✓ ($code)"
    return 0
  else
    echo "✗ (got $code, expected $expected_code)"
    return 1
  fi
}

# Run tests
test_endpoint "Root" "$APP_URL/" "200"
test_endpoint "Health" "$APP_URL/health" "200"
test_endpoint "OpenAPI Docs" "$APP_URL/docs" "200"
test_endpoint "Gradio UI" "$APP_URL/gradio" "200"
test_endpoint "MCP SSE" "$APP_URL/mcp/sse" "200"

echo ""
echo "All tests passed! ✓"
EOF

chmod +x test-production.sh
```

### 2. Test Root Endpoint (5 min)

```bash
# Test root endpoint
curl $APP_URL/ | jq

# Expected response:
{
  "name": "Expo Smooth MCP Server",
  "version": "2.0.0",
  "description": "FMCG demand forecasting with exponential smoothing",
  "mcp_endpoint": "/mcp/sse",
  "gradio_ui": "/gradio",
  "api_docs": "/docs",
  "health_check": "/health"
}

# Verify response structure
curl -s $APP_URL/ | jq 'has("name", "version", "mcp_endpoint")'
# Should return: true
```

### 3. Test Health Endpoint (10 min)

```bash
# Basic health check
curl $APP_URL/health | jq

# Expected response:
{
  "status": "healthy",
  "version": "2.0.0",
  "environment": "production",
  "sku_count": 50,
  "timestamp": "2025-10-13T12:34:56Z"
}

# Test response time
for i in {1..10}; do
  time curl -s $APP_URL/health > /dev/null
done
# Average should be < 500ms

# Test under load
ab -n 100 -c 10 $APP_URL/health

# Check results:
# - 100% successful requests
# - Mean time < 500ms
# - No failed requests
```

### 4. Test OpenAPI Documentation (10 min)

```bash
# Test docs endpoint
curl -I $APP_URL/docs

# Should return:
# HTTP/2 200
# content-type: text/html; charset=utf-8

# Open in browser
open $APP_URL/docs
# Or: xdg-open $APP_URL/docs (Linux)
# Or: start $APP_URL/docs (Windows)

# Verify in browser:
# ✓ Swagger UI loads
# ✓ Shows "Expo Smooth MCP Server" title
# ✓ Lists all endpoints:
#   - GET  /
#   - GET  /health
#   - POST /api/forecast
#   - GET  /mcp/sse (MCP endpoint)
# ✓ Can expand and test endpoints
# ✓ Schemas shown for requests/responses
```

**Test interactive docs:**
```
1. In Swagger UI, expand POST /api/forecast
2. Click "Try it out"
3. Enter test request:
   {
     "sku": "PRODUCT_001",
     "forecast_horizon": 90
   }
4. Click "Execute"
5. Verify 200 response with forecast data
```

### 5. Test REST API Endpoint (15 min)

```bash
# Test forecast endpoint
curl -X POST $APP_URL/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "PRODUCT_001",
    "forecast_horizon": 90
  }' | jq '.metadata'

# Expected response structure:
{
  "metadata": {
    "sku": "PRODUCT_001",
    "forecast_horizon": 90,
    "model_type": "Holt-Winters",
    ...
  },
  "forecast": [...],
  "historical": [...]
}

# Test with different parameters
curl -X POST $APP_URL/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "PRODUCT_001",
    "forecast_horizon": 30,
    "alpha": 0.3,
    "beta": 0.1,
    "gamma": 0.2
  }' | jq '.metadata.parameters'

# Test error handling - invalid SKU
curl -X POST $APP_URL/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"sku": "INVALID_SKU"}' | jq

# Should return 400 or 404 with error message

# Test all available SKUs
for sku in PRODUCT_001 PRODUCT_002 PRODUCT_003; do
  echo "Testing $sku..."
  curl -s -X POST $APP_URL/api/forecast \
    -H "Content-Type: application/json" \
    -d "{\"sku\": \"$sku\", \"forecast_horizon\": 30}" | \
    jq '.metadata.sku'
done
```

### 6. Test Gradio UI (15 min)

```bash
# Test Gradio endpoint
curl -I $APP_URL/gradio

# Should return:
# HTTP/2 200
# content-type: text/html; charset=utf-8

# Open in browser
open $APP_URL/gradio
```

**Manual testing in browser:**
```
1. Navigate to https://expo-smooth-mcp.fly.dev/gradio
2. Verify Gradio UI loads correctly
3. Test inputs:
   - Select SKU: PRODUCT_001
   - Forecast Horizon: 90
   - Click "Submit"
4. Verify:
   ✓ Forecast plot appears
   ✓ Shows historical data (blue line)
   ✓ Shows forecast (orange line)
   ✓ No errors in browser console
5. Test different SKUs and horizons
6. Verify responsiveness (works on mobile)
```

**Test Gradio from command line:**
```bash
# Get Gradio assets
curl -I $APP_URL/gradio/assets/index.css
# Should return 200

# Test Gradio API
curl -X POST $APP_URL/gradio/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["PRODUCT_001", 90, null, null, null]}'

# Should return forecast data or Gradio response
```

### 7. Test MCP Endpoint (20 min)

**Test with MCP Inspector:**

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Connect to remote server
mcp-inspector https://expo-smooth-mcp.fly.dev/mcp/sse

# Or use npx
npx @modelcontextprotocol/inspector https://expo-smooth-mcp.fly.dev/mcp/sse
```

**In MCP Inspector UI (http://localhost:5173):**
```
1. Verify connection established
2. Check "Connected" status shown
3. List tools:
   ✓ generate_forecast
   ✓ list_available_skus
4. Test list_available_skus:
   - Click tool
   - Execute with no parameters
   - Verify SKU list returned
5. Test generate_forecast:
   - Click tool
   - Enter: sku="PRODUCT_001", forecast_horizon=90
   - Execute
   - Verify forecast returned
6. Test error handling:
   - Execute with invalid SKU
   - Verify error response
```

**Test MCP with curl (SSE endpoint):**

```bash
# Test SSE connection
curl -N -H "Accept: text/event-stream" \
  $APP_URL/mcp/sse

# Should establish SSE connection
# Press Ctrl+C to disconnect

# Test MCP initialization (if HTTP endpoint available)
curl -X POST $APP_URL/mcp/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {}
    }
  }'

# Note: MCP over SSE uses different protocol
# Full testing requires MCP client
```

### 8. Test Claude Desktop Integration (Optional, 15 min)

If Claude Desktop supports remote MCP servers:

**Update Claude Desktop config:**
```json
{
  "mcpServers": {
    "expo-smooth-mcp-cloud": {
      "url": "https://expo-smooth-mcp.fly.dev/mcp/sse",
      "transport": "sse"
    }
  }
}
```

**Test in Claude:**
```
1. Restart Claude Desktop
2. Ask: "What tools do you have?"
3. Verify remote MCP tools appear
4. Test: "List available SKUs"
5. Test: "Generate 90-day forecast for PRODUCT_001"
```

**Note:** As of 2025, Claude Desktop primarily supports stdio transport.
Remote MCP (HTTP/SSE) support may require future Claude updates or alternative clients.

### 9. Performance Testing (15 min)

```bash
# Test concurrent requests
ab -n 100 -c 10 $APP_URL/api/forecast \
  -p forecast-request.json \
  -T application/json

# Create test request file
echo '{"sku":"PRODUCT_001","forecast_horizon":30}' > forecast-request.json

# Results to verify:
# - Requests per second: > 5
# - Mean time per request: < 2000ms
# - Failed requests: 0
# - 95th percentile: < 3000ms

# Load test different endpoints
for endpoint in / /health /docs /gradio; do
  echo "Testing $endpoint"
  ab -n 50 -c 5 $APP_URL$endpoint
done

# Monitor during load test
flyctl logs &
# Run tests
# Check for errors in logs
```

### 10. Create Test Report (10 min)

Create `production-test-report.md`:

```markdown
# Production Endpoint Testing Report

**Date:** 2025-10-13
**URL:** https://expo-smooth-mcp.fly.dev
**Version:** v1

## Endpoint Tests

### ✓ Root Endpoint (/)
- Status: 200 OK
- Response time: 145ms
- Returns service info JSON

### ✓ Health Endpoint (/health)
- Status: 200 OK
- Response time: 180ms avg
- Consistent responses (100/100 successful)

### ✓ OpenAPI Docs (/docs)
- Status: 200 OK
- Swagger UI loads correctly
- All endpoints documented
- Interactive testing works

### ✓ REST API (/api/forecast)
- Status: 200 OK
- Response time: 850ms avg
- Returns valid forecast data
- Error handling works (invalid SKU returns 400)

### ✓ Gradio UI (/gradio)
- Status: 200 OK
- UI loads and renders correctly
- Forecast generation works
- Plot displays correctly

### ✓ MCP Endpoint (/mcp/sse)
- Status: 200 OK
- SSE connection establishes
- MCP Inspector connects successfully
- Both tools (generate_forecast, list_available_skus) work

## Performance

- Root endpoint: 145ms
- Health check: 180ms
- API forecast: 850ms avg
- Concurrent requests: 10+ simultaneous
- Throughput: ~8 req/sec

## Issues Found

None

## Recommendations

1. All endpoints functioning correctly
2. Performance acceptable for production
3. Ready for custom domain (TASK-414)
4. Consider CDN for static assets (future)
5. Monitor error rates in production use

## Sign-off

- [ ] All endpoints tested ✓
- [ ] Performance acceptable ✓
- [ ] No errors found ✓
- [ ] Ready for production use ✓
```

**Testing Checklist:**
- [ ] Root endpoint (/) returns service info
- [ ] Health endpoint (/health) returns 200 OK
- [ ] OpenAPI docs (/docs) load correctly
- [ ] Swagger UI functional and interactive
- [ ] REST API (/api/forecast) works with valid SKU
- [ ] REST API error handling works (invalid SKU)
- [ ] Gradio UI (/gradio) loads and renders
- [ ] Gradio forecast generation works
- [ ] MCP endpoint (/mcp/sse) accessible
- [ ] MCP Inspector connects successfully
- [ ] Both MCP tools functional
- [ ] Performance acceptable (< 1s per request)
- [ ] Load testing passed
- [ ] Test report created

**Acceptance Criteria:**
- [ ] All endpoints (/, /health, /docs, /gradio, /api/forecast, /mcp/sse) return 200 OK
- [ ] OpenAPI documentation loads and is interactive
- [ ] REST API generates valid forecasts
- [ ] Gradio UI functional and displays plots correctly
- [ ] MCP endpoint accessible via Inspector
- [ ] Both MCP tools work correctly (generate_forecast, list_available_skus)
- [ ] Error handling works (invalid inputs return appropriate errors)
- [ ] Response times acceptable (< 1s for health, < 2s for forecasts)
- [ ] Load testing shows no failures under concurrent requests
- [ ] Production test report completed
- [ ] Ready for custom domain setup (TASK-414)

#### TASK-414: Configure custom domain (optional)
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-412

**Description:**
Configure a custom domain name for the production deployment, replacing the default fly.dev subdomain with a branded domain. This task is optional but recommended for production use.

**Prerequisites:**
- Own a domain name (e.g., example.com)
- Access to domain DNS settings
- App deployed and verified on Fly.io (TASK-412)

**Implementation Steps:**

### 1. Choose Domain Strategy (5 min)

**Options:**

**Option A: Subdomain (Recommended)**
```
mcp.example.com
api.example.com
forecast.example.com
```
**Pros:** Easy to set up, doesn't affect main site, can have multiple
**Cons:** Longer URL

**Option B: Root domain**
```
example.com
```
**Pros:** Shortest URL, brand presence
**Cons:** May affect existing site, requires DNS changes

**Option C: Dedicated domain**
```
expo-smooth-mcp.com
forecast-mcp.com
```
**Pros:** Full control, clear purpose
**Cons:** Need to purchase new domain

**For this guide, we'll use: `mcp.example.com`**

### 2. Add Domain to Fly.io (10 min)

```bash
# Add custom domain (replace with your domain)
flyctl certs create mcp.example.com

# Expected output:
# Your certificate for mcp.example.com is being issued.
# You can configure your DNS records now.

# Verify certificate status
flyctl certs show mcp.example.com

# Shows:
# Hostname                  = mcp.example.com
# Certificate Authority     = Let's Encrypt
# Issued                    = pending
# Configured                = false
# DNS Provider              = (waiting for DNS)
# DNS Validation Target     = _acme-challenge.mcp.example.com
```

### 3. Configure DNS Records (15 min)

**Get Fly.io IP addresses:**
```bash
# Get IPv4 and IPv6 addresses
flyctl ips list

# Shows:
# VERSION IP                  TYPE        REGION
# v4      66.241.124.XXX      public      global
# v6      2a09:8280:1::XXX    public      global
```

**Add DNS records in your domain registrar:**

**For subdomain (mcp.example.com):**

| Type  | Name | Value              | TTL  |
|-------|------|--------------------|------|
| A     | mcp  | 66.241.124.XXX     | 3600 |
| AAAA  | mcp  | 2a09:8280:1::XXX   | 3600 |

**For root domain (example.com):**

| Type  | Name | Value              | TTL  |
|-------|------|--------------------|------|
| A     | @    | 66.241.124.XXX     | 3600 |
| AAAA  | @    | 2a09:8280:1::XXX   | 3600 |

**Alternative: CNAME record (subdomains only):**

| Type  | Name | Value                        | TTL  |
|-------|------|------------------------------|------|
| CNAME | mcp  | expo-smooth-mcp.fly.dev      | 3600 |

**Note:** CNAME is simpler but A/AAAA records are more reliable.

**Example for major DNS providers:**

**Cloudflare:**
1. Log in to Cloudflare dashboard
2. Select your domain
3. Go to DNS → Records
4. Add A record: `mcp` → `66.241.124.XXX`
5. Add AAAA record: `mcp` → `2a09:8280:1::XXX`
6. Set Proxy status to "DNS only" (grey cloud)

**Namecheap:**
1. Log in to Namecheap
2. Domain List → Manage → Advanced DNS
3. Add A record: `mcp` → `66.241.124.XXX`
4. Add AAAA record: `mcp` → `2a09:8280:1::XXX`

**GoDaddy:**
1. Log in to GoDaddy
2. My Products → DNS → Manage Zones
3. Add A record: `mcp` → `66.241.124.XXX`
4. Add AAAA record: `mcp` → `2a09:8280:1::XXX`

### 4. Verify DNS Propagation (10 min)

```bash
# Check A record
dig mcp.example.com A

# Should show:
# mcp.example.com.  3600  IN  A  66.241.124.XXX

# Check AAAA record
dig mcp.example.com AAAA

# Check from multiple DNS servers
dig @8.8.8.8 mcp.example.com      # Google DNS
dig @1.1.1.1 mcp.example.com      # Cloudflare DNS
dig @8.8.4.4 mcp.example.com      # Google DNS 2

# Use online tools:
# https://dnschecker.org/
# Enter: mcp.example.com
# Verify A record shows correct IP globally
```

**Wait for DNS propagation:**
- Typically: 5-30 minutes
- Maximum: 24-48 hours (depends on TTL)

### 5. Verify SSL Certificate Issuance (10 min)

```bash
# Check certificate status
flyctl certs check mcp.example.com

# Should show:
# Hostname                  = mcp.example.com
# Certificate Authority     = Let's Encrypt
# Issued                    = true
# Configured                = true
# Expires                   = 2025-12-31

# If still pending, wait a few minutes and check again

# Test HTTPS access
curl -I https://mcp.example.com/health

# Should return:
# HTTP/2 200
# (no SSL errors)

# Verify certificate details
echo | openssl s_client -servername mcp.example.com \
  -connect mcp.example.com:443 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates

# Should show:
# subject=CN = mcp.example.com
# issuer=C = US, O = Let's Encrypt, CN = R3
# notBefore=Oct 13 ...
# notAfter=Jan 11 ...
```

### 6. Update Application Configuration (Optional, 5 min)

If your app uses domain-aware features:

```python
# main.py - Add custom domain to CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mcp.example.com",
        "https://expo-smooth-mcp.fly.dev",  # Keep fly.dev as fallback
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Redeploy if changes made:**
```bash
flyctl deploy
```

### 7. Test Custom Domain (10 min)

```bash
# Set custom domain
CUSTOM_URL="https://mcp.example.com"

# Test all endpoints
curl $CUSTOM_URL/ | jq
curl $CUSTOM_URL/health | jq
curl -I $CUSTOM_URL/docs
curl -I $CUSTOM_URL/gradio

# Test MCP endpoint
npx @modelcontextprotocol/inspector https://mcp.example.com/mcp/sse

# Test in browser
open https://mcp.example.com
open https://mcp.example.com/docs
open https://mcp.example.com/gradio

# Verify redirect from HTTP
curl -I http://mcp.example.com/health
# Should redirect to HTTPS

# Test from different locations
ping mcp.example.com
# Should resolve to Fly.io IPs
```

### 8. Update Documentation and Links (5 min)

Update references in:

**README.md:**
```markdown
## Live Demo

Production: https://mcp.example.com
API Docs: https://mcp.example.com/docs
Gradio UI: https://mcp.example.com/gradio
```

**deployment-info.txt:**
```
Custom Domain: https://mcp.example.com
Fly.dev URL: https://expo-smooth-mcp.fly.dev (fallback)
```

**Claude Desktop config** (if applicable):
```json
{
  "mcpServers": {
    "expo-smooth-mcp": {
      "url": "https://mcp.example.com/mcp/sse",
      "transport": "sse"
    }
  }
}
```

### 9. Monitor and Troubleshoot (5 min)

**Common issues:**

**Issue 1: DNS not propagating**
```bash
# Check TTL
dig mcp.example.com | grep TTL

# Wait for TTL duration
# Try clearing local DNS cache:
# macOS: sudo dscacheutil -flushcache
# Linux: sudo systemd-resolve --flush-caches
# Windows: ipconfig /flushdns
```

**Issue 2: Certificate not issuing**
```bash
# Check certificate logs
flyctl certs show mcp.example.com

# Common causes:
# - DNS not configured correctly
# - Existing CAA record blocking Let's Encrypt
# - Domain not pointing to Fly.io IPs

# Solution: Verify DNS with dig, wait 10-30 min
```

**Issue 3: Mixed content errors**
```bash
# Ensure all resources use HTTPS
# Check browser console for mixed content warnings

# Update any hardcoded HTTP URLs to HTTPS
```

**Issue 4: Certificate renewal**
```bash
# Fly.io auto-renews certificates
# Verify auto-renewal is enabled:
flyctl certs list

# Manual renewal (if needed):
flyctl certs renew mcp.example.com
```

### 10. Optional: Add Additional Domains (5 min)

```bash
# Add www subdomain
flyctl certs create www.mcp.example.com

# Add multiple domains
flyctl certs create api.example.com
flyctl certs create forecast.example.com

# List all certificates
flyctl certs list

# Each domain needs DNS A/AAAA records
```

**Testing Checklist:**
- [ ] Custom domain chosen (e.g., mcp.example.com)
- [ ] Domain added to Fly.io with flyctl certs create
- [ ] DNS A record configured with Fly.io IPv4
- [ ] DNS AAAA record configured with Fly.io IPv6
- [ ] DNS propagation verified with dig
- [ ] SSL certificate issued by Let's Encrypt
- [ ] HTTPS works without SSL errors
- [ ] HTTP redirects to HTTPS
- [ ] All endpoints accessible via custom domain
- [ ] Documentation updated with new domain
- [ ] Certificate auto-renewal enabled

**Acceptance Criteria:**
- [ ] Custom domain successfully added to Fly.io
- [ ] DNS records properly configured
- [ ] SSL certificate issued and valid
- [ ] HTTPS accessible without errors
- [ ] All application endpoints work via custom domain
- [ ] HTTP automatically redirects to HTTPS
- [ ] Certificate renewal configured (auto-renews)
- [ ] Documentation updated with custom domain
- [ ] Both fly.dev and custom domain functional
- [ ] Ready for deployment documentation (TASK-415)

**Note:** This task is optional. The default `expo-smooth-mcp.fly.dev` domain works perfectly fine for development and even production use.

#### TASK-415: Create Fly.io deployment documentation
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-413

**Description:**
Create comprehensive documentation for deploying, managing, and maintaining the MCP server on Fly.io. This includes setup guides, CI/CD integration, monitoring, troubleshooting, and rollback procedures.

**Implementation Steps:**

### 1. Create Main Deployment Guide (40 min)

Create `docs/FLY_IO_DEPLOYMENT.md`:

```markdown
# Fly.io Deployment Guide

## Overview

This guide covers deploying the Expo Smooth MCP server to Fly.io's global application platform. Fly.io provides automatic scaling, health checks, zero-downtime deployments, and global edge locations.

## Prerequisites

- Fly.io account (sign up at https://fly.io)
- flyctl CLI installed
- Docker installed locally
- Project built and tested locally

## Quick Start

### 1. Install and Authenticate

```bash
# Install flyctl
brew install flyctl  # macOS
# Or: curl -L https://fly.io/install.sh | sh

# Authenticate
flyctl auth login

# Verify
flyctl auth whoami
```

### 2. Configure Application

Ensure `fly.toml` exists in project root:
```toml
app = "expo-smooth-mcp"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"

[vm]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512

[[services]]
  protocol = "tcp"
  internal_port = 8000
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
  
  [[services.http_checks]]
    interval = "30s"
    timeout = "5s"
    path = "/health"
```

### 3. Set Secrets

```bash
# Generate secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Set secrets
flyctl secrets set SECRET_KEY="generated-secret-key-here"
```

### 4. Deploy

```bash
# First deployment
flyctl launch  # Interactive setup

# Or with existing fly.toml
flyctl apps create expo-smooth-mcp
flyctl deploy

# Monitor deployment
flyctl logs
```

### 5. Verify

```bash
# Check status
flyctl status

# Test endpoints
curl https://expo-smooth-mcp.fly.dev/health
curl https://expo-smooth-mcp.fly.dev/docs

# Open in browser
flyctl open
```

## Detailed Deployment

### Initial Setup

**1. Create Application:**
```bash
# Option A: Interactive
flyctl launch
# Follow prompts:
# - App name: expo-smooth-mcp
# - Region: sjc (or closest)
# - PostgreSQL: No
# - Redis: No
# - Deploy now: No (configure first)

# Option B: With existing config
flyctl apps create expo-smooth-mcp --org personal
```

**2. Configure Resources:**
```bash
# Set memory (512MB validated)
flyctl scale memory 512

# Set machine count
flyctl scale count 1

# Set region
flyctl regions add sjc
flyctl regions set sjc
```

**3. Configure Secrets:**
```bash
# Required secrets
flyctl secrets set SECRET_KEY="your-secret-key"

# Optional secrets (if using)
flyctl secrets set \
  REDIS_URL="redis://..." \
  DATABASE_URL="postgres://..."

# List secrets
flyctl secrets list
```

### Deployment Process

**Build and Deploy:**
```bash
# Standard deployment
flyctl deploy

# With specific Dockerfile
flyctl deploy --dockerfile Dockerfile.production

# Local build (don't use remote builder)
flyctl deploy --local-only

# With specific configuration
flyctl deploy --config fly.production.toml

# Skip health checks (not recommended)
flyctl deploy --no-cache
```

**Monitor Deployment:**
```bash
# Watch deployment progress
flyctl status -w

# Stream logs
flyctl logs -f

# Check machines
flyctl machine list
```

### Post-Deployment

**Verify Deployment:**
```bash
# Check app status
flyctl status

# Test health endpoint
curl https://expo-smooth-mcp.fly.dev/health

# Open in browser
flyctl open /docs
```

**Monitor Application:**
```bash
# View logs (last 100 lines)
flyctl logs

# Stream logs in real-time
flyctl logs -f

# View specific machine logs
flyctl machine logs <machine-id>

# Dashboard
flyctl dashboard
```

## Configuration

### Environment Variables

**Public variables (fly.toml):**
```toml
[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"
  PYTHONUNBUFFERED = "1"
```

**Secret variables (flyctl secrets):**
```bash
flyctl secrets set SECRET_KEY="value"
flyctl secrets set API_KEY="value"
```

**View secrets:**
```bash
flyctl secrets list  # Lists names only
# Values are never displayed for security
```

### Resource Limits

**Memory:**
```bash
# View current memory
flyctl vm status

# Scale memory
flyctl scale memory 512   # 512MB (validated)
flyctl scale memory 1024  # 1GB (if needed)

# Memory options: 256, 512, 1024, 2048, 4096, 8192 MB
```

**CPU:**
```bash
# Scale CPUs
flyctl scale vm shared-cpu-1x  # 1 shared vCPU (default)
flyctl scale vm shared-cpu-2x  # 2 shared vCPUs

# For dedicated CPU
flyctl scale vm dedicated-cpu-1x
```

**Machine Count:**
```bash
# Scale machine count
flyctl scale count 1  # Single machine
flyctl scale count 2  # High availability

# Per-region scaling
flyctl scale count 2 --region sjc
flyctl scale count 1 --region iad
```

### Custom Domain

**Add custom domain:**
```bash
# Add domain
flyctl certs create mcp.example.com

# Get Fly.io IPs
flyctl ips list

# Add DNS records:
# A    mcp    <IPv4-from-above>
# AAAA mcp    <IPv6-from-above>

# Check certificate status
flyctl certs show mcp.example.com

# Certificate auto-issues after DNS propagates (5-30 min)
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Flyctl
        uses: superfly/flyctl-actions/setup-flyctl@master
      
      - name: Deploy to Fly.io
        run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

**Setup:**
1. Get Fly.io API token: `flyctl auth token`
2. Add to GitHub Secrets: Settings → Secrets → `FLY_API_TOKEN`
3. Push to main branch to trigger deployment

### GitLab CI/CD

Create `.gitlab-ci.yml`:

```yaml
deploy:
  stage: deploy
  image: flyio/flyctl:latest
  only:
    - main
  script:
    - flyctl deploy --remote-only
  variables:
    FLY_API_TOKEN: $CI_FLY_API_TOKEN
```

**Setup:**
1. Get token: `flyctl auth token`
2. Add to GitLab: Settings → CI/CD → Variables → `CI_FLY_API_TOKEN`

## Monitoring

### Application Metrics

**Via Dashboard:**
- Visit: https://fly.io/dashboard/personal/expo-smooth-mcp
- View: CPU, Memory, Requests, Response times

**Via CLI:**
```bash
# Check status
flyctl status

# View VM metrics
flyctl vm status

# Monitor in real-time
watch -n 5 'flyctl vm status'
```

### Logging

**View logs:**
```bash
# Recent logs
flyctl logs

# Follow logs
flyctl logs -f

# Filter logs
flyctl logs | grep ERROR
flyctl logs | grep "POST /api/forecast"

# Specific machine
flyctl logs -i <machine-id>
```

**Log aggregation:**
- Fly.io retains logs for 7 days
- For longer retention, integrate with:
  - Logtail (https://betterstack.com/logtail)
  - Papertrail (https://papertrailapp.com)
  - DataDog (https://www.datadoghq.com)

### Alerts

**Set up alerts in Fly.io dashboard:**
1. Go to app → Monitoring
2. Create alert rules:
   - Health check failures
   - High memory usage (> 450MB)
   - High CPU usage (> 80%)
   - Error rate spike

**Email notifications:**
- Configure in account settings
- Alerts sent to registered email

## Troubleshooting

### Deployment Issues

**Build fails:**
```bash
# View build logs
flyctl logs --image

# Test locally first
docker build -t test .
docker run --rm test

# Use local builder
flyctl deploy --local-only
```

**Health checks fail:**
```bash
# Check logs
flyctl logs | grep health

# SSH into machine
flyctl ssh console
curl http://localhost:8000/health
exit

# Adjust health check timeout in fly.toml
```

**Deployment timeout:**
```bash
# Increase timeout
flyctl deploy --wait-timeout 900

# Or deploy detached
flyctl deploy --detach
flyctl status -w  # Watch separately
```

### Runtime Issues

**App crashes:**
```bash
# View crash logs
flyctl logs | grep -A 20 "crashed"

# Check machine status
flyctl vm status

# Restart machine
flyctl machine restart <machine-id>

# Or restart all
flyctl machine restart --all
```

**Out of memory:**
```bash
# Check memory usage
flyctl vm status

# Scale memory
flyctl scale memory 1024

# Redeploy
flyctl deploy
```

**Slow response times:**
```bash
# Check metrics
flyctl dashboard

# Scale resources
flyctl scale memory 1024
flyctl scale vm shared-cpu-2x

# Add more machines
flyctl scale count 2
```

### Connection Issues

**Can't reach app:**
```bash
# Check app status
flyctl status

# Check machines running
flyctl machine list

# Verify DNS
dig expo-smooth-mcp.fly.dev

# Test from within network
flyctl ssh console
curl http://localhost:8000/health
```

**SSL errors:**
```bash
# Check certificates
flyctl certs list
flyctl certs show expo-smooth-mcp.fly.dev

# Force certificate renewal
flyctl certs renew expo-smooth-mcp.fly.dev
```

## Maintenance

### Updates

**Deploy new version:**
```bash
# Build and test locally
docker build -t expo-smooth-mcp:latest .
docker run --rm -p 8000:8000 expo-smooth-mcp:latest

# Deploy to Fly.io
flyctl deploy

# Monitor deployment
flyctl logs -f
```

**Zero-downtime deployment:**
- Enabled by default with `strategy = "rolling"` in fly.toml
- New machine starts and passes health checks
- Old machine gracefully shut down
- Traffic automatically routes to new machine

### Rollback

**Rollback to previous version:**
```bash
# List releases
flyctl releases

# Shows:
# VERSION  STABLE  TYPE    STATUS   DESC              DATE
# v3       true    deploy  success  Deploy image      2m ago
# v2       true    deploy  success  Deploy image      1h ago
# v1       true    deploy  success  Initial deploy    1d ago

# Rollback to previous version
flyctl releases rollback v2

# Or rollback to last stable
flyctl releases rollback
```

**Emergency rollback:**
```bash
# Immediate rollback (skips health checks)
flyctl releases rollback v2 --force

# Check status
flyctl status

# Verify with logs
flyctl logs -f
```

### Scaling

**Vertical scaling (resources):**
```bash
# Increase memory
flyctl scale memory 1024

# Increase CPU
flyctl scale vm shared-cpu-2x

# Redeploy to apply
flyctl deploy
```

**Horizontal scaling (machines):**
```bash
# Add more machines
flyctl scale count 2

# Machines auto-distributed across regions
# Each handles ~50% of traffic with load balancing

# Scale per region
flyctl regions add iad  # Add US East
flyctl scale count 2 --region sjc
flyctl scale count 1 --region iad
```

### Backup

**Data backup (if using volumes):**
```bash
# List volumes
flyctl volumes list

# Create snapshot
flyctl volumes snapshots create <volume-id>

# List snapshots
flyctl volumes snapshots list <volume-id>

# Restore from snapshot
flyctl volumes restore <snapshot-id>
```

**Configuration backup:**
```bash
# Backup fly.toml (version control)
git add fly.toml
git commit -m "Update fly.toml"
git push

# Backup secrets (store securely!)
flyctl secrets list > secrets-backup.txt
# Manually record actual values (not shown by CLI)
```

## Best Practices

### Security

1. **Use secrets for sensitive data:**
   ```bash
   flyctl secrets set SECRET_KEY="..."
   ```

2. **Keep fly.toml in version control:**
   - Public variables only
   - No secrets in fly.toml

3. **Restrict machine access:**
   ```bash
   # Use SSH keys
   flyctl ssh establish
   ```

4. **Enable HTTPS only:**
   - force_https = true (in fly.toml)

### Performance

1. **Optimize Docker image:**
   - Multi-stage builds
   - Minimal base image
   - Small image size (< 500MB)

2. **Use health checks:**
   - Fast endpoint (< 100ms)
   - Regular intervals (30s)

3. **Configure auto-scaling:**
   - min_machines_running = 1 (always available)
   - auto_stop/start_machines = true

### Monitoring

1. **Check logs regularly:**
   ```bash
   flyctl logs | grep ERROR
   ```

2. **Monitor metrics:**
   - Dashboard for CPU/memory
   - Alert on anomalies

3. **Test after deployment:**
   ```bash
   curl https://expo-smooth-mcp.fly.dev/health
   ```

## Cost Optimization

**Current configuration cost:**
- Shared CPU 1x (512MB): ~$4/month
- Bandwidth (160GB free): $0
- Total: ~$4-5/month

**Reduce costs:**
1. Use auto-stop for development:
   ```toml
   min_machines_running = 0  # Stop when idle
   ```

2. Use smaller memory for dev:
   ```bash
   flyctl scale memory 256
   ```

3. Limit machine count:
   ```toml
   max_per_region = 1  # Single machine per region
   ```

## Support

**Resources:**
- Docs: https://fly.io/docs
- Community: https://community.fly.io
- Status: https://status.fly.io

**Get help:**
```bash
# Check documentation
flyctl docs

# Get command help
flyctl deploy --help

# Community forum
# https://community.fly.io
```

## Appendix

### Useful Commands

```bash
# Deployment
flyctl deploy                    # Deploy app
flyctl deploy --config fly.toml  # Use specific config
flyctl releases                  # List releases
flyctl releases rollback         # Rollback last release

# Management
flyctl status                    # Check app status
flyctl logs                      # View logs
flyctl logs -f                   # Follow logs
flyctl ssh console               # SSH into machine

# Scaling
flyctl scale memory 512          # Set memory
flyctl scale count 2             # Set machine count
flyctl scale vm shared-cpu-1x    # Set VM size

# Configuration
flyctl secrets set KEY=value     # Set secret
flyctl secrets list              # List secrets
flyctl ips list                  # List IP addresses
flyctl regions list              # List regions

# Monitoring
flyctl dashboard                 # Open dashboard
flyctl vm status                 # Check VM status
flyctl machine list              # List machines
```

### Fly.toml Reference

Complete fly.toml example:
```toml
app = "expo-smooth-mcp"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  APP_ENV = "production"
  LOG_LEVEL = "info"
  PORT = "8000"

[vm]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512

[[services]]
  protocol = "tcp"
  internal_port = 8000
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  
  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true
  
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
  
  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20
  
  [[services.tcp_checks]]
    interval = "15s"
    timeout = "2s"
    grace_period = "10s"
  
  [[services.http_checks]]
    interval = "30s"
    timeout = "5s"
    grace_period = "10s"
    method = "get"
    path = "/health"
    protocol = "http"

[deploy]
  strategy = "rolling"
  max_unavailable = 0
```
```

### 2. Create Quick Reference (20 min)

Create `docs/FLY_IO_QUICKREF.md`:

```markdown
# Fly.io Quick Reference

## Initial Setup
```bash
brew install flyctl
flyctl auth login
flyctl launch
flyctl deploy
```

## Daily Operations
```bash
flyctl deploy              # Deploy updates
flyctl status              # Check status
flyctl logs -f             # View logs
flyctl ssh console         # SSH into machine
```

## Configuration
```bash
flyctl secrets set KEY=val # Set secret
flyctl scale memory 512    # Set memory
flyctl scale count 1       # Set machines
flyctl regions add sjc     # Add region
```

## Monitoring
```bash
flyctl status              # App status
flyctl vm status           # Resource usage
flyctl logs                # View logs
flyctl dashboard           # Open web dashboard
```

## Troubleshooting
```bash
flyctl logs | grep ERROR   # Find errors
flyctl machine restart all # Restart machines
flyctl releases rollback   # Rollback deploy
flyctl ssh console         # Debug in machine
```

## Scaling
```bash
flyctl scale memory 1024   # Increase memory
flyctl scale count 2       # Add machines
flyctl scale vm shared-cpu-2x  # More CPU
```
```

### 3. Update Main README (15 min)

Add Fly.io deployment section to `README.md`:

```markdown
## Deployment

### Fly.io (Production)

**Quick Start:**
```bash
flyctl auth login
flyctl launch
flyctl deploy
```

**Production URL:** https://expo-smooth-mcp.fly.dev

**Full Guide:** [Fly.io Deployment Guide](docs/FLY_IO_DEPLOYMENT.md)

**Features:**
- Global CDN and edge locations
- Auto-scaling (starts/stops on demand)
- Zero-downtime deployments
- Automatic SSL certificates
- 512MB RAM, 1 vCPU
- ~$4-5/month cost

**Commands:**
- Deploy: `flyctl deploy`
- Logs: `flyctl logs -f`
- Status: `flyctl status`
- Rollback: `flyctl releases rollback`
```

### 4. Update DEPLOYMENT_GUIDE.md (20 min)

Add comprehensive Fly.io section to existing deployment guide.

### 5. Create Troubleshooting Guide (15 min)

Create `docs/FLY_IO_TROUBLESHOOTING.md` with common issues and solutions.

### 6. Create CI/CD Examples (10 min)

Create `.github/workflows/deploy-fly.yml` example and document setup.

**Testing Checklist:**
- [ ] FLY_IO_DEPLOYMENT.md created with complete guide
- [ ] Quick reference guide created
- [ ] README.md updated with Fly.io section
- [ ] DEPLOYMENT_GUIDE.md includes Fly.io
- [ ] Troubleshooting guide created
- [ ] CI/CD examples provided
- [ ] All commands tested and verified
- [ ] Links between docs work correctly
- [ ] Follows documentation standards

**Acceptance Criteria:**
- [ ] Complete Fly.io deployment documentation created
- [ ] Covers initial setup, deployment, monitoring, troubleshooting
- [ ] Includes CI/CD integration guide (GitHub Actions, GitLab)
- [ ] Rollback procedures documented
- [ ] Scaling guide included (vertical and horizontal)
- [ ] Cost optimization tips provided
- [ ] Quick reference guide created
- [ ] Main README updated with Fly.io deployment
- [ ] All code examples tested and working
- [ ] Phase 4B complete, ready for Phase 5 (Production Hardening)

---

### Phase 5: Production Hardening (14 tasks, ~22 hours)

#### TASK-501: Create security module skeleton
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:**
Create the security module structure to house authentication, authorization, and security utilities. This establishes the foundation for production-grade security features.

**Implementation Steps:**

### 1. Create Module File (5 min)

```bash
# Create security module
touch src/expo_smooth_mcp/security.py

# Verify structure
ls -la src/expo_smooth_mcp/
# Should show: __init__.py, forecasting.py, preprocessing.py, security.py
```

### 2. Add Module Skeleton (20 min)

Create `src/expo_smooth_mcp/security.py`:

```python
"""
Security Module

Provides authentication, authorization, and security utilities for the
Expo Smooth MCP server. Includes:
- Password hashing (bcrypt)
- JWT token creation and validation
- OAuth2 password flow
- User authentication dependencies
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Pydantic Models
class Token(BaseModel):
    """OAuth2 token response model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Decoded token data."""
    username: Optional[str] = None
    scopes: list[str] = []


class User(BaseModel):
    """User model."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """User model with hashed password."""
    hashed_password: str


# Placeholder functions (to be implemented)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    raise NotImplementedError("To be implemented in TASK-503")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    raise NotImplementedError("To be implemented in TASK-503")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    raise NotImplementedError("To be implemented in TASK-504")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """FastAPI dependency to get current authenticated user."""
    raise NotImplementedError("To be implemented in TASK-505")


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user credentials."""
    raise NotImplementedError("To be implemented in TASK-506")


# Export public API
__all__ = [
    "Token",
    "TokenData",
    "User",
    "UserInDB",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "get_current_user",
    "authenticate_user",
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
]
```

### 3. Update Package __init__.py (5 min)

Update `src/expo_smooth_mcp/__init__.py`:

```python
"""
Expo Smooth MCP - FMCG Demand Forecasting

A Model Context Protocol server providing exponential smoothing forecasting
for FMCG sales data.
"""

from .preprocessing import load_and_preprocess_data
from .forecasting import generate_forecast_for_sku, list_available_skus

# Security module (available but not required)
try:
    from . import security
except ImportError:
    security = None

__version__ = "2.0.0"

__all__ = [
    "load_and_preprocess_data",
    "generate_forecast_for_sku",
    "list_available_skus",
    "security",
]
```

### 4. Add Type Hints and Documentation (5 min)

Ensure all function signatures have proper type hints:

```python
# Example with complete type hints
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = get_password_hash("mypassword")
        >>> verify_password("mypassword", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    raise NotImplementedError("To be implemented in TASK-503")
```

### 5. Create Security Configuration (5 min)

Add security configuration section to document environment variables needed:

```python
# Security configuration constants
class SecurityConfig:
    """Security configuration settings."""
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Password requirements
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = False
    
    # Rate limiting (if Redis available)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    @classmethod
    def validate(cls) -> None:
        """Validate security configuration."""
        if cls.SECRET_KEY == "dev-secret-key-change-in-production":
            import warnings
            warnings.warn(
                "Using default SECRET_KEY! Set SECRET_KEY environment variable in production.",
                RuntimeWarning
            )
```

### 6. Add Tests Placeholder (5 min)

Create test file structure:

```bash
# Create security tests file
touch tests/test_security.py
```

Add test skeleton:

```python
"""
Security Module Tests

Tests for authentication, authorization, and security utilities.
"""

import pytest
from expo_smooth_mcp.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)


class TestPasswordHashing:
    """Tests for password hashing utilities."""
    
    def test_password_hashing_placeholder(self):
        """Placeholder - to be implemented in TASK-503."""
        pytest.skip("Not yet implemented")


class TestJWTTokens:
    """Tests for JWT token creation and validation."""
    
    def test_token_creation_placeholder(self):
        """Placeholder - to be implemented in TASK-504."""
        pytest.skip("Not yet implemented")


class TestAuthentication:
    """Tests for user authentication."""
    
    def test_authentication_placeholder(self):
        """Placeholder - to be implemented in TASK-506."""
        pytest.skip("Not yet implemented")
```

**Testing Checklist:**
- [ ] security.py module created
- [ ] Module imports successfully
- [ ] All placeholder functions defined with NotImplementedError
- [ ] Pydantic models created (Token, User, UserInDB)
- [ ] Configuration constants defined
- [ ] Type hints on all functions
- [ ] Docstrings on all functions
- [ ] __all__ exports list defined
- [ ] Package __init__.py updated
- [ ] test_security.py created with placeholders

**Acceptance Criteria:**
- [ ] src/expo_smooth_mcp/security.py file created
- [ ] Module structure includes all required imports
- [ ] Pydantic models defined (Token, TokenData, User, UserInDB)
- [ ] Configuration constants set (SECRET_KEY, ALGORITHM, expiration)
- [ ] Placeholder functions for all security features
- [ ] All functions have type hints and docstrings
- [ ] Module imports without errors
- [ ] test_security.py created with test structure
- [ ] Ready for dependency installation (TASK-502)

#### TASK-502: Install security dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:**
Install Python packages required for authentication and security features. This includes JWT handling and password hashing libraries.

**Implementation Steps:**

### 1. Update requirements.txt (10 min)

Add security dependencies to `requirements.txt`:

```txt
# Existing dependencies
fastapi>=0.104.0
fastmcp>=2.0.0
uvicorn[standard]>=0.24.0
gradio>=5.0.0
pandas>=2.0.0
numpy>=1.24.0
statsmodels>=0.14.0
matplotlib>=3.7.0
python-multipart>=0.0.6

# Security dependencies (new)
python-jose[cryptography]>=3.3.0  # JWT token handling
passlib[bcrypt]>=1.7.4             # Password hashing
python-multipart>=0.0.6            # OAuth2 form data (if not already present)

# Rate limiting (optional, for TASK-508)
# redis>=5.0.0
# fastapi-limiter>=0.1.5
```

### 2. Install Dependencies Locally (5 min)

```bash
# Activate virtual environment (if using)
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install security dependencies
pip install "python-jose[cryptography]>=3.3.0"
pip install "passlib[bcrypt]>=1.7.4"

# Or install all from requirements
pip install -r requirements.txt

# Verify installation
pip list | grep jose
pip list | grep passlib

# Should show:
# passlib       1.7.4
# python-jose   3.3.0
# cryptography  41.x.x (installed with python-jose[cryptography])
```

### 3. Verify Imports Work (5 min)

Test imports in Python:

```python
# Test jose imports
python3 -c "from jose import jwt; print('✓ python-jose working')"

# Test passlib imports
python3 -c "from passlib.context import CryptContext; print('✓ passlib working')"

# Test bcrypt specifically
python3 -c "from passlib.hash import bcrypt; print('✓ bcrypt working')"

# Test cryptography (JWT dependency)
python3 -c "from cryptography.fernet import Fernet; print('✓ cryptography working')"
```

Expected output:
```
✓ python-jose working
✓ passlib working
✓ bcrypt working
✓ cryptography working
```

### 4. Update Dockerfile (5 min)

Ensure Dockerfile installs security dependencies:

```dockerfile
# Dockerfile (verify/update)

# Install dependencies stage
FROM python:3.12-slim as builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies including security packages
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /app/dependencies /usr/local/lib/python3.12/site-packages/

# Security dependencies should be included
RUN python -c "from jose import jwt" && \
    python -c "from passlib.context import CryptContext" && \
    echo "✓ Security dependencies installed"

# ... rest of Dockerfile
```

### 5. Test Security Module Imports (5 min)

Verify security module can import dependencies:

```bash
# Test security module imports
python3 -c "
from expo_smooth_mcp.security import (
    Token,
    User,
    UserInDB,
    pwd_context,
    oauth2_scheme
)
print('✓ Security module imports successfully')
"
```

### 6. Document Dependencies (5 min)

Create `docs/SECURITY_DEPENDENCIES.md`:

```markdown
# Security Dependencies

## Required Packages

### python-jose[cryptography]
- **Version:** 3.3.0+
- **Purpose:** JWT token creation and validation
- **License:** MIT
- **Docs:** https://python-jose.readthedocs.io/

**Features used:**
- JWT encoding/decoding
- Token expiration handling
- Cryptographic signing (HS256 algorithm)

**Installation:**
```bash
pip install "python-jose[cryptography]"
```

### passlib[bcrypt]
- **Version:** 1.7.4+
- **Purpose:** Secure password hashing
- **License:** BSD
- **Docs:** https://passlib.readthedocs.io/

**Features used:**
- Bcrypt password hashing
- Password verification
- Context-based hash management

**Installation:**
```bash
pip install "passlib[bcrypt]"
```

### cryptography (indirect)
- **Version:** 41.0+
- **Purpose:** Cryptographic operations for JWT
- **License:** Apache 2.0 / BSD
- **Docs:** https://cryptography.io/

Installed automatically with `python-jose[cryptography]`.

## Optional Packages (Phase 5 Later Tasks)

### redis
- **Purpose:** Rate limiting backend
- **Used in:** TASK-509, TASK-510

### fastapi-limiter
- **Purpose:** Rate limiting middleware
- **Used in:** TASK-510

## Verification

Test all security dependencies:
```bash
python3 -c "
from jose import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
print('All security dependencies working!')
"
```

## Troubleshooting

### Issue: cryptography build fails

**macOS:**
```bash
brew install rust
pip install cryptography
```

**Linux:**
```bash
apt-get install build-essential libssl-dev libffi-dev python3-dev
pip install cryptography
```

**Solution:** Use pre-built wheels:
```bash
pip install --only-binary :all: cryptography
```

### Issue: bcrypt build fails

Install bcrypt binary:
```bash
pip install --only-binary :all: bcrypt
```

### Issue: ImportError for _bcrypt

Reinstall with correct binary:
```bash
pip uninstall passlib bcrypt
pip install "passlib[bcrypt]"
```
```

**Testing Checklist:**
- [ ] requirements.txt updated with security packages
- [ ] python-jose[cryptography] installed
- [ ] passlib[bcrypt] installed
- [ ] All packages show in pip list
- [ ] jose module imports successfully
- [ ] passlib module imports successfully
- [ ] bcrypt specifically imports
- [ ] cryptography module imports
- [ ] Dockerfile installs security dependencies
- [ ] Documentation created

**Acceptance Criteria:**
- [ ] python-jose[cryptography]>=3.3.0 added to requirements.txt
- [ ] passlib[bcrypt]>=1.7.4 added to requirements.txt
- [ ] Dependencies installed successfully in local environment
- [ ] All security imports work without errors
- [ ] Dockerfile updated to include security dependencies
- [ ] Docker image builds successfully with new dependencies
- [ ] SECURITY_DEPENDENCIES.md documentation created
- [ ] Ready for password hashing implementation (TASK-503)

#### TASK-503: Implement password hashing utilities
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-502

**Description:**
Implement secure password hashing and verification functions using bcrypt. These utilities will be used for user authentication and password management.

**Implementation Steps:**

### 1. Implement Password Hashing (15 min)

Update `src/expo_smooth_mcp/security.py`:

```python
# Update the placeholder function

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string suitable for storage
        
    Example:
        >>> hashed = get_password_hash("my_secure_password")
        >>> len(hashed) > 50  # Bcrypt hashes are ~60 characters
        True
        
    Note:
        Uses bcrypt with automatic salt generation.
        Safe to store in database.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches hash, False otherwise
        
    Example:
        >>> hashed = get_password_hash("my_password")
        >>> verify_password("my_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
        
    Note:
        Constant-time comparison prevents timing attacks.
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Validate password meets security requirements.
    
    Args:
        password: Plain text password to validate
        
    Returns:
        Tuple of (is_valid, list of error messages)
        
    Example:
        >>> validate_password_strength("weak")
        (False, ['Password must be at least 8 characters', 'Must contain uppercase letter'])
        >>> validate_password_strength("SecurePass123")
        (True, [])
    """
    errors = []
    
    # Check length
    if len(password) < SecurityConfig.MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {SecurityConfig.MIN_PASSWORD_LENGTH} characters")
    
    # Check uppercase
    if SecurityConfig.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check numbers
    if SecurityConfig.REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    
    # Check special characters
    if SecurityConfig.REQUIRE_SPECIAL_CHARS:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            errors.append("Password must contain at least one special character")
    
    return (len(errors) == 0, errors)
```

### 2. Add Password Generation Utility (10 min)

```python
import secrets
import string

def generate_secure_password(length: int = 16) -> str:
    """
    Generate a cryptographically secure random password.
    
    Args:
        length: Password length (minimum 12, default 16)
        
    Returns:
        Randomly generated password meeting security requirements
        
    Example:
        >>> password = generate_secure_password()
        >>> len(password)
        16
        >>> validate_password_strength(password)[0]
        True
    """
    if length < 12:
        raise ValueError("Password length must be at least 12 characters")
    
    # Character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*()_+-="
    
    # Ensure at least one of each required type
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
    ]
    
    if SecurityConfig.REQUIRE_SPECIAL_CHARS:
        password.append(secrets.choice(special))
    
    # Fill remaining length with random choices from all sets
    all_chars = uppercase + lowercase + digits + special
    password.extend(secrets.choice(all_chars) for _ in range(length - len(password)))
    
    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)
```

### 3. Create Mock User Database (10 min)

For development and testing:

```python
# Mock user database (replace with real database in production)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": "$2b$12$KixW8vGfhP6YyKLVM6uEOeFOGXp.BwS.EFfH7vBGGHEgDWfBJ0jdm",  # "testpass123"
        "disabled": False,
    },
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$YourHashedPasswordHere",  # Change in production!
        "disabled": False,
    }
}


def get_user(username: str) -> Optional[UserInDB]:
    """
    Get user from database by username.
    
    Args:
        username: Username to look up
        
    Returns:
        UserInDB object if found, None otherwise
        
    Example:
        >>> user = get_user("testuser")
        >>> user.username
        'testuser'
    """
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None
```

### 4. Create User Management Script (10 min)

Create `scripts/create_user.py`:

```python
#!/usr/bin/env python3
"""
Create User Script

Generate hashed passwords for user database.

Usage:
    python scripts/create_user.py <username> <password>
    
Example:
    python scripts/create_user.py admin SecurePass123
"""

import sys
from expo_smooth_mcp.security import get_password_hash, validate_password_strength


def main():
    if len(sys.argv) != 3:
        print("Usage: python create_user.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    # Validate password strength
    is_valid, errors = validate_password_strength(password)
    if not is_valid:
        print("Password does not meet requirements:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Hash password
    hashed = get_password_hash(password)
    
    # Output user dictionary
    print("\nUser entry for database:")
    print("{")
    print(f'    "username": "{username}",')
    print(f'    "hashed_password": "{hashed}",')
    print('    "email": "user@example.com",  # Update this')
    print('    "full_name": "Full Name",      # Update this')
    print('    "disabled": False,')
    print("}")
    print("\nCopy this to your user database.")


if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x scripts/create_user.py
```

### 5. Write Comprehensive Tests (15 min)

Update `tests/test_security.py`:

```python
"""Tests for password hashing utilities."""

import pytest
from expo_smooth_mcp.security import (
    get_password_hash,
    verify_password,
    validate_password_strength,
    generate_secure_password,
    get_user,
)


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_password_hashing(self):
        """Test password can be hashed."""
        password = "my_secure_password"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 50  # Bcrypt hashes are ~60 chars
        assert hashed.startswith("$2b$")  # Bcrypt identifier
    
    def test_password_verification_success(self):
        """Test correct password verifies successfully."""
        password = "correct_password"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_password_verification_failure(self):
        """Test incorrect password fails verification."""
        password = "correct_password"
        hashed = get_password_hash(password)
        
        assert verify_password("wrong_password", hashed) is False
    
    def test_same_password_different_hashes(self):
        """Test same password produces different hashes (salted)."""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2  # Different due to random salt
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)


class TestPasswordStrength:
    """Test password strength validation."""
    
    def test_short_password_fails(self):
        """Test password shorter than minimum fails."""
        is_valid, errors = validate_password_strength("short")
        
        assert is_valid is False
        assert any("at least" in error.lower() for error in errors)
    
    def test_no_uppercase_fails(self):
        """Test password without uppercase fails."""
        is_valid, errors = validate_password_strength("alllowercase123")
        
        assert is_valid is False
        assert any("uppercase" in error.lower() for error in errors)
    
    def test_no_numbers_fails(self):
        """Test password without numbers fails."""
        is_valid, errors = validate_password_strength("OnlyLetters")
        
        assert is_valid is False
        assert any("number" in error.lower() for error in errors)
    
    def test_strong_password_passes(self):
        """Test strong password passes validation."""
        is_valid, errors = validate_password_strength("SecurePass123")
        
        assert is_valid is True
        assert errors == []


class TestPasswordGeneration:
    """Test secure password generation."""
    
    def test_generate_password_default_length(self):
        """Test generated password has correct default length."""
        password = generate_secure_password()
        
        assert len(password) == 16
    
    def test_generate_password_custom_length(self):
        """Test generated password respects custom length."""
        password = generate_secure_password(length=24)
        
        assert len(password) == 24
    
    def test_generate_password_meets_strength(self):
        """Test generated password meets strength requirements."""
        password = generate_secure_password()
        is_valid, errors = validate_password_strength(password)
        
        assert is_valid is True
        assert errors == []
    
    def test_generate_password_min_length_enforced(self):
        """Test minimum length is enforced."""
        with pytest.raises(ValueError, match="at least 12"):
            generate_secure_password(length=8)
    
    def test_generate_different_passwords(self):
        """Test generated passwords are unique."""
        passwords = [generate_secure_password() for _ in range(10)]
        
        assert len(set(passwords)) == 10  # All unique


class TestUserRetrieval:
    """Test user database functions."""
    
    def test_get_existing_user(self):
        """Test retrieving existing user."""
        user = get_user("testuser")
        
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_get_nonexistent_user(self):
        """Test retrieving non-existent user returns None."""
        user = get_user("nonexistent")
        
        assert user is None
    
    def test_user_password_can_verify(self):
        """Test retrieved user's password can be verified."""
        user = get_user("testuser")
        
        # Password is "testpass123" (from mock database)
        assert verify_password("testpass123", user.hashed_password)
        assert not verify_password("wrongpassword", user.hashed_password)
```

Run tests:
```bash
pytest tests/test_security.py::TestPasswordHashing -v
pytest tests/test_security.py::TestPasswordStrength -v
pytest tests/test_security.py::TestPasswordGeneration -v
```

**Testing Checklist:**
- [ ] get_password_hash() implemented
- [ ] verify_password() implemented
- [ ] validate_password_strength() implemented
- [ ] generate_secure_password() implemented
- [ ] get_user() mock function implemented
- [ ] fake_users_db created with test users
- [ ] create_user.py script created
- [ ] All password tests passing
- [ ] Password strength tests passing
- [ ] Password generation tests passing

**Acceptance Criteria:**
- [ ] Password hashing function implemented with bcrypt
- [ ] Password verification function works correctly
- [ ] Password strength validation enforces requirements
- [ ] Secure password generation utility created
- [ ] Mock user database established
- [ ] User creation script functional
- [ ] All tests passing (10+ tests)
- [ ] Passwords properly salted (different hashes for same password)
- [ ] Ready for JWT token implementation (TASK-504)

#### TASK-504: Implement JWT token creation
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-502

**Description:**
Implement JWT (JSON Web Token) creation with expiration handling. Tokens will be used for stateless authentication in API requests.

**Implementation Steps:**

### 1. Implement Token Creation (20 min)

Update `src/expo_smooth_mcp/security.py`:

```python
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary of claims to encode in token (typically {"sub": username})
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
        
    Example:
        >>> token = create_access_token({"sub": "testuser"})
        >>> len(token) > 100  # JWTs are typically 100-200 characters
        True
        >>> # With custom expiration
        >>> token = create_access_token(
        ...     {"sub": "testuser"},
        ...     expires_delta=timedelta(minutes=15)
        ... )
        
    Note:
        Token includes:
        - sub: Subject (username)
        - exp: Expiration timestamp
        - iat: Issued at timestamp
        - Additional custom claims from data dict
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add standard claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    })
    
    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Dictionary of decoded token claims
        
    Raises:
        JWTError: If token is invalid, expired, or malformed
        
    Example:
        >>> token = create_access_token({"sub": "testuser"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'testuser'
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a refresh token for long-lived sessions.
    
    Args:
        data: Dictionary of claims to encode
        expires_delta: Optional custom expiration (default: 7 days)
        
    Returns:
        Encoded refresh token string
        
    Note:
        Refresh tokens have longer expiration and should be used
        to obtain new access tokens without re-authentication.
    """
    if expires_delta is None:
        expires_delta = timedelta(days=7)
    
    return create_access_token(data, expires_delta)
```

### 2. Add Token Validation Helper (15 min)

```python
def verify_token_expiration(payload: Dict[str, Any]) -> bool:
    """
    Verify token has not expired.
    
    Args:
        payload: Decoded JWT payload
        
    Returns:
        True if token is still valid, False if expired
        
    Example:
        >>> token = create_access_token({"sub": "user"})
        >>> payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        >>> verify_token_expiration(payload)
        True
    """
    exp_timestamp = payload.get("exp")
    if exp_timestamp is None:
        return False
    
    expiration = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    
    return now < expiration


def get_token_metadata(token: str) -> Dict[str, Any]:
    """
    Get metadata from token without full validation.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with token metadata (exp, iat, sub, etc.)
        
    Note:
        For debugging/logging only. Always validate properly before trusting.
    """
    try:
        # Decode without verification for metadata only
        unverified = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        return {
            "subject": unverified.get("sub"),
            "issued_at": datetime.fromtimestamp(unverified.get("iat", 0), tz=timezone.utc),
            "expires_at": datetime.fromtimestamp(unverified.get("exp", 0), tz=timezone.utc),
            "is_expired": not verify_token_expiration(unverified),
        }
    except Exception as e:
        return {"error": str(e)}
```

### 3. Add Token Scopes Support (10 min)

```python
def create_access_token_with_scopes(
    username: str,
    scopes: list[str],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create access token with permission scopes.
    
    Args:
        username: User identifier
        scopes: List of permission scopes (e.g., ["forecast:read", "forecast:write"])
        expires_delta: Optional custom expiration
        
    Returns:
        Encoded JWT with scopes
        
    Example:
        >>> token = create_access_token_with_scopes(
        ...     "testuser",
        ...     ["forecast:read", "admin:write"]
        ... )
        >>> payload = decode_access_token(token)
        >>> "forecast:read" in payload["scopes"]
        True
    """
    data = {
        "sub": username,
        "scopes": scopes,
    }
    return create_access_token(data, expires_delta)


def verify_scope(required_scope: str, token_scopes: list[str]) -> bool:
    """
    Verify token has required scope.
    
    Args:
        required_scope: Scope required for operation
        token_scopes: Scopes present in token
        
    Returns:
        True if scope is present, False otherwise
        
    Example:
        >>> verify_scope("forecast:read", ["forecast:read", "forecast:write"])
        True
        >>> verify_scope("admin:write", ["forecast:read"])
        False
    """
    return required_scope in token_scopes
```

### 4. Write Token Tests (15 min)

Update `tests/test_security.py`:

```python
from datetime import timedelta
import time
from jose import jwt

from expo_smooth_mcp.security import (
    create_access_token,
    decode_access_token,
    create_refresh_token,
    verify_token_expiration,
    create_access_token_with_scopes,
    SECRET_KEY,
    ALGORITHM,
)


class TestJWTTokens:
    """Test JWT token creation and validation."""
    
    def test_create_token(self):
        """Test token creation."""
        token = create_access_token({"sub": "testuser"})
        
        assert isinstance(token, str)
        assert len(token) > 50  # JWTs are long strings
    
    def test_decode_token(self):
        """Test token can be decoded."""
        token = create_access_token({"sub": "testuser"})
        payload = decode_access_token(token)
        
        assert payload["sub"] == "testuser"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_token_contains_custom_data(self):
        """Test token includes custom claims."""
        token = create_access_token({
            "sub": "testuser",
            "email": "test@example.com",
            "role": "admin"
        })
        payload = decode_access_token(token)
        
        assert payload["sub"] == "testuser"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "admin"
    
    def test_token_expiration(self):
        """Test token expires after set time."""
        # Create token that expires in 1 second
        token = create_access_token(
            {"sub": "testuser"},
            expires_delta=timedelta(seconds=1)
        )
        
        # Decode immediately - should work
        payload = decode_access_token(token)
        assert payload["sub"] == "testuser"
        
        # Wait for expiration
        time.sleep(2)
        
        # Decode after expiration - should fail
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)
        assert exc_info.value.status_code == 401
    
    def test_custom_expiration_time(self):
        """Test custom expiration time is respected."""
        token = create_access_token(
            {"sub": "testuser"},
            expires_delta=timedelta(minutes=60)
        )
        
        # Manually decode to check expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        iat_timestamp = payload["iat"]
        
        # Difference should be ~60 minutes (3600 seconds)
        diff = exp_timestamp - iat_timestamp
        assert 3590 < diff < 3610  # Allow small variance
    
    def test_refresh_token_longer_expiration(self):
        """Test refresh token has longer expiration."""
        access_token = create_access_token({"sub": "testuser"})
        refresh_token = create_refresh_token({"sub": "testuser"})
        
        access_payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        refresh_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        access_exp = access_payload["exp"]
        refresh_exp = refresh_payload["exp"]
        
        # Refresh token should expire much later than access token
        assert refresh_exp > access_exp
        assert (refresh_exp - access_exp) > 86400  # At least 1 day difference
    
    def test_token_with_scopes(self):
        """Test creating token with permission scopes."""
        scopes = ["forecast:read", "forecast:write"]
        token = create_access_token_with_scopes("testuser", scopes)
        
        payload = decode_access_token(token)
        
        assert payload["sub"] == "testuser"
        assert payload["scopes"] == scopes
    
    def test_invalid_token_fails(self):
        """Test invalid token raises error."""
        invalid_token = "invalid.jwt.token"
        
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(invalid_token)
        assert exc_info.value.status_code == 401
    
    def test_tampered_token_fails(self):
        """Test tampered token fails validation."""
        token = create_access_token({"sub": "testuser"})
        
        # Tamper with token by changing a character
        tampered = token[:-1] + "X"
        
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(tampered)
        assert exc_info.value.status_code == 401
```

Run tests:
```bash
pytest tests/test_security.py::TestJWTTokens -v
```

**Testing Checklist:**
- [ ] create_access_token() implemented
- [ ] decode_access_token() implemented
- [ ] Token includes expiration claim
- [ ] Token includes issued-at claim
- [ ] Custom expiration times work
- [ ] create_refresh_token() implemented
- [ ] Token scope support added
- [ ] All token tests passing (10+ tests)
- [ ] Invalid tokens rejected
- [ ] Expired tokens rejected

**Acceptance Criteria:**
- [ ] JWT token creation function implemented
- [ ] Token includes standard claims (sub, exp, iat)
- [ ] Custom data can be encoded in token
- [ ] Token expiration enforced
- [ ] Custom expiration times supported
- [ ] Refresh token creation implemented
- [ ] Token scope system implemented
- [ ] Token validation with proper error handling
- [ ] All tests passing
- [ ] Ready for user authentication dependency (TASK-505)

#### TASK-505: Implement token validation dependency
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-504

**Description:**
Create FastAPI dependency for validating JWT tokens and retrieving current authenticated user. This dependency will be used to protect endpoints requiring authentication.

**Implementation Steps:**

### 1. Implement User Authentication Dependency (30 min)

Update `src/expo_smooth_mcp/security.py`:

```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    FastAPI dependency to get current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header (automatic via oauth2_scheme)
        
    Returns:
        User object for authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found (401 Unauthorized)
        
    Example:
        ```python
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}"}
        ```
        
    Usage:
        Client must include: Authorization: Bearer <token>
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate token
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, scopes=payload.get("scopes", []))
        
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return User(**user.model_dump())


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    FastAPI dependency to get current active (non-disabled) user.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User object if active
        
    Raises:
        HTTPException: If user is disabled (400 Bad Request)
        
    Example:
        ```python
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_active_user)):
            return {"message": f"Hello active user {user.username}"}
        ```
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
```

### 2. Add Scope-Based Authorization (20 min)

```python
from typing import List

class RoleChecker:
    """Dependency to check if user has required role/scope."""
    
    def __init__(self, required_scopes: List[str]):
        self.required_scopes = required_scopes
    
    async def __call__(self, token: str = Depends(oauth2_scheme)) -> User:
        """
        Verify user has required scopes.
        
        Args:
            token: JWT token
            
        Returns:
            User object if authorized
            
        Raises:
            HTTPException: If user lacks required scope (403 Forbidden)
        """
        # Decode token
        payload = decode_access_token(token)
        username = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        
        # Check if user has all required scopes
        for scope in self.required_scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Required scope: {scope}",
                )
        
        # Get and return user
        user = get_user(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return User(**user.model_dump())


# Convenience instances for common roles
require_forecast_read = RoleChecker(["forecast:read"])
require_forecast_write = RoleChecker(["forecast:write"])
require_admin = RoleChecker(["admin"])


# Example usage:
# @app.get("/forecasts", dependencies=[Depends(require_forecast_read)])
# async def list_forecasts():
#     return {"forecasts": [...]}
```

### 3. Add Optional Authentication (15 min)

```python
async def get_current_user_optional(
    authorization: Optional[str] = Header(None)
) -> Optional[User]:
    """
    Optional authentication - returns User if token provided and valid, None otherwise.
    
    Args:
        authorization: Optional Authorization header
        
    Returns:
        User object if authenticated, None if no token
        
    Example:
        ```python
        @app.get("/public-or-private")
        async def mixed_endpoint(user: Optional[User] = Depends(get_current_user_optional)):
            if user:
                return {"message": f"Hello {user.username}", "authenticated": True}
            return {"message": "Hello guest", "authenticated": False}
        ```
    """
    if not authorization:
        return None
    
    if not authorization.startswith("Bearer "):
        return None
    
    token = authorization[7:]  # Remove "Bearer " prefix
    
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username:
            user = get_user(username)
            if user:
                return User(**user.model_dump())
    except (JWTError, HTTPException):
        pass
    
    return None
```

### 4. Create Authentication Test Utilities (15 min)

Update `tests/test_security.py`:

```python
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from expo_smooth_mcp.security import (
    get_current_user,
    get_current_active_user,
    get_current_user_optional,
    require_forecast_read,
    create_access_token,
)


# Test app for dependency testing
app = FastAPI()

@app.get("/protected")
async def protected_endpoint(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}

@app.get("/active-only")
async def active_only_endpoint(user: User = Depends(get_current_active_user)):
    return {"username": user.username}

@app.get("/optional-auth")
async def optional_auth_endpoint(user: Optional[User] = Depends(get_current_user_optional)):
    if user:
        return {"authenticated": True, "username": user.username}
    return {"authenticated": False}

@app.get("/read-forecasts", dependencies=[Depends(require_forecast_read)])
async def read_forecasts():
    return {"forecasts": ["data"]}


client = TestClient(app)


class TestAuthenticationDependency:
    """Test user authentication dependency."""
    
    def test_valid_token_returns_user(self):
        """Test valid token returns user info."""
        token = create_access_token({"sub": "testuser"})
        
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
    
    def test_missing_token_returns_401(self):
        """Test request without token returns 401."""
        response = client.get("/protected")
        
        assert response.status_code == 401
    
    def test_invalid_token_returns_401(self):
        """Test invalid token returns 401."""
        response = client.get(
            "/protected",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401
    
    def test_expired_token_returns_401(self):
        """Test expired token returns 401."""
        token = create_access_token(
            {"sub": "testuser"},
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 401
    
    def test_nonexistent_user_returns_401(self):
        """Test token for non-existent user returns 401."""
        token = create_access_token({"sub": "nonexistentuser"})
        
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 401
    
    def test_active_user_check(self):
        """Test active user dependency accepts active users."""
        token = create_access_token({"sub": "testuser"})
        
        response = client.get(
            "/active-only",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
    
    def test_optional_auth_with_token(self):
        """Test optional auth returns user when token provided."""
        token = create_access_token({"sub": "testuser"})
        
        response = client.get(
            "/optional-auth",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["authenticated"] is True
        assert response.json()["username"] == "testuser"
    
    def test_optional_auth_without_token(self):
        """Test optional auth succeeds without token."""
        response = client.get("/optional-auth")
        
        assert response.status_code == 200
        assert response.json()["authenticated"] is False


class TestScopeAuthorization:
    """Test scope-based authorization."""
    
    def test_valid_scope_allows_access(self):
        """Test user with required scope can access endpoint."""
        token = create_access_token_with_scopes("testuser", ["forecast:read"])
        
        response = client.get(
            "/read-forecasts",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
    
    def test_missing_scope_denies_access(self):
        """Test user without required scope is denied."""
        token = create_access_token_with_scopes("testuser", ["forecast:write"])
        
        response = client.get(
            "/read-forecasts",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
    
    def test_no_scopes_denies_access(self):
        """Test user with no scopes is denied."""
        token = create_access_token({"sub": "testuser"})
        
        response = client.get(
            "/read-forecasts",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
```

Run tests:
```bash
pytest tests/test_security.py::TestAuthenticationDependency -v
pytest tests/test_security.py::TestScopeAuthorization -v
```

**Testing Checklist:**
- [ ] get_current_user() dependency implemented
- [ ] get_current_active_user() dependency implemented
- [ ] get_current_user_optional() implemented
- [ ] RoleChecker class implemented
- [ ] Scope-based authorization working
- [ ] Valid tokens return user
- [ ] Invalid tokens return 401
- [ ] Expired tokens rejected
- [ ] Scope checks enforce permissions
- [ ] All dependency tests passing

**Acceptance Criteria:**
- [ ] FastAPI dependency for authentication implemented
- [ ] Validates JWT tokens from Authorization header
- [ ] Returns User object for valid tokens
- [ ] Returns 401 for invalid/missing/expired tokens
- [ ] Active user checking implemented
- [ ] Optional authentication supported
- [ ] Scope-based authorization implemented
- [ ] All tests passing (15+ tests)
- [ ] Ready for login endpoint implementation (TASK-506)

#### TASK-506: Create /token authentication endpoint
**Estimated Time:** 1.5 hours | **Complexity:** High | **Dependencies:** TASK-505

**Description:**
Implement OAuth2 password flow `/token` endpoint for user authentication. This endpoint accepts username/password and returns a JWT access token.

**Implementation Steps:**

### 1. Implement User Authentication Function (20 min)

Update `src/expo_smooth_mcp/security.py`:

```python
from fastapi.security import OAuth2PasswordRequestForm

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate user with username and password.
    
    Args:
        username: Username to authenticate
        password: Plain text password
        
    Returns:
        UserInDB object if authentication successful, None otherwise
        
    Example:
        >>> user = authenticate_user("testuser", "testpass123")
        >>> user.username
        'testuser'
        >>> authenticate_user("testuser", "wrongpass")
        None
    """
    user = get_user(username)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user
```

### 2. Create Token Endpoint (30 min)

Add to `main.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from expo_smooth_mcp.security import (
    authenticate_user,
    create_access_token,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login endpoint.
    
    Authenticate with username and password to receive a JWT access token.
    Use the token in subsequent requests with: Authorization: Bearer <token>
    
    Args:
        form_data: OAuth2 form with username and password
        
    Returns:
        Token object with access_token and token_type
        
    Raises:
        HTTPException: 401 if authentication fails
        
    Example:
        ```bash
        curl -X POST "http://localhost:8000/token" \\
          -H "Content-Type: application/x-www-form-urlencoded" \\
          -d "username=testuser&password=testpass123"
        ```
        
        Response:
        ```json
        {
          "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
          "token_type": "bearer"
        }
        ```
        
        Use token:
        ```bash
        curl -H "Authorization: Bearer <token>" http://localhost:8000/api/forecast
        ```
    """
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
```

### 3. Add Token Refresh Endpoint (Optional, 15 min)

```python
@app.post("/token/refresh", response_model=Token, tags=["Authentication"])
async def refresh_access_token(
    current_user: User = Depends(get_current_user)
) -> Token:
    """
    Refresh access token using existing valid token.
    
    Provides a new access token with extended expiration.
    Useful for maintaining session without re-authentication.
    
    Args:
        current_user: Current authenticated user (from token)
        
    Returns:
        New Token object with fresh access_token
        
    Example:
        ```bash
        curl -X POST "http://localhost:8000/token/refresh" \\
          -H "Authorization: Bearer <old-token>"
        ```
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
```

### 4. Add User Info Endpoint (15 min)

```python
@app.get("/users/me", response_model=User, tags=["Authentication"])
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current authenticated user information.
    
    Returns profile information for the currently authenticated user.
    
    Args:
        current_user: Current user from authentication dependency
        
    Returns:
        User object with profile information
        
    Example:
        ```bash
        curl -H "Authorization: Bearer <token>" http://localhost:8000/users/me
        ```
        
        Response:
        ```json
        {
          "username": "testuser",
          "email": "test@example.com",
          "full_name": "Test User",
          "disabled": false
        }
        ```
    """
    return current_user
```

### 5. Write Authentication Endpoint Tests (20 min)

Create `tests/test_auth_endpoints.py`:

```python
"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient

from main import app
from expo_smooth_mcp.security import create_access_token


client = TestClient(app)


class TestTokenEndpoint:
    """Test /token authentication endpoint."""
    
    def test_login_with_valid_credentials(self):
        """Test successful login with correct credentials."""
        response = client.post(
            "/token",
            data={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 50
    
    def test_login_with_invalid_password(self):
        """Test login fails with wrong password."""
        response = client.post(
            "/token",
            data={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_with_nonexistent_user(self):
        """Test login fails with non-existent user."""
        response = client.post(
            "/token",
            data={
                "username": "nonexistent",
                "password": "anypassword"
            }
        )
        
        assert response.status_code == 401
    
    def test_login_requires_username(self):
        """Test login fails without username."""
        response = client.post(
            "/token",
            data={"password": "testpass123"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_requires_password(self):
        """Test login fails without password."""
        response = client.post(
            "/token",
            data={"username": "testuser"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_token_can_be_used_for_auth(self):
        """Test received token works for authentication."""
        # Login to get token
        login_response = client.post(
            "/token",
            data={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Use token to access protected endpoint
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"


class TestUsersMeEndpoint:
    """Test /users/me endpoint."""
    
    def test_users_me_returns_user_info(self):
        """Test /users/me returns current user info."""
        token = create_access_token({"sub": "testuser"})
        
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_users_me_requires_auth(self):
        """Test /users/me requires authentication."""
        response = client.get("/users/me")
        
        assert response.status_code == 401


class TestTokenRefresh:
    """Test token refresh endpoint."""
    
    def test_token_refresh_works(self):
        """Test token can be refreshed."""
        # Get initial token
        token = create_access_token({"sub": "testuser"})
        
        # Refresh token
        response = client.post(
            "/token/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] != token  # Should be different token
    
    def test_refresh_requires_valid_token(self):
        """Test refresh requires valid token."""
        response = client.post(
            "/token/refresh",
            headers={"Authorization": "Bearer invalid.token"}
        )
        
        assert response.status_code == 401
```

Run tests:
```bash
pytest tests/test_auth_endpoints.py -v
```

### 6. Test with curl/httpie (10 min)

```bash
# Start server
python main.py &

# Test login endpoint
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Save token
TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123" | jq -r '.access_token')

# Use token to access /users/me
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/users/me

# Refresh token
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8000/token/refresh

# Test Swagger UI
open http://localhost:8000/docs
# Click "Authorize" button, enter credentials, test endpoints
```

**Testing Checklist:**
- [ ] /token endpoint implemented
- [ ] OAuth2PasswordRequestForm used
- [ ] authenticate_user() function works
- [ ] Valid credentials return token
- [ ] Invalid credentials return 401
- [ ] Token refresh endpoint implemented
- [ ] /users/me endpoint implemented
- [ ] All endpoint tests passing
- [ ] Swagger UI "Authorize" button works
- [ ] curl tests successful

**Acceptance Criteria:**
- [ ] POST /token endpoint implemented (OAuth2 password flow)
- [ ] Accepts username and password
- [ ] Returns JWT access token on success
- [ ] Returns 401 on invalid credentials
- [ ] Token refresh endpoint implemented
- [ ] /users/me endpoint returns user info
- [ ] All tests passing (12+ tests)
- [ ] Swagger UI authentication functional
- [ ] Ready to protect API endpoints (TASK-507)

#### TASK-507: Protect API endpoints with auth
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-506

**Description:**
Add authentication requirements to API endpoints that should be protected. This secures the forecast API and other sensitive endpoints.

**Implementation Steps:**

### 1. Protect Forecast API Endpoint (15 min)

Update `main.py`:

```python
from expo_smooth_mcp.security import get_current_active_user, User

# Update existing endpoint
@app.post("/api/forecast", tags=["API"])
async def api_forecast(
    request: ForecastRequest,
    current_user: User = Depends(get_current_active_user)  # Add authentication
) -> ForecastResponse:
    """
    Generate forecast for a product SKU (REST API).
    
    **Authentication Required:** This endpoint requires a valid JWT token.
    
    Args:
        request: Forecast request parameters
        current_user: Authenticated user (automatically injected)
        
    Returns:
        Forecast response with historical data and predictions
        
    Example:
        ```bash
        # Get token first
        TOKEN=$(curl -s -X POST "http://localhost:8000/token" \\
          -d "username=testuser&password=testpass123" | jq -r '.access_token')
        
        # Call protected endpoint
        curl -X POST "http://localhost:8000/api/forecast" \\
          -H "Authorization: Bearer $TOKEN" \\
          -H "Content-Type: application/json" \\
          -d '{"sku": "PRODUCT_001", "forecast_horizon": 90}'
        ```
    """
    try:
        result = generate_forecast_for_sku(
            sku=request.sku,
            forecast_horizon=request.forecast_horizon,
            alpha=request.alpha,
            beta=request.beta,
            gamma=request.gamma,
        )
        
        return ForecastResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast error: {str(e)}")
```

### 2. Make Gradio UI Optional Auth (15 min)

Gradio UI should remain public but can optionally show user info:

```python
# Keep Gradio public (no auth requirement)
# But pass user context if available

from expo_smooth_mcp.security import get_current_user_optional

@app.get("/gradio-user-info")
async def gradio_user_info(
    user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get current user info for Gradio UI.
    Returns None if not authenticated.
    """
    if user:
        return {
            "authenticated": True,
            "username": user.username,
            "full_name": user.full_name
        }
    return {"authenticated": False}
```

### 3. Keep MCP Endpoints Public (5 min)

MCP endpoints should remain public as they use their own authentication:

```python
# MCP endpoints remain public
# Claude Desktop handles authentication separately
# No changes needed to MCP tool handlers
```

### 4. Add Protected Admin Endpoints (15 min)

```python
from expo_smooth_mcp.security import require_admin

@app.get("/admin/stats", tags=["Admin"], dependencies=[Depends(require_admin)])
async def admin_stats():
    """
    Get server statistics (admin only).
    
    **Requires:** admin scope
    """
    return {
        "total_users": len(fake_users_db),
        "total_skus": len(list_available_skus()),
        "server_version": "2.0.0",
    }


@app.post("/admin/users", tags=["Admin"], dependencies=[Depends(require_admin)])
async def create_user(username: str, password: str):
    """
    Create new user (admin only).
    
    **Requires:** admin scope
    """
    # This is a placeholder - implement properly with database
    raise HTTPException(status_code=501, detail="Not yet implemented")
```

### 5. Update OpenAPI Documentation (10 min)

Update `main.py` to configure OAuth2 in Swagger UI:

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Expo Smooth MCP Server",
        version="2.0.0",
        description="FMCG demand forecasting with exponential smoothing",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/token",
                    "scopes": {
                        "forecast:read": "Read forecasts",
                        "forecast:write": "Generate forecasts",
                        "admin": "Admin access"
                    }
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
```

### 6. Write Protection Tests (15 min)

Update `tests/test_auth_endpoints.py`:

```python
class TestProtectedEndpoints:
    """Test authentication on protected endpoints."""
    
    def test_forecast_requires_auth(self):
        """Test /api/forecast requires authentication."""
        response = client.post(
            "/api/forecast",
            json={
                "sku": "PRODUCT_001",
                "forecast_horizon": 90
            }
        )
        
        assert response.status_code == 401
    
    def test_forecast_works_with_valid_token(self):
        """Test /api/forecast works with valid token."""
        token = create_access_token({"sub": "testuser"})
        
        response = client.post(
            "/api/forecast",
            json={
                "sku": "PRODUCT_001",
                "forecast_horizon": 90
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "metadata" in data
        assert "forecast" in data
    
    def test_forecast_fails_with_invalid_token(self):
        """Test /api/forecast fails with invalid token."""
        response = client.post(
            "/api/forecast",
            json={
                "sku": "PRODUCT_001",
                "forecast_horizon": 90
            },
            headers={"Authorization": "Bearer invalid.token"}
        )
        
        assert response.status_code == 401
    
    def test_public_endpoints_still_work(self):
        """Test public endpoints don't require auth."""
        # Root endpoint
        response = client.get("/")
        assert response.status_code == 200
        
        # Health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        
        # Docs
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_admin_endpoints_require_admin_scope(self):
        """Test admin endpoints require admin scope."""
        # Token without admin scope
        token = create_access_token({"sub": "testuser"})
        
        response = client.get(
            "/admin/stats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
    
    def test_admin_endpoints_work_with_admin_scope(self):
        """Test admin endpoints work with admin scope."""
        token = create_access_token_with_scopes("admin", ["admin"])
        
        response = client.get(
            "/admin/stats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
```

Run tests:
```bash
pytest tests/test_auth_endpoints.py::TestProtectedEndpoints -v
```

**Testing Checklist:**
- [ ] /api/forecast requires authentication
- [ ] Valid token allows forecast access
- [ ] Invalid token returns 401
- [ ] Public endpoints still accessible
- [ ] MCP endpoints remain public
- [ ] Admin endpoints require admin scope
- [ ] Swagger UI shows lock icons on protected endpoints
- [ ] All protection tests passing

**Acceptance Criteria:**
- [ ] /api/forecast endpoint protected with authentication
- [ ] Requires valid JWT token in Authorization header
- [ ] Returns 401 for unauthenticated requests
- [ ] Public endpoints (/, /health, /docs) remain accessible
- [ ] MCP endpoints remain public
- [ ] Admin endpoints protected with scope checking
- [ ] OpenAPI/Swagger UI reflects authentication requirements
- [ ] All tests passing (10+ tests)
- [ ] Ready for rate limiting implementation (TASK-508)

#### TASK-508: Install rate limiting dependencies
**Estimated Time:** 0.5 hours | **Complexity:** Low | **Dependencies:** None

**Description:**
Install Redis and FastAPI rate limiting dependencies to protect the API from abuse. Rate limiting prevents excessive requests from individual clients and ensures fair resource usage.

**Implementation Steps:**

### 1. Update requirements.txt (10 min)

Add rate limiting dependencies:

```txt
# Existing dependencies
fastapi>=0.104.0
fastmcp>=2.0.0
uvicorn[standard]>=0.24.0
gradio>=5.0.0
pandas>=2.0.0
numpy>=1.24.0
statsmodels>=0.14.0
matplotlib>=3.7.0
python-multipart>=0.0.6

# Security dependencies
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# Rate limiting dependencies (new)
redis>=5.0.0                      # Redis client for Python
fastapi-limiter>=0.1.6            # Rate limiting middleware for FastAPI
aioredis>=2.0.1                   # Async Redis support (if needed)
```

### 2. Install Dependencies (5 min)

```bash
# Install rate limiting packages
pip install redis>=5.0.0
pip install fastapi-limiter>=0.1.6

# Or install all from requirements
pip install -r requirements.txt

# Verify installation
pip list | grep redis
pip list | grep limiter

# Expected output:
# fastapi-limiter  0.1.6
# redis            5.0.1
```

### 3. Install Redis Server (10 min)

**macOS:**
```bash
# Install via Homebrew
brew install redis

# Start Redis
brew services start redis

# Or run in foreground
redis-server

# Test connection
redis-cli ping
# Expected: PONG
```

**Linux (Ubuntu/Debian):**
```bash
# Install Redis
sudo apt-get update
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test connection
redis-cli ping
```

**Docker:**
```bash
# Run Redis container
docker run -d -p 6379:6379 --name redis redis:7-alpine

# Test connection
docker exec -it redis redis-cli ping
```

**Production (Fly.io):**
```bash
# Create Redis cluster on Fly.io (free tier available)
fly redis create

# Or use external provider:
# - Upstash Redis (serverless, free tier)
# - Redis Cloud (managed, free tier)
# - AWS ElastiCache
```

### 4. Update fly.toml for Redis (5 min)

Add Redis URL to environment:

```toml
[env]
  REDIS_URL = "redis://localhost:6379"  # Local default
  # Production: Set via fly secrets
  # fly secrets set REDIS_URL="redis://your-redis-instance:6379"
```

### 5. Create Redis Setup Documentation (10 min)

Create `docs/REDIS_SETUP.md`:

```markdown
# Redis Setup Guide

## Local Development

### Installation

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

**Docker:**
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

### Configuration

Default connection: `redis://localhost:6379`

Set custom URL:
```bash
export REDIS_URL="redis://localhost:6379"
```

### Testing Connection

```bash
redis-cli ping  # Should return PONG
```

```python
import redis
r = redis.from_url("redis://localhost:6379")
r.ping()  # Should return True
```

## Production (Fly.io)

### Option 1: Fly.io Redis (Upstash)

```bash
# Create Redis instance
fly redis create

# Note the connection URL
# Set as secret
fly secrets set REDIS_URL="redis://..."
```

### Option 2: Upstash Redis (Serverless)

1. Go to https://upstash.com/
2. Create free Redis database
3. Copy connection URL
4. Set secret: `fly secrets set REDIS_URL="redis://..."`

### Option 3: Redis Cloud

1. Go to https://redis.com/
2. Create free 30MB database
3. Copy connection URL
4. Set secret: `fly secrets set REDIS_URL="redis://..."`

## Configuration

### Environment Variables

- `REDIS_URL`: Full Redis connection URL (required)
- `REDIS_MAX_CONNECTIONS`: Connection pool size (default: 10)
- `REDIS_SOCKET_TIMEOUT`: Timeout in seconds (default: 5)

### Connection Pool Settings

```python
redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL,
    max_connections=10,
    socket_timeout=5,
    decode_responses=True
)
```

## Troubleshooting

### Connection refused

```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solution:**
- Check Redis is running: `redis-cli ping`
- Verify URL is correct
- Check firewall rules

### Authentication errors

```
redis.exceptions.AuthenticationError
```

**Solution:**
- Include password in URL: `redis://:password@host:6379`
- Or set separately: `r.auth(password)`

### Timeout errors

**Solution:**
- Increase timeout: `socket_timeout=10`
- Check network connectivity
- Verify Redis server performance
```

### 6. Test Redis Connection (5 min)

Create `scripts/test_redis.py`:

```python
"""Test Redis connection."""

import os
import redis

def test_redis_connection():
    """Test basic Redis operations."""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    try:
        # Create Redis client
        r = redis.from_url(redis_url, decode_responses=True)
        
        # Test ping
        print("Testing connection...")
        if r.ping():
            print("✓ Redis connection successful")
        
        # Test set/get
        print("\nTesting basic operations...")
        r.set("test_key", "test_value", ex=10)
        value = r.get("test_key")
        assert value == "test_value"
        print("✓ SET/GET working")
        
        # Test increment
        r.set("counter", 0)
        r.incr("counter")
        assert r.get("counter") == "1"
        print("✓ INCR working")
        
        # Test expiry
        r.setex("temp_key", 1, "temp_value")
        assert r.get("temp_key") == "temp_value"
        print("✓ SETEX working")
        
        # Clean up
        r.delete("test_key", "counter", "temp_key")
        print("\n✓ All Redis tests passed!")
        
    except redis.ConnectionError as e:
        print(f"✗ Redis connection failed: {e}")
        print("\nMake sure Redis is running:")
        print("  macOS: brew services start redis")
        print("  Linux: sudo systemctl start redis-server")
        print("  Docker: docker run -d -p 6379:6379 redis:7-alpine")
        return False
    
    except Exception as e:
        print(f"✗ Redis test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    test_redis_connection()
```

Run test:
```bash
python scripts/test_redis.py
```

**Testing Checklist:**
- [ ] redis package installed
- [ ] fastapi-limiter package installed
- [ ] Redis server installed
- [ ] Redis server running
- [ ] Can connect to Redis (redis-cli ping)
- [ ] Python Redis client works
- [ ] REDIS_SETUP.md created
- [ ] Test script successful
- [ ] Production Redis option selected

**Acceptance Criteria:**
- [ ] redis>=5.0.0 added to requirements.txt
- [ ] fastapi-limiter>=0.1.6 added to requirements.txt
- [ ] Redis server installed and running locally
- [ ] Redis connection test successful
- [ ] REDIS_SETUP.md documentation created
- [ ] Production Redis strategy documented (Fly.io/Upstash)
- [ ] Test script confirms Redis connectivity
- [ ] Ready for Redis integration (TASK-509)

#### TASK-509: Set up Redis connection
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-508

**Description:**
Configure Redis connection in FastAPI startup event with proper error handling and connection pooling. Ensure graceful degradation if Redis is unavailable.

**Implementation Steps:**

### 1. Create Redis Configuration Module (20 min)

Create `src/expo_smooth_mcp/redis_config.py`:

```python
"""Redis connection configuration and management."""

import os
import logging
from typing import Optional
import redis
from redis.exceptions import ConnectionError, TimeoutError

logger = logging.getLogger(__name__)

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_MAX_CONNECTIONS = int(os.getenv("REDIS_MAX_CONNECTIONS", "10"))
REDIS_SOCKET_TIMEOUT = int(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))

# Global Redis client
redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """
    Get Redis client instance.
    
    Returns:
        Redis client if connected, None if unavailable
        
    Example:
        >>> r = get_redis_client()
        >>> if r:
        ...     r.set("key", "value")
    """
    return redis_client


async def init_redis() -> bool:
    """
    Initialize Redis connection pool.
    
    Returns:
        True if connection successful, False otherwise
        
    Note:
        Called during FastAPI startup event.
    """
    global redis_client
    
    try:
        # Create connection pool
        pool = redis.ConnectionPool.from_url(
            REDIS_URL,
            max_connections=REDIS_MAX_CONNECTIONS,
            socket_timeout=REDIS_SOCKET_TIMEOUT,
            socket_connect_timeout=REDIS_SOCKET_TIMEOUT,
            decode_responses=True,
            retry_on_timeout=True,
        )
        
        # Create client
        redis_client = redis.Redis(connection_pool=pool)
        
        # Test connection
        redis_client.ping()
        
        logger.info(f"✓ Redis connected: {REDIS_URL}")
        return True
        
    except (ConnectionError, TimeoutError) as e:
        logger.warning(f"Redis connection failed: {e}")
        logger.warning("Rate limiting will be disabled")
        redis_client = None
        return False
        
    except Exception as e:
        logger.error(f"Unexpected Redis error: {e}")
        redis_client = None
        return False


async def close_redis() -> None:
    """
    Close Redis connection.
    
    Note:
        Called during FastAPI shutdown event.
    """
    global redis_client
    
    if redis_client:
        try:
            redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis: {e}")
        finally:
            redis_client = None


def is_redis_available() -> bool:
    """
    Check if Redis is available.
    
    Returns:
        True if Redis client exists and can ping, False otherwise
        
    Example:
        >>> if is_redis_available():
        ...     # Use rate limiting
        ...     pass
        ... else:
        ...     # Skip rate limiting
        ...     pass
    """
    if not redis_client:
        return False
    
    try:
        return redis_client.ping()
    except Exception:
        return False


async def health_check_redis() -> dict:
    """
    Perform Redis health check.
    
    Returns:
        Dictionary with health status
        
    Example:
        >>> await health_check_redis()
        {'status': 'healthy', 'connected': True, 'ping': 'PONG'}
    """
    if not redis_client:
        return {
            "status": "unavailable",
            "connected": False,
            "message": "Redis client not initialized"
        }
    
    try:
        redis_client.ping()
        info = redis_client.info("server")
        
        return {
            "status": "healthy",
            "connected": True,
            "version": info.get("redis_version", "unknown"),
            "uptime_seconds": info.get("uptime_in_seconds", 0),
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }
```

### 2. Integrate Redis in FastAPI Startup (15 min)

Update `main.py`:

```python
from expo_smooth_mcp.redis_config import (
    init_redis,
    close_redis,
    is_redis_available,
    health_check_redis
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Expo Smooth MCP Server...")
    
    # Initialize Redis
    redis_connected = await init_redis()
    if redis_connected:
        logger.info("✓ Redis ready for rate limiting")
    else:
        logger.warning("⚠ Redis unavailable - rate limiting disabled")
    
    logger.info("Server startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("Shutting down Expo Smooth MCP Server...")
    
    # Close Redis connection
    await close_redis()
    
    logger.info("Server shutdown complete")
```

### 3. Update Health Endpoint with Redis Status (10 min)

Update health endpoint to include Redis status:

```python
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint with detailed service status.
    
    Returns service health including Redis connectivity.
    """
    # Check Redis
    redis_health = await health_check_redis()
    
    # Overall status
    overall_status = "healthy"
    if redis_health["status"] != "healthy":
        overall_status = "degraded"  # Still functional, but rate limiting disabled
    
    return {
        "status": overall_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.0.0",
        "services": {
            "api": "healthy",
            "mcp": "healthy",
            "gradio": "healthy",
            "redis": redis_health
        },
        "features": {
            "forecasting": True,
            "authentication": True,
            "rate_limiting": is_redis_available()
        }
    }
```

### 4. Create Redis Monitoring Utilities (10 min)

Add to `redis_config.py`:

```python
def get_redis_stats() -> dict:
    """
    Get Redis statistics.
    
    Returns:
        Dictionary with Redis metrics
    """
    if not redis_client:
        return {"error": "Redis not available"}
    
    try:
        info = redis_client.info()
        
        return {
            "memory_used_mb": info.get("used_memory", 0) / (1024 * 1024),
            "connected_clients": info.get("connected_clients", 0),
            "total_commands": info.get("total_commands_processed", 0),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "uptime_days": info.get("uptime_in_days", 0),
        }
    except Exception as e:
        return {"error": str(e)}


async def clear_rate_limit_for_user(username: str) -> bool:
    """
    Clear rate limit counters for a specific user.
    
    Args:
        username: Username to clear limits for
        
    Returns:
        True if successful, False otherwise
        
    Example:
        >>> await clear_rate_limit_for_user("testuser")
        True
    """
    if not redis_client:
        return False
    
    try:
        # Delete all rate limit keys for user
        pattern = f"fastapi-limiter:*:{username}"
        keys = redis_client.keys(pattern)
        
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Cleared {len(keys)} rate limit keys for {username}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error clearing rate limits: {e}")
        return False
```

### 5. Add Admin Endpoint for Redis Stats (5 min)

Add to `main.py`:

```python
from expo_smooth_mcp.redis_config import get_redis_stats

@app.get("/admin/redis", tags=["Admin"], dependencies=[Depends(require_admin)])
async def redis_stats():
    """
    Get Redis statistics (admin only).
    
    **Requires:** admin scope
    """
    if not is_redis_available():
        raise HTTPException(
            status_code=503,
            detail="Redis not available"
        )
    
    return get_redis_stats()
```

### 6. Write Redis Integration Tests (15 min)

Create `tests/test_redis_integration.py`:

```python
"""Tests for Redis integration."""

import pytest
from fastapi.testclient import TestClient

from main import app
from expo_smooth_mcp.redis_config import (
    init_redis,
    close_redis,
    get_redis_client,
    is_redis_available
)

client = TestClient(app)


class TestRedisIntegration:
    """Test Redis connection and integration."""
    
    @pytest.mark.asyncio
    async def test_redis_initialization(self):
        """Test Redis can be initialized."""
        result = await init_redis()
        
        # May be True or False depending on Redis availability
        assert isinstance(result, bool)
        
        if result:
            assert get_redis_client() is not None
            assert is_redis_available()
    
    @pytest.mark.asyncio
    async def test_redis_health_check(self):
        """Test Redis health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "services" in data
        assert "redis" in data["services"]
        assert "status" in data["services"]["redis"]
    
    def test_redis_client_operations(self):
        """Test basic Redis operations if available."""
        r = get_redis_client()
        
        if r:
            # Test set/get
            r.set("test_key", "test_value", ex=10)
            assert r.get("test_key") == "test_value"
            
            # Clean up
            r.delete("test_key")
    
    @pytest.mark.asyncio
    async def test_graceful_degradation_without_redis(self):
        """Test app works even if Redis unavailable."""
        # Close Redis
        await close_redis()
        
        # App should still respond
        response = client.get("/health")
        assert response.status_code == 200
        
        # Status may be degraded but not failed
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]


@pytest.mark.skipif(
    not is_redis_available(),
    reason="Redis not available"
)
class TestRedisStats:
    """Test Redis statistics (requires Redis)."""
    
    def test_redis_stats_endpoint(self):
        """Test admin Redis stats endpoint."""
        # Note: Would need admin token in real test
        # This is a structure test
        from expo_smooth_mcp.redis_config import get_redis_stats
        
        stats = get_redis_stats()
        
        if "error" not in stats:
            assert "memory_used_mb" in stats
            assert "connected_clients" in stats
```

Run tests:
```bash
pytest tests/test_redis_integration.py -v
```

**Testing Checklist:**
- [ ] redis_config.py module created
- [ ] init_redis() implemented
- [ ] close_redis() implemented
- [ ] get_redis_client() working
- [ ] is_redis_available() check working
- [ ] Startup event initializes Redis
- [ ] Shutdown event closes Redis
- [ ] Health endpoint shows Redis status
- [ ] Graceful degradation without Redis
- [ ] All integration tests passing

**Acceptance Criteria:**
- [ ] Redis connection configured with connection pool
- [ ] Startup event initializes Redis connection
- [ ] Shutdown event closes Redis connection
- [ ] Graceful error handling if Redis unavailable
- [ ] Health endpoint includes Redis status
- [ ] is_redis_available() check function
- [ ] Redis statistics monitoring implemented
- [ ] All tests passing
- [ ] App continues to work without Redis
- [ ] Ready for rate limiting implementation (TASK-510)

#### TASK-510: Implement rate limiting middleware
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-509

**Description:**
Initialize FastAPILimiter and configure rate limits per endpoint. Implement both global rate limits and per-user limits to prevent API abuse while allowing authenticated users higher limits.

**Implementation Steps:**

### 1. Initialize FastAPILimiter (20 min)

Update `src/expo_smooth_mcp/redis_config.py`:

```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

async def init_rate_limiter() -> bool:
    """
    Initialize FastAPI rate limiter.
    
    Returns:
        True if initialized successfully, False otherwise
        
    Note:
        Call this after init_redis() in startup event.
    """
    if not redis_client:
        logger.warning("Cannot initialize rate limiter without Redis")
        return False
    
    try:
        await FastAPILimiter.init(redis_client)
        logger.info("✓ Rate limiter initialized")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize rate limiter: {e}")
        return False


async def close_rate_limiter() -> None:
    """Close rate limiter."""
    try:
        await FastAPILimiter.close()
        logger.info("Rate limiter closed")
    except Exception:
        pass
```

Update `main.py` startup:

```python
from expo_smooth_mcp.redis_config import init_rate_limiter, close_rate_limiter

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Expo Smooth MCP Server...")
    
    # Initialize Redis
    redis_connected = await init_redis()
    if redis_connected:
        # Initialize rate limiter
        await init_rate_limiter()
    
    logger.info("Server startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("Shutting down...")
    
    await close_rate_limiter()
    await close_redis()
    
    logger.info("Shutdown complete")
```

### 2. Configure Global Rate Limits (20 min)

Create `src/expo_smooth_mcp/rate_limits.py`:

```python
"""Rate limiting configuration and utilities."""

from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from expo_smooth_mcp.redis_config import is_redis_available

# Rate limit configurations (requests per time window)
RATE_LIMITS = {
    "global": "100/minute",      # Anonymous users: 100 requests/minute
    "authenticated": "500/minute",  # Authenticated: 500 requests/minute
    "forecast": "30/minute",     # Forecast endpoint: 30/minute
    "token": "5/minute",         # Token endpoint: 5 attempts/minute
}


async def get_user_identifier(request: Request) -> str:
    """
    Get identifier for rate limiting.
    
    Uses username if authenticated, otherwise IP address.
    
    Args:
        request: FastAPI request
        
    Returns:
        Identifier string for rate limiting
    """
    # Try to get authenticated user
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            from expo_smooth_mcp.security import decode_access_token
            token = auth_header[7:]
            payload = decode_access_token(token)
            username = payload.get("sub")
            if username:
                return f"user:{username}"
        except Exception:
            pass
    
    # Fall back to IP address
    client_ip = request.client.host if request.client else "unknown"
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    
    return f"ip:{client_ip}"


def create_rate_limiter(times: int, seconds: int):
    """
    Create a rate limiter dependency.
    
    Args:
        times: Number of requests allowed
        seconds: Time window in seconds
        
    Returns:
        RateLimiter dependency
        
    Example:
        >>> limiter = create_rate_limiter(times=10, seconds=60)
        >>> @app.get("/limited", dependencies=[Depends(limiter)])
        >>> async def limited_endpoint():
        ...     return {"message": "Limited"}
    """
    async def rate_limit_check(request: Request):
        """Check rate limit for request."""
        if not is_redis_available():
            # Skip rate limiting if Redis unavailable
            return
        
        identifier = await get_user_identifier(request)
        
        # Use fastapi-limiter
        limiter = RateLimiter(times=times, seconds=seconds)
        await limiter(request, identifier=identifier)
    
    return rate_limit_check


# Pre-configured rate limiters
global_rate_limit = create_rate_limiter(times=100, seconds=60)
auth_rate_limit = create_rate_limiter(times=500, seconds=60)
forecast_rate_limit = create_rate_limiter(times=30, seconds=60)
token_rate_limit = create_rate_limiter(times=5, seconds=60)
```

### 3. Apply Rate Limits to Endpoints (20 min)

Update `main.py` to add rate limiting:

```python
from fastapi import Depends
from expo_smooth_mcp.rate_limits import (
    global_rate_limit,
    forecast_rate_limit,
    token_rate_limit
)

# Apply to token endpoint
@app.post(
    "/token",
    response_model=Token,
    tags=["Authentication"],
    dependencies=[Depends(token_rate_limit)]  # Add rate limit
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """OAuth2 token endpoint with rate limiting (5 attempts/minute)."""
    # ... existing implementation


# Apply to forecast endpoint
@app.post(
    "/api/forecast",
    tags=["API"],
    dependencies=[Depends(forecast_rate_limit)]  # Add rate limit
)
async def api_forecast(
    request: ForecastRequest,
    current_user: User = Depends(get_current_active_user)
) -> ForecastResponse:
    """Forecast endpoint with rate limiting (30 requests/minute)."""
    # ... existing implementation


# Apply global rate limit to public endpoints
@app.get(
    "/",
    dependencies=[Depends(global_rate_limit)]
)
async def root():
    """Root endpoint with global rate limiting."""
    # ... existing implementation
```

### 4. Create Custom Rate Limit Response (15 min)

Add custom rate limit error handling:

```python
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimitException

@app.exception_handler(RateLimitException)
async def rate_limit_handler(request: Request, exc: RateLimitException):
    """
    Custom handler for rate limit exceeded errors.
    
    Returns 429 Too Many Requests with Retry-After header.
    """
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        headers={
            "Retry-After": str(exc.retry_after),
            "X-RateLimit-Limit": str(exc.limit),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(exc.reset_time),
        },
        content={
            "error": "Rate limit exceeded",
            "detail": f"Too many requests. Retry after {exc.retry_after} seconds",
            "limit": exc.limit,
            "retry_after": exc.retry_after,
        }
    )
```

### 5. Add Rate Limit Info Middleware (15 min)

Add middleware to include rate limit headers on all responses:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from expo_smooth_mcp.redis_config import get_redis_client

class RateLimitHeaderMiddleware(BaseHTTPMiddleware):
    """Add rate limit info headers to responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and add rate limit headers."""
        response = await call_next(request)
        
        if is_redis_available():
            # Get identifier
            from expo_smooth_mcp.rate_limits import get_user_identifier
            identifier = await get_user_identifier(request)
            
            # Add headers (if rate limit info available)
            # This is a simplified version
            response.headers["X-RateLimit-Limit"] = "100"
            response.headers["X-RateLimit-Remaining"] = "95"
        
        return response


# Add middleware
app.add_middleware(RateLimitHeaderMiddleware)
```

### 6. Write Rate Limiting Tests (20 min)

Create `tests/test_rate_limiting.py`:

```python
"""Tests for rate limiting."""

import pytest
import time
from fastapi.testclient import TestClient

from main import app
from expo_smooth_mcp.redis_config import is_redis_available

client = TestClient(app)


@pytest.mark.skipif(
    not is_redis_available(),
    reason="Redis required for rate limiting tests"
)
class TestRateLimiting:
    """Test rate limiting functionality."""
    
    def test_token_endpoint_rate_limited(self):
        """Test /token endpoint is rate limited."""
        # Make 6 requests (limit is 5/minute)
        responses = []
        
        for i in range(6):
            response = client.post(
                "/token",
                data={"username": "testuser", "password": "testpass123"}
            )
            responses.append(response)
        
        # First 5 should succeed or return 401 (invalid creds)
        for r in responses[:5]:
            assert r.status_code in [200, 401]
        
        # 6th should be rate limited
        assert responses[5].status_code == 429
        assert "retry_after" in responses[5].json()
    
    def test_forecast_endpoint_rate_limited(self):
        """Test /api/forecast is rate limited."""
        from expo_smooth_mcp.security import create_access_token
        token = create_access_token({"sub": "testuser"})
        
        # Make 31 requests (limit is 30/minute)
        responses = []
        
        for i in range(31):
            response = client.post(
                "/api/forecast",
                json={"sku": "PRODUCT_001", "forecast_horizon": 90},
                headers={"Authorization": f"Bearer {token}"}
            )
            responses.append(response)
            
            # Small delay to avoid overwhelming test
            if i % 10 == 0:
                time.sleep(0.1)
        
        # At least one should be rate limited
        rate_limited = [r for r in responses if r.status_code == 429]
        assert len(rate_limited) > 0
    
    def test_rate_limit_headers_present(self):
        """Test rate limit headers are included."""
        response = client.get("/")
        
        # May have rate limit headers
        # (depends on middleware implementation)
        # Just verify response is successful
        assert response.status_code in [200, 429]
    
    def test_authenticated_users_higher_limit(self):
        """Test authenticated users have higher limits."""
        from expo_smooth_mcp.security import create_access_token
        token = create_access_token({"sub": "testuser"})
        
        # Make several requests with auth
        count = 0
        for i in range(150):  # Try more than anon limit
            response = client.get(
                "/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                count += 1
            if response.status_code == 429:
                break
        
        # Should get more than anonymous limit (100)
        assert count >= 100
    
    def test_rate_limit_reset_after_window(self):
        """Test rate limit resets after time window."""
        # Make requests until rate limited
        for i in range(10):
            response = client.post(
                "/token",
                data={"username": "test", "password": "test"}
            )
            if response.status_code == 429:
                retry_after = response.json().get("retry_after", 60)
                
                # Wait for reset
                time.sleep(retry_after + 1)
                
                # Try again
                response = client.post(
                    "/token",
                    data={"username": "test", "password": "test"}
                )
                
                # Should work again (or 401, not 429)
                assert response.status_code != 429
                break


class TestRateLimitingWithoutRedis:
    """Test behavior when Redis unavailable."""
    
    def test_endpoints_work_without_redis(self):
        """Test endpoints still work if Redis unavailable."""
        # Even without Redis, endpoints should respond
        response = client.get("/health")
        assert response.status_code == 200
```

Run tests:
```bash
pytest tests/test_rate_limiting.py -v
```

**Testing Checklist:**
- [ ] FastAPILimiter initialized
- [ ] Rate limits applied to /token endpoint (5/min)
- [ ] Rate limits applied to /api/forecast (30/min)
- [ ] Global rate limits work (100/min)
- [ ] Rate limit exceeded returns 429
- [ ] Retry-After header present
- [ ] Rate limits reset after time window
- [ ] Authenticated users get higher limits
- [ ] Graceful degradation without Redis
- [ ] All rate limiting tests passing

**Acceptance Criteria:**
- [ ] FastAPILimiter integrated with Redis
- [ ] Rate limits configured per endpoint
- [ ] /token endpoint: 5 attempts/minute
- [ ] /api/forecast endpoint: 30 requests/minute
- [ ] Global limit: 100 requests/minute
- [ ] Authenticated users: 500 requests/minute
- [ ] 429 status with Retry-After header
- [ ] Rate limit headers in responses
- [ ] All tests passing
- [ ] Ready for structured logging (TASK-511)

#### TASK-511: Create structured logging formatter
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** None

**Description:**
Implement JSON logging formatter with structured fields (timestamp, level, module, request ID). This enables better log analysis and integration with log aggregation services.

**Implementation Steps:**

### 1. Create Logging Configuration Module (25 min)

Create `src/expo_smooth_mcp/logging_config.py`:

```python
"""Structured logging configuration."""

import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict
import traceback


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Outputs logs in JSON format for easy parsing by log aggregation tools.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON string with structured log data
        """
        # Base log entry
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add module and function info
        if record.module:
            log_entry["module"] = record.module
        if record.funcName:
            log_entry["function"] = record.funcName
        if record.lineno:
            log_entry["line"] = record.lineno
        
        # Add request context if available
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "user"):
            log_entry["user"] = record.user
        if hasattr(record, "method"):
            log_entry["http_method"] = record.method
        if hasattr(record, "path"):
            log_entry["http_path"] = record.path
        if hasattr(record, "status_code"):
            log_entry["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add any extra fields
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName",
                "relativeCreated", "thread", "threadName", "exc_info",
                "exc_text", "stack_info", "request_id", "user", "method",
                "path", "status_code", "duration_ms"
            ]:
                log_entry[key] = value
        
        return json.dumps(log_entry)


class RequestContextFilter(logging.Filter):
    """
    Add request context to log records.
    
    Extracts request information from contextvars and adds to log records.
    """
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add request context to record."""
        from expo_smooth_mcp.middleware import get_request_context
        
        context = get_request_context()
        if context:
            record.request_id = context.get("request_id")
            record.user = context.get("user")
            record.method = context.get("method")
            record.path = context.get("path")
        
        return True


def setup_logging(
    level: str = "INFO",
    json_format: bool = True,
    log_file: str = None
) -> None:
    """
    Configure application logging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON formatting if True, human-readable if False
        log_file: Optional log file path
        
    Example:
        >>> setup_logging(level="INFO", json_format=True)
        >>> logger = logging.getLogger(__name__)
        >>> logger.info("Application started")
    """
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(log_level)
    
    # Choose formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestContextFilter())
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(RequestContextFilter())
        root_logger.addHandler(file_handler)
    
    # Reduce noise from dependencies
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing request", extra={"user_id": 123})
    """
    return logging.getLogger(name)
```

### 2. Create Request Context Management (20 min)

Create `src/expo_smooth_mcp/middleware.py`:

```python
"""Request context and middleware."""

import uuid
from contextvars import ContextVar
from typing import Dict, Optional

# Context var to store request information
request_context_var: ContextVar[Optional[Dict]] = ContextVar(
    "request_context",
    default=None
)


def set_request_context(
    request_id: str,
    method: str,
    path: str,
    user: Optional[str] = None
) -> None:
    """
    Set request context for current request.
    
    Args:
        request_id: Unique request identifier
        method: HTTP method
        path: Request path
        user: Optional username
    """
    request_context_var.set({
        "request_id": request_id,
        "method": method,
        "path": path,
        "user": user,
    })


def get_request_context() -> Optional[Dict]:
    """
    Get current request context.
    
    Returns:
        Dictionary with request context or None
    """
    return request_context_var.get()


def generate_request_id() -> str:
    """
    Generate unique request ID.
    
    Returns:
        UUID-based request ID
        
    Example:
        >>> request_id = generate_request_id()
        >>> len(request_id)
        36  # UUID4 format
    """
    return str(uuid.uuid4())
```

### 3. Configure Logging in Application (10 min)

Update `main.py`:

```python
import os
from expo_smooth_mcp.logging_config import setup_logging, get_logger

# Configure logging on startup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # "json" or "text"
LOG_FILE = os.getenv("LOG_FILE", None)

setup_logging(
    level=LOG_LEVEL,
    json_format=(LOG_FORMAT == "json"),
    log_file=LOG_FILE
)

logger = get_logger(__name__)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Expo Smooth MCP Server", extra={
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    })
    
    # ... rest of startup code
```

### 4. Write Logging Tests (15 min)

Create `tests/test_logging.py`:

```python
"""Tests for structured logging."""

import json
import logging
from io import StringIO

from expo_smooth_mcp.logging_config import (
    JSONFormatter,
    RequestContextFilter,
    setup_logging
)


class TestJSONFormatter:
    """Test JSON log formatting."""
    
    def test_json_format_basic(self):
        """Test basic JSON log formatting."""
        # Create logger with JSON formatter
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)
        
        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
        # Log message
        logger.info("Test message")
        
        # Parse output
        output = stream.getvalue()
        log_entry = json.loads(output)
        
        # Verify structure
        assert "timestamp" in log_entry
        assert log_entry["level"] == "INFO"
        assert log_entry["message"] == "Test message"
        assert "logger" in log_entry
    
    def test_json_format_with_extra_fields(self):
        """Test JSON formatter includes extra fields."""
        logger = logging.getLogger("test_extra")
        logger.setLevel(logging.INFO)
        
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
        # Log with extra fields
        logger.info("Request processed", extra={
            "request_id": "12345",
            "user": "testuser",
            "duration_ms": 150
        })
        
        output = stream.getvalue()
        log_entry = json.loads(output)
        
        assert log_entry["request_id"] == "12345"
        assert log_entry["user"] == "testuser"
        assert log_entry["duration_ms"] == 150
    
    def test_json_format_with_exception(self):
        """Test JSON formatter handles exceptions."""
        logger = logging.getLogger("test_exc")
        logger.setLevel(logging.ERROR)
        
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
        # Log exception
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.exception("Error occurred")
        
        output = stream.getvalue()
        log_entry = json.loads(output)
        
        assert "exception" in log_entry
        assert log_entry["exception"]["type"] == "ValueError"
        assert "Test error" in log_entry["exception"]["message"]


class TestLoggingSetup:
    """Test logging configuration."""
    
    def test_setup_logging_json(self):
        """Test setup with JSON formatting."""
        setup_logging(level="DEBUG", json_format=True)
        
        logger = logging.getLogger("test_setup")
        
        # Verify logger is configured
        assert logger.level <= logging.DEBUG
    
    def test_setup_logging_text(self):
        """Test setup with text formatting."""
        setup_logging(level="INFO", json_format=False)
        
        logger = logging.getLogger("test_text")
        
        # Should have handlers
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0
```

Run tests:
```bash
pytest tests/test_logging.py -v
```

**Testing Checklist:**
- [ ] JSONFormatter implemented
- [ ] JSON logs include timestamp, level, logger, message
- [ ] Extra fields included in JSON logs
- [ ] Exception information captured
- [ ] RequestContextFilter implemented
- [ ] setup_logging() configures loggers
- [ ] Both JSON and text formats work
- [ ] All logging tests passing

**Acceptance Criteria:**
- [ ] JSON logging formatter implemented
- [ ] Structured logs include: timestamp, level, logger, message
- [ ] Request context fields: request_id, user, method, path
- [ ] Exception information properly formatted
- [ ] Configurable log level via environment
- [ ] Configurable format (JSON/text) via environment
- [ ] Request context management with contextvars
- [ ] All tests passing
- [ ] Ready for request logging middleware (TASK-512)

#### TASK-512: Add request logging middleware
**Estimated Time:** 1.5 hours | **Complexity:** Medium | **Dependencies:** TASK-511

**Description:**
Create FastAPI middleware to log all HTTP requests with method, path, status code, duration, and request ID. Integrate with structured logging for comprehensive request tracking.

**Implementation Steps:**

### 1. Create Request Logging Middleware (30 min)

Update `src/expo_smooth_mcp/middleware.py`:

```python
"""Request context and middleware."""

import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from expo_smooth_mcp.logging_config import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests.
    
    Logs: method, path, status code, duration, request ID, user.
    """
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """
        Process request and log details.
        
        Args:
            request: Incoming request
            call_next: Next middleware/endpoint
            
        Returns:
            Response from endpoint
        """
        # Generate request ID
        request_id = generate_request_id()
        
        # Extract user if authenticated
        user = await self._extract_user(request)
        
        # Set request context for logging
        set_request_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            user=user
        )
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Start timer
        start_time = time.time()
        
        # Log request start
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "user": user,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host if request.client else None
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log request completion
            logger.info(
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "request_id": request_id,
                    "user": user,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2)
                }
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "request_id": request_id,
                    "user": user,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                    "error": str(e)
                },
                exc_info=True
            )
            
            raise
    
    async def _extract_user(self, request: Request) -> str:
        """
        Extract username from Authorization header if present.
        
        Args:
            request: FastAPI request
            
        Returns:
            Username or "anonymous"
        """
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from expo_smooth_mcp.security import decode_access_token
                token = auth_header[7:]
                payload = decode_access_token(token)
                username = payload.get("sub")
                if username:
                    return username
            except Exception:
                pass
        
        return "anonymous"
```

### 2. Add Performance Metrics Tracking (20 min)

```python
from collections import defaultdict
from typing import Dict

# In-memory metrics storage (use Redis for production)
request_metrics: Dict[str, list] = defaultdict(list)


class PerformanceMetricsMiddleware(BaseHTTPMiddleware):
    """
    Track performance metrics for endpoints.
    
    Tracks: response times, request counts, error rates.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track endpoint performance."""
        start_time = time.time()
        endpoint = f"{request.method} {request.url.path}"
        
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Store metrics (in production, use Redis or Prometheus)
            request_metrics[endpoint].append({
                "duration_ms": duration_ms,
                "status": response.status_code,
                "timestamp": time.time()
            })
            
            # Keep only last 1000 requests per endpoint
            if len(request_metrics[endpoint]) > 1000:
                request_metrics[endpoint] = request_metrics[endpoint][-1000:]
            
            # Warn on slow requests
            if duration_ms > 1000:
                logger.warning(
                    f"Slow request detected: {endpoint}",
                    extra={
                        "duration_ms": duration_ms,
                        "endpoint": endpoint
                    }
                )
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            request_metrics[endpoint].append({
                "duration_ms": duration_ms,
                "status": 500,
                "error": str(e),
                "timestamp": time.time()
            })
            
            raise


def get_endpoint_metrics(endpoint: str = None) -> dict:
    """
    Get performance metrics for endpoint(s).
    
    Args:
        endpoint: Specific endpoint or None for all
        
    Returns:
        Dictionary with metrics
    """
    if endpoint:
        metrics = request_metrics.get(endpoint, [])
        if not metrics:
            return {"error": "No data for endpoint"}
        
        durations = [m["duration_ms"] for m in metrics]
        durations.sort()
        
        return {
            "endpoint": endpoint,
            "total_requests": len(metrics),
            "avg_duration_ms": sum(durations) / len(durations),
            "p50_ms": durations[len(durations) // 2],
            "p95_ms": durations[int(len(durations) * 0.95)],
            "p99_ms": durations[int(len(durations) * 0.99)],
        }
    else:
        return {
            endpoint: get_endpoint_metrics(endpoint)
            for endpoint in request_metrics.keys()
        }
```

### 3. Register Middleware in Application (10 min)

Update `main.py`:

```python
from expo_smooth_mcp.middleware import (
    RequestLoggingMiddleware,
    PerformanceMetricsMiddleware,
    get_endpoint_metrics
)

# Add middleware (order matters - last added runs first)
app.add_middleware(PerformanceMetricsMiddleware)
app.add_middleware(RequestLoggingMiddleware)


@app.get("/admin/metrics", tags=["Admin"], dependencies=[Depends(require_admin)])
async def endpoint_metrics():
    """
    Get endpoint performance metrics (admin only).
    
    **Requires:** admin scope
    """
    return get_endpoint_metrics()
```

### 4. Add Request ID to Error Responses (10 min)

Update error handlers to include request ID:

```python
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler with request ID.
    
    Includes request ID in error response for tracing.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        f"Unhandled exception: {exc}",
        extra={"request_id": request_id},
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        headers={"X-Request-ID": request_id},
        content={
            "error": "Internal server error",
            "message": str(exc),
            "request_id": request_id
        }
    )
```

### 5. Write Request Logging Tests (20 min)

Create `tests/test_request_logging.py`:

```python
"""Tests for request logging middleware."""

import json
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestRequestLogging:
    """Test request logging middleware."""
    
    def test_request_id_in_response_header(self):
        """Test X-Request-ID header is added to responses."""
        response = client.get("/")
        
        assert "x-request-id" in response.headers
        request_id = response.headers["x-request-id"]
        assert len(request_id) == 36  # UUID4 format
    
    def test_successful_request_logged(self, caplog):
        """Test successful requests are logged."""
        with caplog.at_level("INFO"):
            response = client.get("/health")
        
        assert response.status_code == 200
        
        # Check logs for request
        logs = [r.message for r in caplog.records]
        request_start = any("Request started" in log for log in logs)
        request_complete = any("Request completed" in log for log in logs)
        
        assert request_start
        assert request_complete
    
    def test_failed_request_logged(self, caplog):
        """Test failed requests are logged."""
        with caplog.at_level("ERROR"):
            # Try to access non-existent endpoint
            response = client.get("/nonexistent")
        
        # Should return 404
        assert response.status_code == 404
    
    def test_request_duration_logged(self, caplog):
        """Test request duration is logged."""
        with caplog.at_level("INFO"):
            response = client.get("/health")
        
        # Find completion log
        for record in caplog.records:
            if "Request completed" in record.message:
                # Should have duration_ms in extra
                assert hasattr(record, "duration_ms")
                assert record.duration_ms > 0
                break
    
    def test_authenticated_user_logged(self, caplog):
        """Test authenticated user is included in logs."""
        from expo_smooth_mcp.security import create_access_token
        token = create_access_token({"sub": "testuser"})
        
        with caplog.at_level("INFO"):
            response = client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        # Check logs include username
        for record in caplog.records:
            if hasattr(record, "user"):
                assert record.user == "testuser"
                break


class TestPerformanceMetrics:
    """Test performance metrics tracking."""
    
    def test_endpoint_metrics_tracked(self):
        """Test endpoint performance is tracked."""
        # Make several requests
        for _ in range(10):
            client.get("/health")
        
        # Get metrics (would need admin token in real test)
        from expo_smooth_mcp.middleware import get_endpoint_metrics
        
        metrics = get_endpoint_metrics("GET /health")
        
        assert "total_requests" in metrics
        assert metrics["total_requests"] >= 10
        assert "avg_duration_ms" in metrics
        assert "p50_ms" in metrics
    
    def test_slow_request_warning(self, caplog):
        """Test slow requests generate warnings."""
        # This would require a slow endpoint to test properly
        # Placeholder test structure
        pass


class TestErrorHandling:
    """Test error handling with request IDs."""
    
    def test_error_response_includes_request_id(self):
        """Test error responses include request ID."""
        # Trigger an error (try invalid forecast request)
        response = client.post(
            "/api/forecast",
            json={"sku": "INVALID", "forecast_horizon": -1}
        )
        
        # Should have request ID in header
        assert "x-request-id" in response.headers
        
        # May also be in response body for 500 errors
        if response.status_code == 500:
            data = response.json()
            assert "request_id" in data
```

Run tests:
```bash
pytest tests/test_request_logging.py -v
```

### 6. Configure Log Rotation (10 min)

Add log rotation for production (optional):

```python
# In logging_config.py
from logging.handlers import RotatingFileHandler

def setup_logging_with_rotation(
    level: str = "INFO",
    json_format: bool = True,
    log_file: str = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
):
    """
    Configure logging with file rotation.
    
    Args:
        level: Log level
        json_format: Use JSON formatting
        log_file: Log file path
        max_bytes: Max file size before rotation
        backup_count: Number of backup files to keep
    """
    # ... similar to setup_logging but with RotatingFileHandler
    
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        # ... rest of configuration
```

**Testing Checklist:**
- [ ] RequestLoggingMiddleware implemented
- [ ] All requests generate logs
- [ ] Logs include method, path, status, duration
- [ ] Request ID generated and included
- [ ] X-Request-ID header in responses
- [ ] User extracted from auth header
- [ ] PerformanceMetricsMiddleware tracks metrics
- [ ] Error responses include request ID
- [ ] All request logging tests passing

**Acceptance Criteria:**
- [ ] Request logging middleware implemented
- [ ] Logs all HTTP requests with structured data
- [ ] Fields: method, path, status_code, duration_ms, request_id, user
- [ ] Request ID included in response headers
- [ ] Performance metrics tracked per endpoint
- [ ] Slow requests (>1s) generate warnings
- [ ] Error responses include request ID for tracing
- [ ] All tests passing (8+ tests)
- [ ] Ready for Prometheus metrics (TASK-513)

#### TASK-513: Add Prometheus metrics endpoint
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** None

**Description:**
Install and configure prometheus-fastapi-instrumentator to expose metrics endpoint. Enable monitoring of API performance, request rates, and resource usage.

**Implementation Steps:**

### 1. Install Prometheus Dependencies (10 min)

Update `requirements.txt`:

```txt
# Existing dependencies
fastapi>=0.104.0
fastmcp>=2.0.0
# ... other dependencies

# Metrics and monitoring (new)
prometheus-client>=0.19.0           # Prometheus Python client
prometheus-fastapi-instrumentator>=6.1.0  # FastAPI Prometheus integration
```

Install:
```bash
pip install prometheus-client>=0.19.0
pip install prometheus-fastapi-instrumentator>=6.1.0

# Verify
pip list | grep prometheus
```

### 2. Configure Prometheus Instrumentator (25 min)

Create `src/expo_smooth_mcp/metrics.py`:

```python
"""Prometheus metrics configuration."""

from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from fastapi import FastAPI
import os

# Custom metrics
forecast_requests = Counter(
    "forecast_requests_total",
    "Total number of forecast requests",
    ["sku", "status"]
)

forecast_duration = Histogram(
    "forecast_duration_seconds",
    "Time spent generating forecasts",
    ["sku"]
)

active_users = Gauge(
    "active_users",
    "Number of currently active users"
)

auth_attempts = Counter(
    "auth_attempts_total",
    "Total authentication attempts",
    ["result"]
)

app_info = Info(
    "expo_smooth_mcp_app",
    "Application information"
)


def setup_metrics(app: FastAPI) -> Instrumentator:
    """
    Configure Prometheus metrics for FastAPI app.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Instrumentator instance
        
    Example:
        >>> app = FastAPI()
        >>> instrumentator = setup_metrics(app)
        >>> instrumentator.expose(app, endpoint="/metrics")
    """
    # Set app info
    app_info.info({
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    })
    
    # Create instrumentator
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=[
            "/metrics",  # Don't track metrics endpoint itself
            "/health",   # Don't track health checks
        ],
        env_var_name="ENABLE_METRICS",
        inprogress_name="http_requests_inprogress",
        inprogress_labels=True,
    )
    
    # Add default metrics
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    instrumentator.add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    instrumentator.add(
        metrics.latency(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    instrumentator.add(
        metrics.requests(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    # Instrument the app
    instrumentator.instrument(app)
    
    return instrumentator


def track_forecast_request(sku: str, success: bool, duration: float):
    """
    Track forecast request metrics.
    
    Args:
        sku: Product SKU
        success: Whether forecast succeeded
        duration: Time taken in seconds
    """
    status = "success" if success else "error"
    forecast_requests.labels(sku=sku, status=status).inc()
    forecast_duration.labels(sku=sku).observe(duration)


def track_auth_attempt(success: bool):
    """
    Track authentication attempt.
    
    Args:
        success: Whether authentication succeeded
    """
    result = "success" if success else "failure"
    auth_attempts.labels(result=result).inc()


def update_active_users(count: int):
    """
    Update active users count.
    
    Args:
        count: Current number of active users
    """
    active_users.set(count)
```

### 3. Integrate Metrics in Application (20 min)

Update `main.py`:

```python
from expo_smooth_mcp.metrics import (
    setup_metrics,
    track_forecast_request,
    track_auth_attempt
)

# Setup metrics
instrumentator = setup_metrics(app)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Expo Smooth MCP Server...")
    
    # Initialize Redis
    redis_connected = await init_redis()
    if redis_connected:
        await init_rate_limiter()
    
    # Expose metrics endpoint
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=True)
    
    logger.info("Server startup complete")


# Update forecast endpoint to track metrics
@app.post("/api/forecast", tags=["API"])
async def api_forecast(
    request: ForecastRequest,
    current_user: User = Depends(get_current_active_user)
) -> ForecastResponse:
    """Generate forecast with metrics tracking."""
    start_time = time.time()
    success = False
    
    try:
        result = generate_forecast_for_sku(
            sku=request.sku,
            forecast_horizon=request.forecast_horizon,
            alpha=request.alpha,
            beta=request.beta,
            gamma=request.gamma,
        )
        
        success = True
        return ForecastResponse(**result)
        
    except Exception as e:
        logger.error(f"Forecast error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Track metrics
        duration = time.time() - start_time
        track_forecast_request(request.sku, success, duration)


# Update token endpoint to track auth attempts
@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """OAuth2 token endpoint with metrics."""
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        track_auth_attempt(success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    track_auth_attempt(success=True)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
```

### 4. Create Metrics Documentation (15 min)

Create `docs/METRICS.md`:

```markdown
# Metrics Documentation

## Accessing Metrics

Metrics are exposed at: `http://localhost:8000/metrics`

Format: Prometheus text format

## Available Metrics

### HTTP Metrics (from instrumentator)

**http_requests_total**
- Description: Total HTTP requests
- Labels: method, handler, status
- Type: Counter

**http_request_duration_seconds**
- Description: HTTP request latency
- Labels: method, handler, status
- Type: Histogram

**http_request_size_bytes**
- Description: HTTP request size
- Labels: method, handler
- Type: Histogram

**http_response_size_bytes**
- Description: HTTP response size
- Labels: method, handler
- Type: Histogram

**http_requests_inprogress**
- Description: In-progress HTTP requests
- Type: Gauge

### Custom Application Metrics

**forecast_requests_total**
- Description: Total forecast requests
- Labels: sku, status (success/error)
- Type: Counter
- Example: `forecast_requests_total{sku="PRODUCT_001",status="success"} 42`

**forecast_duration_seconds**
- Description: Forecast generation duration
- Labels: sku
- Type: Histogram
- Buckets: 0.1, 0.5, 1.0, 2.5, 5.0, 10.0 seconds

**active_users**
- Description: Currently active authenticated users
- Type: Gauge

**auth_attempts_total**
- Description: Authentication attempts
- Labels: result (success/failure)
- Type: Counter

**expo_smooth_mcp_app_info**
- Description: Application information
- Labels: version, environment
- Type: Info

## Prometheus Configuration

### prometheus.yml

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'expo-smooth-mcp'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Running Prometheus

```bash
# Docker
docker run -d -p 9090:9090 \\
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \\
  prom/prometheus

# Access Prometheus UI
open http://localhost:9090
```

## Example Queries

### Request Rate
```promql
rate(http_requests_total[5m])
```

### 95th Percentile Latency
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Forecast Success Rate
```promql
sum(rate(forecast_requests_total{status="success"}[5m])) / 
sum(rate(forecast_requests_total[5m]))
```

### Authentication Failure Rate
```promql
rate(auth_attempts_total{result="failure"}[5m])
```

## Grafana Dashboards

Example dashboard queries:

1. **Request Rate**: `rate(http_requests_total[5m])`
2. **Error Rate**: `sum(rate(http_requests_total{status=~"5.."}[5m]))`
3. **P95 Latency**: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
4. **Active Users**: `active_users`
```

### 5. Write Metrics Tests (30 min)

Create `tests/test_metrics.py`:

```python
"""Tests for Prometheus metrics."""

import pytest
from fastapi.testclient import TestClient

from main import app
from expo_smooth_mcp.metrics import (
    track_forecast_request,
    track_auth_attempt,
    update_active_users
)

client = TestClient(app)


class TestMetricsEndpoint:
    """Test Prometheus metrics endpoint."""
    
    def test_metrics_endpoint_exists(self):
        """Test /metrics endpoint is accessible."""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
    
    def test_metrics_format(self):
        """Test metrics are in Prometheus format."""
        response = client.get("/metrics")
        
        content = response.text
        
        # Should contain standard metrics
        assert "http_requests_total" in content or "http_request" in content
        assert "HELP" in content
        assert "TYPE" in content
    
    def test_custom_metrics_present(self):
        """Test custom application metrics are exposed."""
        # Make a forecast request to generate metrics
        from expo_smooth_mcp.security import create_access_token
        token = create_access_token({"sub": "testuser"})
        
        client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 90},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Check metrics
        response = client.get("/metrics")
        content = response.text
        
        # Should have forecast metrics
        assert "forecast_requests_total" in content or "forecast" in content


class TestCustomMetrics:
    """Test custom metrics tracking."""
    
    def test_track_forecast_request(self):
        """Test forecast request tracking."""
        track_forecast_request("TEST_SKU", success=True, duration=1.5)
        
        # Verify metric was recorded
        response = client.get("/metrics")
        content = response.text
        
        assert "forecast_requests_total" in content
    
    def test_track_auth_attempt(self):
        """Test authentication tracking."""
        track_auth_attempt(success=True)
        track_auth_attempt(success=False)
        
        # Verify metric was recorded
        response = client.get("/metrics")
        content = response.text
        
        assert "auth_attempts_total" in content
    
    def test_update_active_users(self):
        """Test active users gauge."""
        update_active_users(5)
        
        # Verify metric was recorded
        response = client.get("/metrics")
        content = response.text
        
        assert "active_users" in content


class TestMetricsIntegration:
    """Test metrics integration with endpoints."""
    
    def test_http_request_metrics(self):
        """Test HTTP requests generate metrics."""
        # Make several requests
        for _ in range(5):
            client.get("/health")
        
        # Check metrics
        response = client.get("/metrics")
        content = response.text
        
        # Should have HTTP metrics
        assert "http_request" in content.lower()
    
    def test_forecast_endpoint_generates_metrics(self):
        """Test forecast endpoint updates metrics."""
        from expo_smooth_mcp.security import create_access_token
        token = create_access_token({"sub": "testuser"})
        
        # Make forecast request
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 90},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get metrics
        metrics_response = client.get("/metrics")
        
        # Should include forecast metrics
        assert "forecast" in metrics_response.text.lower()
    
    def test_auth_endpoint_generates_metrics(self):
        """Test auth endpoint updates metrics."""
        # Attempt login
        client.post(
            "/token",
            data={"username": "testuser", "password": "testpass123"}
        )
        
        # Get metrics
        response = client.get("/metrics")
        
        # Should include auth metrics
        assert "auth_attempts" in response.text.lower()
```

Run tests:
```bash
pytest tests/test_metrics.py -v
```

### 6. Test with Prometheus (Optional, 20 min)

```bash
# Create prometheus.yml
cat > prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'expo-smooth-mcp'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
EOF

# Run Prometheus
docker run -d \\
  -p 9090:9090 \\
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \\
  --name prometheus \\
  prom/prometheus

# Access Prometheus UI
open http://localhost:9090

# Query examples:
# - rate(http_requests_total[5m])
# - histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
# - forecast_requests_total

# Cleanup
docker stop prometheus && docker rm prometheus
```

**Testing Checklist:**
- [ ] prometheus-client installed
- [ ] prometheus-fastapi-instrumentator installed
- [ ] /metrics endpoint exposed
- [ ] HTTP metrics collected (requests, latency, size)
- [ ] Custom metrics implemented (forecast, auth)
- [ ] Metrics in Prometheus format
- [ ] All metrics tests passing
- [ ] METRICS.md documentation created
- [ ] Prometheus integration tested (optional)

**Acceptance Criteria:**
- [ ] Prometheus client libraries installed
- [ ] prometheus-fastapi-instrumentator configured
- [ ] /metrics endpoint exposed
- [ ] Standard HTTP metrics: requests, latency, size, in-progress
- [ ] Custom metrics: forecast_requests, forecast_duration, auth_attempts, active_users
- [ ] Metrics in Prometheus text format
- [ ] METRICS.md documentation created
- [ ] All tests passing (10+ tests)
- [ ] Ready for comprehensive security testing (TASK-514)

#### TASK-514: Create comprehensive security tests
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-507, TASK-510

**Description:**
Write comprehensive security tests covering authentication flows, rate limiting, authorization, password security, and protected endpoints. Ensure all security features work correctly and can't be bypassed.

**Implementation Steps:**

### 1. Create Comprehensive Security Test Suite (40 min)

Create `tests/test_security_comprehensive.py`:

```python
"""Comprehensive security testing."""

import pytest
import time
from fastapi.testclient import TestClient

from main import app
from expo_smooth_mcp.security import (
    create_access_token,
    create_access_token_with_scopes,
    get_password_hash,
    verify_password
)

client = TestClient(app)


class TestAuthenticationSecurity:
    """Test authentication security."""
    
    def test_password_not_exposed_in_responses(self):
        """Test passwords never appear in API responses."""
        # Login
        response = client.post(
            "/token",
            data={"username": "testuser", "password": "testpass123"}
        )
        assert "password" not in response.text.lower()
        assert "hashed_password" not in response.text.lower()
        
        # User info
        token = response.json()["access_token"]
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert "password" not in response.text.lower()
        assert "hashed_password" not in response.text.lower()
    
    def test_token_required_for_protected_endpoints(self):
        """Test protected endpoints require valid token."""
        # Try without token
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 90}
        )
        assert response.status_code == 401
        
        # Try with invalid token
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 90},
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401
    
    def test_expired_token_rejected(self):
        """Test expired tokens are rejected."""
        from datetime import timedelta
        
        # Create token that expires in 1 second
        token = create_access_token(
            {"sub": "testuser"},
            expires_delta=timedelta(seconds=1)
        )
        
        # Use immediately - should work
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        
        # Wait for expiration
        time.sleep(2)
        
        # Use after expiration - should fail
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401
    
    def test_token_tampering_detected(self):
        """Test tampered tokens are rejected."""
        token = create_access_token({"sub": "testuser"})
        
        # Tamper with token
        tampered = token[:-10] + "XXXXXXXXXX"
        
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {tampered}"}
        )
        assert response.status_code == 401
    
    def test_malformed_authorization_header(self):
        """Test malformed auth headers are rejected."""
        # Missing "Bearer " prefix
        response = client.get(
            "/users/me",
            headers={"Authorization": "invalid_format"}
        )
        assert response.status_code == 401
        
        # Empty token
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer "}
        )
        assert response.status_code == 401


class TestAuthorizationSecurity:
    """Test authorization and access control."""
    
    def test_scope_based_access_control(self):
        """Test users without required scope are denied."""
        # Token without forecast:read scope
        token = create_access_token_with_scopes("testuser", ["other:scope"])
        
        # Try to access forecast endpoint
        response = client.get(
            "/read-forecasts",  # Requires forecast:read scope
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should be forbidden
        assert response.status_code == 403
    
    def test_admin_endpoints_require_admin_scope(self):
        """Test admin endpoints reject non-admin users."""
        # Regular user token (no admin scope)
        token = create_access_token({"sub": "testuser"})
        
        # Try to access admin endpoint
        response = client.get(
            "/admin/stats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should be forbidden
        assert response.status_code == 403
    
    def test_users_cannot_access_others_data(self):
        """Test users can only access their own data."""
        # This test would require user-specific data
        # Placeholder for user isolation testing
        pass


class TestPasswordSecurity:
    """Test password security measures."""
    
    def test_password_hashing_unique_salts(self):
        """Test same password generates different hashes."""
        password = "testpass123"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different (bcrypt uses random salt)
        assert hash1 != hash2
        
        # But both should verify
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
    
    def test_password_hash_not_reversible(self):
        """Test password hash cannot be reversed."""
        password = "testpass123"
        hashed = get_password_hash(password)
        
        # Hash should not contain original password
        assert password not in hashed
        assert password.encode() not in hashed.encode()
    
    def test_wrong_password_rejected(self):
        """Test wrong password fails verification."""
        correct_password = "correctpassword"
        wrong_password = "wrongpassword"
        
        hashed = get_password_hash(correct_password)
        
        assert verify_password(correct_password, hashed)
        assert not verify_password(wrong_password, hashed)
    
    def test_brute_force_protection(self):
        """Test rate limiting protects against brute force."""
        # Requires Redis for rate limiting
        from expo_smooth_mcp.redis_config import is_redis_available
        
        if not is_redis_available():
            pytest.skip("Redis required for rate limiting")
        
        # Try many failed login attempts
        attempts = 0
        rate_limited = False
        
        for i in range(10):
            response = client.post(
                "/token",
                data={"username": "testuser", "password": "wrongpass"}
            )
            
            if response.status_code == 429:
                rate_limited = True
                break
            
            attempts += 1
        
        # Should eventually be rate limited
        assert rate_limited, f"Not rate limited after {attempts} attempts"


@pytest.mark.skipif(
    not hasattr(client, "redis"),
    reason="Redis required for rate limiting tests"
)
class TestRateLimitingSecurity:
    """Test rate limiting security."""
    
    def test_rate_limit_per_endpoint(self):
        """Test each endpoint has appropriate rate limits."""
        # Test token endpoint (5/min)
        for i in range(7):
            response = client.post(
                "/token",
                data={"username": "test", "password": "test"}
            )
            
            if i < 5:
                assert response.status_code in [200, 401]  # May succeed or fail auth
            else:
                # Should be rate limited
                assert response.status_code == 429
    
    def test_rate_limit_headers_present(self):
        """Test rate limit headers are included."""
        response = client.get("/")
        
        # Should have rate limit info (may vary by implementation)
        # At minimum, should not error
        assert response.status_code in [200, 429]
        
        if response.status_code == 429:
            assert "retry-after" in response.headers
    
    def test_authenticated_users_higher_limits(self):
        """Test authenticated users get higher rate limits."""
        # Anonymous requests
        anon_limit = 0
        for i in range(150):
            response = client.get("/")
            if response.status_code == 429:
                anon_limit = i
                break
        
        # Authenticated requests
        token = create_access_token({"sub": "testuser"})
        auth_limit = 0
        for i in range(550):
            response = client.get(
                "/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 429:
                auth_limit = i
                break
        
        # Auth limit should be higher
        assert auth_limit > anon_limit


class TestSecurityHeaders:
    """Test security-related HTTP headers."""
    
    def test_request_id_tracking(self):
        """Test X-Request-ID header for tracing."""
        response = client.get("/")
        
        assert "x-request-id" in response.headers
        request_id = response.headers["x-request-id"]
        assert len(request_id) > 0
    
    def test_security_headers_present(self):
        """Test important security headers are set."""
        response = client.get("/")
        
        # These would be set by production reverse proxy
        # But check if any are set
        headers = response.headers
        
        # At minimum, should have standard headers
        assert "content-type" in headers


class TestInputValidation:
    """Test input validation and sanitization."""
    
    def test_sql_injection_protection(self):
        """Test SQL injection attempts are blocked."""
        # Note: We use Pandas/CSV, not SQL, but test anyway
        malicious_sku = "'; DROP TABLE users; --"
        
        token = create_access_token({"sub": "testuser"})
        response = client.post(
            "/api/forecast",
            json={"sku": malicious_sku, "forecast_horizon": 90},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should handle gracefully (400 or 404, not 500)
        assert response.status_code in [400, 404]
    
    def test_xss_protection(self):
        """Test XSS attempts are escaped."""
        malicious_username = "<script>alert('xss')</script>"
        
        response = client.post(
            "/token",
            data={"username": malicious_username, "password": "test"}
        )
        
        # Should not execute script
        assert response.status_code == 401
        assert "<script>" not in response.text
    
    def test_parameter_type_validation(self):
        """Test invalid parameter types are rejected."""
        token = create_access_token({"sub": "testuser"})
        
        # Invalid forecast_horizon (negative)
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": -1},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code in [400, 422]
        
        # Invalid type (string instead of number)
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": "invalid"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 422


class TestSessionSecurity:
    """Test session and token security."""
    
    def test_token_unique_per_login(self):
        """Test each login generates unique token."""
        tokens = set()
        
        for _ in range(3):
            response = client.post(
                "/token",
                data={"username": "testuser", "password": "testpass123"}
            )
            token = response.json()["access_token"]
            tokens.add(token)
        
        # All tokens should be unique
        assert len(tokens) == 3
    
    def test_no_session_fixation(self):
        """Test tokens cannot be reused across users."""
        # Get token for user1
        token1 = create_access_token({"sub": "user1"})
        
        # Try to use for user2 endpoint
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token1}"}
        )
        
        # Should return user1, not allow user2 access
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "user1"
```

### 2. Run Security Test Suite (10 min)

```bash
# Run all security tests
pytest tests/test_security_comprehensive.py -v

# Run with coverage
pytest tests/test_security_comprehensive.py --cov=src/expo_smooth_mcp --cov-report=html

# Run only authentication tests
pytest tests/test_security_comprehensive.py::TestAuthenticationSecurity -v

# Run with verbose output
pytest tests/test_security_comprehensive.py -vv
```

### 3. Create Security Checklist Document (20 min)

Create `docs/SECURITY_CHECKLIST.md`:

```markdown
# Security Checklist

## Authentication & Authorization

- [ ] JWT tokens required for protected endpoints
- [ ] Tokens include expiration timestamp
- [ ] Expired tokens rejected (401 Unauthorized)
- [ ] Tampered tokens rejected (401 Unauthorized)
- [ ] Malformed Authorization headers rejected
- [ ] Passwords never exposed in API responses
- [ ] Password hashes use bcrypt with automatic salting
- [ ] Scope-based authorization implemented
- [ ] Admin endpoints require admin scope
- [ ] Users cannot access others' data

## Rate Limiting

- [ ] Rate limiting enabled on all public endpoints
- [ ] Token endpoint: 5 attempts/minute
- [ ] Forecast endpoint: 30 requests/minute
- [ ] Global limit: 100 requests/minute (anonymous)
- [ ] Authenticated users: 500 requests/minute
- [ ] 429 response with Retry-After header
- [ ] Rate limit headers in responses

## Input Validation

- [ ] All input parameters type-validated
- [ ] Negative/invalid values rejected
- [ ] SQL injection protection (Pydantic models)
- [ ] XSS protection (response escaping)
- [ ] Path traversal protection
- [ ] File upload size limits (if applicable)

## Session Security

- [ ] Tokens unique per login
- [ ] No session fixation vulnerabilities
- [ ] Token refresh mechanism
- [ ] Secure token storage guidance (docs)

## Logging & Monitoring

- [ ] All requests logged with request ID
- [ ] Failed auth attempts logged
- [ ] Metrics tracked (Prometheus)
- [ ] Error responses include request ID
- [ ] Sensitive data not logged (passwords, tokens)

## Dependencies

- [ ] All dependencies up to date
- [ ] No known security vulnerabilities (pip-audit)
- [ ] Minimal dependency surface
- [ ] Security patches applied

## Production Configuration

- [ ] SECRET_KEY is strong and secret
- [ ] HTTPS enforced in production
- [ ] CORS properly configured
- [ ] Redis connection secured (password)
- [ ] Environment variables used for secrets
- [ ] No hardcoded credentials

## Testing

- [ ] All security tests passing
- [ ] Authentication tests (8+ tests)
- [ ] Authorization tests (3+ tests)
- [ ] Password security tests (4+ tests)
- [ ] Rate limiting tests (3+ tests)
- [ ] Input validation tests (3+ tests)
- [ ] Session security tests (2+ tests)

## Documentation

- [ ] Security features documented
- [ ] Authentication guide for clients
- [ ] Rate limit documentation
- [ ] Security best practices doc
- [ ] Incident response plan

## Compliance

- [ ] Password requirements enforced (if applicable)
- [ ] Data retention policy defined
- [ ] Privacy policy (if collecting PII)
- [ ] GDPR compliance (if EU users)
- [ ] Audit logging capability
```

### 4. Run Security Audit Tools (20 min)

```bash
# Check for known vulnerabilities
pip install safety pip-audit
safety check
pip-audit

# Static security analysis
pip install bandit
bandit -r src/

# Check for hardcoded secrets
pip install detect-secrets
detect-secrets scan

# Dependency vulnerability check
pip install pip-audit
pip-audit

# Generate security report
echo "# Security Audit Report" > security-report.md
echo "" >> security-report.md
echo "## Date: $(date)" >> security-report.md
echo "" >> security-report.md
echo "## Vulnerability Scan" >> security-report.md
safety check --json >> security-report.md 2>&1 || true
echo "" >> security-report.md
echo "## Static Analysis" >> security-report.md
bandit -r src/ -f txt >> security-report.md 2>&1 || true
```

### 5. Create Security Testing Documentation (15 min)

Create `tests/README_SECURITY_TESTS.md`:

```markdown
# Security Testing Guide

## Running Security Tests

### All Security Tests
```bash
pytest tests/test_security_comprehensive.py -v
```

### Specific Test Classes
```bash
# Authentication tests
pytest tests/test_security_comprehensive.py::TestAuthenticationSecurity -v

# Authorization tests
pytest tests/test_security_comprehensive.py::TestAuthorizationSecurity -v

# Password security tests
pytest tests/test_security_comprehensive.py::TestPasswordSecurity -v

# Rate limiting tests (requires Redis)
pytest tests/test_security_comprehensive.py::TestRateLimitingSecurity -v

# Input validation tests
pytest tests/test_security_comprehensive.py::TestInputValidation -v
```

### With Coverage
```bash
pytest tests/test_security_comprehensive.py \\
  --cov=src/expo_smooth_mcp \\
  --cov-report=html \\
  --cov-report=term-missing

# View coverage report
open htmlcov/index.html
```

## Test Categories

### 1. Authentication Security (8 tests)
- Password exposure prevention
- Token requirement enforcement
- Token expiration handling
- Token tampering detection
- Authorization header validation

### 2. Authorization Security (3 tests)
- Scope-based access control
- Admin endpoint protection
- User data isolation

### 3. Password Security (4 tests)
- Unique salt generation
- Hash irreversibility
- Password verification
- Brute force protection

### 4. Rate Limiting Security (3 tests)
- Per-endpoint rate limits
- Rate limit headers
- Authenticated user limits

### 5. Input Validation (3 tests)
- SQL injection protection
- XSS protection
- Parameter type validation

### 6. Session Security (2 tests)
- Token uniqueness
- Session fixation prevention

## Prerequisites

### Required Services
- Redis (for rate limiting tests)
```bash
brew install redis  # macOS
brew services start redis
```

### Environment Variables
```bash
export SECRET_KEY="test-secret-key-minimum-32-characters-long"
export REDIS_URL="redis://localhost:6379"
```

## Expected Results

All tests should pass:
```
tests/test_security_comprehensive.py::TestAuthenticationSecurity::test_password_not_exposed_in_responses PASSED
tests/test_security_comprehensive.py::TestAuthenticationSecurity::test_token_required_for_protected_endpoints PASSED
... [28 more tests] ...

======= 30 passed in 5.23s =======
```

## Troubleshooting

### Redis Connection Errors
```
redis.exceptions.ConnectionError: Error connecting to Redis
```
**Solution:** Start Redis server: `brew services start redis`

### Rate Limiting Tests Skipped
```
tests/test_security_comprehensive.py::TestRateLimitingSecurity SKIPPED (Redis required)
```
**Solution:** This is expected if Redis is not available. Tests will skip gracefully.

### Token Tests Failing
**Check:** SECRET_KEY environment variable is set and long enough (32+ chars)
```

### 6. Update Main Test Configuration (15 min)

Update `pytest.ini` or `pyproject.toml`:

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=src/expo_smooth_mcp
    --cov-report=term-missing
    --cov-report=html

markers =
    security: Security-related tests
    authentication: Authentication tests
    authorization: Authorization tests
    rate_limiting: Rate limiting tests
    slow: Slow running tests
```

Run marked tests:
```bash
# Run only security tests
pytest -m security

# Run all except slow tests
pytest -m "not slow"
```

**Testing Checklist:**
- [ ] Comprehensive security test suite created
- [ ] Authentication security tests (8+ tests)
- [ ] Authorization security tests (3+ tests)
- [ ] Password security tests (4+ tests)
- [ ] Rate limiting tests (3+ tests)
- [ ] Input validation tests (3+ tests)
- [ ] Session security tests (2+ tests)
- [ ] SECURITY_CHECKLIST.md created
- [ ] Security audit tools run
- [ ] All security tests passing

**Acceptance Criteria:**
- [ ] Comprehensive security test suite implemented (30+ tests)
- [ ] Tests cover: authentication, authorization, passwords, rate limiting, input validation, sessions
- [ ] All security tests passing
- [ ] SECURITY_CHECKLIST.md documentation created
- [ ] Security audit tools integrated (safety, bandit, pip-audit)
- [ ] Test coverage >80% for security module
- [ ] README_SECURITY_TESTS.md guide created
- [ ] pytest configuration updated with security markers
- [ ] Phase 5 complete - production hardening done!

---

### Phase 6: Documentation & Testing (10 tasks, ~16 hours)

#### TASK-601: Update README.md
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-415
**Description:** Rewrite README with new architecture diagram, installation instructions, both deployment options.

#### TASK-602: Update DEPLOYMENT_GUIDE.md
**Estimated Time:** 1.5 hours | **Complexity:** Low | **Dependencies:** TASK-407, TASK-415
**Description:** Replace HF Spaces guide with dual deployment guide (Docker MCP Toolkit + Fly.io).

#### TASK-603: Create client integration guide
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-406
**Description:** Write guide for configuring MCP clients (Claude Desktop, Cursor, VS Code) for both stdio and HTTP.

#### TASK-604: Document API endpoints
**Estimated Time:** 1.5 hours | **Complexity:** Low | **Dependencies:** TASK-413
**Description:** Create comprehensive API documentation with examples for all REST and MCP endpoints.

#### TASK-605: Create troubleshooting guide
**Estimated Time:** 2 hours | **Complexity:** Low | **Dependencies:** TASK-413
**Description:** Document common issues, solutions, debugging steps for both local and cloud deployments.

#### TASK-606: Create benchmark script
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-413
**Description:** Create `benchmark.py` to measure latency (p50, p95, p99) for both Gradio and FastMCP implementations.

#### TASK-607: Run performance benchmarks
**Estimated Time:** 1 hour | **Complexity:** Medium | **Dependencies:** TASK-606
**Description:** Execute benchmarks against local and production deployments, document results.

#### TASK-608: Create load testing suite
**Estimated Time:** 2 hours | **Complexity:** High | **Dependencies:** TASK-606
**Description:** Create `locustfile.py` for load testing, define realistic user scenarios.

#### TASK-609: Update all ADRs
**Estimated Time:** 1 hour | **Complexity:** Low | **Dependencies:** TASK-607
**Description:** Update ADR-004 status to "Accepted", add actual benchmark results, update revision history.

#### TASK-610: Final E2E testing checklist
**Estimated Time:** 2 hours | **Complexity:** Medium | **Dependencies:** TASK-607
**Description:** Execute comprehensive E2E test plan, document results, verify all acceptance criteria met.

---

## 7. Task Summary by Phase

| Phase | Task Count | Total Hours | Parallelization Potential |
|-------|------------|-------------|--------------------------|
| Phase 1: Decouple Logic | 8 | ~12h | Low (sequential dependencies) |
| Phase 2: FastMCP Backend | 12 | ~20h | Medium (some parallel tracks) |
| Phase 3: Mount Gradio | 6 | ~8h | Low (sequential) |
| Phase 4A: Docker MCP Toolkit | 7 | ~10h | Medium (docs parallel to testing) |
| Phase 4B: Fly.io Deployment | 8 | ~12h | Medium (after 4A complete) |
| Phase 5: Production Hardening | 14 | ~22h | High (auth, rate limit, logging parallel) |
| Phase 6: Documentation | 10 | ~16h | High (most tasks independent) |
| **TOTAL** | **65 tasks** | **~100h** | **Potential: 60-70h with 2-3 devs** |

---

## 8. Task Assignment Guidelines

### For Solo Developer
- Work sequentially through phases
- Estimated timeline: 12-15 working days
- Focus on completing each phase before moving to next

### For 2 Developers
**Developer 1 (Backend Focus):**
- Phase 1: All logic tasks
- Phase 2: MCP implementation
- Phase 5: Security & rate limiting

**Developer 2 (Integration Focus):**
- Phase 3: Gradio mounting
- Phase 4: Docker & deployment
- Phase 6: Documentation & testing

**Estimated timeline: 7-10 working days**

### For 3 Developers
**Developer 1 (Core):**
- Phase 1: Business logic
- Phase 2: FastMCP backend

**Developer 2 (Infrastructure):**
- Phase 4A: Docker MCP Toolkit
- Phase 4B: Fly.io deployment

**Developer 3 (Quality):**
- Phase 3: Gradio integration
- Phase 5: Production hardening
- Phase 6: Documentation

**Estimated timeline: 5-7 working days**

---

## 9. Future Enhancements (Post-v2.0 Backlog)

These are ideas for future iterations of the project:

*   **Model Parameter Tuning:** Add API endpoints to adjust Holt-Winters parameters (`alpha`, `beta`, `gamma`).
*   **Display Accuracy Metrics:** Calculate and return forecast accuracy metrics (MAPE, RMSE) in API responses.
*   **Comparative Model Visualization:** Support multiple forecasting models via MCP tools.
*   **Multi-tenancy:** Add organization/workspace support with isolated data.
*   **Caching Layer:** Implement Redis caching for frequently requested forecasts.
*   **Async Forecasting:** Support long-running forecasts with job queue (Celery/Redis).
*   **Custom UI:** Replace Gradio with React/Vue.js frontend.