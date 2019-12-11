import numpy as np
from copy import deepcopy
import log_experiments
from importlib import reload
reload(log_experiments)


class Auction():
    """
    Modified second-price sealed-bid (Vickrey) auction
    """
    def __init__(self, n_buyers, n_sellers, n_rounds, max_price, penalty,
                 bidding_factors=None, increase_factors=None, decrease_factors=None,
                 leveled=False, display=False, experiment_name="experiment.csv"):
        # TODO: make random components parameters, if not supplied, only then random
        assert(n_buyers > 1)
        assert(n_sellers > 0)
        assert(n_buyers > n_sellers)
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
        # TODO: examine these initializations
        if isinstance(bidding_factors, type(None)):
            self.bidding_factors = 1 + np.random.random(size=(n_buyers, n_sellers))
        else:
            self.bidding_factors = bidding_factors
        if isinstance(decrease_factors, type(None)):
            self.decrease_factors = np.tile(np.random.uniform(low=0.9, high=1, size=(n_buyers)).reshape(-1, 1), (1, n_sellers))
        else:
            self.decrease_factors = decrease_factors
        if isinstance(increase_factors, type(None)):
            self.increase_factors = np.tile(1 + np.random.random(size=(n_buyers)).reshape(-1, 1), (1, n_sellers))
        else:
            self.increase_factors = increase_factors
        
        # keep track of results
        self.display = display
        self.experiment_logger = log_experiments.ExperimentLogger(self.n_buyers, self.n_sellers)
        self.experiment_name = experiment_name

        # TODO: enable user to set starting values somehow?

    def get_bids(self, starting_prices):
        """
        @param starting_prices: array of n_sellers
        @return: rows: buyers, cols: items
        """
        return np.multiply(self.bidding_factors, starting_prices)

    def get_starting_prices(self):
        return np.random.randint(low=1, high=self.max_price, size=(self.n_sellers))

    def get_auction_results(self, starting_prices, bids):
        """
        @param bids: array of n_buyers x n_sellers
        @param market_prices: n_sellers array
        """
        starting_prices = deepcopy(starting_prices)
        bids = deepcopy(bids)
        pay_mat = np.zeros(bids.shape)
        market_prices = np.zeros(self.n_sellers)
        for i in range(self.n_sellers):
            bids_i = bids[:, i]
            
            if self.leveled and (i > 0):  # in case of leveled commitment, adjust bids by opportunity cost
                buyer_profits, seller_profits = self.get_profits(market_prices[:i], pay_mat[:, :i])
                potential_penalty = np.where(pay_mat > 0, self.penalty*pay_mat, 0).sum(axis=1)
                opp_cost = buyer_profits + potential_penalty  
                bids_i -= opp_cost
                bids_i = np.where(bids_i < starting_prices[i], np.NaN, bids_i)
                bids[:, i] = bids_i  # update bids

            market_prices[i] = np.nanmean(bids_i)
            potential_winners = np.where(bids_i < market_prices[i], bids_i, 0)
            winner_bid, winner_idx = np.nanmax(potential_winners), np.nanargmax(potential_winners)
            potential_winners[winner_idx] = np.NaN  # set winners price to zero, so you get second best price

            if np.count_nonzero(potential_winners) > 1:
                winner_price = np.nanmax(potential_winners) 
            else:
                winner_price = 0.5*(starting_prices[i] + winner_bid)

            if self.leveled:  # take into account leveled commitment penalty mechanism
                gain = market_prices[i] - winner_price
                opportunity_index = pay_mat[winner_idx, :].argmax()
                if pay_mat[winner_idx, opportunity_index] > 0:
                    opportunity_cost = market_prices[opportunity_index] - pay_mat[winner_idx, opportunity_index]
                    # indicate withdrawal cost by negative sign
                    if opportunity_cost > gain:
                        pay_mat[winner_idx, i] = - (self.penalty * winner_price)
                    else:
                        pay_mat[winner_idx, i] = winner_price
                        pay_mat[winner_idx, opportunity_index] = - (self.penalty * pay_mat[winner_idx, opportunity_index])
                else:
                    pay_mat[winner_idx, i] = winner_price
            else:
                pay_mat[winner_idx, i] = winner_price
                try:
                    bids[winner_idx, i+1:] = np.NaN
                except:
                    IndexError
        return pay_mat, market_prices, bids

    def get_profits(self, market_prices, pay_mat):
        market_prices = deepcopy(market_prices)
        pay_mat = deepcopy(pay_mat)
        market_prices = np.tile(market_prices, (self.n_buyers, 1))
        market_prices = np.where(pay_mat > 0, market_prices, 0.0)
        buyer_increase = (market_prices - pay_mat).sum(axis=1)
        seller_increase = np.abs(pay_mat).sum(axis=0)
        return buyer_increase, seller_increase

    def update_profits(self, market_prices, pay_mat):
        buyer_increase, seller_increase = self.get_profits(market_prices, pay_mat)
        self.buyer_profits += buyer_increase
        self.seller_profits += seller_increase
        return buyer_increase, seller_increase

    def update_bidding_factors(self, bids, market_prices, pay_mat):
        """update bidding factors for each buyer given bidding results"""
        # TODO: explore other bidding strategies!
        bids = deepcopy(bids)
        market_prices = deepcopy(market_prices)
        pay_mat = deepcopy(pay_mat)
        market_prices = np.tile(market_prices, (self.n_buyers, 1))
        updates = np.where(np.nan_to_num(bids) >= market_prices, self.decrease_factors, self.increase_factors)
        updates = np.where(np.isnan(bids), 1.0, updates)
        updates = np.where(pay_mat > np.zeros(pay_mat.shape), self.decrease_factors, updates)
        self.bidding_factors = np.multiply(self.bidding_factors, updates)
        self.bidding_factors = np.where(self.bidding_factors > 1, self.bidding_factors, 1.0)

    def display_output(self, auction_round, starting_prices, bids, nan_bids, market_prices, pay_mat, buyer_profits, seller_profits,
     old_bidding_factors, new_bidding_factors):
        # TODO: use all the pring stmts from auction
        print(f"-----AUCTION ROUND {auction_round+1}------")
        print(f"starting_prices:\n {starting_prices}\n")
        print(f"original bids (buyers x sellers):\n {bids}\n")
        print(f"adjusted bids (buyers x sellers):\n {nan_bids}")
        print(f"market_prices between bidding buyers:\n {market_prices}")
        print(f"payment matrix (buyers x sellers, negative values indicate penalty payments):\n {pay_mat}\n")
        print(f"buyer_profits:\t {buyer_profits}")
        print(f"seller_profits:\t {seller_profits}\n")
        print(f"old bidding factors (buyers x sellers): \n {old_bidding_factors}")
        print(f"new bidding factors (buyers x sellers): \n {new_bidding_factors}\n\n")
        pass

    def run_auction(self):
        # TODO: keep the printed info around in dataframe for experiments
        for auction_round in range(self.n_rounds):
            starting_prices = self.get_starting_prices()
            bids = self.get_bids(starting_prices)
            pay_mat, market_prices, nan_bids = self.get_auction_results(starting_prices, bids)
            buyer_profits, seller_profits = self.update_profits(market_prices, pay_mat)
            old_bidding_factors = self.bidding_factors

            # log
            self.experiment_logger.append_results(starting_prices, buyer_profits, seller_profits, old_bidding_factors)

            self.update_bidding_factors(bids=nan_bids, market_prices=market_prices, pay_mat=pay_mat)
            new_bidding_factors = self.bidding_factors

            if self.display:
                self.display_output(auction_round, starting_prices, bids, nan_bids, market_prices, pay_mat, buyer_profits, seller_profits,
                                    old_bidding_factors, new_bidding_factors)

        self.experiment_logger.save_individual_results(name=self.experiment_name)

if __name__ == "__main__":
    params = {
        "n_buyers": 3,
        "n_sellers": 2,
        "n_rounds": 10,
        "max_price": 10,
        "penalty": 0.1,
        "bidding_factors": None,
        "increase_factors": None,
        "decrease_factors": None,
        "leveled": True,
        "display": True,
        "experiment_name": "experiment"
    }
    auction = Auction(**params)
    auction.run_auction()

