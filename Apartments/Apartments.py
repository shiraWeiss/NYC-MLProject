import pandas as pd
from geopy.geocoders import Nominatim
from ExtractionUtils import TEST_LINES

geolocator = Nominatim(user_agent="utils123", timeout=5)

class Apartments:
    def __init__(self):
        self._createBaseDB()

    def getAptsData(self):
        return self.data

    def _createBaseDB(self):
        self.data = pd.read_csv("Datasets/nyc-rolling-sales.csv")
        self.data = self.data.head(TEST_LINES)  # todo - remove! short for testing
        self._removeAptsWithNoArea()
        self.data['ADDRESS'] = self.data.apply(self._getFullAddress, axis=1)

    def _removeAptsWithNoArea(self):
        self.data = self.data.loc[self.data['LAND SQUARE FEET'] != ' -  '].loc[self.data['LAND SQUARE FEET'] != '0']

    def _getFullAddress(self, row):
        new_address = row['ADDRESS']  + ', NYC' + ', ' + toBorough(row['BOROUGH'])
        return new_address

def addressToCoordinates(address):
    data = pd.read_csv("Datasets/nyc-rolling-sales-coord.csv")
    address_data = data.loc[data['ADDRESS'] == address]
    return float(address_data['LAT']), float(address_data['LON'])

def addressToCoordinates_aux(address):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

def createCoordinatesFile():
    apts = Apartments()
    coord = apts.data['ADDRESS'].apply(addressToCoordinates_aux)
    apts.data[['LAT', 'LON']] = coord.apply(pd.Series)
    apts.data.to_csv(path_or_buf="../Datasets/nyc-rolling-sales-coord.csv", index=False)

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