library(ggplot2)
library(ggridges)
library(tidyverse)
library(viridis)

df = read_csv("experiments/experiment.csv")


### market prices
plt_market_prices = ggplot(df) + 
    # geom_line(aes(x=Round, y=market_price_0), color="blue") +
    geom_point(aes(x=Round, y=market_price_1), color="green") +
    scale_y_continuous(name="Item 1") + 
    theme_light()
plt_market_prices

### buyer profits
buyer_df = df %>% 
    select(Round, grep("^buyer_", colnames(df))) %>%
    gather(key="buyer_name", value="buyer_profit", -Round)

# TODO: maybe we could need some starting values somewhere here? :O
buyer_profit_line = ggplot(buyer_df) +
    geom_point(aes(x=Round, y=buyer_profit, color=buyer_name)) + 
    scale_y_continuous(limits=c(0, 0.5)) + 
    theme_light() + 
    theme(legend.position="None")
buyer_profit_line

buyer_profit_violin = ggplot(buyer_df) + 
    geom_violin(aes(x=as.factor(buyer_name), y=buyer_profit, fill=as.factor(buyer_name))) + 
    scale_y_continuous(limits=c(0, 0.5))
    theme_light() + 
    theme(legend.position="None")
buyer_profit_violin

buyer_profit_ridge = ggplot(buyer_df) +
    geom_density_ridges_gradient(aes(x=buyer_profit, y=as.factor(buyer_name), fill=..x..)) + 
    scale_x_continuous(limits=c(0, 0.4)) + 
    scale_fill_viridis(name="profits", begin=0.5, end=1)
buyer_profit_ridge

### seller profits

### bidding factors
# TODO: something about the nameing of the bidding factors is off
# TODO: maybe the initial bidding factors would be interesting to have in this context
# TODO: make this a better plot
bidding_factor_plt = ggplot(df) +
    geom_point(aes(x=Round, y=bidding_factor_buyer_0_seller_2, color="green")) + 
    geom_point(aes(x=Round, y=bidding_factor_buyer_1_seller_2, color="blue"))

bidding_factor_plt