"""
Run some promising experiments, keep track of settings!
"""


import auction

if __name__ == "__main__":
    params = {
        "n_buyers": 100,
        "n_sellers": 10,
        "n_rounds": 1000,
        "max_price": 10,
        "penalty": 0.1,
        "leveled": True,
        "display": False
    }
    auction = auction.Auction(**params)
    auction.run_auction()