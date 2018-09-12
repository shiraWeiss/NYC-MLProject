import re
import pandas as pd

from Data.Apartments.Apartments import Apartments
from Data.ExtractionUtils import geocode, geolocator, TEST_LINES, selectCols, calcDistBetweenCoords


class Museums:
    def __init__(self, radius):
        self.loadMuseumsDB(radius)

    '''
    Load the parks DB from csv, or create it if necessary
    '''
    def loadMuseumsDB(self, radius):
        try:
            self.data = pd.read_csv("Data/Datasets/museums_db" + str(radius) + ".csv")
            self.data = selectCols(self.data, ['ADDRESS', 'museums_in_radius'])
        except FileNotFoundError:
            self.pushMuseumsDB(radius)


    '''
    Create the parks DB and save it to CSV
    '''
    def pushMuseumsDB(self, radius):
        self.museums = self._extractMuseumsData()
        self.data = Apartments.getInstance().getData()
        self.data = selectCols(self.data, ['ADDRESS', 'LAT', 'LON'])
        self.data['museums_in_radius'] = self.data.apply(self._countMuseumsInRadius, args=(radius,), axis=1)
        self.data.to_csv(path_or_buf="Data/Datasets/museums_db" + str(radius) + ".csv", index=False)


    def _countMuseumsInRadius(self, apartment_location, radius):
        counter = 0
        for museum_row in self.museums.iterrows():
            museum_coord = museum_row[1]['LAT'], museum_row[1]['LON']
            apartment_coord = apartment_location['LAT'], apartment_location['LON']
            dist = calcDistBetweenCoords(apartment_coord, museum_coord)
            if dist <= radius:
                counter += 1
        return counter

    '''
    @return the data with the following fields:
    MUSEUM_COORDS
    '''
    def _extractMuseumsData(self):
        museums = pd.read_csv("museums.csv")
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


if __name__ == '__main__':
    a = Museums(5)