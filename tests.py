import unittest
import auction
from importlib import reload
reload(auction)
import numpy as np


def initialize_auc():
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
    auc = initialize_auc()
    starting_prices = auc.get_starting_prices()
    starting_prices = np.array([1, 1])
    print(f"starting_prices:\n {starting_prices}")

    # bidding factor multiplied by starting price
    bids = auc.get_bids(starting_prices)
    print(f"bids:\n {bids}")

    winner_matrix, market_prices = auc.get_winners(starting_prices, bids)
    print(f"market_prices:\n {market_prices}")
    # print(f"winner_matrix:\n {winner_matrix}")

    # auc.update_profits(bids, market_prices, winner_matrix)
    # buyer_profits, seller_profits = auc.get_results()
    # print(f"buyer_profits:\t {buyer_profits}")
    # print(f"seller_profits:\t {seller_profits}")
    # auc.update_bidding_factors(bids, winner_matrix)
















# class testAuctino(unittest.TestCase):
#     def __init__(self):
#         super.__init__()

#     def test_1(self):
#         pass

# def integration_test(auc):
#     # TODO: compare to hand-calculated results
#     pass

# def integration_test2(self, auc):
#     # TODO: turn into proper testing
#     """run all auc steps manually"""
#     starting_prices = auc.get_starting_prices()
#     print(f"starting_prices:\n {starting_prices}")
#     bids = auc.get_bids(starting_prices)
#     print(f"bids:\n {bids}")
#     market_prices = auc.get_market_prices(bids)
#     print(f"market_prices:\t {market_prices}")
#     winner_matrix = auc.get_winner_matrix(bids, market_prices)
#     print(f"winner_matrix:\n {winner_matrix}")
#     auc.update_profits(bids, market_prices, winner_matrix)
#     buyer_profits, seller_profits = auc.get_results()
#     print(f"buyer_profits:\t {buyer_profits}")
#     print(f"seller_profits:\t {seller_profits}")