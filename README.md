# AMM Arbitrage Path Evaluator

## Project Structure

.
├── README.md
├── input
│ ├── paths.json
│ └── tokens.json
├── output
│ └── opportunities.json
├── requirements.txt
└── src
├── **pycache**
├── config.py
├── main.py
├── processor.py
├── storage.py
└── utils.py

## Result logs

Loaded data for **1534** pairs.
Found **67** opportunities.

## How It Works

This project analyzes token swap paths on Uniswap (or similar AMMs) to identify potential arbitrage opportunities, starting and ending with **WETH**. It fetches on-chain reserves for the involved trading pairs and simulates swaps to calculate profitability.

## Technical choice

Python is ideal for this AMM imbalance detection because it balances fast development with precise numerical handling. The task involves parsing JSON path data, interacting with Ethereum smart contracts, fetching token reserves, and performing math-heavy swap calculations — all of which are straightforward with Python's mature ecosystem. Libraries like `web3.py` make Ethereum RPC calls easy to manage, while Python's native support for large integers ensures accurate handling of toke

## Example Output

Here is an example of what the output looks like :

```json
[
  {
    "initial_amount": 1000000000000000000,
    "final_amount": 1200000000000000000,
    "profit": 200000000000000000,
    "path": [
      ["WETH", ["0xPairAddress1"]],
      ["DAI", ["0xPairAddress2"]]
    ]
  }
]
```

## Configuration

Set your Ethereum provider URL in `config.py`:

```python
YOUR_INFURA_PROJECT_ID = ""
```

Replace `YOUR_INFURA_PROJECT_ID` with your actual Infura project ID.

## Run the Script

```bash
python3 src/main.py
```

Make sure you have installed all dependencies (e.g., web3) and configured the config file accordingly.

## Function Overview

### main.py

- **main()**  
  The entry point of the script.
  - Connects to the Ethereum network via Infura.
  - Loads token swap paths from the configured JSON file.
  - Extracts all unique liquidity pairs from those paths.
  - Fetches on-chain reserve and token data for each pair.
  - Processes each path to detect profitable arbitrage opportunities using `process_path`.
  - Saves found opportunities to a JSON output file.

### processor.py

- **process_path(w3, path, data)**  
  Simulates token swaps along a given path:
  - Starts with an initial amount of WETH.
  - For each hop, calculates the best possible output amount by checking all pairs available for that hop.
  - Updates the current token and amount after each hop.
  - Returns opportunity details (initial amount, final amount, profit, and human-readable path) if the final token is WETH and profit is positive.

### utils.py

- **to_checksum(address)**  
  Converts Ethereum addresses to their checksum format for consistency and correctness.

- **get_pair_tokens(w3, pair)**  
  Retrieves the two tokens that make up a Uniswap liquidity pair from the blockchain.

- **get_pairs_data(w3, pairs)**  
  Collects reserve amounts and token info for a list of liquidity pairs in a batch call to optimize performance.

- **get_amount_out(amount_in, reserve_in, reserve_out)**  
  Calculates the expected output amount from a swap, applying the Uniswap fee (0.3%).

- **readable(path)**  
  Translates token addresses in a path to their symbols by referencing the token metadata file, making output easier to interpret.

### storage.py

- **load_json(path)**  
  Reads and parses JSON data from a file.

- **save_json(data, path)**  
  Saves data as pretty-formatted JSON to a file.

## Customisation

- Adjust `get_amount_out` function in utils.py to modify fee or simulate different output (testing).
- Change `amount_init` in processor.py to test different starting amounts.

## What to improve ?

- Add more checks on data lecture and treatment. The current code is expecting correct paths and does not manage malicious or incorrect data.
- Add dynamic possibility to change input token and amount, with related data selection.
- Add .env data and .env.example to store Infura key for example.

## Requirements

- **Python 3.8+**  
  The script requires Python version 3.8 or higher.

- **Web3.py**  
  The Ethereum Python library for blockchain interaction. Install with:  
  `pip install web3`

- **Ethereum Node Access**  
  Access to an Ethereum node, e.g., via [Infura](https://infura.io/) or another provider, to query blockchain data.

- **JSON Files Configuration**  
  Properly configured JSON files for:
  - `PATHS_FILE` containing the token swap paths
  - `TOKENS_FILE` containing token metadata such as addresses and symbols
