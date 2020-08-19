import pandas as pd
import numpy as np

df = pd.read_csv("sku_info.csv")

# add 4 oz for packaging weight in this size tier
# greater of dim weight or unit weight + packaging then roundup to whole pound
standard_size_product_tiers = {
    "Small standard-size (10 oz or less)": 2.50,
    "Small standard-size (10+ to 16 oz)" : 2.63,
    "Large standard-size (10 oz or less)": 3.31,
    "Large standard-size (10+ to 16 oz)": 3.48,
    "Large standard-size (1+ to 2 lb)": 4.90,
    "Large standard-size (2+ to 3 lb)": 5.42,
    "Large standard-size (3+ lb to 21 lb)": "$5.42 + $0.38/lb above first 3 lb"
}

# add 1 lb for packaging weight in this size tier
# greater of dim weight or unit weight + packaging then roundup to whole pound
oversized_product_tiers = {
    " Small oversize 71 lb or less" : "$8.26 + $0.38/lb above first 2 lb",
    " Medium oversize 151 lb or less": "$11.37 + $0.39/lb above first 2 lb",
    " Large oversize 151 lb or less": "$75.78 + $0.79/lb above first 90 lb",
    " Special oversize" : "$137.32 + $0.91/lb above first 90 lb"
}