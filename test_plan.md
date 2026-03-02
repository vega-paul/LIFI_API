# LIFI API QA Test Plan

## Scope & Objective
Comprehensive testing of the LIFI API endpoints to ensure functionality, reliability, and robustness. The test suite will validate the following endpoints:
- `GET /v1/quote` - Request quotes for token transfers (cross-chain or same-chain)
- `POST /v1/advanced/routes` - Get optimized routes for token transfers
- `GET /v1/tools` - Retrieve available bridges and exchanges

**Primary Goal:** Ensure the API behaves correctly under various conditions, including happy paths, edge cases, and error scenarios.

## Approach
- **Automation Framework:** Playwright API for HTTP request/response handling
- **Test Strategy:** Combination of automated functional testing and manual verification
- **Coverage Areas:**
  - Functional testing (happy paths)
  - Input validation and error handling
  - Response schema validation
  - Authentication and authorization
  - Edge cases and boundary conditions
- **Data Strategy:** Mix of static test data and dynamic data retrieved from the API
- **Validation:** Pydantic schemas for response validation against OpenAPI specification

## Test Cases

### Functional Testing - Happy Path Scenarios

#### GET /v1/quote
- **TC-QUOTE-001:** Valid quote for Ethereum WETH → Polygon WETH (cross-chain bridge)
- **TC-QUOTE-002:** Valid quote for Solana SOL → Bitcoin BTC (cross-chain swap)
- **TC-QUOTE-003:** Valid quote for SUI SUI → Ethereum WETH (cross-chain bridge)
- **Schema Validation:** All responses match QuoteResponse schema
- **Status Code:** 200 OK for valid requests

#### POST /v1/advanced/routes
- **TC-ROUTES-001:** Valid routes for Ethereum WETH → Polygon WETH with FASTEST order
- **TC-ROUTES-002:** Valid routes for Solana SOL → Bitcoin BTC with slippage tolerance
- **TC-ROUTES-003:** Valid routes for SUI SUI → Ethereum WETH with custom options
- **Schema Validation:** All responses match RoutesResponse schema
- **Status Code:** 200 OK for valid requests

#### GET /v1/tools
- **TC-TOOLS-001:** Retrieve bridges and exchanges for Solana (chain filtering)
- **TC-TOOLS-002:** Retrieve bridges and exchanges for Bitcoin (chain filtering)
- **TC-TOOLS-003:** Retrieve bridges and exchanges for SUI (chain filtering)
- **TC-TOOLS-004:** Token search functionality (search for "USDC")
- **Schema Validation:** All responses match ToolsResponse schema
- **Status Code:** 200 OK for valid requests

### Input Validation & Error Handling

#### GET /v1/quote - Negative Tests
- **TC-QUOTE-NEG-001:** Invalid token address (0xInvalidAddress)
- **TC-QUOTE-NEG-002:** Negative amount (-1000000000000000000)
- **TC-QUOTE-NEG-003:** Zero amount (0)
- **TC-QUOTE-NEG-004:** Missing required field (fromAmount)
- **TC-QUOTE-NEG-005:** Unsupported chain ("UNSUPPORTED")
- **TC-QUOTE-NEG-006:** Missing API key (401/403 expected)
- **TC-QUOTE-NEG-007:** Invalid API key (401/403 expected)

#### POST /v1/advanced/routes - Negative Tests
- **TC-ROUTES-NEG-001:** Invalid chain ID (99999)
- **TC-ROUTES-NEG-002:** Negative amount (-1000000000000000000)
- **TC-ROUTES-NEG-003:** Zero amount (0)
- **TC-ROUTES-NEG-004:** Missing required field (fromAmount)
- **TC-ROUTES-NEG-005:** Invalid token address (0xInvalidAddress)
- **TC-ROUTES-NEG-006:** Missing API key (401/403 expected)
- **TC-ROUTES-NEG-007:** Invalid API key (401/403 expected)

### Non-Functional Testing
- **Performance:** Response times within acceptable limits (< 5 seconds)
- **Reliability:** Consistent behavior across multiple requests
- **Error Messages:** Clear and informative error responses

## Test Data

### Static Test Data
```python
TEST_PAIRS = [
    # Ethereum to Polygon (WETH)
    {
        "fromChain": "ETH",
        "toChain": "POL",
        "fromToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "toToken": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "fromAmount": "1000000000000000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    },
    # Solana to Bitcoin (SOL to BTC)
    {
        "fromChain": "SOL",
        "toChain": "BTC",
        "fromToken": "So11111111111111111111111111111111111111112",
        "toToken": "BTC",
        "fromAmount": "1000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    },
    # SUI to Ethereum (SUI to WETH)
    {
        "fromChain": "SUI",
        "toChain": "ETH",
        "fromToken": "0x2::sui::SUI",
        "toToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "fromAmount": "1000000000",
        "fromAddress": config.DEFAULT_FROM_ADDRESS
    }
]
```

### Dynamic Test Data
- Bridge and exchange keys retrieved from `/v1/tools` endpoint
- Chain-specific filtering for Solana, Bitcoin, and SUI

### Invalid Test Data
- Invalid token addresses: "0xInvalidAddress"
- Invalid chain IDs: 99999
- Invalid amounts: -1000000000000000000, 0
- Unsupported chains: "UNSUPPORTED"
- Invalid API keys: "invalid_key"

## Environment & Configuration

### Prerequisites
- Python 3.12+
- Virtual environment
- API key (optional, some endpoints work without authentication)

### Configuration
- Base URL: https://li.quest/v1
- API Key: Loaded from environment variable `LIFI_API_KEY`
- Default test address: 0x000000000000000000000000000000000000dead

## Risks & Mitigations

### API Rate Limits
- **Risk:** Tests may be throttled or blocked
- **Mitigation:** Implement delays between requests, use API key if available

### Dynamic Data Changes
- **Risk:** Supported tokens/chains may change
- **Mitigation:** Use well-established token pairs, document assumptions

### Network Instability
- **Risk:** External network issues affecting test reliability
- **Mitigation:** Implement retry logic, run tests multiple times

### Authentication Issues
- **Risk:** API key expiration or invalidation
- **Mitigation:** Support both authenticated and unauthenticated test scenarios

## Test Execution & Reporting

### Execution Strategy
1. Environment setup and dependency installation
2. Run smoke tests to verify API connectivity
3. Execute functional tests (happy paths)
4. Execute negative and edge case tests
5. Generate comprehensive test reports

### Success Criteria
- All happy path tests pass (100% success rate)
- Error scenarios return appropriate status codes and messages
- Response schemas validate correctly
- No critical bugs identified

### Bug Reporting
- Document any unexpected behavior
- Include request/response details
- Suggest severity and priority levels
- Provide reproduction steps

## Verification & Sign-off
- Automated test suite execution
- Manual review of test results
- Cross-browser/API client verification if needed
- Final test report with recommendations
