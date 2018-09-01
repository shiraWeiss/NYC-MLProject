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

'''
This function fetches the coordinates from 'nyc-rolling-sales-coord.csv' after createApartmentsTableWithCoordinates()
built the file.
Notice! if this is called BEFORE createApartmentsTableWithCoordinates - it's not good. This probably wouldn't
happne, but still.

:)
'''
def fromTableAddressToCoordinates(address):
    data = pd.read_csv("Data/Datasets/nyc-rolling-sales-coord.csv")
    address_data = data.loc[data['ADDRESS'] == address]
    if not address_data.empty:
        address_data = address_data.iloc[0]
        return float(address_data['LAT']), float(address_data['LON'])
    else:
        return 0, 0


'''
Use geolocator to find coordinates by address.

@:param: address - the full address (with NYC etc.) in 'nyc-rolling-sales.csv' format, as string.

@:return: coordinates in lat, lon format.
'''
def getAddressToCoordinates(address):
    try:
        coord =  geolocator.geocode(address)
        if coord is None: return None
        return coord.latitude, coord.longitude
    except GeocoderTimedOut:
        return getAddressToCoordinates(address)

'''
Creates the world famous "nyc-rolling-sales-coord.csv" file with coordinates for each apartment.
~~~~~~~     "nyc-rolling-sales-coord.csv" - Get One NOW! in the Closest Store to You    ~~~~~~~

This basically needs to be run once on the entire Apartments DB, but as Shira is doing right now - it's run
over and over again so geolocator would succeed. Way to go, geolocator...

'''
def createApartmentsTableWithCoordinates():
    apts = Apartments.getInstance()
    coord = apts.data['ADDRESS'].apply(getAddressToCoordinates)
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
    createApartmentsTableWithCoordinates()
