import numpy as np

class auction():
    """
    Modified second-price sealed-bid (Vickrey) auction
    """
    def __init__(self, n_sellers, n_buyers, n_rounds, max_price, penalty, leveled=False):
        self.n_sellers = n_sellers
        self.n_buyers = n_buyers
        self.n_rounds = n_rounds
        self.max_price = max_price
        self.penalty = penalty
        self.leveled = leveled
        self.market_prices = []
        self.sellers_profits = []
        self.buyers_profits = []
        self.bidding_factors = 1 + np.random.random(size=(n_buyers))  # each buyer bids a multiple of the starting price

    def update_biddign_factors(self):
        """update bidding factors for each buyer given bidding results"""
        pass

    def get_bids(self):
        """create a vector of n buyers placing k bids each (n x k)"""
        """returns unique bidding factor for each buyer"""
        return self.bidding_factors

    def get_starting_prices(self):
        return np.random.randint(low=0, high=self.max_price, size=(self.n_buyers, self.n_sellers))

    def get_market_price(self):
        pass
    
    def auction_round(self):
        pass

    def get_results(self):
        return self.market_prices, self.sellers_profits, self.buyers_profits


if __name__ == "__main__":
    pass