"""
Run some promising experiments, keep track of settings!
"""
import numpy as np
from importlib import reload
import auction
reload(auction)

experiment_1 = {
    "n_buyers": 3,
    "n_sellers": 2,
    "n_rounds": 100,
    "max_price": 10,
    "penalty": 0.1,
    "bidding_factors": np.array([[2.0, 4.0],
                                 [3.0, 6.0],
                                 [4.0, 8.0]]),
    "increase_factors": np.array([[1.1, 1.1],
                                  [1.2, 1.2],
                                  [1.3, 1.3]]),
    "decrease_factors": np.array([[0.7, 0.7],
                                  [0.8, 0.8],
                                  [0.9, 0.9]]),
    "leveled": True,
    "display": False,
    "experiment_name": "experiment_1.csv"
}

experiment_2 = {
    "n_buyers": 3,
    "n_sellers": 2,
    "n_rounds": 100,
    "max_price": 10,
    "penalty": 0.1,
    "bidding_factors": None,
    "increase_factors": None,
    "decrease_factors": None,
    "leveled": True,
    "display": False,
    "experiment_name": "experiment_2.csv"
}


if __name__ == "__main__":
    auc = auction.Auction(**experiment_1)
    auc.run_auction()

    auc = auction.Auction(**experiment_2)
    auc.run_auction()