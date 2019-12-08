import numpy as np


class Auction():
    """
    Modified second-price sealed-bid (Vickrey) auction
    """
    def __init__(self, n_buyers, n_sellers, n_rounds, max_price, penalty, leveled=False):
        # TODO: asserts (more buyers than sellers, sensible ranges, ...)
        self.n_buyers = n_buyers
        self.n_sellers = n_sellers
        self.n_rounds = n_rounds
        self.max_price = max_price
        self.penalty = penalty
        self.leveled = leveled
        self.market_prices = np.zeros((n_sellers, n_rounds))
        self.seller_profits = np.zeros(n_sellers)
        self.buyer_profits = np.zeros(n_buyers)
        self.bidding_factors = 1 + np.random.random(size=(n_buyers, n_sellers))
        self.decrease_factors = np.tile(np.random.random(size=(n_buyers)).reshape(-1, 1), (1, n_sellers))
        self.increase_factors = np.tile(1 + np.random.random(size=(n_buyers)).reshape(-1, 1), (1, n_sellers))

    def get_bids(self, starting_prices):
        """
        @param starting_prices: array of n_sellers
        @return: rows: buyers, cols: items
        """
        return np.multiply(self.bidding_factors, starting_prices)

    def get_starting_prices(self):
        return np.tile(np.random.randint(low=1, high=self.max_price, size=(self.n_sellers)), (self.n_buyers, 1))

    def determine_winners(self, starting_prices, bids):
        """
        @param bids: array of n_buyers x n_sellers
        @param market_prices: n_sellers array
        """
        # TODO: in pure auctions, no buyer can win in multiple auctions.
        # -> implement auctions as step-by-step process?
        winners = np.zeros(bids.shape)
        market_prices = np.zeros(bids.shape)
        for i in range(self.n_sellers):
            market_prices[:, i] = np.nanmean(bids[:, i])
            potential_winners = np.where(bids[:, i] < market_prices[0, i], bids[:, i], 0)
            winner_bid, winner_index = np.nanmax(potential_winners), np.nanargmax(potential_winners)
            potential_winners[winner_index] = np.NaN
            winner_price = max(np.nanmax(potential_winners), 0.5*(starting_prices[0, i] + winner_bid))
            winners[winner_index, i] = winner_price
            bids[winner_index, :] = np.NaN

        # potential_winners = np.where(bids < market_prices, bids, 0)
        # winner_prices = potential_winners.max(axis=0)
        # winners = np.where(potential_winners==winner_prices, potential_winners, 0)
        return winners, market_prices
    
    def update_profits(self, starting_prices, bids, market_prices, winner_matrix):
        market_prices = np.where(winner_matrix>0, market_prices, 0)
        market_prices = np.where(market_prices==starting_prices, 0.5*(market_prices+starting_prices), market_prices)
        self.buyer_profits += (market_prices - winner_matrix).sum(axis=1)
        self.seller_profits += winner_matrix.sum(axis=0)

    def update_bidding_factors(self, bids, winner_matrix):
        # TODO: explore other bidding strategies!
        """update bidding factors for each buyer given bidding results"""
        updates = np.where(bids>=winner_matrix, self.decrease_factors, self.increase_factors)
        self.bidding_factors *= updates
    
    def run_auction(self):
        # TODO: keep the printed info around in dataframe for experiments
        for i in range(self.n_rounds):
            starting_prices = self.get_starting_prices()
            print(f"starting_prices:\n {starting_prices}")
            bids = self.get_bids(starting_prices)
            print(f"bids:\n {bids}")
            winner_matrix, market_prices = auction.determine_winners(starting_prices, bids)
            print(f"winner_matrix:\n {winner_matrix}")
            print(f"market_prices:\n {market_prices}")
            self.update_profits(starting_prices, bids, market_prices, winner_matrix)
            buyer_profits, seller_profits = self.get_results()
            print(f"buyer_profits:\t {buyer_profits}")
            print(f"seller_profits:\t {seller_profits}")
            # self.update_bidding_factors(bids, winner_matrix)
        
    def get_results(self):
        return self.buyer_profits, self.seller_profits


def integration_test(self, auction):
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


if __name__ == "__main__":
    params = {
        "n_buyers": 4,
        "n_sellers": 2,
        "n_rounds": 3,
        "max_price": 10,
        "penalty": 1
    }
    auction = Auction(**params)
    auction.run_auction()



    
