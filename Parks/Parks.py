import overpy
import pandas as pd
from geopy.distance import geodesic

from Apartments.Apartments import Apartments
from ExtractionUtils import *

'''
Create a data frame that maps an apartment address to the number of parks near the apartment, and the total area of the
parks.
'''


def _acresToSquareMeter(acre):
    return 4046.85642 * acre


class Parks:
    """
    @param radius: in what radius from the apartment should we look for parks.
    min area: what is the minimal area that we consider a legit park.
    """
    def __init__(self, radius, min_area):
        self.parks_data = self._extractParksData(min_area)  # parks_data doesn't contain the relation to the apartments
        self.data = Apartments().data['ADDRESS'].to_frame()  # data will contain a mapping from each apartment to
        parks_and_areas = self.data['ADDRESS'].apply(self._countAndSumParksInRadius, args=(radius,))
        self.data[['NUM_OF_PARKS', 'AREA_OF_PARKS']] = parks_and_areas.apply(pd.Series)

    '''
    @return the data with the following fields:
    PARK_NAME, LOCATION, PARK_AREA, where 'LOCATION' is the coordinates of the park
    '''
    def _extractParksData(self, min_area):
        self.parks_data = pd.read_csv("Parks/parksProperties.csv")
        self.parks_data = self.parks_data.head(TEST_LINES)  # todo remove!! short only for testing
        self._keepRelevantParksData()
        self._filterOutParksSmallerThan(min_area)
        return self.parks_data

    def getData(self):
        return self.data

    '''
    @return - a tuple of number of parks around the given address and their total area.
    '''

    def _countAndSumParksInRadius(self, address, radius):
        location = geolocator.geocode(address)
        apartment_coords = (location.latitude, location.longitude)
        counter = 0
        total_area = 0
        for park in self.parks_data.iterrows():
            dist = self._getShortestDistFromApartment(apartment_coords, park[1]['COORDS'])
            if dist <= radius:
                counter += 1
                total_area += park[1]['PARK_AREA']
        return counter, total_area

    '''
    Opens the parks csv and adds the addresses of the apartments.
    @return the data frame with apartments parm name, park location and park area 
    '''
    def _keepRelevantParksData(self):
        data = self.parks_data.head(TEST_LINES)  # todo remove!! short only for testing
        data = data[data.CLASS == 'PARK']  # keep only the parks
        # select the park name, shape (coordinates that surround the park) and area
        data = selectCols(data, ['NAME311', 'the_geom', 'ACRES'])
        data.columns = ['PARK_NAME', 'COORDS', 'PARK_AREA']
        data['PARK_AREA'] = data['PARK_AREA'].to_frame().apply(_acresToSquareMeter, axis=1)  # change area units to meter^2
        self.parks_data = data

    def _filterOutParksSmallerThan(self, min_area):
        self.parks_data = self.parks_data[self.parks_data.PARK_AREA >= min_area]

    '''
    @param apartment coordinates, and park coordinates - a list of coordinates that 
    surrounds the park
    @return the closest point to the apartment 
    '''
    def _getShortestDistFromApartment(self, apartment_coord, park_coords):
        shortest = 10000
        coords_list = park_coords.replace('MULTIPOLYGON', '').replace(')', '').replace('(', '').split(',')
        coords_list = coords_list[:5] # todo - remove! for tests
        for coord in coords_list:
            # for some reason 'coord' is in reversed order, so [::-1] flip it back to the wanted order
            distance = geodesic(apartment_coord, coord.split(' ')[::-1]).kilometers
            shortest = min(shortest, distance)
        return shortest
