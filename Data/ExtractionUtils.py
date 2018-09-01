import pandas as pd

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
geolocator = Nominatim(user_agent="utils123")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

TEST_LINES = 1000

def removeRowsWithEmptyCol(df, col):
    return df.loc[df[col].apply(str) != ' -  '].loc[df[col].apply(str) != '0'].dropna(subset=[col])

'''
Turns all the values of a dataframes' column to Int type
'''
def colToInt(df, col_name):
    return df[col_name].apply(int)

'''
@params df - a dataframe, cols - a list of columns that we want to keep from the df
@return return a dataframe that contains only the input columns
'''
def selectCols(df, cols):
    return df[cols]

'''
@params df - a dataframe, cols - a list of columns that we want to remove from df
@return return a dataframe without the input columns
'''
def removeCols(df, cols):
    return df.drop(columns=cols)

def getAbbreviation(full_name):
    res = str()
    for c in full_name:
        if c.isupper():
            res = res + c
    return res

def getOnlyNumbers(full_name):
    res = str()
    for c in full_name:
        if c.isdigit():
            res = res + c
    if res == '':
        return 0
    else:
        return res

'''
@param: values - a Series containing the values.
@param: amounts - a Series containing the amount of objects to be calculated. 
'''
def getExpectedValue(values, amounts):
    n = amounts.sum()
    fraction = 0
    for v, a in zip(values, amounts):
        fraction = fraction + float(v)*float(a)
    return fraction / n

