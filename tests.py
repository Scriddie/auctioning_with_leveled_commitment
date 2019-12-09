import unittest

class testAuctino(unittest.TestCase):
    def __init__(self):
        super.__init__()

    def test_1(self):
        pass

def integration_test(auction):
    # TODO: compare to hand-calculated results
    pass

def integration_test2(self, auction):
    # TODO: turn into proper testing
    """run all auction steps manually"""
    starting_prices = auction.get_starting_prices()
    print(f"starting_prices:\n {starting_prices}")
    bids = auction.get_bids(starting_prices)
    print(f"bids:\n {bids}")
    market_prices = auction.get_market_prices(bids)
    print(f"market_prices:\t {market_prices}")
    winner_matrix = auction.get_winner_matrix(bids, market_prices)
    print(f"winner_matrix:\n {winner_matrix}")
    auction.update_profits(bids, market_prices, winner_matrix)
    buyer_profits, seller_profits = auction.get_results()
    print(f"buyer_profits:\t {buyer_profits}")
    print(f"seller_profits:\t {seller_profits}")