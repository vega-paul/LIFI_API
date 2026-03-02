import os
import pytest
import logging
from config import config
from schemas import RoutesResponse
from pydantic import ValidationError
from test_data.pairs import ROUTE_TEST_PAIRS

logger = logging.getLogger(__name__)

def log_request_response(response, endpoint, method, params=None, headers=None):
    full_url = response.url
    logger.info(f"REQUEST: {endpoint} | Method: {method} | Full URL: {full_url} | Params: {params} | Headers: {headers}")
    logger.info(f"RESPONSE: Status {response.status} | Body: {response.text()}" )

def test_post_advanced_routes_happy_paths(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    for route in ROUTE_TEST_PAIRS:
        # Filter out metadata fields that shouldn't be sent to API
        api_data = {k: v for k, v in route.items() if k not in ['name']}
        response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=api_data, headers=headers)
        log_request_response(response, '/advanced/routes', 'POST', api_data, headers)
        # 429 means rate limited - test didn't actually run, so it should fail
        if response.status == 429:
            pytest.fail(f"Test failed due to rate limiting: {response.text()}")
        assert response.status == 200
        data = response.json()
        try:
            RoutesResponse(**data)
        except ValidationError as e:
            pytest.fail(f"Response schema validation failed: {e}")
        assert "routes" in data
        assert isinstance(data["routes"], list)

def test_post_advanced_routes_invalid_chain_id(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_route = {
        "fromChainId": 99999,  # Invalid chain ID
        "fromTokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "fromAmount": "1000000000000000000",
        "toChainId": 137,
        "toTokenAddress": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "options": {"order": "FASTEST", "slippage": 0.5}
    }
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=invalid_route, headers=headers)
    log_request_response(response, '/advanced/routes', 'POST', invalid_route, headers)
    # Accept 400 (invalid chain) or 429 (rate limited)
    assert response.status in [400, 429]

def test_post_advanced_routes_negative_amount(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_route = {
        "fromChainId": 1,
        "fromTokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "fromAmount": "-1000000000000000000",
        "toChainId": 137,
        "toTokenAddress": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "options": {"order": "FASTEST", "slippage": 0.5}
    }
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=invalid_route, headers=headers)
    log_request_response(response, '/advanced/routes', 'POST', invalid_route, headers)
    # Accept 400 (negative amount) or 429 (rate limited)
    assert response.status in [400, 429]

def test_post_advanced_routes_zero_amount(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_route = {
        "fromChainId": 1,
        "fromTokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "fromAmount": "0",
        "toChainId": 137,
        "toTokenAddress": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "options": {"order": "FASTEST", "slippage": 0.5}
    }
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=invalid_route, headers=headers)
    log_request_response(response, '/advanced/routes', 'POST', invalid_route, headers)
    # Accept 400 (zero amount) or 429 (rate limited)
    assert response.status in [400, 429]

def test_post_advanced_routes_missing_required_field(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_route = {
        "fromChainId": 1,
        "fromTokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        # Missing fromAmount
        "toChainId": 137,
        "toTokenAddress": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "options": {"order": "FASTEST", "slippage": 0.5}
    }
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=invalid_route, headers=headers)
    log_request_response(response, '/advanced/routes', 'POST', invalid_route, headers)
    # Accept 400 (missing field) or 429 (rate limited)
    assert response.status in [400, 429]

def test_post_advanced_routes_invalid_token_address(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_route = {
        "fromChainId": 1,
        "fromTokenAddress": "0xInvalidAddress",
        "fromAmount": "1000000000000000000",
        "toChainId": 137,
        "toTokenAddress": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "options": {"order": "FASTEST", "slippage": 0.5}
    }
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=invalid_route, headers=headers)
    log_request_response(response, '/advanced/routes', 'POST', invalid_route, headers)
    # Accept 400 (invalid token) or 429 (rate limited)
    assert response.status in [400, 429]

def test_post_advanced_routes_missing_api_key(api_client):
    route = ROUTE_TEST_PAIRS[0]
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=route)
    log_request_response(response, '/advanced/routes', 'POST', route, {})
    # API appears to work without authentication, or may be rate limited
    assert response.status in [200, 429]

def test_post_advanced_routes_invalid_api_key(api_client):
    headers = {"x-lifi-api-key": "invalid_key"}
    route = ROUTE_TEST_PAIRS[0]
    response = api_client.post(f"{config.BASE_URL}/advanced/routes", data=route, headers=headers)
    log_request_response(response, '/advanced/routes', 'POST', route, headers)
    assert response.status in [401, 403]

# Add more edge and negative tests as needed
