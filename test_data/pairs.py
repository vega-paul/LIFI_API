# Generated test pairs for happy path testing
# Discovered via discover_pairs.py utility
# Run: python discover_pairs.py --chains eth,pol,arb --tokens USDC,USDT

TEST_PAIRS = [
    {
        "name": "ETH_POL_USDC",
        "fromChain": "eth",
        "toChain": "pol",
        "fromToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "toToken": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "fromAmount": "1000000",
        "fromAddress": "0x000000000000000000000000000000000000dead",
        "tool": "across",
    },
    {
        "name": "ETH_ARB_USDC",
        "fromChain": "eth",
        "toChain": "arb",
        "fromToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "toToken": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "fromAmount": "1000000",
        "fromAddress": "0x000000000000000000000000000000000000dead",
        "tool": "across",
    },
    {
        "name": "POL_ETH_USDC",
        "fromChain": "pol",
        "toChain": "eth",
        "fromToken": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "toToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "fromAmount": "1000000",
        "fromAddress": "0x000000000000000000000000000000000000dead",
        "tool": "across",
    },
]

# Routes version (with chain IDs for /advanced/routes endpoint)
ROUTE_TEST_PAIRS = [
    {
        "name": "ETH_POL_USDC",
        "fromChainId": 1,
        "fromTokenAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "fromAmount": "1000000",
        "toChainId": 137,
        "toTokenAddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "fromAddress": "0x000000000000000000000000000000000000dead",
        "options": {'order': 'FASTEST', 'slippage': 0.5},
        "tool": "across",
    },
    {
        "name": "ETH_ARB_USDC",
        "fromChainId": 1,
        "fromTokenAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "fromAmount": "1000000",
        "toChainId": 42161,
        "toTokenAddress": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "fromAddress": "0x000000000000000000000000000000000000dead",
        "options": {'order': 'FASTEST', 'slippage': 0.5},
        "tool": "across",
    },
    {
        "name": "POL_ETH_USDC",
        "fromChainId": 137,
        "fromTokenAddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "fromAmount": "1000000",
        "toChainId": 1,
        "toTokenAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "fromAddress": "0x000000000000000000000000000000000000dead",
        "options": {'order': 'FASTEST', 'slippage': 0.5},
        "tool": "across",
    },
]

# Generated 3 working pairs
# Total chains tested: 3
# Token types: USDC