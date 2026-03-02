import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("LIFI_BASE_URL", "https://li.quest/v1")
    API_KEY = os.getenv("LIFI_API_KEY")
    DEFAULT_FROM_CHAIN = "ETH"
    DEFAULT_TO_CHAIN = "POL"
    DEFAULT_FROM_TOKEN = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # WETH
    DEFAULT_TO_TOKEN = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"    # WETH on Polygon
    DEFAULT_FROM_AMOUNT = "1000000000000000000"
    DEFAULT_FROM_ADDRESS = "0x000000000000000000000000000000000000dead"
    DEFAULT_SOLANA_FROM_ADDRESS = "11111111111111111111111111111112"  # Solana system program address
    DEFAULT_SUI_FROM_ADDRESS = "0x2::sui::SUI"  # SUI object ID format

config = Config()
