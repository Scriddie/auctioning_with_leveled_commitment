import unittest
import auction
from importlib import reload
reload(auction)
import numpy as np
from copy import deepcopy


def initialize_auction():
    params = {
        "n_buyers": 3,
        "n_sellers": 2,
        "n_rounds": 1,
        "max_price": 10,
        "penalty": 0.1,
        "leveled": False
    }

    auc = auction.Auction(**params)

    auc.bidding_factors = np.array([[2.0, 3.0],
                                    [4.0, 5.0],
                                    [6.0, 7.0]])

    auc.decrease_factors = np.array([[0.1, 0.2],
                                     [0.3, 0.4],
                                     [0.5, 0.6]])

    auc.increase_factors = np.array([[1.1, 1.2],
                                     [1.2, 1.4],
                                     [1.5, 1.6]])

    return(auc)


### run the auc

if __name__ == "__main__":
    auction = initialize_auction()
    # auction.run_auction()
    starting_prices = auction.get_starting_prices()
    starting_prices = np.array([1, 1])
    print(f"starting_prices:\n {starting_prices}")

    bids = auction.get_bids(starting_prices)
    print(f"original bids:\n {bids}")

    pay_mat, market_prices, nan_bids = auction.get_winners(starting_prices, bids)
    print(f"sequential bids:\n {nan_bids}")
    print(f"market_prices between bidding buyers:\n {market_prices}")
    print(f"pay_mat:\n {pay_mat}")

    auction.update_profits(market_prices, pay_mat)
    buyer_profits, seller_profits = auction.get_results()
    print(f"buyer_profits:\t {buyer_profits}")
    print(f"seller_profits:\t {seller_profits}")

    print(f"old bidding factors: \n {auction.bidding_factors}")
    auction.update_bidding_factors(bids=nan_bids, market_prices=market_prices, pay_mat=pay_mat)
    print(f"new bidding factors: \n {auction.bidding_factors}")


### start collecting desired outcomes.
 
# starting_prices:
#  [1 1]
# original bids:
#  [[2. 3.]
#  [4. 5.]
#  [6. 7.]]
# market_prices between bidding buyers:
#  [4. 6.]
# payment_matrix:
#  [[1.5 0. ]
#  [0.  3. ]
#  [0.  0. ]]
# buyer_profits:   [2.5 3.  0. ]
# seller_profits:  [1.5 3. ]
# old bidding factors:
#  [[2. 3.]
#  [4. 5.]
#  [6. 7.]]
# new bidding factors:
#  [[2.2 3.6]
#  [4.8 7. ]
#  [3.  4.2]]











# class testAuctino(unittest.TestCase):
#     def __init__(self):
#         super.__init__()

#     def test_1(self):
#         pass

# def integration_test(auc):
#     # TODO: compare to hand-calculated results
#     pass
