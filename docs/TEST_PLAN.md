
# Test Plan

- **Version:** 1.0
- **Status:** Final
- **Last Updated:** 2025-07-05 by Maksim Ilin
- **Summary:** This document outlines the testing strategy, scope, and specific test cases for the `expo-smooth-mcp` project to ensure its correctness, reliability, and alignment with research goals.

---

## 1. Objective

The primary objective of this test plan is to verify that the application and its underlying components function as designed. This includes validating the data pipeline, the forecasting model's output, the user interface's behavior, and the MCP server's API contract.

## 2. Testing Scope

### In-Scope
*   **Backend Logic:** Data preprocessing and forecasting functions.
*   **Application UI:** The functionality of the Gradio web interface.
*   **API Endpoint:** The MCP server's response to valid and invalid requests.
*   **Data Handling:** The application's ability to handle both the default dataset and user-uploaded files.

### Out-of-Scope
*   **Performance/Load Testing:** We will not test the application's performance under high concurrent user load.
*   **Security Testing:** We will not perform formal security vulnerability scanning.
*   **Cross-Browser Compatibility:** Testing will be limited to the latest versions of Chrome and Firefox.

## 3. Testing Levels & Tools

Our testing strategy is divided into three distinct levels:

| Level | Tool / Method | Purpose |
| :--- | :--- | :--- |
| **Unit Testing** | `pytest` | To verify that individual Python functions (e.g., `preprocess_data`) work correctly in isolation. |
| **Integration Testing** | `curl` / MCP Client | To verify that the running server correctly calls the backend functions and returns data via the MCP endpoint. |
| **End-to-End (E2E) Testing** | Manual Checklist | To verify the complete user workflow from the perspective of an end-user interacting with the Gradio UI. |

## 4. Test Cases

### 4.1. Unit Test Cases (Automated)

These tests are implemented in the `/tests/` directory and run via the `pytest` command.

| Test Case ID | Module | Function | Description | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **UT-001** | `preprocessing` | `preprocess_data` | Verify that the output DataFrame has the correct schema (index, columns). | Test passes. |
| **UT-002** | `preprocessing` | `preprocess_data` | Verify that the output `quantity` column contains no null values. | Test passes. |
| **UT-003** | `preprocessing` | `preprocess_data` | Verify that the date index for a single SKU is continuous and daily. | Test passes. |
| **UT-004** | `forecasting` | `generate_forecast` | Verify that the output DataFrame has the correct columns (`actuals`, `forecast`). | Test passes. |
| **UT-005** | `forecasting` | `generate_forecast` | Verify the output length is `history + forecast_horizon`. | Test passes. |
| **UT-006** | `forecasting` | `generate_forecast` | Verify that a `ValueError` is raised when an invalid SKU is provided. | `ValueError` is caught. Test passes. |

### 4.2. Integration Test Cases (Manual API Check)

These tests are performed against a running application server.

| Test Case ID | Endpoint | Method | Description | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **IT-001** | `/gradio_api/mcp/sse` | `POST` | Send a valid MCP request for a known SKU. | A `200 OK` response with a JSON payload containing forecast data. The `result` field is not null. |
| **IT-002** | `/gradio_api/mcp/sse` | `POST` | Send an MCP request with a non-existent SKU. | A `200 OK` response with a JSON payload containing an `error` object. |
| **IT-003** | `/gradio_api/mcp/sse` | `POST` | Send an MCP request with a malformed JSON body. | A `4xx` error response (e.g., `422 Unprocessable Entity`). |

### 4.3. End-to-End Test Cases (Manual UI Checklist)

This checklist will be executed manually before each deployment to ensure the user experience is correct.

| Test Case ID | User Action | Description | Expected Result |
| :--- | :--- | :--- | :--- |
| **E2E-001** | App Launch | Launch the application using `python app.py`. | The Gradio interface loads in the browser without any errors. The SKU dropdown is populated with items from the default CSV. |
| **E2E-002** | Default Forecast | Select the first SKU from the dropdown. | The "Forecast Visualization" plot updates, showing a blue line for historicals and a red dashed line for the forecast. The plot title updates to include the selected SKU. |
| **E2E-003** | Clear Selection | Clear the selection from the dropdown menu. | The plot clears and displays a "Please select a product SKU..." message. |
| **E2E-004** | **[Future]** File Upload | Use the "Upload CSV" component to upload a valid, compatible CSV file. | The SKU dropdown is cleared and repopulated with the SKUs from the new file. |
| **E2E-005** | **[Future]** Forecast from Upload | Select a SKU from the newly populated dropdown. | A new forecast plot is generated correctly based on the data from the uploaded file. |
| **E2E-006** | **[Future]** Invalid File Upload | Upload a file that is not a CSV or has an incompatible schema. | A user-friendly error message is displayed, and the application does not crash. The SKU dropdown remains unchanged. |

**(Note:** Test cases marked **[Future]** correspond to functionality that is planned but not yet implemented.)