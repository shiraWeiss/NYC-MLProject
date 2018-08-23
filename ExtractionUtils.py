from geopy.geocoders import Nominatim
import pandas as pd
TEST_LINES = 10

geolocator = Nominatim(user_agent="utils123", timeout=5)


def removeRowsWithEmptyCol(df, col):
    return df.loc[df[col] != ' -  '].loc[df[col] != '0']


'''
Turns all the values of a dataframes' column to Int type
'''
def colToInt(df, col_name):
    return df[col_name].apply(int)


def addressToCoordinates(address):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


'''
@params df - a dataframe, cols - a list of columns that we want to keep from the df
@return return a dataframe that contains only the input columns
'''
def selectCols(df, cols):
    return df[cols]

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

