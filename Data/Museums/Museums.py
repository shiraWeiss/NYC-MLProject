import re

import pandas as pd
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut

from Data.Apartments import Apartments
from Data.ExtractionUtils import geocode, geolocator, TEST_LINES, selectCols


class Museums:
    def __init__(self):
        self.loadMuseumsDB(1)

    '''
    Load the parks DB from csv, or create it if necessary
    '''
    def loadMuseumsDB(self, radius):
        try:
            self.data = pd.read_csv("Data/Museums/museums_db" + str(radius) + ".csv")
        except FileNotFoundError:
            self.pushMuseumsDB(radius)


    '''
    Create the parks DB and save it to CSV
    '''
    def pushMuseumsDB(self, radius):
        self.museums = self._extractMuseumsData()
        self.data = pd.read_csv("Data/Datasets/nyc-rolling-sales-coord.csv") # todo use the Apartments instead
        self.data['MUSEUMS'] = self.data.apply(self._countMuseumsInRadius, args=(radius,), axis=1)
        self.data.to_csv(path_or_buf="Data/Museums/museums_db" + str(radius) + ".csv", index=False)


    def _countMuseumsInRadius(self, apartment_location, radius):
        counter = 0
        for museum_row in self.museums.iterrows():
            museum_coord = museum_row[1]['LAT'], museum_row[1]['LON']
            apartment_coord = apartment_location['LAT'], apartment_location['LON']
            if apartment_coord == (0, 0): return 0      #   not to insert noise to the table
            dist = geodesic(apartment_coord, museum_coord).kilometers
            if dist <= radius:
                counter += 1
        return counter

    '''
    @return the data with the following fields:
    MUSEUM_COORDS
    '''
    def _extractMuseumsData(self):
        museums = pd.read_csv("Data/Museums/museums.csv")
        museums = museums # .head(TEST_LINES)  # todo remove!! short only for testing
        museums = self._getMuseumsCoords(museums)
        return museums

    '''
    @return: data frame with each museum's coordinates under 'MUSEUM_COORDS' field
    '''
    def _getMuseumsCoords(self, museums):
        museums = museums['the_geom']
        # get from 'the_geom' only the coordinate
        museums = museums.apply(lambda geom: re.match(r"POINT \((.* .*)\)", geom).group(1))
        # the coordinates are in flipped order, so flip them back
        museums = museums.apply(lambda coord: coord.split(' ')[::-1])
        museums = museums.apply(pd.Series)
        museums.columns = ['LAT', 'LON']
        return museums

    def getData(self):
        return self.data