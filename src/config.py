# === RPC ===
YOUR_INFURA_PROJECT_ID = ""
INFURA_URL = f"https://mainnet.infura.io/v3/{YOUR_INFURA_PROJECT_ID}"

# === Contracts ===
WETH_ADDRESS = "0xC02aaa39b223FE8D0A0e5C4F27eAD9083C756Cc2"
UNISWAP_VIEW_ADDRESS = "0x416355755f32b2710ce38725ed0fa102ce7d07e6"

# === Paths ===
PATHS_FILE = "input/paths.json"
TOKENS_FILE = "input/tokens.json"
PAIRS_FILE = "input/pairs.json"
OUTPUT_FILE = "output/opportunity.json"

# === ABIs ===
UNISWAP_VIEW_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_pair", "type": "address[]"}],
        "name": "viewPair",
        "outputs": [{"name": "", "type": "uint112[]"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]
UNISWAP_CONTRACT_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "token0",
        "outputs": [{"name": "", "type": "address"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token1",
        "outputs": [{"name": "", "type": "address"}],
        "type": "function"
    }
]