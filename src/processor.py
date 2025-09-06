from config import WETH_ADDRESS
from utils import to_checksum, get_amount_out, readable

def process_path(w3, path, data):
    token_init = to_checksum(WETH_ADDRESS)
    token_in = token_init
    amount_init = 1e18
    amount_in = amount_init

    used_hops = []

    for token_out, pairs in path:
        best_amount_out = 0
        best_pair = None

        for pair in pairs:
            pair = to_checksum(pair)
            token0, token1 = data[pair]["token0"], data[pair]["token1"]
            reserve0, reserve1 = data[pair]["reserve0"], data[pair]["reserve1"]

            if token_in == token0:
                reserve_in, reserve_out = reserve0, reserve1
            elif token_in == token1:
                reserve_in, reserve_out = reserve1, reserve0
            else:
                continue

            amount_out = get_amount_out(amount_in, reserve_in, reserve_out)
            if amount_out > best_amount_out:
                best_amount_out = amount_out
                best_pair = pair

        if best_amount_out == 0 or best_pair is None:
            return None

        token_in = to_checksum(token_out)
        amount_in = best_amount_out
        used_hops.append((token_out, [best_pair]))

    if token_in == token_init and amount_in > amount_init:
        return {
            "initial_amount": amount_init,
            "final_amount": amount_in,
            "profit": amount_in - amount_init,
            "path": readable(used_hops)
        }

    return None
