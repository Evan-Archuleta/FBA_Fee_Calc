"""
Calculate FBA Fees From Weight and Dimensions
https://sell.amazon.com/pricing.html?ref_=asus_soa_rd&#fulfillment-fees
"""

import pandas as pd
import numpy as np

df = pd.read_csv("sku_info.csv")
print(df)
