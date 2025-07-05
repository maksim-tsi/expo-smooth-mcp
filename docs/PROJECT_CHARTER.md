# Project Charter: Exponential Smoothing via MCP

- **Version:** 1.0
- **Status:** Final
- **Last Updated:** 2025-07-05 by Maksim Ilin
- **Summary:** This document defines the mission, scope, success criteria, and high-level architecture for the `expo-smooth-mcp` research project.

---

## 1. Research Question

The central research question this project aims to address is:

> **To what extent can encapsulating an Exponential Smoothing model as a tool, served via the Model Context Protocol (MCP), enhance the reliability and utility of an LLM-based assistant for common logistics forecasting tasks?**

## 2. Goals & Success Criteria

### Project Goals
1.  To develop a functional, interactive prototype demonstrating the integration of a statistical forecasting model with an LLM-accessible architecture.
2.  To produce a research paper detailing our approach and findings, suitable for submission to the RelStat conference.

### Success Criteria
The project will be considered successful when the following criteria are met:

*   **Prototype Success (Definition of Done):**
    *   **Unit Tests:** A `pytest` suite for critical data preprocessing and forecasting functions achieves a 100% pass rate.
    *   **Application Executability:** The Gradio application launches without error and allows a user to:
        1.  Load the default FMCG dataset automatically.
        2.  Select any Product SKU from a dynamically populated dropdown.
        3.  Generate and display a forecast plot and key metrics.
        4.  Upload a custom CSV file, which then correctly populates the product selector.
    *   **MCP Server Executability:** The MCP endpoint is verifiable via an MCP client (e.g., `curl`), returning a valid JSON forecast when provided with a valid SKU.

*   **Research Success:**
    *   The primary research goal is achieved upon the **acceptance of our research paper for publication at the RelStat conference.**

## 3. Scope

### In-Scope
*   **Modeling:** Implementation of Exponential Smoothing, including the Holt-Winters method to handle trend and seasonality.
*   **User Interface:** A Gradio web application for interactive forecasting and visualization.
*   **API:** An MCP server exposing the forecasting function as a callable tool.
*   **Data Handling:** The application will load from a local CSV by default and will support user uploads of custom CSV files with a compatible schema.
*   **Deployment:** A publicly accessible demo hosted on Hugging Face Spaces.

### Out-of-Scope
*   **Alternative Models:** Implementation of ARIMA, Regression, or other machine learning models.
*   **Production Features:** User authentication, permissions, persistent user storage, or a production-grade database. The application is a self-contained research prototype.
*   **Advanced Error Handling:** Error handling will be limited to basic input validation.

## 4. Key Deliverables

1.  **Application Source Code:** All Python scripts (`app.py`, `mcp_server.py`, etc.), and configuration files (`requirements.txt`).
2.  **Public GitHub Repository:** A well-documented repository containing all code and documentation.
3.  **Live Hugging Face Spaces Demo:** A publicly accessible, interactive web application.
4.  **Project Documentation:** A `/docs` directory containing this Charter, developer guides, and a `/ADRs` directory for key decisions.
5.  **Research Paper Draft:** A complete draft of the paper for submission to RelStat.

## 5. Technology Stack

*   **Language:** Python 3.10
*   **Data Handling:** Pandas
*   **Statistical Modeling:** Statsmodels
*   **UI & API Server:** Gradio (`gradio[mcp]`)
*   **Web Server:** Uvicorn
*   **Deployment Platform:** Hugging Face Spaces
*   **Version Control:** Git
*   **Environment Management:** Conda / Pip + venv

## 6. Data Architecture & Preprocessing Plan

*   **Data Source:** The project will use the "FMCG Sales Demand Forecasting and Optimization" dataset from Kaggle, stored locally as `FMCG_Sales.csv`.
*   **Preprocessing Pipeline:** All data (default or user-uploaded) will be processed through the following standardized pipeline:
    1.  **Load Data:** Read the CSV into a pandas DataFrame.
    2.  **Standardize Columns:** Rename columns to `date`, `sku`, `quantity`, and `warehouse`.
    3.  **Convert Data Types:** Convert `date` to datetime objects and ensure `quantity` is numeric.
    4.  **Clean Data:** Drop any rows with null values in `date`, `sku`, or `quantity`.
    5.  **Aggregate Daily Sales:** Group data by `date` and `sku` and sum the `quantity` to ensure a unique value per product per day.
    6.  **Create Continuous Time Index:** For each `sku`, create a complete, unbroken daily date range from its first to its last sale date. Reindex the data against this range and fill any resulting missing `quantity` values with `0`.
*   **Final Structure:** The processed DataFrame will have a `MultiIndex` of `(sku, date)` and a single `quantity` column, ready for modeling.

## 7. Testing Approach

*   **Unit Testing:**
    *   **Tool:** `pytest`
    *   **Scope:** Key data preprocessing and forecasting functions will be tested in isolation.
    *   **Location:** `test_*.py` files.
*   **Integration Testing:**
    *   **Tool:** `curl` or VS Code MCP Client extension.
    *   **Scope:** Verify the connection between the running server and the forecasting function via the MCP endpoint (`/gradio_api/mcp/sse`).
*   **End-to-End (E2E) Manual Testing:**
    *   **Tool:** Human tester following a checklist.
    *   **Scope:** Validate the full user workflow in the Gradio application, including default data loading, SKU selection, plot generation, and custom CSV upload.