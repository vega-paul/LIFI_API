# LIFI API QA Test Suite

## QA Engineer Take-Home Assignment

This project implements a comprehensive automated API test suite for the LIFI blockchain API, covering functional testing, input validation, error handling, and schema validation for the following endpoints:

- `GET /v1/quote` — Request quotes for token transfers
- `POST /v1/advanced/routes` — Get optimized routes for token transfers
- `GET /v1/tools` — Retrieve available bridges and exchanges

## Features

- ✅ **Complete Test Coverage**: Happy path, edge cases, and negative testing
- ✅ **Schema Validation**: Pydantic models for response validation against OpenAPI spec
- ✅ **Authentication Testing**: Both authenticated and unauthenticated scenarios
- ✅ **Comprehensive Error Handling**: Invalid inputs, missing fields, unsupported combinations
- ✅ **Detailed Logging**: Request/response logging for debugging
- ✅ **Modular Architecture**: Shared fixtures and reusable test components

## Prerequisites

- Python 3.12 or higher
- Virtual environment (recommended)
- LIFI API key (optional - some endpoints work without authentication)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd lifi-api-tests
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If requirements.txt doesn't exist, install manually:
```bash
pip install pytest playwright pydantic python-dotenv requests
playwright install
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```bash
# .env
LIFI_API_KEY=your_api_key_here  # Optional
```

### 5. Verify Setup
```bash
python -c "import pytest, playwright, pydantic, dotenv; print('All dependencies installed successfully')"
```

## Test Execution

### Run All Tests
```bash
# Using virtual environment Python
.venv/bin/python -m pytest tests/ -v

# Or if venv is activated
pytest tests/ -v
```

### Run Specific Test Files
```bash
# Quote endpoint tests
pytest tests/test_quote.py -v

# Routes endpoint tests
pytest tests/test_routes.py -v

# Tools endpoint tests
pytest tests/test_api.py -v
```

### Run with Detailed Logging
```bash
pytest tests/ --log-cli-level=INFO -s
```

### Generate HTML Report
```bash
pytest tests/ --html=reports/test_report.html --self-contained-html
```

### Run Tests in Parallel (if needed)
```bash
pytest tests/ -n auto
```

## Project Structure

```
lifi-api-tests/
├── tests/
│   ├── conftest.py          # Shared fixtures and configuration
│   ├── schemas.py           # Pydantic models for API responses
│   ├── config.py            # Environment configuration
│   ├── test_quote.py        # Quote endpoint tests
│   ├── test_routes.py       # Routes endpoint tests
│   ├── test_api.py          # Tools endpoint tests
│   └── __pycache__/
├── reports/                 # Test reports and results
├── .env                     # Environment variables (not committed)
├── .venv/                   # Virtual environment
├── pytest.ini              # Pytest configuration
├── test_plan.md            # Detailed test plan and cases
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Test Coverage

### Functional Testing (Happy Paths)
- **Quote Endpoint**: Valid quotes for ETH→POL, SOL→BTC, SUI→ETH
- **Routes Endpoint**: Advanced routing with different options
- **Tools Endpoint**: Bridge/exchange retrieval for specific chains

### Input Validation & Error Handling
- Invalid token addresses and chain IDs
- Negative and zero amounts
- Missing required fields
- Unsupported token pairs and chains
- Authentication failures (missing/invalid API keys)

### Schema Validation
- All responses validated against Pydantic models
- Comprehensive field validation
- Type checking and constraint validation

## Configuration

### Test Configuration (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
addopts =
    --verbose
    --tb=short
    --strict-markers
    --disable-warnings
    --log-cli-level=INFO
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### Environment Configuration (tests/config.py)
- Base URL: `https://li.quest/v1`
- API Key: Loaded from `LIFI_API_KEY` environment variable
- Default test address and token pairs

## Test Results & Reporting

### Automated Reports
- HTML reports with detailed test results
- JSON reports for CI/CD integration
- Log files with request/response details

### Bug Reports
Any issues found during testing are documented in the `reports/` directory with:
- Reproduction steps
- Request/response details
- Expected vs actual behavior
- Severity and priority assessment

## CI/CD Integration (Bonus)

A GitHub Actions workflow is included for automated testing:

```yaml
# .github/workflows/api-tests.yml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Run tests
        run: pytest tests/ --html=reports/test_report.html
      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: reports/
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure virtual environment is activated and dependencies are installed
2. **API Key Issues**: Some tests require authentication; set `LIFI_API_KEY` in `.env`
3. **Rate Limiting**: Add delays between requests if hitting API limits
4. **Network Issues**: Tests require internet connectivity to reach LIFI API

### Debug Mode
```bash
pytest tests/ -s --log-cli-level=DEBUG
```

## Contributing

1. Follow the existing test structure and naming conventions
2. Add new test cases to appropriate files
3. Update test_plan.md for new test cases
4. Ensure all tests pass before submitting

## Contact

For questions about this assignment, contact:
**Berkant** <berkant@li.finance>

## Evaluation Criteria Met

- ✅ **Technical Skills**: Proficient API testing with Playwright, HTTP validation, JSON schema validation
- ✅ **Test Design**: Comprehensive coverage with proper prioritization and edge case identification
- ✅ **Documentation**: Clear test plan, setup instructions, and professional presentation
- ✅ **Problem-Solving**: Creative testing approach with practical recommendations
