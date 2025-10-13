# tests/test_logic.py
import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.expo_smooth_mcp import logic

# --- Fixtures ---

@pytest.fixture
def sample_df():
    """Create sample preprocessed DataFrame for testing."""
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    skus = ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_003']

    # Create MultiIndex DataFrame
    data = []
    for sku in skus:
        for date in dates:
            # Create realistic but simple test data
            quantity = hash(f"{sku}_{date}") % 100 + 10  # Deterministic but varied
            data.append({'date': date, 'sku': sku, 'quantity': quantity})

    df = pd.DataFrame(data)
    df = df.set_index(['sku', 'date'])
    return df

# --- Test Cases ---

class TestGetProcessedData:
    """Tests for get_processed_data() function."""

    def test_missing_file_raises_error(self):
        """Should raise FileNotFoundError for missing CSV."""
        with pytest.raises(FileNotFoundError, match="Data file not found"):
            logic.get_processed_data('nonexistent.csv', force_reload=True)

    def test_force_reload_parameter(self):
        """Should accept force_reload parameter without error."""
        # Test that force_reload works with existing file (should not raise error)
        df1 = logic.get_processed_data()
        df2 = logic.get_processed_data(force_reload=True)
        # Both should succeed and return data
        assert df1 is not None
        assert df2 is not None

class TestGetAvailableSkus:
    """Tests for get_available_skus() function."""

    def test_returns_sorted_skus(self, sample_df):
        """Should return sorted list of unique SKUs."""
        result = logic.get_available_skus(sample_df)
        expected = ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_003']
        assert result == expected
        assert isinstance(result, list)

    def test_empty_dataframe_raises_error(self):
        """Should raise ValueError for empty DataFrame."""
        with pytest.raises(ValueError, match="DataFrame is empty"):
            logic.get_available_skus(pd.DataFrame())

    def test_invalid_index_raises_error(self):
        """Should raise ValueError if no 'sku' level in index."""
        df = pd.DataFrame({'col': [1, 2, 3]})
        with pytest.raises(ValueError, match="MultiIndex"):
            logic.get_available_skus(df)

class TestValidateForecastRequest:
    """Tests for validate_forecast_request() function."""

    def test_valid_request_returns_none(self, sample_df):
        """Should return None for valid inputs."""
        skus = logic.get_available_skus(sample_df)
        result = logic.validate_forecast_request('PRODUCT_001', 90, skus)
        assert result is None

    def test_invalid_sku_returns_error(self, sample_df):
        """Should return error message for non-existent SKU."""
        skus = logic.get_available_skus(sample_df)
        result = logic.validate_forecast_request('INVALID', 90, skus)
        assert result is not None
        assert "not found" in result

    def test_invalid_horizon_range_returns_error(self, sample_df):
        """Should return error message for out-of-range horizon."""
        skus = logic.get_available_skus(sample_df)
        result = logic.validate_forecast_request('PRODUCT_001', 500, skus)
        assert result is not None
        assert "between 1 and 365" in result

    def test_invalid_horizon_type_returns_error(self, sample_df):
        """Should return error message for non-integer horizon."""
        skus = logic.get_available_skus(sample_df)
        result = logic.validate_forecast_request('PRODUCT_001', "90", skus)
        assert result is not None
        assert "must be integer" in result

    def test_minimum_valid_horizon(self, sample_df):
        """Should accept minimum valid horizon (1)."""
        skus = logic.get_available_skus(sample_df)
        result = logic.validate_forecast_request('PRODUCT_001', 1, skus)
        assert result is None

    def test_maximum_valid_horizon(self, sample_df):
        """Should accept maximum valid horizon (365)."""
        skus = logic.get_available_skus(sample_df)
        result = logic.validate_forecast_request('PRODUCT_001', 365, skus)
        assert result is None

class TestGetForecastData:
    """Tests for get_forecast_data() function."""

    def test_returns_correct_structure(self, sample_df):
        """Should return dict with required keys."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)

        assert isinstance(result, dict)
        required_keys = {'dates', 'actuals', 'forecast', 'metadata'}
        assert set(result.keys()) == required_keys

    def test_dates_are_strings(self, sample_df):
        """Should return dates as ISO format strings."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)
        dates = result['dates']

        assert all(isinstance(d, str) for d in dates)
        # Check that dates look like ISO format
        assert len(dates) > 0
        assert '-' in dates[0]  # Contains date separators

    def test_actuals_and_forecast_are_lists(self, sample_df):
        """Should return actuals and forecast as lists."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)

        assert isinstance(result['actuals'], list)
        assert isinstance(result['forecast'], list)
        assert len(result['actuals']) == len(result['forecast'])

    def test_metadata_complete(self, sample_df):
        """Should include all metadata fields."""
        result = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)
        metadata = result['metadata']

        assert metadata['sku'] == 'PRODUCT_001'
        assert metadata['forecast_horizon'] == 5
        assert 'historical_points' in metadata
        assert 'forecast_points' in metadata
        assert isinstance(metadata['historical_points'], int)
        assert isinstance(metadata['forecast_points'], int)

    def test_invalid_sku_raises_error(self, sample_df):
        """Should raise ValueError for invalid SKU."""
        with pytest.raises(ValueError, match="not found"):
            logic.get_forecast_data(sample_df, 'INVALID', 5)

class TestCreateForecastPlot:
    """Tests for create_forecast_plot() function."""

    def test_returns_plotly_figure(self, sample_df):
        """Should return Plotly Figure object."""
        data = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)
        fig = logic.create_forecast_plot(data)

        # Check if it's a Plotly figure (has data attribute)
        assert hasattr(fig, 'data')
        assert hasattr(fig, 'layout')

    def test_plot_has_two_traces(self, sample_df):
        """Should create plot with two traces (actuals + forecast)."""
        data = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)
        fig = logic.create_forecast_plot(data)

        assert len(fig.data) == 2

    def test_plot_styling(self, sample_df):
        """Should apply correct styling to traces."""
        data = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)
        fig = logic.create_forecast_plot(data)

        # Check first trace (historical/actuals)
        trace1 = fig.data[0]
        assert trace1.mode == 'lines+markers'
        assert trace1.line.color == 'blue'
        assert trace1.name == 'Historical Sales'

        # Check second trace (forecast)
        trace2 = fig.data[1]
        assert trace2.mode == 'lines'
        assert trace2.line.color == 'red'
        assert trace2.line.dash == 'dash'
        assert trace2.name == 'Forecasted Sales'

    def test_plot_layout(self, sample_df):
        """Should set correct layout properties."""
        data = logic.get_forecast_data(sample_df, 'PRODUCT_001', 5)
        fig = logic.create_forecast_plot(data)

        layout = fig.layout
        assert 'Sales Forecast for SKU: PRODUCT_001' in layout.title.text
        assert layout.xaxis.title.text == 'Date'
        assert layout.yaxis.title.text == 'Quantity Sold'
        assert layout.legend.title.text == 'Series'
        assert layout.hovermode == 'x unified'
        assert layout.height == 500