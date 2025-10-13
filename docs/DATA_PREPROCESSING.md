
# Data Preprocessing Guide

- **Version:** 1.0
- **Status:** Final
- **Last Updated:** 2025-07-05 by Maksim Ilin
- **Summary:** This document provides the definitive, step-by-step guide for transforming the raw FMCG sales data into a clean, model-ready format for time-series forecasting.

---

## 1. Objective

The purpose of this guide is to serve as the technical specification for a Python function that preprocesses our sales data. Following these steps ensures that the input to our Exponential Smoothing model is consistent, clean, and correctly structured, which is critical for reproducibility and model accuracy.

## 2. Input and Output Schema

*   **Input:** A pandas DataFrame loaded from the `FMCG_Sales.csv` file.
    *   **Expected Columns:** `Warehouse`, `OrderDate`, `Product_Code`, `Order_Quantity`.

*   **Output:** A pandas DataFrame with the following characteristics:
    *   **Index:** A pandas `MultiIndex` with levels `sku` (string) and `date` (datetime).
    *   **Columns:** A single `quantity` column (integer).
    *   **Properties:** The DataFrame will have no null values, and the time series for each SKU will be continuous (i.e., no missing dates).

## 3. Proposed Function Signature

The implementation of this guide should adhere to the following function signature, to be placed in a `preprocessing.py` module.

```python
import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms the raw FMCG sales data into a model-ready time-series format.

    Args:
        df (pd.DataFrame): The raw DataFrame loaded from the CSV.

    Returns:
        pd.DataFrame: A cleaned DataFrame with a (sku, date) MultiIndex and a 'quantity' column.
    """
    # Implementation will follow the steps below
    pass
```

## 4. Step-by-Step Implementation Guide

1.  **Standardize Column Names:**
    Create a mapping to rename the columns for consistency.

    ```python
    column_mapping = {
        'OrderDate': 'date',
        'Product_Code': 'sku',
        'Order_Quantity': 'quantity',
        'Warehouse': 'warehouse'
    }
    df = df.rename(columns=column_mapping)
    ```

2.  **Ensure Correct Data Types:**
    Convert columns to their appropriate types. This is crucial for date-based operations.

    ```python
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = pd.to_numeric(df['quantity'])
    ```

3.  **Clean Invalid Data:**
    Remove any rows that have null values in the essential columns.

    ```python
    df.dropna(subset=['date', 'sku', 'quantity'], inplace=True)
    ```

4.  **Aggregate to Daily Sales per SKU:**
    The dataset may contain multiple orders for the same SKU on the same day. We must sum these to get a single daily total.

    ```python
    daily_sales = df.groupby(['sku', 'date'])['quantity'].sum().reset_index()
    ```

5.  **Create Continuous Time Index:**
    This is the most critical step for time-series modeling. We will ensure each SKU has an unbroken timeline from its first to its last sale, filling non-sale days with zero.

    ```python
    # Create the final model-ready DataFrame by iterating through each SKU
    model_ready_dfs = []
    for sku in daily_sales['sku'].unique():
        # Isolate the data for one SKU
        sku_df = daily_sales[daily_sales['sku'] == sku]
        
        # Set the date as the index
        sku_df = sku_df.set_index('date')
        
        # Determine the full date range for this SKU
        min_date = sku_df.index.min()
        max_date = sku_df.index.max()
        full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        
        # Reindex the DataFrame to the full range and fill missing values with 0
        sku_df = sku_df.reindex(full_date_range)
        sku_df['quantity'].fillna(0, inplace=True)
        
        # Add back the sku identifier
        sku_df['sku'] = sku
        
        model_ready_dfs.append(sku_df)

    # Concatenate all SKU DataFrames and set the final MultiIndex
    final_df = pd.concat(model_ready_dfs).set_index(['sku'], append=True).reorder_levels(['sku', 'date'])
    ```

## 5. Validation Checks

The `preprocess_data` function should be tested to ensure its output meets the following conditions:

*   The function returns a pandas DataFrame.
*   The DataFrame's index is a `pd.MultiIndex`.
*   The names of the index levels are `['sku', 'date']`.
*   The DataFrame has exactly one column named `quantity`.
*   There are no `NaN` values in the `quantity` column (`df['quantity'].isnull().sum() == 0`).

## 6. User-Provided Data Support

The system now supports user-provided data files through both the Gradio web interface and MCP server. This section documents the requirements and processing for custom data uploads.

### Supported File Formats

- **CSV** (.csv): Comma-separated values with automatic delimiter detection
- **Excel** (.xlsx, .xls): Microsoft Excel spreadsheets (first sheet used)
- **JSON** (.json): JavaScript Object Notation with array of objects format

### Required Data Structure

User-provided data files must contain the following information:

1. **Date Column**: Transaction/order dates
   - Accepted names: `date`, `Date`, `order_date`, `OrderDate`, `timestamp`, `Timestamp`
   - Format: Automatically parsed (ISO dates, MM/DD/YYYY, DD-MM-YYYY, etc.)

2. **Product/SKU Column**: Product or SKU identifiers  
   - Accepted names: `sku`, `SKU`, `product`, `Product`, `product_code`, `Product_Code`, `item`, `Item`
   - Type: String/text values

3. **Quantity Column**: Sales/order quantities
   - Accepted names: `quantity`, `Quantity`, `sales`, `Sales`, `order_quantity`, `Order_Quantity`, `amount`, `Amount`
   - Type: Numeric values (integers or floats)

### Data Quality Requirements

- **No Missing Values**: Essential columns (date, sku, quantity) cannot contain null/empty values
- **Valid Dates**: Date values must be parseable by pandas `to_datetime()`
- **Numeric Quantities**: Quantity values must be convertible to numbers
- **Reasonable Size**: Files should be under 100KB when Base64-encoded for MCP usage

### Processing Pipeline for Custom Data

When a user uploads a file, the system follows this processing pipeline:

1. **File Type Detection**: Based on file extension and content analysis
2. **Column Name Mapping**: Automatic mapping of user columns to standard names
3. **Data Type Conversion**: Dates to datetime, quantities to numeric
4. **Data Validation**: Check for required columns and data quality
5. **Preprocessing**: Apply the same cleaning and aggregation steps as the default dataset
6. **SKU Extraction**: Identify available products for forecasting

### Error Handling

The system provides clear error messages for common issues:

- **Missing Required Columns**: "Could not identify required columns (date, sku, quantity) in uploaded file"
- **Invalid Data Types**: "Quantity column contains non-numeric values"
- **Empty File**: "Uploaded file contains no data"
- **Unsupported Format**: "File format not supported. Please use CSV, Excel, or JSON"
- **File Too Large**: "File exceeds size limit (100KB Base64-encoded). Please use a smaller file"

### Example Data Formats

**CSV Format:**
```csv
date,product_code,sales_amount
2024-01-01,PROD_001,150
2024-01-02,PROD_001,200
2024-01-01,PROD_002,75
```

**JSON Format:**
```json
[
  {"date": "2024-01-01", "sku": "PROD_001", "quantity": 150},
  {"date": "2024-01-02", "sku": "PROD_001", "quantity": 200},
  {"date": "2024-01-01", "sku": "PROD_002", "quantity": 75}
]
```

**Excel Format:**
| date       | sku      | quantity |
|------------|----------|----------|
| 2024-01-01 | PROD_001 | 150      |
| 2024-01-02 | PROD_001 | 200      |
| 2024-01-01 | PROD_002 | 75       |