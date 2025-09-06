import json
from web3 import Web3
from config import INFURA_URL, PATHS_FILE, OUTPUT_FILE
from storage import load_json, save_json
from utils import get_pairs_data, get_best_opportunity
from processor import process_path

def main():
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    paths = load_json(PATHS_FILE)
   
    # Gather all unique pairs from paths
    unique_pairs = set()
    for path in paths:
        for _, pairs in path:
            unique_pairs.update(pairs)

    # Fetch data for all unique pairs
    data = get_pairs_data(w3, list(unique_pairs))
    print(f"Loaded data for {len(data)} pairs")

    # Process each path to find opportunities
    opportunities = []
    for path in paths:
        opportunity = process_path(w3, path, data)
        if opportunity:
            opportunities.append(opportunity)

    print(f"Found {len(opportunities)} opportunities")
    best_opportunity = get_best_opportunity(opportunities)
    save_json(best_opportunity, OUTPUT_FILE)

if __name__ == "__main__":
    main()