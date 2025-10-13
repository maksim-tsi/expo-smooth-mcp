# ADR 005: Support for User-Provided Data in Forecasting

- **Status:** Accepted
- **Date:** 2025-10-13
- **Deciders:** maksim-tsi, GitHub Copilot
- **Stage:** 3A

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
