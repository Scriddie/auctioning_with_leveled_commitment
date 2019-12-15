library(ggplot2)
library(ggridges)
library(tidyverse)
library(viridis)

experiment_name = "experiment_1"
df = read_csv(paste("experiments/", experiment_name, ".csv", sep=""))

### bidding prices
df_bidding_factors = df %>% 
    select(Round, grep("bidding_factor_", colnames(df))) %>%
    gather(key="Buyer", value="bidding_factor", -Round)

plt_bidding_factor = ggplot(df_bidding_factors) + 
    geom_line(aes(x=Round, y=bidding_factor, color=Buyer), size=0.8) +
    scale_y_continuous(name="Bidding Factor") + 
    scale_x_continuous(limits=c(0, 30))
    labs(color="Item") + 
    # theme_light() +
    theme(legend.position="None")
plt_bidding_factor

ggsave(filename=paste("visualizations/figs/", experiment_name, "_plt_bidding_factor_pure.png", sep=""),
       plot=plt_bidding_factor, device="png", units=c("in"), width=9, height=6)

### One Item
df_one_item = df %>%
    select(
        Round,
        market_price_item_0,
        grep("seller_0", colnames(df)),
    )

df_bids_item_1 = df %>% 
    select(Round, grep("bidding_factor_.*_seller_0", colnames(df))) %>%
    gather(key="Buyer", value="bidding_factor", -Round)

df_one_item["relative_market_price_0"] = df_one_item["market_price_item_0"] / df["starting_price_0"]
plt_one_item = ggplot() + 
    geom_line(data=df_one_item, aes(x=Round, y=relative_market_price_0, color="Market Price Item 0")) + 
    geom_point(data=df_bids_item_1, aes(x=Round, y=bidding_factor, color=Buyer)) + 
    scale_x_continuous(limits=c(0, 10)) +
    scale_y_continuous(name="Price relative to market price") + 
    # scale_colour_viridis_d(option="plasma") +
    # theme(legend.position="None")
    labs(color="Legend")
plt_one_item

ggsave(filename=paste("visualizations/figs/", experiment_name, "_example_item.png", sep=""),
       plot=plt_one_item, device="png", units=c("in"), width=9, height=6)
###


