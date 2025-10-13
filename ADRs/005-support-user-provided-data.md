# ADR 005: Support for User-Provided Data in Forecasting

- **Status:** Accepted (Extended in Phase 3B)
- **Date:** 2025-10-13 (Extended: 2025-10-13)
- **Deciders:** maksim-tsi, GitHub Copilot
- **Stage:** 3A (Extended: 3B)

---

## Context and Problem Statement

The application currently relies on a hard-coded dataset (`FMCG_Sales.csv`) for generating sales forecasts. To be practically useful, users and MCP clients must be able to provide their own sales data for analysis. The system needs a mechanism to accept user data through both the Gradio web UI and the MCP interface.

The primary challenge is defining a data ingestion method that is both user-friendly for the UI and technically feasible for programmatic clients, while respecting the constraints of the MCP protocol and client limitations.

## Decision Drivers

1.  **Usability:** The solution for the Gradio UI must be intuitive for non-technical users (e.g., file drag-and-drop).
2.  **Interoperability:** The MCP client solution must work reliably with major clients like the Claude app and VS Code extensions.
3.  **Scalability:** The chosen patterns should ideally handle a reasonable range of data sizes, from small CSVs to larger datasets.
4.  **Simplicity:** The initial implementation should be achievable within a limited scope (Stage 3A).

## Considered Options

### Option 1: Base64 Encoding in MCP Tool Call (Pattern A)

- **Description:** The client reads a data file, encodes its content into a Base64 string, and passes this string as a parameter in a single MCP tool call. The server decodes the string in memory and processes it.
- **Pros:**
    - Atomic operation; the entire request is self-contained.
    - Simple server-side logic (no state to manage).
- **Cons:**
    - **Severe Size Limitations:** Research indicates that clients (Claude, VS Code) and the underlying models have strict payload and token limits. This pattern is likely to fail for files larger than ~32-64KB.
    - Inefficient due to ~33% size increase from Base64 encoding.
    - Can be slow for both client and server.

### Option 2: Two-Step Upload-then-Process (Pattern B)

- **Description:** The client first uploads the file to a dedicated REST endpoint (`POST /api/upload`), which returns a unique `data_id`. The client then makes an MCP tool call, passing this `data_id` instead of the file content.
- **Pros:**
    - Highly scalable and robust; suitable for large files.
    - Uses standard, efficient HTTP for file transfer.
    - Keeps MCP tool call payloads small and fast.
- **Cons:**
    - More complex client logic (requires two separate API calls).
    - Requires state management on the server to map `data_id` to temporary files.

### Option 3: Gradio File Upload Component

- **Description:** Use the native `gr.File()` component in the Gradio UI to allow users to upload files directly through their browser.
- **Pros:**
    - The most intuitive and standard UX for web applications.
    - Handles file transfer efficiently.
    - Integrates seamlessly with Gradio's session management.
- **Cons:**
    - Only applicable to the Gradio UI, not MCP clients.

## Decision Outcome

**Chosen Approach: A Hybrid Strategy for Stage 3A**

1.  **For the Gradio UI:** We will implement **Option 3 (Gradio File Upload)**. It provides the best possible user experience and is the standard for web-based file handling.

2.  **For MCP Clients:** We will implement **Option 1 (Base64 Encoding)**, but with a strict and explicit limitation. This respects the user's preference for Pattern A while acknowledging its technical constraints.

**Rationale:**

- This hybrid approach delivers immediate value to both UI users and programmatic clients within the limited scope of Stage 3A.
- The Gradio implementation is straightforward and provides a high-quality user feature.
- The MCP implementation (Pattern A) provides a basic data-passing mechanism for small files, which is a good first step.
- By documenting the limitations of Pattern A, we are making a conscious architectural trade-off, prioritizing initial implementation speed over scalability. We formally acknowledge that Pattern B is the correct long-term solution for MCP clients and should be prioritized in a future development phase.

---

## Implementation Plan (Stage 3A)

### Component 1: Gradio UI Enhancement (`app.py`)

- **TASK-3A-01:** Add a `gr.File()` component to the Gradio UI to create a file upload area.
- **TASK-3A-02:** Implement a file-processing function that triggers on upload. This function will:
    - Read the uploaded file into a pandas DataFrame.
    - Store the DataFrame in a `gr.State` object for the user's session.
    - Extract SKU/product identifiers from the data.
    - Dynamically update the "Select SKU" dropdown with the extracted identifiers.
- **TASK-3A-03:** Modify the main forecasting function to use the DataFrame from the session state if it exists, otherwise fall back to the default `FMCG_Sales.csv`.

### Component 2: MCP Server Enhancement (`src/expo_smooth_mcp/main.py`)

