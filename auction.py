import numpy as np


class Auction():
    """
    Modified second-price sealed-bid (Vickrey) auction
    """
    def __init__(self, n_buyers, n_sellers, n_rounds, max_price, penalty, leveled=False):
        assert(n_buyers > n_sellers)
        # assert(n_buyers >= 2)
        # assert(n_sellers > 0)
        self.n_buyers = n_buyers
        self.n_sellers = n_sellers
        self.n_rounds = n_rounds
        self.max_price = max_price
        self.penalty = penalty
        self.leveled = leveled
        self.market_prices = np.zeros((n_sellers, n_rounds))
        self.seller_profits = np.zeros(n_sellers)
        self.buyer_profits = np.zeros(n_buyers)

        # parts with random initialization
        self.bidding_factors = 1 + np.random.random(size=(n_buyers, n_sellers))
        self.decrease_factors = np.tile(np.random.random(size=(n_buyers)).reshape(-1, 1), (1, n_sellers))
        self.increase_factors = np.tile(1 + np.random.random(size=(n_buyers)).reshape(-1, 1), (1, n_sellers))

    # TODO: enable user to set starting values somehow?

    def get_bids(self, starting_prices):
        """
        @param starting_prices: array of n_sellers
        @return: rows: buyers, cols: items
        """
        return np.multiply(self.bidding_factors, starting_prices)

    def get_starting_prices(self):
        return np.random.randint(low=1, high=self.max_price, size=(self.n_sellers))

    def get_winners(self, starting_prices, bids):
        """
        @param bids: array of n_buyers x n_sellers
        @param market_prices: n_sellers array
        """
        winners = np.zeros(bids.shape)
        market_prices = np.zeros(self.n_sellers)
        for i in range(self.n_sellers):
            market_prices[i] = np.nanmean(bids[:, i])
            potential_winners = np.where(bids[:, i] < market_prices[i], bids[:, i], 0)
            winner_bid, winner_index = np.nanmax(potential_winners), np.nanargmax(potential_winners)
            potential_winners[winner_index] = np.NaN
            winner_price = max(np.nanmax(potential_winners), 0.5*(starting_prices[i] + winner_bid))
            if self.leveled:
                gain = market_prices[i] - winner_price
                opportunity_index = winners[winner_index, :].argmax()
                if winners[winner_index, opportunity_index] > 0:
                    opportunity_cost = market_prices[opportunity_index] - winners[winner_index, opportunity_index]
                    # indicate withdrawal cost by negative sign
                    if opportunity_cost > gain:
                        winners[winner_index, i] = - (self.penalty * winner_price)
                    else:
                        winners[winner_index, i] = winner_price
                        winners[winner_index, opportunity_index] = - (self.penalty * winners[winner_index, opportunity_index])
                else:
                    winners[winner_index, i] = winner_price
            else:
                winners[winner_index, i] = winner_price
                bids[winner_index, :] = np.NaN
        return winners, market_prices

    def update_profits(self, bids, market_prices, pay_mat):
        # TODO: maybe keep starting prices and market prices as 1D array up until here?
        market_prices = np.tile(market_prices, (self.n_buyers, 1))
        market_prices = np.where(pay_mat > 0, market_prices, 0)
        self.buyer_profits += (market_prices - pay_mat).sum(axis=1)
        self.seller_profits += np.abs(pay_mat).sum(axis=0)

    def update_bidding_factors(self, bids, pay_mat):
        # TODO: explore other bidding strategies!
        """update bidding factors for each buyer given bidding results"""
        # TODO: fix
        updates = np.where(bids>=pay_mat, self.decrease_factors, self.increase_factors)
        self.bidding_factors *= updates
    
    def run_auction(self):
        # TODO: keep the printed info around in dataframe for experiments
        for i in range(self.n_rounds):
            starting_prices = self.get_starting_prices()
            print(f"starting_prices:\n {starting_prices}")

            bids = self.get_bids(starting_prices)
            print(f"original bids:\n {bids}")

            pay_mat, market_prices = self.get_winners(starting_prices, bids)
            print(f"market_prices between bidding buyers:\n {market_prices}")
            print(f"pay_mat:\n {pay_mat}")

            self.update_profits(bids, market_prices, pay_mat)
            buyer_profits, seller_profits = self.get_results()
            print(f"buyer_profits:\t {buyer_profits}")
            print(f"seller_profits:\t {seller_profits}")
            self.update_bidding_factors(bids, pay_mat)
        
    def get_results(self):
        return self.buyer_profits, self.seller_profits


if __name__ == "__main__":
    params = {
        "n_buyers": 3,
        "n_sellers": 2,
        "n_rounds": 3,
        "max_price": 10,
        "penalty": 0.1,
        "leveled": True
    }
    auction = Auction(**params)
    auction.run_auction()

