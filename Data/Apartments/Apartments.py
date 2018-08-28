import re

from geopy.exc import GeocoderTimedOut

from Data.ExtractionUtils import *


class Apartments:
    _instance = None

    def __init__(self):
        Apartments._instance = self
        self._createBaseDB()
        # createCoordinatesFile()

    @staticmethod
    def getInstance():
        if Apartments._instance == None:
            Apartments()
        return Apartments._instance


    def getAptsData(self):
        return self.data

    def _createBaseDB(self):
        self.data = pd.read_csv("Data/Datasets/nyc-rolling-sales.csv")
        self.data = self.data.head(TEST_LINES)  # todo - remove! short for testing
        self._removeAptsWithMissingData()
        self._fixAddress()
        self._normalizeApartsPrice()

    '''
    Remove apartments that doesn't have information about their price or area
    @Return updated data frame
    '''
    def _removeAptsWithMissingData(self):
        self.data = removeRowsWithEmptyCol(self.data, 'LAND SQUARE FEET')
        self.data = removeRowsWithEmptyCol(self.data, 'SALE PRICE')

    def _getFullAddress(self, row):
        new_address = row['ADDRESS']  + ', NYC' + ', ' + toBorough(row['BOROUGH'])
        return new_address
      
    '''
    Normalizes the apartment's price into dollars per square feet.
    '''

    def _normalizeApartsPrice(self):
        self.data['SQR_FEET_PRICE'] = self.data.apply(lambda row : float(row['SALE PRICE'])/float(row['LAND SQUARE FEET']), axis=1)
        # self.data = removeCols(self.data, 'SALE PRICE')

    '''
    Remove the apartment's apartment number (in the building), and add NY borough  
    '''
    def _fixAddress(self):
        self.data['ADDRESS'] = self.data['ADDRESS'].apply(lambda address: re.sub(r',.*', "", address))
        self.data['ADDRESS'] = self.data.apply(self._getFullAddress, axis=1)

def addressToCoordinates(address):
    data = pd.read_csv("Data/Datasets/nyc-rolling-sales-coord.csv")
    address_data = data.loc[data['ADDRESS'] == address].iloc[0]
    return float(address_data['LAT']), float(address_data['LON'])

def addressToCoordinates_aux(address):
    try:
        coord =  geolocator.geocode(address)
        if coord is None: return None
        return coord.latitude, coord.longitude
    except GeocoderTimedOut:
        return addressToCoordinates_aux(address)


def createCoordinatesFile():
    apts = Apartments.getInstance()
    coord = apts.data['ADDRESS'].apply(addressToCoordinates_aux)
    # get the coordinates to a new column, so we remove rows without valid coordinates from the data
    apts.data['tmp'] = coord
    apts.data = removeRowsWithEmptyCol(apts.data, 'tmp')
    apts.data[['LAT', 'LON']] = coord.apply(pd.Series)
    removeCols(apts.data, 'tmp')

    apts.data.to_csv(path_or_buf="Data/Datasets/nyc-rolling-sales-coord.csv", index=False)

def toBorough(borough_num):
    if borough_num == 1:
        return 'Manhattan'
    if borough_num == 2:
        return 'Bronx'
    if borough_num == 3:
        return 'Brooklyn'
    if borough_num == 4:
        return 'Queens'
    return 'Staten island'

if __name__ == '__main__':
    createCoordinatesFile()
