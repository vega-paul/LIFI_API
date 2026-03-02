import os
import pytest
import logging
from config import config
from schemas import ToolsResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def test_get_tools_auth(api_client, log_request):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    response = api_client.get(f"{config.BASE_URL}/tools", headers=headers)
    log_request(response, '/tools', 'GET', None, headers)
    assert response.status == 200
    data = response.json()
    assert "bridges" in data
    assert "exchanges" in data
    assert isinstance(data["bridges"], list)
    assert isinstance(data["exchanges"], list)

def test_get_tools_auth_schema(api_client, log_request):
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    response = api_client.get(f"{config.BASE_URL}/tools", headers=headers)
    log_request(response, '/tools', 'GET', None, headers)
    assert response.status == 200
    data = response.json()
    try:
        ToolsResponse(**data)
    except ValidationError as e:
        pytest.fail(f"Response schema validation failed: {e}")

def test_get_tools_noauth(api_client, log_request):
    response = api_client.get(f"{config.BASE_URL}/tools")
    log_request(response, '/tools', 'GET', None, None)
    assert response.status == 200
    data = response.json()
    assert "bridges" in data
    assert "exchanges" in data
    assert isinstance(data["bridges"], list)
    assert isinstance(data["exchanges"], list)

def test_get_tools_for_solana_bitcoin_sui(api_client, log_request):
    # Use chain names as expected by API
    chains = ["SOL", "BTC", "SUI"]
    params = {"chains": ",".join(chains)}
    headers = {"x-lifi-api-key": config.API_KEY} if config.API_KEY else {}
    response = api_client.get(f"{config.BASE_URL}/tools", params=params, headers=headers)
    log_request(response, '/tools', 'GET', params, headers)
    assert response.status == 200
    data = response.json()
    assert "bridges" in data
    assert "exchanges" in data
    assert isinstance(data["bridges"], list)
    assert isinstance(data["exchanges"], list)
    # Since the API filters by chains, we just check that we get some results
    assert len(data["bridges"]) > 0
    assert len(data["exchanges"]) > 0