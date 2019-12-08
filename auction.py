import numpy as np


class Auction():
    """
    Modified second-price sealed-bid (Vickrey) auction
    """
    def __init__(self, n_buyers, n_sellers, n_rounds, max_price, penalty, leveled=False):
        self.n_buyers = n_buyers
        self.n_sellers = n_sellers
        self.n_rounds = n_rounds
        self.max_price = max_price
        self.penalty = penalty
        self.leveled = leveled
        self.market_prices = np.zeros((n_sellers, n_rounds))
        self.seller_profits = np.zeros(n_sellers)
        self.buyer_profits = np.zeros(n_buyers)
        self.bidding_factors = 1 + np.random.random(size=(n_buyers))  # each buyer bids a multiple of the starting price

    def get_bids(self, starting_prices):
        """
        @param starting_prices: array of n_sellers
        @return: rows: buyers, cols: items
        """
        bf = self.bidding_factors.reshape(-1, 1)
        sp = starting_prices.reshape(1, -1)
        return np.dot(bf, sp)

    def get_starting_prices(self):
        return np.random.randint(low=1, high=self.max_price, size=(self.n_sellers))

    def get_market_prices(self, bids):
        return bids.mean(axis=0)

    def get_winner_matrix(self, bids, market_prices):
        """
        @param bids: array of n_buyers x n_sellers
        @param market_prices: n_sellers array
        """
        potential_winners = np.where(bids < market_prices, bids, 0)
        winner_prices = potential_winners.max(axis=0)
        winners = np.where(potential_winners==winner_prices, potential_winners, 0)
        return winners
    
    def update_profits(self, bids, market_prices, winner_matrix):
        market_prices_matrix = np.tile(market_prices, (winner_matrix.shape[0], 1))
        market_prices_matrix = np.where(winner_matrix>0, market_prices_matrix, 0)
        self.buyer_profits += (market_prices_matrix - winner_matrix).sum(axis=1)
        self.seller_profits += winner_matrix.sum(axis=0)

    def update_biddign_factors(self):
        # TODO: finish
        """update bidding factors for each buyer given bidding results"""
        pass
    
    def auction_round(self):
        # TODO: finish
        for i in range(self.n_rounds):
            starting_prices = self.get_starting_prices()
            bids = self.get_bids(starting_prices)
            market_prices = self.get_market_prices(bids)
            winner_matrix = auction.get_winner_matrix(bids, market_prices)
            self.update_profits(bids, market_prices, winner_matrix)
            # self.update_bidding_factors()
        
    def get_results(self):
        return self.buyer_profits, self.seller_profits


if __name__ == "__main__":
    params = {
        "n_buyers": 3,
        "n_sellers": 5,
        "n_rounds": 1,
        "max_price": 10,
        "penalty": 1
    }
    auction = Auction(**params)
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
