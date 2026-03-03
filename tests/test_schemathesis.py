import schemathesis
import pytest
import os
from tests.config import config

# Load the OpenAPI schema
schema = schemathesis.openapi.from_path("openapi.yaml")

# Set base URL
schema.base_url = "https://li.quest/v1"

# Configure output sanitization to show tokens in cURL snippets
schema.config.output.sanitization.update(enabled=False)

# Filter schemas for specific endpoints and set base URL
quote_schema = schema.include(path="/v1/quote")
quote_schema.base_url = "https://li.quest/v1"

routes_schema = schema.include(path="/v1/advanced/routes")
routes_schema.base_url = "https://li.quest/v1"

tools_schema = schema.include(path="/v1/tools")
tools_schema.base_url = "https://li.quest/v1"


@quote_schema.parametrize()
def test_quote_endpoint(case, log_request):
    """Test GET /v1/quote endpoint with schemathesis"""
    response = case.call_and_validate(base_url="https://li.quest/v1")
    log_request(response, '/v1/quote', case.method, case.query, case.headers)


@routes_schema.parametrize()
def test_routes_endpoint(case, log_request):
    """Test POST /v1/advanced/routes endpoint with schemathesis"""
    response = case.call_and_validate(base_url="https://li.quest/v1")
    log_request(response, '/v1/advanced/routes', case.method, case.body, case.headers)


@tools_schema.parametrize()
def test_tools_endpoint(case, log_request):
    """Test GET /v1/tools endpoint with schemathesis"""
    response = case.call_and_validate(base_url="https://li.quest/v1")
    log_request(response, '/v1/tools', case.method, case.query, case.headers)
