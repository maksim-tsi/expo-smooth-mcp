---
title: Exponential Smoothing for Supply Chain Forecasting
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
python_version: 3.10
requirements_file: requirements.txt
---

# Exponential Smoothing Forecasting via Model Context Protocol (MCP)

This repository contains the implementation for our research on provisioning established statistical methods to Large Language Model (LLM) agents. It features a Gradio web application that provides an interactive demonstration of Exponential Smoothing for time-series forecasting, using a real-world Supply Chain Management (SCM) dataset.

## Research Context and Motivation

This project serves as a proof-of-concept for research aimed at enhancing LLM-based assistants with robust, traditional statistical capabilities. While LLMs excel at reasoning and language, they are not inherently reliable for precise mathematical forecasting.

Our central hypothesis is that by encapsulating trusted statistical models (like Exponential Smoothing) as tools and serving them via the **Model Context Protocol (MCP)**, we can create AI agents that are both conversational and quantitatively sound. This approach allows an LLM to "call" the statistical tool when a user asks for a forecast, grounding its response in a proven algorithm.

## System Architecture

The system is designed with a clear separation of concerns, enabling the LLM to leverage a specialized forecasting tool:

```
+-----------+       +------------------+       +---------------------+
|   User    | <---> |  Gradio Web App  | <---> |   LLM-based Agent   |
+-----------+       +------------------+       +----------+----------+
                                                          |
                                  (MCP Request: "Forecast SKU X")
                                                          |
                                                 +--------v--------+
                                                 |    MCP Server   |
                                                 | (Python/Flask)  |
                                                 +--------+--------+
                                                          |
                                              +-----------v-----------+
                                              | Exponential Smoothing |
                                              |   (statsmodels)       |
                                              +-----------------------+
```

## Live Demo (Hugging Face Space)

You can try out the live Gradio application hosted on Hugging Face Spaces. This demo allows you to select a product and visualize its demand forecast.

