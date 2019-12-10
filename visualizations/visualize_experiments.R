library(ggplot2)
library(tidyverse)

df = read_csv("experiments/experiment.csv")


ggplot(df, aes(x=market_price_0, y=market_price_1)) + 
    geom_point()