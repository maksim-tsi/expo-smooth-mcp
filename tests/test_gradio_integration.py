# tests/test_gradio_integration.py
"""
Integration tests for Gradio UI mounted in FastAPI.

Tests verify that:
- Gradio UI is accessible at /gradio
- UI can communicate with FastAPI backend
- All functionality works end-to-end
"""

import pytest
from fastapi.testclient import TestClient
from src.expo_smooth_mcp.main import app, PROCESSED_DF
from src.expo_smooth_mcp import logic

# --- Fixtures ---

@pytest.fixture
def client():
    """Create FastAPI test client."""
    return TestClient(app)

# --- Gradio Endpoint Tests ---

class TestGradioMounting:
    """Tests for Gradio UI mounting."""

    def test_gradio_endpoint_accessible(self, client):
        """Should be able to access /gradio endpoint."""
        response = client.get("/gradio")

        # Gradio might redirect to /gradio/ (with trailing slash)
        assert response.status_code in [200, 307, 308], \
            f"Expected 200/307/308, got {response.status_code}"

    def test_gradio_with_trailing_slash(self, client):
        """Should be accessible with trailing slash."""
        response = client.get("/gradio/")
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"

    def test_gradio_content_exists(self, client):
        """Gradio should return HTML content."""
        response = client.get("/gradio/")

        if response.status_code == 200:
            # Check response contains HTML
            assert len(response.text) > 0
            assert "<!DOCTYPE" in response.text or "<html" in response.text.lower()

class TestGradioFunctionality:
    """Tests for Gradio UI functionality."""

    def test_gradio_can_access_data(self, client):
        """Gradio should have access to SKU list."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")

        # The Gradio interface should be initialized with SKU list
        skus = logic.get_available_skus(PROCESSED_DF)
        assert len(skus) > 0, "No SKUs available for Gradio"

        # Verify SKUs are valid
        assert all(isinstance(sku, str) for sku in skus)
        assert len(skus) == 3, f"Expected 3 SKUs, got {len(skus)}"

class TestGradioAPIIntegration:
    """Tests for Gradio-FastAPI integration."""

    def test_gradio_backend_uses_same_data(self, client):
        """Gradio and REST API should use same data source."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")

        # Get SKU count from REST API
        rest_response = client.get("/")
        rest_data = rest_response.json()
        rest_sku_count = rest_data["sku_count"]

        # Get SKU count from logic (used by Gradio)
        gradio_sku_count = len(logic.get_available_skus(PROCESSED_DF))

        # Should be the same
        assert rest_sku_count == gradio_sku_count, \
            f"REST API shows {rest_sku_count} SKUs, Gradio has {gradio_sku_count}"

    def test_gradio_forecast_uses_same_logic(self, client):
        """Gradio forecast should produce same results as REST API."""
        if PROCESSED_DF is None:
            pytest.skip("Data not loaded")

        skus = logic.get_available_skus(PROCESSED_DF)
        test_sku = skus[0]

        # Get forecast via REST API
        rest_response = client.post(
            "/api/forecast",
            json={"sku": test_sku, "forecast_horizon": 90}
        )
        assert rest_response.status_code == 200
        rest_data = rest_response.json()

        # Get forecast via logic (same as Gradio uses)
        gradio_data = logic.get_forecast_data(PROCESSED_DF, test_sku, 90)

        # Should produce identical results
        assert rest_data["metadata"]["sku"] == gradio_data["metadata"]["sku"]
        assert rest_data["metadata"]["forecast_horizon"] == \
               gradio_data["metadata"]["forecast_horizon"]
        assert len(rest_data["forecast"]) == len(gradio_data["forecast"])

        # First few forecast values should match
        for i in range(min(5, len(rest_data["forecast"]))):
            assert abs(rest_data["forecast"][i] - gradio_data["forecast"][i]) < 0.01, \
                f"Forecast mismatch at index {i}"

class TestGradioEndpointListing:
    """Tests for Gradio in service discovery."""

    def test_root_endpoint_lists_gradio(self, client):
        """Root endpoint should list Gradio UI in endpoints."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "endpoints" in data
        assert "gradio_ui" in data["endpoints"]
        assert data["endpoints"]["gradio_ui"]["path"] == "/gradio"
        assert data["endpoints"]["gradio_ui"]["method"] == "GET"

    def test_root_endpoint_usage_includes_gradio(self, client):
        """Root endpoint usage should mention Gradio."""
        response = client.get("/")
        data = response.json()

        assert "usage" in data
        assert "web_ui" in data["usage"]
        assert "/gradio" in data["usage"]["web_ui"]

class TestGradioErrorHandling:
    """Tests for Gradio error scenarios."""

    def test_gradio_accessible_even_if_data_not_loaded(self, client):
        """Gradio UI should be accessible even if data fails to load."""
        # The /gradio endpoint should return 200 regardless of data status
        response = client.get("/gradio/")

        # Should not return 503 or 500
        assert response.status_code in [200, 307, 308]

class TestGradioPerformance:
    """Performance tests for Gradio integration."""

    def test_gradio_page_load_time(self, client):
        """Gradio page should load quickly."""
        import time

        start = time.time()
        response = client.get("/gradio/")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 2.0, f"Gradio took {elapsed:.2f}s to load (should be < 2s)"

# Run tests with: pytest tests/test_gradio_integration.py -v