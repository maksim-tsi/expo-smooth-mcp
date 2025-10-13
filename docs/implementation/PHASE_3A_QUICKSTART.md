# Phase 3A: Custom Data Support - Quick Start Guide

**Project:** Exponential Smoothing Forecasting via MCP  
**Phase:** 3A - User-Provided Data Enhancement  
**Version:** 1.0.0  
**Estimated Time:** 7 hours

---

## Overview

Phase 3A adds the ability for users to provide their own sales data through both the Gradio UI and MCP protocol, making the application useful for real-world forecasting scenarios.

**What You'll Build:**
- 📤 File upload in Gradio UI (CSV, Excel, JSON)
- 🔧 New MCP tool for custom data (Base64 encoding)
- ✅ Comprehensive test coverage
- 📚 Updated documentation

---

## Prerequisites

- ✅ Phase 3 complete: Gradio UI mounted and functional
- ✅ All existing tests passing (59 tests)
- ✅ ADR 005 reviewed

---

## Quick Implementation (7 hours)

### Task 1: Gradio File Upload (1.5h)

**What:** Add file upload component to Gradio UI

**Files to Edit:**
- `app.py`

**Key Changes:**
```python
# Add file processing function
def process_uploaded_file(file):
    # Read CSV/Excel/JSON
    # Validate columns
    # Extract SKU list
    # Return DataFrame
    
# Update Gradio interface
file_upload = gr.File(label="Upload CSV, Excel, or JSON")
custom_data_state = gr.State(None)
```

**Test:**
```bash
# Start server
python -m src.expo_smooth_mcp.main

# Open http://localhost:8000/gradio
# Upload a CSV file
# Verify SKU dropdown updates
```

---

### Task 2: MCP Custom Data Tool (2h)

**What:** Create new MCP tool accepting Base64-encoded data

**Files to Edit:**
- `src/expo_smooth_mcp/main.py`

**Key Changes:**
```python
@mcp.tool()
async def forecast_with_custom_data(
    file_data_base64: str,
    file_name: str,
    sku: str,
    forecast_horizon: int = 90
):
    # Validate size (<100KB Base64)
    # Decode Base64
    # Parse file (CSV/Excel/JSON)
    # Validate columns
    # Generate forecast
```

**Test:**
```python
# Test with small CSV
import base64
with open("test.csv", "rb") as f:
    data = base64.b64encode(f.read()).decode()

# Call via Claude Desktop
# "Use forecast_with_custom_data with my test.csv file"
```

---

### Task 3: Comprehensive Tests (2.5h)

**What:** Create test suite for both interfaces

**Files to Create:**
- `tests/test_custom_data.py`

**Test Coverage:**
- ✅ File upload processing (valid/invalid)
- ✅ Base64 encoding/decoding
- ✅ Size limit enforcement
- ✅ Format validation (CSV/Excel/JSON)
- ✅ Column validation
- ✅ SKU extraction
- ✅ Error handling
- ✅ Integration workflows

**Run Tests:**
```bash
pytest tests/test_custom_data.py -v
# Expected: 15+ tests, all passing
```

---

### Task 4: Update Documentation (1h)

**What:** Add usage examples and requirements

**Files to Edit:**
- `README.md` - Usage examples
- `docs/DATA_PREPROCESSING.md` - Format requirements
- `ADRs/005-support-user-provided-data.md` - Update status

**Key Additions:**
- How to upload via Gradio UI
- How to use MCP tool with Base64
- Data format requirements
- Size limitations
- Troubleshooting guide

---

## Validation Checklist

### Functionality
- [ ] Gradio accepts CSV upload
- [ ] Gradio accepts Excel upload
- [ ] Gradio accepts JSON upload
- [ ] SKU dropdown updates after upload
- [ ] Forecast works with custom data
- [ ] MCP tool accepts Base64 data
- [ ] MCP tool rejects files >100KB
- [ ] Error messages are clear

