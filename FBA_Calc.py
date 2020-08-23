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
def np_round (value, resolution):
    return np.ceil(value / resolution) * resolution
    #df['fba-funct-weight'] = df['item-package-weight'].apply(lambda x: np_round(x, .0625) + .25 if x <= 1 else x)
    # TO DO: we'll need this for adding in the packaging in the future 

#https://datatofish.com/if-condition-in-pandas-dataframe/
def fba_functional_weight():
    """
    Calculates weights Amazon will use to determine shipping fees.
    Link for rates in README
    for standard size tiers under 1 lbs is rounded to nearest oz (.0625 lbs)
    """
    #Left off here after the else works if we aren't comparing / finding the max of dim vs actual weight 
    #calculating weird value of 0    0.76 
    b = np.maximum(df['dim-weight'], df['item-package-weight'])
    df['fba-funct-weight'] = df['item-package-weight'].apply(lambda x: x if x <= 1 else df['dim-weight'])
    
    print(b)
    return df

#def product_tier_size():
#     """calculates if an item is standard or oversized

#     """

length_plus_girth()
dimensional_weight()
fba_functional_weight()
print(df.head(10))

df.to_csv('output.csv')