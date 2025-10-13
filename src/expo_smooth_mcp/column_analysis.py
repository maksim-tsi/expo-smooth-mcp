"""
Column Analysis Module for Intelligent Data Mapping.

This module provides lightweight heuristic-based detection of column types
in user-provided datasets, specifically for time-series forecasting in
supply chain management contexts.
"""

import pandas as pd
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


# Common column name patterns for different types
DATE_KEYWORDS = [
    'date', 'time', 'day', 'period', 'ds',
    'timestamp', 'datetime', 'order_date', 'orderdate',
    'transaction_date', 'week', 'month', 'year'
]

METRIC_KEYWORDS = [
    'sales', 'quantity', 'demand', 'revenue',
    'units', 'value', 'amount', 'y', 'units_sold',
    'order_quantity', 'qty', 'volume', 'orders'
]

PRODUCT_KEYWORDS = [
    'sku', 'product', 'item', 'id', 'code',
    'product_id', 'product_code', 'item_id', 'item_code',
    'productid', 'itemid', 'productcode', 'itemcode'
]


def analyze_columns(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze DataFrame columns and suggest mappings for forecasting.

    Uses lightweight heuristics to detect:
    - Date/time columns (for time series index)
    - Metric columns (numeric values to forecast)
    - Product identifier columns (for grouping/filtering)

    Args:
        df: Input DataFrame to analyze

    Returns:
        Dictionary with analysis results:
        {
            "all_columns": List of all column names,
            "date_candidates": List of likely date columns,
            "metric_candidates": List of likely metric columns,
            "product_candidates": List of likely product ID columns,
            "suggested_date": Best guess for date column,
            "suggested_metric": Best guess for metric column,
            "suggested_product": Best guess for product column,
            "analysis_details": Detailed scoring information
        }

    Example:
        >>> df = pd.read_csv("sales.csv")
        >>> analysis = analyze_columns(df)
        >>> print(f"Suggested date: {analysis['suggested_date']}")
        >>> print(f"Suggested metric: {analysis['suggested_metric']}")
    """
    if df is None or df.empty:
        return _empty_analysis()

    analysis = {
        "all_columns": df.columns.tolist(),
        "date_candidates": [],
        "metric_candidates": [],
        "product_candidates": [],
        "suggested_date": None,
        "suggested_metric": None,
        "suggested_product": None,
        "analysis_details": {}
    }

    # Analyze each column
    for col in df.columns:
        col_lower = str(col).lower().strip()
        col_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "scores": {}
        }

        # Check for date column
        date_score = _score_date_column(df[col], col_lower)
        if date_score > 0:
            col_info["scores"]["date"] = date_score
            analysis["date_candidates"].append({
                "column": col,
                "score": date_score
            })

        # Check for metric column (must be numeric)
        if pd.api.types.is_numeric_dtype(df[col]):
            metric_score = _score_metric_column(df[col], col_lower)
            if metric_score > 0:
                col_info["scores"]["metric"] = metric_score
                analysis["metric_candidates"].append({
                    "column": col,
                    "score": metric_score
                })

        # Check for product identifier column
        product_score = _score_product_column(df[col], col_lower)
        if product_score > 0:
            col_info["scores"]["product"] = product_score
            analysis["product_candidates"].append({
                "column": col,
                "score": product_score
            })

        analysis["analysis_details"][col] = col_info

    # Sort candidates by score
    analysis["date_candidates"].sort(key=lambda x: x["score"], reverse=True)
    analysis["metric_candidates"].sort(key=lambda x: x["score"], reverse=True)
    analysis["product_candidates"].sort(key=lambda x: x["score"], reverse=True)

    # Pick best suggestions
    if analysis["date_candidates"]:
        analysis["suggested_date"] = analysis["date_candidates"][0]["column"]

    if analysis["metric_candidates"]:
        analysis["suggested_metric"] = analysis["metric_candidates"][0]["column"]

    if analysis["product_candidates"]:
        analysis["suggested_product"] = analysis["product_candidates"][0]["column"]

    logger.info(f"Column analysis complete: {len(df.columns)} columns analyzed")
    logger.info(f"Suggestions - Date: {analysis['suggested_date']}, "
                f"Metric: {analysis['suggested_metric']}, "
                f"Product: {analysis['suggested_product']}")

    return analysis


def _score_date_column(series: pd.Series, col_name_lower: str) -> float:
    """
    Score how likely a column is to be a date/time column.

    Returns score from 0.0 (definitely not) to 1.0 (definitely is).
    """
    score = 0.0

    # Check column name keywords (0.5 points)
    for keyword in DATE_KEYWORDS:
        if keyword in col_name_lower:
            score += 0.5
            break

    # Check if data is parseable as datetime (0.5 points)
    # But only if it's not purely numeric (to avoid false positives with quantities)
    if not pd.api.types.is_numeric_dtype(series):
        try:
            # Test on a sample to avoid processing large datasets
            sample_size = min(100, len(series))
            sample = series.head(sample_size)

            parsed = pd.to_datetime(sample, errors='coerce')
            valid_ratio = parsed.notna().sum() / len(sample)

            # If >80% of values parse successfully, add score
            if valid_ratio > 0.8:
                score += 0.5
        except Exception:
            pass

    return min(score, 1.0)
def _score_metric_column(series: pd.Series, col_name_lower: str) -> float:
    """
    Score how likely a numeric column is to be a metric to forecast.

    Returns score from 0.0 (definitely not) to 1.0 (definitely is).
    """
    score = 0.0

    # Check column name keywords
    for keyword in METRIC_KEYWORDS:
        if keyword in col_name_lower:
            # Higher score for exact matches
            if col_name_lower == keyword:
                score += 0.8
            else:
                score += 0.5
            break

    # Check if values are reasonable for metrics (0.2 points)
    # Most metrics should be non-negative
    if (series >= 0).mean() > 0.9:
        score += 0.2

    return min(score, 1.0)
def _score_product_column(series: pd.Series, col_name_lower: str) -> float:
    """
    Score how likely a column is to be a product identifier.

    Returns score from 0.0 (definitely not) to 1.0 (definitely is).
    """
    score = 0.0

    # Check column name keywords
    for keyword in PRODUCT_KEYWORDS:
        if keyword in col_name_lower:
            # Higher score for exact matches
            if col_name_lower == keyword or col_name_lower == f"{keyword}_id":
                score += 0.8
            else:
                score += 0.5
            break

    # Check cardinality (0.2 points)
    # Product IDs typically have moderate cardinality
    unique_ratio = series.nunique() / len(series) if len(series) > 0 else 0
    if 0.01 < unique_ratio < 0.5:
        score += 0.2

    return min(score, 1.0)


def _empty_analysis() -> Dict[str, Any]:
    """Return empty analysis structure for edge cases."""
    return {
        "all_columns": [],
        "date_candidates": [],
        "metric_candidates": [],
        "product_candidates": [],
        "suggested_date": None,
        "suggested_metric": None,
        "suggested_product": None,
        "analysis_details": {}
    }


def validate_column_mapping(
    df: pd.DataFrame,
    date_column: str,
    metric_column: str,
    product_column: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate that specified column mapping is valid for forecasting.

    Args:
        df: DataFrame to validate against
        date_column: Name of the date column
        metric_column: Name of the metric column
        product_column: Optional name of product ID column

    Returns:
        Dictionary with validation results:
        {
            "valid": True/False,
            "errors": List of error messages,
            "warnings": List of warning messages
        }

    Example:
        >>> validation = validate_column_mapping(df, "OrderDate", "Sales", "SKU")
        >>> if not validation["valid"]:
        >>>     print("Errors:", validation["errors"])
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }

    # Check columns exist
    if date_column not in df.columns:
        result["valid"] = False
        result["errors"].append(f"Date column '{date_column}' not found in data")

    if metric_column not in df.columns:
        result["valid"] = False
        result["errors"].append(f"Metric column '{metric_column}' not found in data")

    if product_column and product_column not in df.columns:
        result["valid"] = False
        result["errors"].append(f"Product column '{product_column}' not found in data")

    if not result["valid"]:
        return result

    # Validate date column can be parsed
    try:
        parsed = pd.to_datetime(df[date_column], errors='coerce')
        valid_ratio = parsed.notna().sum() / len(df)

        if valid_ratio < 0.5:
            result["valid"] = False
            result["errors"].append(
                f"Date column '{date_column}' has too many invalid dates "
                f"({valid_ratio:.1%} valid)"
            )
        elif valid_ratio < 0.95:
            result["warnings"].append(
                f"Date column '{date_column}' has some invalid dates "
                f"({valid_ratio:.1%} valid)"
            )
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Cannot parse date column '{date_column}': {str(e)}")

    # Validate metric column is numeric
    if not pd.api.types.is_numeric_dtype(df[metric_column]):
        result["valid"] = False
        result["errors"].append(
            f"Metric column '{metric_column}' must be numeric, "
            f"got {df[metric_column].dtype}"
        )

    # Check for missing values
    if df[metric_column].isna().sum() > 0:
        missing_pct = df[metric_column].isna().mean() * 100
        result["warnings"].append(
            f"Metric column '{metric_column}' has {missing_pct:.1f}% missing values"
        )

    return result