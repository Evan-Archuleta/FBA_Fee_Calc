import pandas as pd
import numpy as np
from numpy import median

df = pd.read_csv("sku_info.csv")

# add 4 oz for packaging weight in this size tier
# greater of dim weight or unit weight + packaging then roundup to whole pound

standard_size_product_tiers = pd.Series( data= [2.5, 2.63, 3.31, 3.48, 4.9, 5.42, 5.42], index = ["Small standard-size (10 oz or less)",
    "Small standard-size (10+ to 16 oz)",
    "Large standard-size (10 oz or less)",
    "Large standard-size (10+ to 16 oz)",
    "Large standard-size (1+ to 2 lb)",
    "Large standard-size (2+ to 3 lb)",
    "Large standard-size (3+ lb to 21 lb)"])
# add 1 lb for packaging weight in this size tier
# greater of dim weight or unit weight + packaging then roundup to whole pound
oversized_product_tiers = {
    " Small oversize 71 lb or less" : "$8.26 + $0.38/lb above first 2 lb",
    " Medium oversize 151 lb or less": "$11.37 + $0.39/lb above first 2 lb",
    " Large oversize 151 lb or less": "$75.78 + $0.79/lb above first 90 lb",
    " Special oversize" : "$137.32 + $0.91/lb above first 90 lb"
}
def length_plus_girth():
    """
    Calculates Length + girth with steps from Amazon

    Calculate the girth by adding the shortest and median sides and multiplying by 2.
    Add the longest side and girth.

    Returns df: 'length_plus_girth' in inches
    """

    df['length_plus_girth'] = ((df['shortest-side']+df['median-side']) * 2) + df['longest-side']
    return df

def dimensional_weight():
    """
    Calculates (LxHxW) / 139 from Amazon's dim weight rules. Link can be found in README.
    The dimensional weight for oversize items assumes a minimum width and height of 2 inches.
    The total shipping weight for each unit is rounded up to the nearest pound.
    """
    df['dim-weight'] = np.round(((df['longest-side']*df['median-side']*df['shortest-side'])/139), 2)
    return df

# Rounds up to the next oz 
# https://stackoverflow.com/questions/53201470/how-to-always-round-up-a-xx-5-in-numpy
# TO DO: we'll need this for adding in the packaging in the future
def np_round (value, resolution):
    return np.ceil(value / resolution) * resolution

# Calculates the weight Amazon will use for calculations 
# https://datatofish.com/if-condition-in-pandas-dataframe/
# TO DO: incorporate the greater than 150 lbs special oversized fringe case 
def fba_functional_weight():
    """
    Calculates weights Amazon will use to determine shipping fees.
    Link for rates in README
    for standard size tiers under 1 lbs is rounded to nearest oz (.0625 lbs)
    """
    b = np.maximum(df['dim-weight'], df['item-package-weight'])

    df['fba-funct-weight'] = np.choose(df['item-package-weight'] < 1 , [b, df['item-package-weight']]) 
    return df


def standard_or_oversize():
    """ Determine if object is standard size or oversized """

    bins = [0, .75, 20, 70, 150, 150.01, 500]
    labels = ['small standard-size', 'large standard-size', 'small oversize', 'medium oversize', 'large oversize', 'special oversized']
    df['product-size'] = pd.cut(df['fba-funct-weight'], bins, labels = labels)
    return df
    

length_plus_girth()
dimensional_weight()
fba_functional_weight()
standard_or_oversize()
print(df.head(10))

df.to_csv('output.csv')