**[Visit the Hugging Face Space here!](YOUR_HUGGING_FACE_SPACE_URL_HERE)**
*(e.g., https://huggingface.co/spaces/your-username/expo-smooth-mcp)*

## GitHub Repository

The complete source code for this project is hosted publicly on GitHub. You are welcome to explore the implementation, open issues, or suggest improvements.

**[Visit the GitHub Repository here!](YOUR_GITHUB_REPO_URL_HERE)**
*(e.g., https://github.com/your-username/expo-smooth-mcp)*

## Dataset

This demonstration uses a real-world public dataset to ensure the results are relevant and reproducible.

*   **Title:** FMCG Sales Demand Forecasting and Optimization
*   **Source:** Kaggle
*   **Link:** [https://www.kaggle.com/datasets/krishanukalita/fmcg-sales-demand-forecasting-and-optimization](https://www.kaggle.com/datasets/krishanukalita/fmcg-sales-demand-forecasting-and-optimization)
*   **Description:** The dataset contains daily order quantities for various products across different warehouses, making it ideal for demonstrating time-series forecasting.

## Custom Data Support

The application now supports user-provided data for both interactive analysis and programmatic access. You can upload your own sales data through the Gradio web interface or use the MCP server for automated forecasting.

### Supported File Formats

- **CSV files** (.csv) - Comma-separated values
- **Excel files** (.xlsx, .xls) - Microsoft Excel spreadsheets  
- **JSON files** (.json) - JavaScript Object Notation

### Data Format Requirements

The application is designed to be flexible and can work with various data formats.

#### Option 1: Default Column Names
If your data uses the following standard column names, no extra configuration is needed:
- **`date`**: The column containing dates or timestamps.
- **`sales`**: The numeric column with the values you want to forecast (e.g., sales, quantity, revenue).
- **`sku`**: The column with product identifiers (optional, for multi-product datasets).

#### Option 2: Custom Column Names
If your data uses different column names (e.g., `transaction_date`, `revenue`, `product_id`), you can easily map them to the required fields.

- **Gradio UI**: After uploading your file, a "Column Mapping" section will appear, allowing you to select which of your columns correspond to the Date, Metric, and Product fields. The system will provide smart suggestions to guide you.
- **MCP Tool**: When calling the `forecast_with_custom_data` tool, you can use the optional `date_col`, `metric_col`, and `product_col` parameters to specify your column names.

**Example CSV with custom columns:**
```csv
transaction_date,product_id,revenue
2024-01-01,WIDGET-A,150.75
2024-01-02,WIDGET-A,165.50
2024-01-01,GADGET-B,80.00
2024-01-02,GADGET-B,95.25
```

### Gradio Web Interface

1. **Upload Your Data**: Use the file upload area in the Gradio interface to select and upload your CSV, Excel, or JSON file.
2. **Map Your Columns**: If your column names are non-standard, use the dropdowns that appear to map your columns to the required `Date`, `Metric`, and `Product` fields.
3. **Generate Forecasts**: Select a product from the updated dropdown and specify your forecast horizon to generate predictions.

### MCP Server Tool

For programmatic access, use the `forecast_with_custom_data` MCP tool.

**Tool Parameters:**
- `file_data_base64` (str): Base64-encoded file content.
- `file_name` (str): Original filename (for format detection).
- `sku` (str): Product/SKU identifier to forecast.
- `forecast_horizon` (int): Number of days to forecast (default: 90).
- `date_col` (Optional[str]): Name of your date column.
- `metric_col` (Optional[str]): Name of your metric/sales column.
- `product_col` (Optional[str]): Name of your product/SKU column.

**Size Limit**: Files must be under 100KB when Base64-encoded (approximately 66KB raw data).

**Example 1: Using Default Column Names (`date`, `sales`, `sku`)**
```python
# Encode your CSV file to Base64
import base64
with open('my_sales_data.csv', 'rb') as f:
    file_data = base64.b64encode(f.read()).decode('utf-8')

# Call the MCP tool
result = await forecast_with_custom_data(
    file_data_base64=file_data,
    file_name="my_sales_data.csv", 
    sku="PRODUCT_A",
    forecast_horizon=30
)
```

**Example 2: Using Custom Column Names**
```python
# Assume your data has columns: 'transaction_date', 'revenue', 'product_id'
result = await forecast_with_custom_data(
    file_data_base64=file_data,
    file_name="my_sales_data.csv", 
    sku="WIDGET-A",
    forecast_horizon=30,
    date_col="transaction_date",
    metric_col="revenue",
    product_col="product_id"
)
```

## Getting Started (Local Development)

To set up and run this project on your local machine, please follow the instructions below.

### For External Contributors (Recommended Method)

If you are contributing for the first time or prefer using standard Python virtual environments, this is the recommended approach.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/maksim-tsi/expo-smooth-mcp.git
    cd expo-smooth-mcp
    ```

2.  **Create and Activate a Virtual Environment:**
    We recommend using `venv`, which is included with Python.
    ```bash
    # Create the environment
    python -m venv venv

    # Activate the environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required packages using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio Application:**
    ```bash
    python app.py
    ```
    Access the application in your browser at the local URL provided (e.g., `http://127.0.0.1:7860/`).

---

<details>
<summary><b>Alternative Setup for Conda Users</b></summary>

If you prefer using `conda` for environment management, you can follow these steps to create a new, dedicated environment for this project.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/maksim-tsi/expo-smooth-mcp.git
    cd expo-smooth-mcp
    ```

2.  **Create and Activate a Conda Environment:**
    This command creates a new environment named `expo-smooth-mcp` with the specified Python version.
    ```bash
    conda create --name expo-smooth-mcp python=3.10 -y
    conda activate expo-smooth-mcp
    ```

3.  **Install Dependencies:**
    Once the environment is active, install the required packages using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio Application:**
    ```bash
    python app.py
    ```

</details>

<br>

<details>
<summary><b>For the Core Development Team (Internal)</b></summary>

This section is for the core team using the pre-configured `tsi` conda environment.

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone git@github.com-alternative:maksim-tsi/expo-smooth-mcp.git
    cd expo-smooth-mcp
    ```

2.  **Activate the Shared Environment:**
    ```bash
    conda activate tsi
    ```

3.  **Sync Dependencies:**
    Even when using a shared environment, it's crucial to ensure you have the exact package versions for this project. This command will update/install the necessary dependencies within the active `tsi` environment.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio Application:**
    ```bash
    python app.py
    ```

</details>

## Documentation

### Project Planning & Specifications
- **[Project Roadmap](docs/PROJECT_ROADMAP.md)** - Timeline, status tracking, and milestones
- **[Technical Specification](docs/SPECIFICATION.md)** - Complete technical reference for all 65 tasks (~21,000 lines)
- **[Phase Implementation Guides](docs/implementation/)** - Focused guides for each development phase
- **[Project Charter](docs/PROJECT_CHARTER.md)** - Project goals, requirements, and scope

### Technical Documentation
- **[Architecture Decision Records (ADRs)](ADRs/)** - Key architectural decisions
- **[Test Plan](docs/TEST_PLAN.md)** - Comprehensive testing strategy
- **[Data Preprocessing](docs/DATA_PREPROCESSING.md)** - Data pipeline documentation

### Development Guides  
- **[Phase 1: Decouple Logic](docs/implementation/PHASE_1_IMPLEMENTATION.md)** - Extract business logic
- **[Phase 2: FastMCP Backend](docs/implementation/PHASE_2_IMPLEMENTATION.md)** - Build MCP server with dual-transport
- **[Phase 2: Code Review](docs/PHASE_2_CODE_REVIEW.md)** - Comprehensive code review and validation
- **[Phase 3: Mount Gradio UI](docs/implementation/PHASE_3_IMPLEMENTATION.md)** - Integrate Gradio web interface
- **[Phase 3: Quick Start](docs/implementation/PHASE_3_QUICKSTART.md)** - Quick reference for Phase 3

### Claude Desktop Integration
- **[Claude Desktop Test Report](docs/CLAUDE_DESKTOP_TEST_REPORT.md)** - Complete validation test results
- **[Integration Guide](docs/PHASE_2_CODE_REVIEW.md#claude-desktop-integration)** - Setup instructions and troubleshooting

### Current Status
✅ **Phase 1 Complete** - Business logic extracted and validated (27/27 tests passing)  
✅ **Phase 2 Complete** - FastMCP backend deployed and validated with Claude Desktop  
📋 **Phase 3 Ready** - Gradio UI integration documentation complete, ready to implement

See [PROJECT_ROADMAP.md](docs/PROJECT_ROADMAP.md) for detailed status and timeline.

## Contribution

Contributions to this research project are welcome. Please feel free to fork the repository, create a new branch for your feature or bug fix, and submit a Pull Request.

## Citation

*A placeholder for our future publication will be added here upon acceptance.*