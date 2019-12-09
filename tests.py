import unittest
import auction
from importlib import reload
reload(auction)
import numpy as np
from copy import deepcopy


class TestAuction(unittest.TestCase):

    def initialize_auction(self, leveled):
            params = {
                "n_buyers": 3,
                "n_sellers": 2,
                "n_rounds": 1,
                "max_price": 10,
                "penalty": 0.1,
                "leveled": leveled
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


    def integration_pure(self):
        auction = self.initialize_auction(leveled=False)
        starting_prices = np.array([1, 1])
        self.assertListEqual(starting_prices.tolist(), np.array([1, 1]).tolist())

        bids = auction.get_bids(starting_prices)
        self.assertListEqual(bids.tolist(), [[2.0, 3.0],
                                             [4.0, 5.0],
                                             [6.0, 7.0]])

        pay_mat, market_prices, nan_bids = auction.get_auction_results(starting_prices, bids)
        self.assertListEqual(pay_mat.tolist(), [[1.5, 0.0],
                                                [0.0, 3.0],
                                                [0.0, 0.0]])
        self.assertListEqual(market_prices.tolist(), [4, 6])
        self.assertListEqual(np.nan_to_num(nan_bids).tolist(), [[2.0, 0.0],
                                                                [4.0, 5.0],
                                                                [6.0, 7.0]])

        buyer_profits, seller_profits = auction.update_profits(market_prices, pay_mat)
        self.assertListEqual(buyer_profits.tolist(), [2.5, 3.0, 0.0])
        self.assertListEqual(seller_profits.tolist(), [1.5, 3.0])
        
        auction.update_bidding_factors(bids=nan_bids, market_prices=market_prices, pay_mat=pay_mat)
        self.assertListEqual(auction.bidding_factors.tolist(), [[0.2, 3.0],
                                                                [1.2, 2.0],
                                                                [3.0, 4.2]])


    def integration_leveled(self):
        auction = self.initialize_auction(leveled=True)
        starting_prices = np.array([1, 1])
        self.assertListEqual(starting_prices.tolist(), np.array([1, 1]).tolist())

        initial_bids = auction.get_bids(starting_prices)
        self.assertListEqual(initial_bids.tolist(), [[2.0, 3.0],
                                                     [4.0, 5.0],
                                                     [6.0, 7.0]])

        pay_mat, market_prices, opportunity_bids = auction.get_auction_results(starting_prices, initial_bids)
        self.assertListEqual(pay_mat.tolist(), [[1.5, ],
                                                [0.0, ],
                                                [0.0, ]])
        # TODO: maybe check profits? # buyer_profits, seller_profits = auction.get
        self.assertListEqual(market_prices.tolist(), [4.0, 12.35/3])
        self.assertListEqual(opportunity_bids.tolist(), [[2.0, 0.35],
                                                         [4.0, 5.0],
                                                         [6.0, 7.0]])
        # TODO: complete
        pass


if __name__ == "__main__":
    unittest.main()