### Tests
- [ ] 15+ new tests created
- [ ] All new tests passing
- [ ] No regressions in existing tests
- [ ] Tests run in <30 seconds

### Documentation
- [ ] README.md updated
- [ ] DATA_PREPROCESSING.md updated
- [ ] ADR 005 marked as "Accepted"
- [ ] Usage examples provided

---

## Testing Guide

### Manual Testing: Gradio UI

1. **Start Server:**
   ```bash
   python -m src.expo_smooth_mcp.main
   ```

2. **Open Browser:**
   ```
   http://localhost:8000/gradio
   ```

3. **Test File Upload:**
   ```
   - Create test CSV with date, sku, sales columns
   - Click "Upload CSV, Excel, or JSON"
   - Select your file
   - Verify status message shows success
   - Check SKU dropdown updates
   - Select a SKU and generate forecast
   ```

4. **Test Error Handling:**
   ```
   - Upload file without required columns → See error
   - Upload unsupported format (.txt) → See error
   - Upload empty file → See error
   ```

### Manual Testing: MCP Tool

1. **Prepare Test Data:**
   ```python
   # create_test_data.py
   import base64
   
   csv_content = """date,sku,sales
   2024-01-01,TEST001,100
   2024-01-02,TEST001,105
   2024-01-03,TEST001,110"""
   
   encoded = base64.b64encode(csv_content.encode()).decode()
   print(f"Base64: {encoded}")
   print(f"Size: {len(encoded)} bytes")
   ```

2. **Test in Claude Desktop:**
   ```
   Prompt: "Use the forecast_with_custom_data tool with this Base64 data:
   [paste encoded data]
   filename: test.csv
   sku: TEST001
   horizon: 7"
   ```

3. **Verify Response:**
   - Should return forecast with 7 days
   - Should include metadata
   - Should show TEST001 SKU

---

## Common Issues & Solutions

### Issue: "File too large" Error

**Problem:** MCP tool returns size limit error

**Solution:**
- File must be <66KB (100KB Base64)
- Remove unnecessary columns
- Use Gradio UI for larger files
- Wait for Pattern B (future phase)

### Issue: "Missing required columns"

**Problem:** Error about date/sales columns

**Solution:**
```python
# Check your columns
import pandas as pd
df = pd.read_csv("your_file.csv")
print(df.columns.tolist())

# Must have: 'date', 'sales', 'sku'
```

### Issue: SKU Dropdown Not Updating

**Problem:** Dropdown still shows default SKUs after upload

**Solution:**
- Check file_upload.change() is wired correctly
- Verify process_uploaded_file() returns SKU list
- Check browser console for errors
- Refresh Gradio interface

---

## Time Estimate

| Task | Time |
|------|------|
| Gradio File Upload | 1.5h |
| MCP Custom Data Tool | 2.0h |
| Comprehensive Tests | 2.5h |
| Update Documentation | 1.0h |
| **Total** | **7.0h** |

---

## Success Criteria

✅ **Phase 3A Complete When:**
- All 4 tasks implemented
- 15+ tests passing
- Zero test regressions
- Documentation updated
- Manual testing validated
- Code reviewed

---

## Next Steps

After Phase 3A:

1. **Code Review:**
   - Review implementation quality
   - Check for edge cases
   - Validate error handling

2. **User Testing:**
   - Test with real-world data
   - Collect feedback
   - Document issues

3. **Proceed to Phase 4:**
   - Docker MCP Toolkit deployment
   - Fly.io cloud deployment
   - Production hardening

---

## Support

**Detailed Guide:** `docs/implementation/PHASE_3A_IMPLEMENTATION.md`  
**ADR 005:** `ADRs/005-support-user-provided-data.md`  
**Test Examples:** `tests/test_custom_data.py`

---

**Phase 3A Quick Start Complete**  
**Ready to Enhance Application with Custom Data**  
**Estimated Time: 7 hours**
