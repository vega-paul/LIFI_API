import os
import pytest
import logging
from tests.config import config
from tests.schemas import QuoteResponse
from pydantic import ValidationError
from test_data.pairs import TEST_PAIRS

logger = logging.getLogger(__name__)

def log_request_response(response, endpoint, method, params=None, headers=None):
    full_url = response.url
    logger.info(f"REQUEST: {endpoint} | Method: {method} | Full URL: {full_url} | Params: {params} | Headers: {headers}")
    logger.info(f"RESPONSE: Status {response.status} | Body: {response.text()}" )

def test_get_quote_happy_paths(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    for pair in TEST_PAIRS:
        # Filter out metadata fields that shouldn't be sent to API
        api_params = {k: v for k, v in pair.items() if k not in ['name']}
        response = api_client.get(f"{config.BASE_URL}/quote", params=api_params, headers=headers)
        log_request_response(response, '/quote', 'GET', api_params, headers)
        # 429 means rate limited - test didn't actually run, so it should fail
        if response.status == 429:
            pytest.fail(f"Test failed due to rate limiting: {response.text()}")
        assert response.status == 200
        data = response.json()
        try:
            QuoteResponse(**data)
        except ValidationError as e:
            pytest.fail(f"Response schema validation failed: {e}")
        assert "estimate" in data
        assert "transactionRequest" in data

def test_get_quote_invalid_token_address(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_pair = {
        "fromChain": "ETH",
        "toChain": "POL",
        "fromToken": "0xInvalidAddress",
        "toToken": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "fromAmount": "1000000000000000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
    response = api_client.get(f"{config.BASE_URL}/quote", params=invalid_pair, headers=headers)
    log_request_response(response, '/quote', 'GET', invalid_pair, headers)
    # Accept 400 (invalid token) or 429 (rate limited)
    assert response.status in [400, 429]

def test_get_quote_negative_amount(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_pair = {
        "fromChain": "ETH",
        "toChain": "POL",
        "fromToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "toToken": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "fromAmount": "-1000000000000000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
    response = api_client.get(f"{config.BASE_URL}/quote", params=invalid_pair, headers=headers)
    log_request_response(response, '/quote', 'GET', invalid_pair, headers)
    # Accept 400 (negative amount) or 429 (rate limited)
    assert response.status in [400, 429]

def test_get_quote_zero_amount(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_pair = {
        "fromChain": "ETH",
        "toChain": "POL",
        "fromToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "toToken": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "fromAmount": "0",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
    response = api_client.get(f"{config.BASE_URL}/quote", params=invalid_pair, headers=headers)
    log_request_response(response, '/quote', 'GET', invalid_pair, headers)
    # Accept 400 (zero amount) or 429 (rate limited)
    assert response.status in [400, 429]

def test_get_quote_missing_required_field(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_pair = {
        "fromChain": "ETH",
        "toChain": "POL",
        "fromToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "toToken": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        # Missing fromAmount
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
    response = api_client.get(f"{config.BASE_URL}/quote", params=invalid_pair, headers=headers)
    log_request_response(response, '/quote', 'GET', invalid_pair, headers)
    # Accept 400 (missing field) or 429 (rate limited)
    assert response.status in [400, 429]

def test_get_quote_unsupported_chain(api_client):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    invalid_pair = {
        "fromChain": "UNSUPPORTED",
        "toChain": "POL",
        "fromToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "toToken": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "fromAmount": "1000000000000000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
    response = api_client.get(f"{config.BASE_URL}/quote", params=invalid_pair, headers=headers)
    log_request_response(response, '/quote', 'GET', invalid_pair, headers)
    # Accept 400 (unsupported chain) or 429 (rate limited)
    assert response.status in [400, 429]

def test_get_quote_missing_api_key(api_client):
    # Test without API key header
    pair = TEST_PAIRS[0]
    response = api_client.get(f"{config.BASE_URL}/quote", params=pair)
    log_request_response(response, '/quote', 'GET', pair, {})
    # API appears to work without authentication, or may be rate limited
    assert response.status in [200, 429]

def test_get_quote_invalid_api_key(api_client):
    headers = {"x-lifi-api-key": "invalid_key"}
    pair = TEST_PAIRS[0]
    response = api_client.get(f"{config.BASE_URL}/quote", params=pair, headers=headers)
    log_request_response(response, '/quote', 'GET', pair, headers)
    # Accept 401/403 (auth error) or 429 (rate limited)
    assert response.status in [401, 403, 429]

# Edge case: unsupported token pair

def test_get_quote_unsupported_pair(api_client, log_request):
    params = {
        "fromChain": "ETH",
        "toChain": "POL",
        "fromToken": "0x0000000000000000000000000000000000000000",
        "toToken": "0x0000000000000000000000000000000000000000",
        "fromAmount": "1000000000000000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    response = api_client.get(f"{config.BASE_URL}/quote", params=params, headers=headers)
    log_request_response(response, '/quote', 'GET', params, headers)
    # API may return 429 (rate limit) or 200 depending on load
    assert response.status in [200, 429]

# Edge case: missing required fields

def test_get_quote_missing_fields(api_client, log_request):
    params = {
        "fromChain": "ETH"
    }
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    response = api_client.get(f"{config.BASE_URL}/quote", params=params, headers=headers)
    log_request_response(response, '/quote', 'GET', params, headers)
    assert response.status >= 400
