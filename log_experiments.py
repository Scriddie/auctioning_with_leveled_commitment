import numpy as np
import pandas as pd
import os
from copy import deepcopy

class ExperimentLogger():
    def __init__(self, n_buyers, n_sellers):
        self.all_starting_prices = np.array([])
        self.all_market_prices = np.array([])
        self.all_buyer_profits = np.array([])
        self.all_seller_profits = np.array([])
        self.all_bidding_factors = np.array([])
        self.n_buyers = n_buyers
        self.n_sellers = n_sellers

    def append_results(self, starting_prices, market_prices, buyer_profits, seller_profits, bidding_factors):
        """unroll observations into 1D, append to individual arrays"""
        starting_prices = starting_prices.reshape(1, -1)
        if self.all_starting_prices.size == 0:
            self.all_starting_prices = starting_prices
        else:
            self.all_starting_prices = np.concatenate((self.all_starting_prices, starting_prices), axis=0)

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
        
        bidding_factors = bidding_factors.flatten().reshape(1, -1)
        if self.all_bidding_factors.size == 0:
            self.all_bidding_factors = bidding_factors
        else:
            self.all_bidding_factors = np.concatenate((self.all_bidding_factors, bidding_factors), axis=0)

    def save_aggregate_results(self):
        # TODO: maybe save some averages or something??
        pass

    def save_individual_results(self, directory="experiments", name="experiment.csv"):
        """append all variables with suitable names"""
        df_dict = dict()

        for i in range(self.all_starting_prices.shape[1]):
            col_name = f"starting_price_{i}"
            df_dict[col_name] = self.all_starting_prices[:, i]

        for i in range(self.all_market_prices.shape[1]):
            col_name = f"market_price_item_{i}"
            df_dict[col_name] = self.all_market_prices[:, i]

        for i in range(self.all_buyer_profits.shape[1]):
            col_name = f"buyer_{i}_profit"
            df_dict[col_name] = self.all_buyer_profits[:, i]

        # for i in range(self.all_seller_profits.shape[1]):
        #     col_name = f"seller_{i}_profit"
        #     df_dict[col_name] = self.all_seller_profits[:, i]
        
        ind = 0
        for buyer_ind in range(self.n_buyers):
            for seller_ind in range(self.n_sellers):  # sellers
                col_name = f"bidding_factor_buyer_{buyer_ind}_seller_{seller_ind}"
                df_dict[col_name] = self.all_bidding_factors[:, ind]
                ind +=1 

        # check path existance
        if not os.path.isdir(directory):
            os.mkdir(directory)

        df = pd.DataFrame(df_dict)
        df.index.name = "Round"
        df.to_csv(path_or_buf=os.path.join(directory, name), index=True)

if __name__ == "__main__":
    el = ExperimentLogger(2, 2)
    el.append_results(np.array([1]), np.array([1]), np.array([1]), np.array([1]))
    el.save_individual_results()