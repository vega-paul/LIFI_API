import pytest
import logging
from playwright.sync_api import sync_playwright
from tests.config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def api_client():
    """Shared API client fixture using Playwright."""
    with sync_playwright() as p:
        request_context = p.request.new_context()
        yield request_context
        request_context.dispose()

@pytest.fixture(scope="session")
def base_headers():
    """Base headers including API key if available."""
    headers = {}
    if config.API_KEY:
        headers["x-lifi-api-key"] = config.API_KEY
    return headers

@pytest.fixture(scope="session")
def log_request():
    """Fixture to provide logging function for requests."""
    def log_request_response(response, endpoint, method, params=None, headers=None):
        full_url = response.url
        logger.info(f"REQUEST: {endpoint} | Method: {method} | Full URL: {full_url} | Params: {params} | Headers: {headers}")
        logger.info(f"RESPONSE: Status {response.status} | Body: {response.text()}")
    return log_request_response