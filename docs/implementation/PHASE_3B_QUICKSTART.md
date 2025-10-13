# Phase 3B: Intelligent Column Mapping - Quick Start Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** 3B - Flexible Data Column Mapping  
**Version:** 1.0.0  
**Estimated Time:** 9.5 hours

---

## Overview

Phase 3B makes the application work with any reasonably structured data by adding intelligent column detection and flexible mapping. Users no longer need to rename their columns to match rigid `date` and `sales` requirements.

**What You'll Build:**
- 🔍 Lightweight column analysis with heuristic detection
- 🎨 Interactive column mapping UI in Gradio
- 🔧 Extended MCP tool with column parameters
- ✅ 15+ comprehensive tests
- 📚 Updated documentation

---

## Prerequisites

- ✅ Phase 3A complete (custom data upload working)
- ✅ All 94 tests passing
- ✅ ADR 005 extended with Phase 3B decisions

---

## Quick Implementation (9.5 hours)

### Task 1: Column Analysis Module (2h)

**What:** Create lightweight module to detect column types

**File:** `src/expo_smooth_mcp/column_analysis.py` (new)

**Key Functions:**
```python
def analyze_columns(df: pd.DataFrame) -> dict:
    """
    Analyze columns and suggest mappings.
    Returns suggested date, metric, and product columns.
    """

def validate_column_mapping(df, date_col, metric_col, product_col) -> dict:
    """
    Validate that specified columns are appropriate.
    Returns validation result with errors/warnings.
    """
```

**Detection Logic:**
- Date columns: Keywords + parseability test
- Metric columns: Numeric + keywords (sales, quantity, demand, etc.)
- Product columns: Keywords (sku, product_id, item_id, etc.)

**Test:**
```python
from src.expo_smooth_mcp import column_analysis

df = pd.read_csv("your_data.csv")
analysis = column_analysis.analyze_columns(df)
print(f"Date: {analysis['suggested_date']}")
print(f"Metric: {analysis['suggested_metric']}")
```

---

### Task 2: Gradio UI Column Mapping (2h)

**What:** Add interactive mapping section to Gradio

**File:** `app.py`

**Key Changes:**
1. Import column analysis
2. Update `process_uploaded_file()` to run analysis
3. Add mapping section with 3 dropdowns:
   - 📅 Date/Time column
   - 📈 Metric column
   - 🏷️ Product ID column (optional)
4. Pre-populate with smart suggestions
5. Update forecast function to use mappings

**UI Flow:**
```
Upload File → Analysis → Show Dropdowns (pre-filled) → User Confirms → Forecast
```

**Test:**
```bash
python -m src.expo_smooth_mcp.main
# Open http://localhost:8000/gradio
# Upload CSV with custom column names
# Verify dropdowns show correct suggestions
# Generate forecast
```

---

### Task 3: Extend MCP Tool (1.5h)

**What:** Add column mapping parameters to MCP tool

**File:** `src/expo_smooth_mcp/main.py`

**Key Changes:**
```python
@mcp.tool()
async def forecast_with_custom_data(
    file_data_base64: str,
    file_name: str,
    sku: str,
    forecast_horizon: int = 90,
    date_column: str = "date",        # NEW
    metric_column: str = "sales",     # NEW
    product_column: Optional[str] = None  # NEW
):
    # Validate column mapping
    validation = column_analysis.validate_column_mapping(...)
    
    # Rename columns to expected format
    df_mapped = df.rename(columns={
        date_column: 'date',
        metric_column: 'sales',
        product_column: 'sku'
    })
    
    # Continue with existing logic
    ...
```

**Test:**
```python
# Create test CSV with custom columns
import base64

csv_data = """OrderDate,Product_Code,Units_Sold
2024-01-01,PROD_001,100
2024-01-02,PROD_001,105"""

encoded = base64.b64encode(csv_data.encode()).decode()

# Test with MCP client or directly
result = await forecast_with_custom_data(
    file_data_base64=encoded,
    file_name="orders.csv",
    sku="PROD_001",
    date_column="OrderDate",
    metric_column="Units_Sold",
    product_column="Product_Code"
)
```

---

### Task 4: Refactor Backend (1.5h)

**What:** Make forecasting functions accept column names

**File:** `src/expo_smooth_mcp/logic.py`

**Key Changes:**
```python
def get_forecast_data(
    df: pd.DataFrame,
    sku: str,
    forecast_horizon: int,
    date_col: str = 'date',      # NEW
    metric_col: str = 'sales',   # NEW
    product_col: str = 'sku'     # NEW
):
    # Rename columns if needed
    df_work = df.rename(columns={
        date_col: 'date',
        metric_col: 'sales',
        product_col: 'sku'
    })
    
    # Rest of logic unchanged
    ...
```

**Test:**
```python
# Test with default columns
forecast1 = logic.get_forecast_data(df, "SKU_001", 90)

# Test with custom columns  
forecast2 = logic.get_forecast_data(
    df, "SKU_001", 90,
    date_col="OrderDate",
    metric_col="Units_Sold"
)
```

---

### Task 5: Comprehensive Tests (1.5h)

**What:** Create test suite for column mapping

**File:** `tests/test_column_mapping.py` (new)

**Test Categories:**
1. **Column Analysis (8 tests)**
   - Standard column names
   - Custom SCM names
   - Ambiguous columns
   - Empty DataFrame
   - Date detection
   - Metric detection
   - Product detection
   - Scoring system

2. **Validation (4 tests)**
   - Valid mapping
   - Missing columns
   - Non-numeric metric
   - Invalid dates

3. **Integration (3 tests)**
   - Gradio workflow
   - MCP workflow
   - Backend flexibility

