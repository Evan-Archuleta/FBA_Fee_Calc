"""
Calculate FBA Fees From Weight and Dimensions
https://sell.amazon.com/pricing.html?ref_=asus_soa_rd&#fulfillment-fees
Dimensional Weight and more info
https://sellercentral.amazon.com/gp/help/help.html?itemID=G201112670&language=en_US#:~:text=The%20dimensional%20weight%20is%20equal,up%20to%20the%20nearest%20pound.
"""
# Use this to test 
# https://sellercentral.amazon.com/fba/revenuecalculator/index?lang=en_US

import pandas as pd
import numpy as np

df = pd.read_csv("sku_info.csv")

