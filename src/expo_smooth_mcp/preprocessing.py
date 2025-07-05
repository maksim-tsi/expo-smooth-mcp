import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms the raw FMCG sales data into a model-ready time-series format.

    This function follows the steps outlined in the project's DATA_PREPROCESSING.md guide.

    Args:
        df (pd.DataFrame): The raw DataFrame, typically loaded from the source CSV.

    Returns:
        pd.DataFrame: A cleaned DataFrame with a (sku, date) MultiIndex and a 'quantity' column,
                      ready for time-series analysis.
    """
    # 1. Standardize Column Names
    column_mapping = {
        'OrderDate': 'date',
        'Product_Code': 'sku',
        'Order_Quantity': 'quantity',
        'Warehouse': 'warehouse'
    }
    df = df.rename(columns=column_mapping)

    # 2. Ensure Correct Data Types
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce') # Coerce errors will be dropped

    # 3. Clean Invalid Data
    essential_columns = ['date', 'sku', 'quantity']
    df.dropna(subset=essential_columns, inplace=True)
    df['quantity'] = df['quantity'].astype(int)

    # 4. Aggregate to Daily Sales per SKU
    daily_sales = df.groupby(['sku', 'date'])['quantity'].sum().reset_index()

    # 5. Create Continuous Time Index
    model_ready_dfs = []
    for sku in daily_sales['sku'].unique():
        sku_df = daily_sales[daily_sales['sku'] == sku].copy()
        sku_df = sku_df.set_index('date')
        
        min_date = sku_df.index.min()
        max_date = sku_df.index.max()
        
        # Create a full date range for this SKU
        full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        
        # Reindex, fill missing values with 0, and ensure correct types
        sku_df = sku_df.reindex(full_date_range)
        sku_df['quantity'].fillna(0, inplace=True)
        sku_df['quantity'] = sku_df['quantity'].astype(int)
        
        # Add back the sku identifier (which was lost during reindexing)
        sku_df['sku'] = sku
        
        model_ready_dfs.append(sku_df)
    
    # Concatenate all SKU DataFrames and set the final MultiIndex
    if not model_ready_dfs:
        return pd.DataFrame(columns=['quantity']).set_index(['sku', 'date']) # Return empty if no data
        
    final_df = pd.concat(model_ready_dfs)
    final_df = final_df.reset_index().rename(columns={'index': 'date'})
    final_df = final_df.set_index(['sku', 'date'])
    
    return final_df[['quantity']] # Return only the quantity column