from config import WETH_ADDRESS
from utils import to_checksum, get_amount_out, readable

def process_paths(w3, paths, data):
    token_init = to_checksum(WETH_ADDRESS)
    amount_init = 10 ** 18

    opportunities = []
    for path in paths:
        opportunity = process_path(path, data, token_init, amount_init)
        if opportunity:
            opportunities.append(opportunity)
    return opportunities 

def process_path(path, data, token_init, amount_init):  
    token_in = token_init
    amount_in = amount_init

    used_hops = []
    for token_out, hops in path:
        best_amount_out, best_hop = process_hops(token_in, amount_in, hops, data)
        if best_hop is None:
            return None

        token_in = to_checksum(token_out)
        amount_in = best_amount_out
        used_hops.append((token_out, [best_hop]))

    if token_in == token_init and amount_in > amount_init:
        return {
            "initial_amount": amount_init,
            "final_amount": amount_in,
            "profit": amount_in - amount_init,
            "path": readable(used_hops)
        }
    return None

def process_hops(token_in, amount_in, hops, data):
    best_amount_out = 0
    best_hop = None

    for hop in hops:
        hop = to_checksum(hop)
        pair_data = data.get(hop)
        if not pair_data:
            continue

        token0, token1 = pair_data["token0"], pair_data["token1"]
        reserve0, reserve1 = pair_data["reserve0"], pair_data["reserve1"]

        if token_in == token0:
            reserve_in, reserve_out = reserve0, reserve1
            token_out = token1
        elif token_in == token1:
            reserve_in, reserve_out = reserve1, reserve0
            token_out = token0
        else:
            continue

        amount_out = get_amount_out(amount_in, reserve_in, reserve_out)

        if amount_out > best_amount_out:
            best_amount_out = amount_out
            best_hop = hop

    return best_amount_out, best_hop