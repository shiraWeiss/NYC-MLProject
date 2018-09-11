import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
geolocator = Nominatim(user_agent="utils123")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
from math import sin, cos, sqrt, atan2, radians

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

def substringMaxMatchLen_aux(str1, str2):
    longest = 0

    for i in range(1, len(str1)):
        sub_str1 = str1[i:]
        curr_longest = 0
        curr_str = str()
        for c in sub_str1:
            curr_str += c
            if curr_str in str2:
                curr_longest += 1
        longest = max(curr_longest, longest)

    return longest


def substringMaxMatchLen(str1, str2):
    return max(substringMaxMatchLen_aux(str1, str2), substringMaxMatchLen_aux(str2, str1))

def substringMatchPercentage(str1, str2):
    return ( substringMaxMatchLen(str1, str2) / len(str2) ) * 100


def calcDistBetweenCoords(coord1, coord2):
    lat1 = radians(float(coord1[0]))
    lon1 = radians(float(coord1[1]))
    lat2 = radians(float(coord2[0]))
    lon2 = radians(float(coord2[1]))
    R = 6373.0  # earth radius

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  + 0.04586793507 # 0.04586793507 is the difference from the geopy output according to our experiments

if __name__ == '__main__':
    str1 = 'dor'
    str2 = 'Fdor'
    print(substringMaxMatchLen(str1, str2))