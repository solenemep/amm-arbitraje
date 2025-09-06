import json
from web3 import Web3
from config import INFURA_URL, PATHS_FILE, PAIRS_FILE
from storage import load_json, save_json
from utils import get_unique_pairs, get_pairs_tokens

def pairs():
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    paths = load_json(PATHS_FILE)
    unique_pairs = get_unique_pairs(paths)

    tokens = get_pairs_tokens(w3, list(unique_pairs))
    save_json(tokens, PAIRS_FILE)

if __name__ == "__main__":
    pairs()