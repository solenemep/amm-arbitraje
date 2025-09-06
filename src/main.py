import json
from web3 import Web3
from config import INFURA_URL, PATHS_FILE, OUTPUT_FILE
from storage import load_json, save_json
from utils import get_unique_pairs, get_pairs_data, get_best_opportunity
from processor import process_paths

def main():
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    paths = load_json(PATHS_FILE)
    unique_pairs = get_unique_pairs(paths)

    # Fetch data for all unique pairs
    data = get_pairs_data(w3, list(unique_pairs))
    print(f"Loaded data for {len(data)} pairs")

    # Process each path to find opportunities
    opportunities = process_paths(w3, paths, data)
    print(f"Found {len(opportunities)} opportunities")

    # Get the best opportunity
    if len(opportunities) > 0:
        best_opportunity = get_best_opportunity(opportunities)
        save_json(best_opportunity, OUTPUT_FILE)

if __name__ == "__main__":
    main()