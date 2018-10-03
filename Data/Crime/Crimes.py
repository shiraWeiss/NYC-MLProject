# use 'pip install uszipcode' to install library
from uszipcode import ZipcodeSearchEngine as zipcode

import pandas as pd

from Data.ExtractionUtils import colToInt, TEST_LINES, selectCols, DATASETS_PATH


class Crimes:
    X_COORD = 'Latitude'
    Y_COORD = 'Longitude'

    def __init__(self):
        try:
            self.data = pd.read_csv(DATASETS_PATH + "/crimes_db.csv").drop_duplicates()
        except FileNotFoundError:
            self.data = pd.read_csv(DATASETS_PATH + "/crimes_db.csv")
            self._keepOnlyCoordsCols()
            self._coordsToZipcode()
            # add the number of crimes column to the zip codes
            self.data = self.data.groupby(['ZIP CODE']).size().reset_index(name='CRIMES').drop_duplicates()
            self.data.to_csv(path_or_buf=DATASETS_PATH + "/crimes.csv", index=False)

    def _keepOnlyCoordsCols(self):
        self.data = selectCols(self.data, [self.X_COORD, self.Y_COORD])
        self.data = self.data.dropna()

    '''
    Turns the dataframe with coordinates values toa new data frame with NYC zip codes
    '''
    def _coordsToZipcode(self):
        self.i = 0
        self.data = self.data.apply(self._getZipcodeFromCoord, axis=1).to_frame()
        self.data.columns = ['ZIP CODE']
        self.data['ZIP CODE'] = colToInt(self.data, 'ZIP CODE')

    '''
    This function receives a row of (x coord, y coord), and turns it into NYC zip code
    '''
    def _getZipcodeFromCoord(self, row):
        self.i += 1
        print(self.i)
        search = zipcode()
        res = search.by_coordinate(row[0], row[1], returns=1)
        return int(res[0].Zipcode)

    def getData(self):
        return self.data