- **TASK-3A-04:** Create a new MCP tool named `forecast_with_custom_data`.
- **TASK-3A-05:** Define the tool's schema to accept `file_data_base64: str`, `file_name: str`, `sku: str`, and `horizon: int`.
- **TASK-3A-06:** Implement the tool's logic:
    - Add a size check for the incoming `file_data_base64` string. If it exceeds a predefined limit (e.g., 100KB, corresponding to a ~66KB file), return an error instructing the user to use a smaller file.
    - Decode the Base64 string.
    - Use an in-memory buffer (`io.BytesIO`) and pandas to read the data.
    - Call the existing forecasting logic with the new DataFrame.
    - Return the forecast result.
- **TASK-3A-07:** Update the `list_tools` function to include the new tool and its description, clearly mentioning the file size limitation.

### Component 3: Documentation

- **TASK-3A-08:** Create a new test file `tests/test_custom_data.py` with tests for both the new Gradio functionality and the MCP tool.
- **TASK-3A-09:** Update project documentation (e.g., `README.md`, `SPECIFICATION.md`) to reflect the new capabilities and their usage.

## Consequences

- **Positive:**
    - The application becomes significantly more useful as it can now operate on user-provided data.
    - The feature is available to both UI users and programmatic clients.
- **Negative / Risks:**
    - MCP clients will face errors if they attempt to send files larger than the small, predefined limit. This risk is mitigated by returning a clear error message.
    - This introduces a "technical debt" of needing to implement the more robust Pattern B in the future. This is an accepted trade-off.

---

## Extension: Flexible Column Mapping (Phase 3B)

**Date Extended:** October 13, 2025  
**Context:** After implementing Phase 3A, user testing revealed that the rigid requirement for columns named exactly `date` and `sales` creates a poor user experience. Real-world supply chain datasets use varied column names like `timestamp`, `order_date`, `quantity`, `demand`, `revenue`, etc.

### Additional Problem Statement

**The "Column Name Rigidity" Problem:**

Phase 3A successfully enables users to upload their own data, but it fails immediately if their columns aren't named exactly `date` and `sales`. This is impractical because:

1. **Supply Chain datasets have diverse naming conventions:**
   - Time columns: `date`, `timestamp`, `day`, `period`, `order_date`, `ds`
   - Metric columns: `sales`, `quantity`, `demand`, `revenue`, `units_sold`, `orders`, `y`
   - Identifier columns: `sku`, `product_id`, `item_id`, `product_code`

2. **Users expect the tool to adapt to their data, not vice versa.**

3. **Error messages like "File must contain 'date' and 'sales' columns" provide no guidance on how to fix the issue.**

### Additional Decision Drivers

1. **Usability:** The tool must work with common SCM column names without requiring users to rename columns.
2. **Discoverability:** Users should understand what the tool needs from their data.
3. **Lightweight:** The solution should not require ML models or complex NLP.
4. **Consistency:** The solution must work for both Gradio UI and MCP protocol.

### Considered Options for Column Mapping

#### Option A: Automatic Column Renaming with Heuristics

- **Description:** Automatically detect column types using simple pattern matching on column names and data types, then internally rename them to `date` and `sales`.
- **Pros:**
    - Zero user interaction required
    - Works immediately for common cases
    - Simple implementation
