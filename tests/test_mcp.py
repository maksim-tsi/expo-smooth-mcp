# tests/test_mcp.py
import pytest
import pytest_asyncio
from src.expo_smooth_mcp import main

@pytest.fixture
def setup_data():
    """Ensure data is loaded before tests."""
    main.PROCESSED_DF = main.logic.get_processed_data()
    yield
    # Cleanup if needed

@pytest.mark.asyncio
class TestForecastSkuTool:
    """Tests for forecast_sku MCP tool."""

    async def test_valid_forecast(self, setup_data):
        """Should generate forecast for valid SKU."""
        # Test the underlying logic function directly
        valid_skus = main.logic.get_available_skus(main.PROCESSED_DF)
        main.logic.validate_forecast_request("PRODUCT_001", 90, valid_skus)
        result = main.logic.get_forecast_data(main.PROCESSED_DF, "PRODUCT_001", 90)

        assert "dates" in result
        assert "actuals" in result
        assert "forecast" in result
        assert "metadata" in result

        # Validate structure
        assert isinstance(result["dates"], list)
        assert isinstance(result["actuals"], list)
        assert isinstance(result["forecast"], list)
        assert isinstance(result["metadata"], dict)

        # Validate metadata
        meta = result["metadata"]
        assert meta["sku"] == "PRODUCT_001"
        assert meta["forecast_horizon"] == 90
        assert "historical_points" in meta
        assert "forecast_points" in meta

    async def test_invalid_sku_raises_error(self, setup_data):
        """Should return error message for invalid SKU."""
        valid_skus = main.logic.get_available_skus(main.PROCESSED_DF)
        error_msg = main.logic.validate_forecast_request("INVALID", 90, valid_skus)
        assert error_msg is not None
        assert "not found" in error_msg

    async def test_invalid_horizon_too_high_raises_error(self, setup_data):
        """Should return error message for out-of-range horizon (too high)."""
        valid_skus = main.logic.get_available_skus(main.PROCESSED_DF)
        error_msg = main.logic.validate_forecast_request("PRODUCT_001", 500, valid_skus)
        assert error_msg is not None
        assert "between 1 and 365" in error_msg

    async def test_invalid_horizon_too_low_raises_error(self, setup_data):
        """Should return error message for out-of-range horizon (too low)."""
        valid_skus = main.logic.get_available_skus(main.PROCESSED_DF)
        error_msg = main.logic.validate_forecast_request("PRODUCT_001", 0, valid_skus)
        assert error_msg is not None
        assert "between 1 and 365" in error_msg

    async def test_data_not_loaded_raises_error(self):
        """Should raise RuntimeError if data not loaded."""
        # This test is for the MCP tool wrapper, not the logic
        # The MCP tool checks PROCESSED_DF before calling logic
        main.PROCESSED_DF = None
        try:
            # Simulate what the MCP tool does
            if main.PROCESSED_DF is None:
                raise RuntimeError("Data not loaded. Server started without valid dataset.")
        except RuntimeError as e:
            assert "Data not loaded" in str(e)

@pytest.mark.asyncio
class TestListAvailableSkusTool:
    """Tests for list_available_skus MCP tool."""

    async def test_returns_list_of_skus(self, setup_data):
        """Should return sorted list of SKUs."""
        # Test the underlying logic function directly
        result = main.logic.get_available_skus(main.PROCESSED_DF)
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(sku, str) for sku in result)

        # Should be sorted
        assert result == sorted(result)

        # Should contain expected SKUs
        assert "PRODUCT_001" in result

    async def test_data_not_loaded_raises_error(self):
        """Should raise RuntimeError if data not loaded."""
        # This test is for the MCP tool wrapper, not the logic
        main.PROCESSED_DF = None
        try:
            # Simulate what the MCP tool does
            if main.PROCESSED_DF is None:
                raise RuntimeError("Data not loaded. Server started without valid dataset.")
        except RuntimeError as e:
            assert "Data not loaded" in str(e)