"""
Tests for column analysis module.
"""
import pytest
import pandas as pd
from src.expo_smooth_mcp.column_analysis import (
    analyze_columns,
    validate_column_mapping,
    _score_date_column,
    _score_metric_column,
    _score_product_column
)


class TestAnalyzeColumns:
    """Test the analyze_columns function."""

    def test_analyze_standard_columns(self):
        """Test analysis of standard column names."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'sku': ['A', 'B'],
            'quantity': [100, 200]
        })

        result = analyze_columns(df)

        assert result['suggested_date'] == 'date'
        assert result['suggested_metric'] == 'quantity'
        assert result['suggested_product'] == 'sku'
        assert len(result['date_candidates']) == 1
        assert len(result['metric_candidates']) == 1
        assert len(result['product_candidates']) == 1

    def test_analyze_custom_columns(self):
        """Test analysis of custom column names."""
        df = pd.DataFrame({
            'OrderDate': ['2024-01-01', '2024-01-02'],
            'Product_Code': ['A', 'B'],
            'Order_Quantity': [100, 200]
        })

        result = analyze_columns(df)

        assert result['suggested_date'] == 'OrderDate'
        assert result['suggested_metric'] == 'Order_Quantity'
        assert result['suggested_product'] == 'Product_Code'

    def test_analyze_mixed_columns(self):
        """Test analysis with mixed column types."""
        df = pd.DataFrame({
            'timestamp': ['2024-01-01', '2024-01-02'],
            'product_id': ['A', 'B'],
            'sales': [100.5, 200.5],
            'category': ['X', 'Y'],
            'notes': ['note1', 'note2']
        })

        result = analyze_columns(df)

        assert result['suggested_date'] == 'timestamp'
        assert result['suggested_metric'] == 'sales'
        assert result['suggested_product'] == 'product_id'

    def test_analyze_no_good_candidates(self):
        """Test analysis when no good candidates are found."""
        df = pd.DataFrame({
            'name': ['John', 'Jane'],
            'age': [25, 30],
            'city': ['NY', 'LA']
        })

        result = analyze_columns(df)

        assert result['suggested_date'] is None
        assert result['suggested_metric'] == 'age'  # Only numeric column
        assert result['suggested_product'] is None

    def test_analyze_empty_dataframe(self):
        """Test analysis of empty DataFrame."""
        df = pd.DataFrame()

        result = analyze_columns(df)

        assert result['all_columns'] == []
        assert result['suggested_date'] is None
        assert result['suggested_metric'] is None
        assert result['suggested_product'] is None

    def test_analyze_none_dataframe(self):
        """Test analysis with None input."""
        result = analyze_columns(None)

        assert result['all_columns'] == []
        assert result['suggested_date'] is None
        assert result['suggested_metric'] is None
        assert result['suggested_product'] is None


class TestScoreDateColumn:
    """Test the _score_date_column function."""

    def test_score_date_exact_match(self):
        """Test scoring with exact date keyword match."""
        series = pd.Series(['2024-01-01', '2024-01-02'])
        score = _score_date_column(series, 'date')
        assert score == 1.0  # 0.5 keyword + 0.5 parseable

    def test_score_date_partial_match(self):
        """Test scoring with partial date keyword match."""
        series = pd.Series(['2024-01-01', '2024-01-02'])
        score = _score_date_column(series, 'order_date')
        assert score == 1.0  # 0.5 keyword + 0.5 parseable

    def test_score_date_no_keyword(self):
        """Test scoring with parseable dates but no keyword."""
        series = pd.Series(['2024-01-01', '2024-01-02'])
        score = _score_date_column(series, 'created_at')
        assert score == 0.5  # 0.5 parseable only

    def test_score_date_unparseable(self):
        """Test scoring with unparseable data."""
        series = pd.Series(['not a date', 'also not'])
        score = _score_date_column(series, 'date')
        assert score == 0.5  # 0.5 keyword only


class TestScoreMetricColumn:
    """Test the _score_metric_column function."""

    def test_score_metric_exact_match(self):
        """Test scoring with exact metric keyword match."""
        series = pd.Series([100, 200, 300])
        score = _score_metric_column(series, 'sales')
        assert score == 1.0  # 0.8 exact match + 0.2 non-negative

    def test_score_metric_partial_match(self):
        """Test scoring with partial metric keyword match."""
        series = pd.Series([100, 200, 300])  # 3 unique out of 3 (100% unique)
        score = _score_metric_column(series, 'order_quantity')
        assert abs(score - 0.8) < 1e-10  # 0.5 partial match + 0.2 non-negative + 0.1 variance

    def test_score_metric_no_keyword_positive(self):
        """Test scoring with no keyword but positive values."""
        series = pd.Series([100, 200, 300])  # 3 unique out of 3 (100% unique)
        score = _score_metric_column(series, 'measurement')  # Not a keyword
        assert abs(score - 0.3) < 1e-10  # 0.2 non-negative + 0.1 variance

    def test_score_metric_negative_values(self):
        """Test scoring with negative values."""
        series = pd.Series([-100, 200, 300])  # 2/3 non-negative (<90%), 3/3 unique (100%)
        score = _score_metric_column(series, 'sales')
        assert score == 0.9  # 0.8 keyword exact match + 0.1 variance (no non-negative bonus)


class TestScoreProductColumn:
    """Test the _score_product_column function."""

    def test_score_product_exact_match(self):
        """Test scoring with exact product keyword match."""
        series = pd.Series(['A', 'A', 'A', 'B'])  # 2 unique out of 4 (0.5 ratio, not < 0.5)
        score = _score_product_column(series, 'sku')
        assert score == 0.8  # 0.8 exact match only (cardinality not in bonus range)

    def test_score_product_partial_match(self):
        """Test scoring with partial product keyword match."""
        series = pd.Series(['A', 'A', 'A', 'B'])  # 2/4 = 0.5 ratio, not < 0.5
        score = _score_product_column(series, 'product_code')
        assert score == 0.5  # 0.5 partial match only (no cardinality bonus)

    def test_score_product_good_cardinality(self):
        """Test scoring with good cardinality but no keyword."""
        series = pd.Series(['A', 'A', 'A', 'A', 'B', 'B'])  # 2 unique out of 6 (0.33 ratio)
        score = _score_product_column(series, 'reference')
        assert score == 0.2  # 0.2 cardinality only

    def test_score_product_bad_cardinality(self):
        """Test scoring with bad cardinality."""
        series = pd.Series(['A'] * 100)  # All same value
        score = _score_product_column(series, 'sku')
        assert score == 0.8  # 0.8 keyword only (cardinality too low)


class TestValidateColumnMapping:
    """Test the validate_column_mapping function."""

    def test_validate_valid_mapping(self):
        """Test validation of valid column mapping."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'sku': ['A', 'B'],
            'quantity': [100, 200]
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is True
        assert result['errors'] == []
        assert result['warnings'] == []

    def test_validate_missing_date_column(self):
        """Test validation when date column doesn't exist."""
        df = pd.DataFrame({
            'sku': ['A', 'B'],
            'quantity': [100, 200]
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is False
        assert len(result['errors']) == 1
        assert 'Date column \'date\' not found' in result['errors'][0]

    def test_validate_missing_metric_column(self):
        """Test validation when metric column doesn't exist."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'sku': ['A', 'B']
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is False
        assert len(result['errors']) == 1
        assert 'Metric column \'quantity\' not found' in result['errors'][0]

    def test_validate_invalid_date_format(self):
        """Test validation with invalid date format."""
        df = pd.DataFrame({
            'date': ['not a date', 'also invalid'],
            'sku': ['A', 'B'],
            'quantity': [100, 200]
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is False
        assert len(result['errors']) == 1
        assert 'too many invalid dates' in result['errors'][0]

    def test_validate_non_numeric_metric(self):
        """Test validation with non-numeric metric column."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'sku': ['A', 'B'],
            'quantity': ['100', '200']  # String instead of numeric
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is False
        assert len(result['errors']) == 1
        assert 'must be numeric' in result['errors'][0]

    def test_validate_missing_values_warning(self):
        """Test validation with missing values in metric column."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'sku': ['A', 'B', 'C'],
            'quantity': [100, None, 200]  # One missing value
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is True
        assert result['errors'] == []
        assert len(result['warnings']) == 1
        assert 'missing values' in result['warnings'][0]

    def test_validate_partial_date_parsing_warning(self):
        """Test validation with some invalid dates."""
        df = pd.DataFrame({
            'date': ['2024-01-01', 'not a date', '2024-01-03'],
            'sku': ['A', 'B', 'C'],
            'quantity': [100, 200, 300]
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is True
        assert result['errors'] == []
        assert len(result['warnings']) == 1
        assert 'some invalid dates' in result['warnings'][0]

    def test_validate_optional_product_column(self):
        """Test validation without product column (optional)."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'quantity': [100, 200]
        })

        result = validate_column_mapping(df, 'date', 'quantity')

        assert result['valid'] is True
        assert result['errors'] == []
        assert result['warnings'] == []

    def test_validate_missing_product_column(self):
        """Test validation when specified product column doesn't exist."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'quantity': [100, 200]
        })

        result = validate_column_mapping(df, 'date', 'quantity', 'sku')

        assert result['valid'] is False
        assert len(result['errors']) == 1
        assert 'Product column \'sku\' not found' in result['errors'][0]