import json
from web3 import Web3
from config import TOKENS_FILE, PAIRS_FILE, UNISWAP_VIEW_ADDRESS, UNISWAP_VIEW_ABI, UNISWAP_CONTRACT_ABI
from storage import load_json

def to_checksum(address):
    return Web3.to_checksum_address(address)

def get_unique_pairs(paths):
    unique_pairs = set()
    for path in paths:
        for _, pairs in path:
            unique_pairs.update(pairs)
    return unique_pairs

def get_pairs_tokens(w3, pairs):
    block = w3.eth.block_number

    tokens = {}
    for pair in pairs:
        contract = w3.eth.contract(address=to_checksum(pair), abi=UNISWAP_CONTRACT_ABI)
        token0 = contract.functions.token0().call(block_identifier=block)
        token1 = contract.functions.token1().call(block_identifier=block)
        
        tokens[pair] = {
            "token0": to_checksum(token0),
            "token1": to_checksum(token1),
        }
    return tokens

def get_pairs_data(w3, pairs):
    pairs_tokens = load_json(PAIRS_FILE)
    pairs_tokens = {to_checksum(k): v for k, v in pairs_tokens.items()}

    block = w3.eth.block_number
    contract = w3.eth.contract(address=to_checksum(UNISWAP_VIEW_ADDRESS), abi=UNISWAP_VIEW_ABI)

    pairs = [to_checksum(pair) for pair in pairs] 
    pairs_reserves = contract.functions.viewPair(pairs).call(block_identifier=block)
    
    data = {}
    for i, pair in enumerate(pairs):
        pair_tokens = pairs_tokens.get(pair)
        token0 = to_checksum(pair_tokens["token0"])
        token1 = to_checksum(pair_tokens["token1"])
        reserve0, reserve1 = pairs_reserves[i * 2], pairs_reserves[i * 2 + 1]
        
        data[pair] = {
            "token0": token0,
            "token1": token1,
            "reserve0": reserve0,
            "reserve1": reserve1
        }
    return data

def get_amount_out(amount_in, reserve_in, reserve_out):
    amount_in_with_fee = amount_in * 997
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1000 + amount_in_with_fee 
    amount_out = numerator // denominator 
    return amount_out

def readable(path):
    tokens = {to_checksum(token["address"]): token.get("symbol", "") for token in load_json(TOKENS_FILE)}
    return [
        [tokens.get(to_checksum(token_out), token_out), pairs]
        for token_out, pairs in path
    ]

def load_token_decimals():
    return {
        to_checksum(token["address"]): int(token.get("decimals", 18))
        for token in load_json(TOKENS_FILE)
    }

def normalize_to_18(value, decimals):
    if decimals < 18:
        return value * 10 ** (18 - decimals)
    elif decimals > 18:
        return value // 10 ** (decimals - 18)
    else:
        return value

def denormalize_from_18(value_18, decimals):
    if decimals < 18:
        return value_18 // 10 ** (18 - decimals)
    elif decimals > 18:
        return value_18 * 10 ** (decimals - 18)
    else:
        return value_18

def get_best_opportunity(opportunities):
    return max(opportunities, key=lambda opportunity: opportunity["profit"])