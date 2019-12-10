import numpy as np
import pandas as pd
import os
from copy import deepcopy
import experiments

class ExperimentLogger():
    def __init__(self):
        self.all_market_prices = np.array([])
        self.all_buyer_profits = np.array([])
        self.all_seller_profits = np.array([])
        self.all_bidding_factors = np.array([])

    def append_results(self, market_prices, buyer_profits, seller_profits, bidding_factors):
        """unroll observations into 1D, append to individual arrays"""
        market_prices = market_prices.reshape(1, -1)
        if self.all_market_prices.size == 0:
            self.all_market_prices = market_prices
        else:
            self.all_market_prices = np.concatenate((self.all_market_prices, market_prices), axis=0)

        buyer_profits = buyer_profits.reshape(1, -1)
        if self.all_buyer_profits.size == 0:
            self.all_buyer_profits = buyer_profits
        else:
            self.all_buyer_profits = np.concatenate((self.all_buyer_profits, buyer_profits), axis=0)
        
        seller_profits = seller_profits.reshape(1, -1)
        if self.all_seller_profits.size == 0:
            self.all_seller_profits = seller_profits
        else:
            self.all_seller_profits = np.concatenate((self.all_seller_profits, seller_profits), axis=0)
        
        bidding_factors = bidding_factors.reshape(1, -1)
        if self.all_bidding_factors.size == 0:
            self.all_bidding_factors = bidding_factors
        else:
            self.all_bidding_factors = np.concatenate((self.all_bidding_factors, bidding_factors), axis=0)

    def save_aggregate_results(self):
        # TODO: maybe save some averages or something??
        pass

    def save_individual_results(self, dir="experiments", name="experiment.csv"):
        """append all variables with suitable names"""
        df_dict = dict()

        for i in range(self.all_market_prices.shape[1]):
            col_name = f"market_price_{i}"
            df_dict[col_name] = self.all_market_prices[:, i]

        for i in range(self.all_buyer_profits.shape[1]):
            col_name = f"buyer_{i}"
            df_dict[col_name] = self.all_buyer_profits[:, i]

        for i in range(self.all_seller_profits.shape[1]):
            col_name = f"seller_{i}"
            df_dict[col_name] = self.all_seller_profits[:, i]
        
        seller_ind = 0
        buyer_ind = 0
        n_buyers = self.all_buyer_profits.shape[1]
        for i in range(self.all_bidding_factors.shape[1]):
            if i % n_buyers == 0:
                seller_ind += 1
                buyer_ind = 0
            col_name = f"bidding_factor_buyer_{buyer_ind}_seller_{seller_ind}"
            df_dict[col_name] = self.all_bidding_factors[:, i]
            buyer_ind += 1

        # check path existance
        if not os.path.isdir(dir):
            os.mkdir(dir)

        df = pd.DataFrame(df_dict)
        df.index.name = "Round"
        df.to_csv(path_or_buf=os.path.join(dir, name), index=True)

if __name__ == "__main__":
    el = ExperimentLogger()
    el.append_results(np.array([1]), np.array([1]), np.array([1]), np.array([1]))
    el.save_individual_results()