- **Cons:**
    - May guess wrong
    - No user control
    - Opaque behavior (users don't know what happened)

#### Option B: Interactive Column Mapping UI

- **Description:** After file upload, present dropdowns allowing users to explicitly map their columns to required roles (date, metric, product ID). Use heuristics to pre-populate smart suggestions.
- **Pros:**
    - User has full control
    - Transparent process
    - Handles edge cases
    - Educational (users learn what the tool needs)
- **Cons:**
    - Requires one additional user interaction
    - Slightly more complex UI

#### Option C: Support Multiple Column Name Aliases

- **Description:** Hardcode a list of acceptable column names (e.g., `date`, `timestamp`, `day` all work for the date column).
- **Pros:**
    - Simple implementation
    - No UI changes needed
- **Cons:**
    - Never complete (always missing someone's column name)
    - Still breaks with custom names
    - No flexibility

### Decision Outcome: Option B (Interactive Column Mapping) for Both Gradio and MCP

**Rationale:**

- **Option B provides the best balance** between automation and user control.
- **Heuristics make it fast:** If our suggestions are correct, it's just 2 clicks.
- **It's still lightweight:** No ML models, just string matching on column names.
- **It's transparent:** Users understand exactly what's being forecast.
- **It works for both interfaces:** Gradio gets dropdowns, MCP gets explicit parameters.

### Implementation Plan (Stage 3B)

#### Component 1: Column Analysis Module (`src/expo_smooth_mcp/column_analysis.py`)

**New Module:** Create a lightweight column analyzer

```python
def analyze_columns(df: pd.DataFrame) -> dict:
    """
    Analyze DataFrame columns and suggest mappings.
    
    Returns:
        {
            "all_columns": [...],
            "date_candidates": [...],
            "metric_candidates": [...],
            "product_candidates": [...],
            "suggested_date": "...",
            "suggested_metric": "...",
            "suggested_product": "..."
        }
    """
```

**Detection Rules:**
- **Date columns:** Check for keywords (`date`, `time`, `day`, `period`, `ds`) + validate parseability
- **Metric columns:** Check numeric dtype + keywords (`sales`, `quantity`, `demand`, `revenue`, `units`, `value`, `y`)
- **Product columns:** Check for keywords (`sku`, `product`, `item`, `id`)

#### Component 2: Gradio UI Enhancement

**New UI Flow:**
1. User uploads file → Analysis runs automatically
2. Show "Map Your Data" section with 3 dropdowns:
   - 📅 Date/Time column (pre-selected with best guess)
   - 📈 Metric column to forecast (pre-selected)
   - 🏷️ Product ID column (optional, pre-selected)
3. Display auto-detection hints
4. User confirms/adjusts selections
5. Generate forecast button enabled

#### Component 3: MCP Tool Enhancement

**Extend `forecast_with_custom_data` tool** to accept column mapping parameters:

```python
@mcp.tool()
async def forecast_with_custom_data(
    file_data_base64: str,
    file_name: str,
    sku: str,
    forecast_horizon: int = 90,
    date_column: str = "date",           # NEW: Allow custom mapping
    metric_column: str = "sales",        # NEW: Allow custom mapping
    product_column: Optional[str] = None # NEW: Allow custom mapping
) -> dict:
    """
    Generate forecast using user-provided data with flexible column mapping.
    
    New Parameters:
        date_column: Name of the date/time column in your data (default: "date")
        metric_column: Name of the metric column to forecast (default: "sales")
        product_column: Name of the product identifier column (default: None)
    
    Example:
        # Data with columns: "OrderDate", "Product_Code", "Units_Sold"
        result = await forecast_with_custom_data(
            file_data_base64=data,
            file_name="orders.csv",
            sku="PROD123",
            date_column="OrderDate",
            metric_column="Units_Sold",
            product_column="Product_Code"
        )
    """
```

**Column Validation:**
- Verify specified columns exist in the uploaded data
- Verify date column is parseable as datetime
- Verify metric column is numeric
- Provide clear error messages if validation fails

#### Component 4: Backend Refactoring

**Refactor forecasting functions** to accept column names as parameters:

```python
# Before (rigid):
def generate_forecast(df):
    df['date'] = pd.to_datetime(df['date'])
    model = ExponentialSmoothing(df['sales'], ...)

# After (flexible):
def generate_forecast(
    df, 
    date_col='date', 
    metric_col='sales',
    product_col=None
):
    # Rename to expected format internally
    df_work = df.copy()
    df_work = df_work.rename(columns={
        date_col: 'date',
        metric_col: 'sales'
    })
    
    if product_col:
        df_work = df_work.rename(columns={product_col: 'sku'})
    
    # Rest of logic unchanged
    df_work['date'] = pd.to_datetime(df_work['date'])
    model = ExponentialSmoothing(df_work['sales'], ...)
```

### Implementation Tasks (Phase 3B)

- **TASK-3B-01:** Create `column_analysis.py` module with heuristic detection (2h)
- **TASK-3B-02:** Update Gradio UI with column mapping interface (2h)
- **TASK-3B-03:** Extend MCP tool with column mapping parameters (1.5h)
- **TASK-3B-04:** Refactor forecasting functions to accept column names (1.5h)
- **TASK-3B-05:** Create comprehensive tests for column mapping (1.5h)
- **TASK-3B-06:** Update documentation with column mapping examples (1h)

**Total Estimated Time:** 9.5 hours

### Why This Stays Lightweight

| Aspect | Complexity | Implementation |
|--------|-----------|----------------|
| **Algorithm** | Very Simple | String matching on column names |
| **Processing** | <100ms | Only analyzes column metadata |
| **Dependencies** | Zero new | Uses existing pandas |
| **Code Size** | ~250 lines | Small footprint |
| **User Effort** | Minimal | 2 clicks if suggestions correct |

### Extended Consequences

**Additional Positive:**
- Users can upload datasets with any reasonable column structure
- Tool adapts to common SCM naming conventions
- Works for both Gradio UI and MCP protocol
- Backward compatible (default values maintain old behavior)

**Additional Risks (Mitigated):**
- Heuristics might guess wrong → **Mitigation:** User can override suggestions
- Extra UI complexity → **Mitigation:** Suggestions minimize user effort
- MCP clients need to specify mappings → **Mitigation:** Sensible defaults + clear documentation

### Success Criteria

**Phase 3B is successful if:**
1. ✅ Users can upload data with common SCM column names without errors
2. ✅ Heuristic suggestions are correct >80% of the time for standard datasets
3. ✅ Both Gradio UI and MCP tool support column mapping
4. ✅ Backward compatibility maintained (existing `date`/`sales` data still works)
5. ✅ All tests pass (15+ new tests for mapping logic)
6. ✅ Documentation includes examples for common column naming patterns
