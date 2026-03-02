#!/usr/bin/env python3
"""
LIFI API Pair Discovery Utility

Discovers working cross-chain token pairs for testing by:
1. Fetching supported chains from /chains endpoint
2. Fetching popular tokens from /tokens endpoint
3. Testing pairs via /quote endpoint to validate they work
4. Outputting working pairs in Python dict format for test files

Usage:
    python discover_pairs.py --chains eth,pol,arb --tokens USDC,USDT --output test_pairs.py
    python discover_pairs.py --help
"""

import argparse
import json
import sys
import time
from typing import Dict, List, Optional, Tuple
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class PairDiscoverer:
    """Discovers working cross-chain token pairs for LIFI API testing."""

    def __init__(self, base_url: str = "https://li.quest/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        # Default test address
        self.test_address = "0x000000000000000000000000000000000000dead"

    def get_chains(self) -> Dict[str, Dict]:
        """Fetch all supported chains."""
        url = f"{self.base_url}/chains"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        chains = {}
        for chain in data.get('chains', []):
            chains[chain['key']] = {
                'id': chain['id'],
                'name': chain['name'],
                'key': chain['key']
            }
        return chains

    def get_tokens(self, chains: List[str] = None, tags: List[str] = None) -> Dict[str, List[Dict]]:
        """Fetch tokens for specified chains."""
        params = {}
        if chains:
            params['chains'] = ','.join(chains)
        if tags:
            params['tags'] = ','.join(tags)

        url = f"{self.base_url}/tokens"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data.get('tokens', {})

    def test_pair_quote(self, from_chain: str, to_chain: str, from_token: Dict, to_token: Dict) -> Optional[Dict]:
        """Test if a token pair works by making a quote request."""
        try:
            params = {
                'fromChain': from_chain,
                'toChain': to_chain,
                'fromToken': from_token['address'],
                'toToken': to_token['address'],
                'fromAmount': str(10 ** from_token.get('decimals', 18)),  # 1 token unit
                'fromAddress': self.test_address
            }

            url = f"{self.base_url}/quote"
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                estimate = data.get('estimate', {})

                return {
                    'from_chain': from_chain,
                    'to_chain': to_chain,
                    'from_token': from_token,
                    'to_token': to_token,
                    'tool': estimate.get('tool', 'unknown'),
                    'estimate': estimate,
                    'params': params
                }
            elif response.status_code == 429:
                print(f"Rate limited testing {from_chain}→{to_chain} {from_token['symbol']}")
                time.sleep(1)  # Brief pause on rate limit
                return None
            else:
                return None

        except Exception as e:
            print(f"Error testing {from_chain}→{to_chain} {from_token['symbol']}: {e}")
            return None

    def discover_pairs(self, chains: List[str] = None, tokens: List[str] = None,
                      max_pairs: int = 10) -> List[Dict]:
        """Discover working token pairs across chains."""
        print("Fetching supported chains...")
        all_chains = self.get_chains()

        # Filter chains if specified
        if chains:
            target_chains = {k: v for k, v in all_chains.items() if k in chains}
        else:
            # Default to popular chains
            popular = ['eth', 'pol', 'arb', 'bsc', 'opt']
            target_chains = {k: v for k, v in all_chains.items() if k in popular}

        print(f"Testing with chains: {list(target_chains.keys())}")

        print("Fetching tokens...")
        chain_keys = list(target_chains.keys())
        tokens_data = self.get_tokens(chains=chain_keys, tags=['stablecoin'])

        # Group tokens by chain
        tokens_by_chain = {}
        for chain_id, token_list in tokens_data.items():
            chain_key = None
            for tk, chain_info in target_chains.items():
                if str(chain_info['id']) == str(chain_id):
                    chain_key = tk
                    break

            if chain_key:
                tokens_by_chain[chain_key] = token_list

        # Filter tokens if specified
        if tokens:
            for chain_key in tokens_by_chain:
                tokens_by_chain[chain_key] = [
                    t for t in tokens_by_chain[chain_key]
                    if t.get('symbol') in tokens
                ]

        print("Testing token pairs...")
        working_pairs = []

        # Test pairs between different chains
        chain_keys = list(tokens_by_chain.keys())
        for i, from_chain in enumerate(chain_keys):
            for j, to_chain in enumerate(chain_keys):
                if from_chain == to_chain:
                    continue  # Skip same-chain transfers

                from_tokens = tokens_by_chain.get(from_chain, [])
                to_tokens = tokens_by_chain.get(to_chain, [])

                if not from_tokens or not to_tokens:
                    continue

                # Test first token of each type (prioritize stablecoins)
                for from_token in from_tokens[:3]:  # Test up to 3 tokens per chain
                    for to_token in to_tokens[:3]:
                        if from_token['symbol'] == to_token['symbol']:  # Same token symbol
                            result = self.test_pair_quote(from_chain, to_chain, from_token, to_token)
                            if result:
                                working_pairs.append(result)
                                print(f"✅ Found working pair: {from_chain}→{to_chain} {from_token['symbol']}")

                                if len(working_pairs) >= max_pairs:
                                    return working_pairs

                                # Small delay to avoid rate limiting
                                time.sleep(0.5)

        return working_pairs

    def generate_test_output(self, pairs: List[Dict]) -> str:
        """Generate Python dict output for test files."""
        # Get chain ID mappings
        all_chains = self.get_chains()

        output = [
            "# Generated test pairs for happy path testing",
            "# Discovered via discover_pairs.py utility",
            "# Run: python discover_pairs.py --chains eth,pol,arb --tokens USDC,USDT",
            "",
            "TEST_PAIRS = ["
        ]

        for pair in pairs:
            from_token = pair['from_token']
            to_token = pair['to_token']

            # Calculate appropriate amount (1 full token unit)
            decimals = from_token.get('decimals', 18)
            amount = str(10 ** decimals)

            pair_dict = {
                "name": f"{pair['from_chain'].upper()}_{pair['to_chain'].upper()}_{from_token['symbol']}",
                "fromChain": pair['from_chain'],
                "toChain": pair['to_chain'],
                "fromToken": from_token['address'],
                "toToken": to_token['address'],
                "fromAmount": amount,
                "fromAddress": self.test_address,
                "tool": pair['tool']
            }

            output.append("    {")
            for key, value in pair_dict.items():
                if isinstance(value, str):
                    output.append(f'        "{key}": "{value}",')
                else:
                    output.append(f'        "{key}": {value},')
            output.append("    },")

        output.extend([
            "]",
            "",
            "# Routes version (with chain IDs for /advanced/routes endpoint)",
            "ROUTE_TEST_PAIRS = ["
        ])

        for pair in pairs:
            from_token = pair['from_token']
            to_token = pair['to_token']

            # Get chain IDs from our chains data
            from_chain_id = all_chains.get(pair['from_chain'], {}).get('id', 1)
            to_chain_id = all_chains.get(pair['to_chain'], {}).get('id', 137)

            decimals = from_token.get('decimals', 18)
            amount = str(10 ** decimals)

            route_dict = {
                "name": f"{pair['from_chain'].upper()}_{pair['to_chain'].upper()}_{from_token['symbol']}",
                "fromChainId": from_chain_id,
                "fromTokenAddress": from_token['address'],
                "fromAmount": amount,
                "toChainId": to_chain_id,
                "toTokenAddress": to_token['address'],
                "fromAddress": self.test_address,
                "options": {"order": "FASTEST", "slippage": 0.5},
                "tool": pair['tool']
            }

            output.append("    {")
            for key, value in route_dict.items():
                if isinstance(value, str):
                    output.append(f'        "{key}": "{value}",')
                elif isinstance(value, dict):
                    output.append(f'        "{key}": {value},')
                else:
                    output.append(f'        "{key}": {value},')
            output.append("    },")

        output.extend([
            "]",
            "",
            f"# Generated {len(pairs)} working pairs",
            f"# Total chains tested: {len(set(p['from_chain'] for p in pairs) | set(p['to_chain'] for p in pairs))}",
            f"# Token types: {', '.join(set(p['from_token']['symbol'] for p in pairs))}"
        ])

        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Discover working LIFI API token pairs for testing")
    parser.add_argument('--chains', help='Comma-separated chain keys (e.g., eth,pol,arb)')
    parser.add_argument('--tokens', help='Comma-separated token symbols (e.g., USDC,USDT)')
    parser.add_argument('--max-pairs', type=int, default=10, help='Maximum pairs to discover')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--base-url', default='https://li.quest/v1', help='LIFI API base URL')

    args = parser.parse_args()

    chains = args.chains.split(',') if args.chains else None
    tokens = args.tokens.split(',') if args.tokens else None

    discoverer = PairDiscoverer(args.base_url)

    try:
        print("🔍 Discovering working token pairs...")
        pairs = discoverer.discover_pairs(chains=chains, tokens=tokens, max_pairs=args.max_pairs)

        if not pairs:
            print("❌ No working pairs found")
            sys.exit(1)

        print(f"✅ Found {len(pairs)} working pairs")

        output = discoverer.generate_test_output(pairs)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"📄 Output written to {args.output}")
        else:
            print("\n" + "="*80)
            print(output)
            print("="*80)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()