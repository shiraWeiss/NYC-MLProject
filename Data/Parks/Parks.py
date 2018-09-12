from geopy.distance import geodesic

from Data.Apartments.Apartments import Apartments
from Data.ExtractionUtils import *

'''
Create a data frame that maps an apartment address to the number of parks near the apartment, and the total area of the
parks.
'''


def _acresToSquareMeter(acre):
    return 4046.85642 * acre

class Parks:
    """
    @param radius: in what radius from the apartment should we look for parks (km).
    min area: what is the minimal area that we consider a legit park (in square meters).
    """
    def __init__(self, radius, min_area):
        self.loadParksDB(radius, min_area)

    '''
    Load the parks DB from csv, or create it if necessary
    '''
    def loadParksDB(self, radius, min_area):
        try:
            self.data = pd.read_csv("parks_radius" + str(radius) + "_area" + str(min_area) + ".csv")
            self.data = selectCols(self.data, ['ADDRESS', 'NUM_OF_PARKS', 'AREA_OF_PARKS'])
        except FileNotFoundError:
           self.pushParksDB(radius, min_area)

    '''
    Create the parks DB and save it to CSV
    '''

    def pushParksDB(self, radius, min_area):
        self.parks_data = self._extractParksData(min_area)  # parks_data doesn't contain the relation to the apartments
        self.data = Apartments.getInstance().getData()[['LAT', 'LON']] # data will contain a mapping from each apartment to

        self.data = self.data.iloc[25613:]
        self.data = selectCols(self.data, ['ADDRESS', 'LAT', 'LON'])
        self.iteration = 0
        parks_and_areas = self.data.apply(self._countAndSumParksInRadius, args=(radius,), axis=1)
        self.data[['NUM_OF_PARKS', 'AREA_OF_PARKS']] = parks_and_areas.apply(pd.Series)
        self.data.to_csv(path_or_buf="../Parks/parks_radius" + str(radius) + "_area" + str(min_area) + ".csv", index=False)

    '''
    @return the data with the following fields:
    PARK_NAME, LOCATION, PARK_AREA, where 'LOCATION' is the coordinates of the park
    '''
    def _extractParksData(self, min_area):
        self.parks_data = pd.read_csv("../Parks/parksProperties.csv")
        self.parks_data = self.parks_data
        self._keepRelevantParksData()
        self._filterOutParksSmallerThan(min_area)
        return self.parks_data

    def getData(self):
        return self.data

    '''
    Opens the parks csv and adds the addresses of the apartments.
    @return the data frame with apartments parm name, park location and park area 
    '''
    def _keepRelevantParksData(self):
        data = self.parks_data
        data = data[data.CLASS == 'PARK']  # keep only the parks (there are other classes in this dataset
        # select the park name, shape (coordinates that surround the park) and area
        data = selectCols(data, ['NAME311', 'the_geom', 'ACRES'])
        data.columns = ['PARK_NAME', 'PARK_COORD', 'PARK_AREA']
        data['PARK_AREA'] = data['PARK_AREA'].to_frame().apply(_acresToSquareMeter, axis=1)  # change area units to meter^2
        self.parks_data = data

    '''
        @return - a tuple of number of parks around the given address and their total area.
        '''

    def _countAndSumParksInRadius(self, apartment_row, radius):
        self.iteration += 1
        print(self.iteration)
        apartment_coords = apartment_row['LAT'], apartment_row['LON']
        counter = 0
        total_area = 0
        for park in self.parks_data.iterrows():
            dist = self._getShortestDistFromApartment(apartment_coords, park[1]['PARK_COORD'])
            if dist <= radius:
                counter += 1
                total_area += park[1]['PARK_AREA']
        return counter, total_area

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
        for coord in coords_list:
            # for some reason 'coord' is in reversed order, so [::-1] flip it back to the wanted order
            distance = calcDistBetweenCoords(coord.split(' ')[::-1], apartment_coord)
            shortest = min(shortest, distance)
        return shortest

if __name__ == '__main__':
    a = Parks(1,100)