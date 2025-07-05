
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