**Run Tests:**
```bash
pytest tests/test_column_mapping.py -v
pytest tests/ -v  # All tests (should be 109 passing)
```

---

### Task 6: Update Documentation (1h)

**What:** Add column mapping guidance to docs

**Files:** 
- `README.md`
- `docs/DATA_PREPROCESSING.md`

**Key Sections:**
1. Flexible Column Mapping overview
2. Supported column types with examples
3. Common SCM column names table
4. Usage examples for Gradio and MCP
5. Detection logic explanation

**Example Addition to README:**
```markdown
### Flexible Column Mapping

Your data can use any column names! The system automatically detects:

**Common SCM Column Names:**
- Date: `date`, `timestamp`, `order_date`, `period`, `ds`
- Metric: `sales`, `quantity`, `demand`, `revenue`, `units_sold`
- Product: `sku`, `product_id`, `item_id`, `product_code`

**Example with Custom Columns:**
```python
# Data: OrderDate, Product_Code, Units_Sold
result = await forecast_with_custom_data(
    ...,
    date_column="OrderDate",
    metric_column="Units_Sold",
    product_column="Product_Code"
)
```
```

---

## Testing Checklist

### Manual Testing

**Gradio UI:**
- [ ] Upload CSV with standard columns (`date`, `sales`)
- [ ] Upload CSV with custom columns (`OrderDate`, `Units_Sold`)
- [ ] Verify smart suggestions are correct
- [ ] Override suggestions manually
- [ ] Generate forecast successfully
- [ ] Try invalid column selection (should show error)

**MCP Tool:**
- [ ] Test with default column names (backward compatibility)
- [ ] Test with custom column names
- [ ] Test with missing columns (should error)
- [ ] Test with invalid column types (should error)

### Automated Testing

```bash
# Run Phase 3B tests
pytest tests/test_column_mapping.py -v

# Run all tests (no regressions)
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src/expo_smooth_mcp --cov-report=html
```

**Expected Results:**
- 15+ new tests passing
- 94 existing tests still passing
- Total: 109+ tests passing
- No regressions

---

## Common Issues & Solutions

### Issue: Analysis Returns No Suggestions

**Cause:** Column names don't match any keywords

**Solution:**
```python
# Add custom keywords to column_analysis.py
DATE_KEYWORDS.append('your_custom_date_name')
METRIC_KEYWORDS.append('your_custom_metric_name')
```

### Issue: Date Column Not Parsing

**Cause:** Unusual date format

**Solution:**
```python
# In preprocessing.py, add format hint
pd.to_datetime(df['date'], format='%Y/%m/%d')
```

### Issue: Multiple Numeric Columns Confuse Detection

**Cause:** Revenue, price, and quantity all numeric

**Solution:**
- Keywords help prioritize (quantity > price)
- User can manually select correct column

### Issue: Backward Compatibility Broken

**Cause:** Default parameters changed

**Solution:**
```python
# Verify defaults are correct
def forecast(..., date_col='date', metric_col='sales')
                           ^^^^^^           ^^^^^^^
```

---

## Validation Before Proceeding

Before considering Phase 3B complete, verify:

### Functionality
- [ ] Column analysis runs in <100ms
- [ ] Heuristics are >80% accurate on test data
- [ ] Gradio UI shows mapping section after upload
- [ ] Smart suggestions pre-selected
- [ ] Manual override works
- [ ] MCP tool accepts column parameters
- [ ] Forecasts generate with custom columns

### Quality
- [ ] All 109+ tests passing
- [ ] No regressions in existing tests
- [ ] Code coverage >90%
- [ ] No performance degradation

### Documentation
- [ ] README.md updated
- [ ] DATA_PREPROCESSING.md updated
- [ ] ADR 005 extended (✅ already done)
- [ ] Code comments comprehensive
- [ ] Examples provided

### User Experience
- [ ] Upload → Analysis → Mapping → Forecast flows smoothly
- [ ] Error messages clear and helpful
- [ ] Works with common SCM datasets
- [ ] Backward compatible with Phase 3A data

---

## Quick Reference

### Key Files Created/Modified

| File | Status | Purpose |
|------|--------|---------|
| `src/expo_smooth_mcp/column_analysis.py` | NEW | Column detection & validation |
| `app.py` | MODIFIED | Mapping UI |
| `src/expo_smooth_mcp/main.py` | MODIFIED | MCP tool extension |
| `src/expo_smooth_mcp/logic.py` | MODIFIED | Flexible column support |
| `tests/test_column_mapping.py` | NEW | Test suite |
| `README.md` | MODIFIED | User docs |
| `docs/DATA_PREPROCESSING.md` | MODIFIED | Technical docs |

### Key Concepts

**Heuristic Detection:**
- Keyword matching on column names
- Data type validation
- Scoring system for prioritization

**Column Mapping:**
- User columns → Standard names internally
- Transparent renaming
- Validation before processing

**Backward Compatibility:**
- Default parameter values maintain Phase 3A behavior
- No breaking changes
- Existing data/code works unchanged

---

## Success Criteria

Phase 3B is complete when:

1. ✅ Column analysis module working
2. ✅ Gradio UI has mapping interface
3. ✅ MCP tool accepts column parameters
4. ✅ Backend supports flexible columns
5. ✅ 15+ tests passing (109+ total)
6. ✅ Documentation updated
7. ✅ Heuristics >80% accurate
8. ✅ No regressions
9. ✅ Backward compatible
10. ✅ User testing successful

---

**Phase Owner:** maksim-tsi  
**Estimated Time:** 9.5 hours  
**Status:** Ready for Implementation  
**Next Phase:** Phase 4 - Docker MCP Deployment
