# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.expo_smooth_mcp import main

# Create TestClient with raise_server_exceptions=True to see lifespan errors
# Note: TestClient now automatically handles lifespan in context manager mode
# We need to use it as a context manager or fixture
@pytest.fixture(scope="module")
def client():
    """Create test client that properly runs lifespan events."""
    with TestClient(main.app) as test_client:
        yield test_client

class TestRootEndpoint:
    """Tests for / endpoint."""

    def test_root_returns_service_info(self, client):
        """Should return service metadata."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Expo Smooth MCP Server"
        assert data["version"] == "2.0.0"
        assert data["status"] == "operational"
        assert "endpoints" in data
        assert "usage" in data
        assert "data_status" in data
        assert "sku_count" in data

    def test_root_includes_all_endpoints(self, client):
        """Should document all available endpoints."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        endpoints = data["endpoints"]
        required_endpoints = ["health", "mcp_tools", "rest_api", "gradio_ui", "documentation"]
        for endpoint in required_endpoints:
            assert endpoint in endpoints
            assert "path" in endpoints[endpoint]
            assert "method" in endpoints[endpoint]
            assert "description" in endpoints[endpoint]

    def test_root_includes_usage_info(self, client):
        """Should provide usage instructions."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        usage = data["usage"]
        assert "mcp_clients" in usage
        assert "rest_clients" in usage
        assert "web_ui" in usage

class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_when_data_loaded(self, client):
        """Should return 200 when healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"
        assert data["data_loaded"] is True
        assert "sku_count" in data
        assert "timestamp" in data
        assert isinstance(data["sku_count"], int)
        assert data["sku_count"] > 0

    def test_health_response_format(self, client):
        """Should return properly formatted JSON response."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()

        # Validate all required fields are present
        required_fields = ["status", "timestamp", "version", "data_loaded", "sku_count"]
        for field in required_fields:
            assert field in data

        # Validate data types
        assert isinstance(data["status"], str)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["data_loaded"], bool)
        assert isinstance(data["sku_count"], int)

class TestForecastAPI:
    """Tests for /api/forecast endpoint."""

    def test_forecast_with_valid_request(self, client):
        """Should return forecast for valid request."""
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 30}
        )
        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "dates" in data
        assert "actuals" in data
        assert "forecast" in data
        assert "metadata" in data

        # Validate data types
        assert isinstance(data["dates"], list)
        assert isinstance(data["actuals"], list)
        assert isinstance(data["forecast"], list)
        assert isinstance(data["metadata"], dict)

        # Validate metadata
        meta = data["metadata"]
        assert meta["sku"] == "PRODUCT_001"
        assert meta["forecast_horizon"] == 30
        assert "historical_points" in meta
        assert "forecast_points" in meta

        # Validate dates are strings
        assert all(isinstance(date, str) for date in data["dates"])

        # Validate forecast has expected length
        assert len(data["forecast"]) == 50  # historical_points (20) + forecast_horizon (30)

    def test_forecast_with_default_horizon(self, client):
        """Should use default horizon of 90 when not specified."""
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001"}  # No forecast_horizon specified
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["forecast"]) == 110  # historical_points (20) + default horizon (90)
        assert data["metadata"]["forecast_horizon"] == 90

    def test_forecast_with_invalid_sku(self, client):
        """Should return 400 for invalid SKU."""
        response = client.post(
            "/api/forecast",
            json={"sku": "INVALID_PRODUCT", "forecast_horizon": 30}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]

    def test_forecast_with_invalid_horizon_too_high(self, client):
        """Should return 422 for horizon too high (Pydantic validation)."""
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 500}
        )
        assert response.status_code == 422  # Pydantic validation error

    def test_forecast_with_invalid_horizon_too_low(self, client):
        """Should return 422 for horizon too low (Pydantic validation)."""
        response = client.post(
            "/api/forecast",
            json={"sku": "PRODUCT_001", "forecast_horizon": 0}
        )
        assert response.status_code == 422  # Pydantic validation error

    def test_forecast_with_invalid_json(self, client):
        """Should return 422 for invalid JSON."""
        response = client.post(
            "/api/forecast",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_forecast_with_missing_sku(self, client):
        """Should return 422 for missing SKU field."""
        response = client.post(
            "/api/forecast",
            json={"forecast_horizon": 30}  # Missing sku
        )
        assert response.status_code == 422

class TestOpenAPISpec:
    """Tests for OpenAPI documentation."""

    def test_openapi_json_available(self, client):
        """Should serve OpenAPI JSON specification."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_openapi_includes_forecast_endpoint(self, client):
        """Should document the forecast API endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()

        assert "/api/forecast" in data["paths"]
        forecast_path = data["paths"]["/api/forecast"]
        assert "post" in forecast_path

        post_spec = forecast_path["post"]
        assert "summary" in post_spec
        assert "requestBody" in post_spec
        assert "responses" in post_spec

    def test_openapi_includes_root_endpoint(self, client):
        """Should document the root endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()

        assert "/" in data["paths"]
        root_path = data["paths"]["/"]
        assert "get" in root_path

    def test_openapi_includes_health_endpoint(self, client):
        """Should document the health endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()

        assert "/health" in data["paths"]
        health_path = data["paths"]["/health"]
        assert "get" in health_path

class TestHTTPMethods:
    """Tests for HTTP method handling."""

    def test_forecast_get_not_allowed(self, client):
        """Should return 405 for GET on forecast endpoint."""
        response = client.get("/api/forecast")
        assert response.status_code == 405

    def test_root_post_not_allowed(self, client):
        """Should return 405 for POST on root endpoint."""
        response = client.post("/")
        assert response.status_code == 405

    def test_health_post_not_allowed(self, client):
        """Should return 405 for POST on health endpoint."""
        response = client.post("/health")
        assert response.status_code == 405

class TestContentType:
    """Tests for content type handling."""

    def test_forecast_requires_json_content_type(self, client):
        """Should handle missing content-type gracefully."""
        response = client.post(
            "/api/forecast",
            data='{"sku": "PRODUCT_001", "forecast_horizon": 30}'  # No content-type header
        )
        # Should still work due to FastAPI's automatic JSON parsing
        assert response.status_code in [200, 422]  # Either success or validation error