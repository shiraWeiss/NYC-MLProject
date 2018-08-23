# use 'pip install uszipcode' to install library
from uszipcode import ZipcodeSearchEngine as zipcode

import pandas as pd

from Data.ExtractionUtils import colToInt, TEST_LINES


class Crimes:
    X_COORD = 'Latitude'
    Y_COORD = 'Longitude'

    def __init__(self):
        self.data = pd.read_csv("Data/Crime/crimes.csv")
        self.data = self.data.head(TEST_LINES)  # todo remove!! short only for testing
        self.keepOnlyCoordsCols()
        self.coordsToZipcode()
        # add the number of crimes column to the zip codes
        self.data = self.data.groupby(['ZIP CODE']).size().reset_index(name='CRIMES')

    def keepOnlyCoordsCols(self):
        self.data = self.data[[self.X_COORD, self.Y_COORD]]
        self.data = self.data.dropna()

    '''
    Turns the dataframe with coordinates values toa new data frame with NYC zip codes
    '''
    def coordsToZipcode(self):
        self.data = self.data.apply(self._getZipcodeFromCoord, axis=1).to_frame()
        self.data.columns = ['ZIP CODE']
        self.data['ZIP CODE'] = colToInt(self.data, 'ZIP CODE')

    '''
    This function receives a row of (x coord, y coord), and turns it into NYC zip code
    '''
    def _getZipcodeFromCoord(self, row):
        search = zipcode()
        res = search.by_coordinate(row[0], row[1], returns=1)
        return res[0].Zipcode

    def getData(self):
        return self.data
