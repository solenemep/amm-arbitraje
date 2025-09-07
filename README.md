# AMM Arbitrage Path Evaluator

## Project Structure

```bash
.
├── README.md
├── input
│ ├── pairs.json
│ ├── paths.json
│ └── tokens.json
├── output
│ └── opportunity.json
├── requirements.txt
└── src
├── **pycache**
├── config.py
├── main.py
├── pairs.py
├── processor.py
├── storage.py
└── utils.py
```

## How It Works

This project analyzes token swap paths on Uniswap (or similar AMMs) to identify potential arbitrage opportunities, starting and ending with **WETH**. It fetches on-chain reserves for the involved trading pairs and simulates swaps to calculate profitability.

## Technical choice

Python is ideal for this AMM imbalance detection because it balances fast development with precise numerical handling. The task involves parsing JSON path data, interacting with Ethereum smart contracts, fetching token reserves, and performing math-heavy swap calculations — all of which are straightforward with Python's mature ecosystem. Libraries like `web3.py` make Ethereum RPC calls easy to manage, while Python's native support for large integers ensures accurate handling of toke

## Example Output

Here is an example of what the output looks like :

```json
{
  "opportunity": {
    "initial_amount": 1000000000000000000,
    "final_amount": 1200000000000000000,
    "profit": 200000000000000000,
    "path": [
      ["WETH", ["0xPairAddress1"]],
      ["DAI", ["0xPairAddress2"]]
    ]
  }
}
```

## Configuration

Set your Ethereum provider URL in `config.py`:

```python
YOUR_INFURA_PROJECT_ID = ""
```

Replace `YOUR_INFURA_PROJECT_ID` with your actual Infura project ID.

## Run the Script

First, you need to extract the token0/token1 addresses for each pair by running:

```bash
python3 src/pairs.py
```

This will create a JSON file in the output directory with the token pairs information.

Then, you can run the processor to find the best opportunity by running:

```bash
python3 src/main.py
```

Make sure you have installed all dependencies (e.g., web3) and configured the config file accordingly.

```bash
pip install -r requirements.txt
```

## Function Overview

### main.py

- **main()**  
  The entry point of the script. Handles all steps from connecting to Ethereum, loading paths, extracting pairs, fetching reserves, processing arbitrage, and saving results.

### pairs.py

- **pairs()**  
  Connects to the Ethereum network, loads swap paths, extracts all unique pair addresses, fetches token0/token1 for each pair using `get_pairs_tokens`, and saves the result to a JSON file defined by `PAIRS_FILE`. This file is used as a reference for token pairs in the rest of the project. Run this script before running the main arbitrage processor to ensure you have up-to-date token pair information.

### processor.py

- **process_paths(w3, paths, data)**  
  Iterates over a list of swap paths, calls `process_path` for each, and collects all profitable opportunities into a list. Returns all found opportunities for further analysis or selection.

- **process_path(w3, path, data)**  
  Simulates token swaps along a given path, updating token and amount at each hop, and returns opportunity details if profitable.

- **process_hops(token_in, amount_in, hops, data)**  
  For a given input token and amount, iterates over all possible pairs (hops) for a swap step, normalizes for decimals, and returns the best output amount and corresponding pair.

### storage.py

- **load_json(path)**  
  Reads and parses JSON data from a file.

- **save_json(data, path)**  
  Saves data as pretty-formatted JSON to a file.

### utils.py

- **to_checksum(address)**  
  Converts Ethereum addresses to their checksum format for consistency and correctness.

- **get_unique_pairs(paths)**  
  Extracts and returns a set of all unique pair addresses from the provided swap paths. Used to identify which pairs need to be queried for token and reserve data.

- **get_pairs_tokens(w3, pair)**  
  Retrieves the two tokens that make up a Uniswap liquidity pair from the blockchain.

- **get_pairs_data(w3, pairs)**  
  Collects reserve amounts and token info for a list of liquidity pairs in a batch call to optimize performance.

- **get_amount_out(amount_in, reserve_in, reserve_out)**  
  Calculates the expected output amount from a swap, applying the Uniswap fee (0.3%).

- **readable(path)**  
  Translates token addresses in a path to their symbols by referencing the token metadata file, making output easier to interpret.

- **load_token_decimals(address)**  
  Looks up and returns the decimals value for a given token address from the tokens metadata JSON file. If the token is not found or the decimals field is missing, it returns 18 by default. This ensures calculations are accurate for tokens with non-standard decimals.

- **normalize_to_18(amount, decimals)**  
  Converts a token amount with any decimals to the equivalent value in 18 decimals, using integer math. Handles both cases where decimals are less than or greater than 18.

- **denormalize_from_18(amount_18, decimals)**  
  Converts an amount in 18 decimals back to the token's native decimals, using integer math. Handles both cases where decimals are less than or greater than 18.

- **get_best_opportunity(opportunities)**  
  Returns the opportunity with the highest profit from a list of opportunities. If the list is empty, returns None.

## Customisation

- Adjust `get_amount_out` function in utils.py to modify fee or simulate different output (testing).
- Change `amount_init` in processor.py to test different starting amounts.

## What to improve ?

- Add more checks on data lecture and treatment. The current code is expecting correct paths and does not manage malicious or incorrect data.
- Add dynamic possibility to change input token and amount, with related data selection.
- Include gas fee calculations to be more precise on wether swap gas fee don't cancel yield.
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
