import pandas as pd

from ExtractionUtils import TEST_LINES


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


class Apartments:
    def __init__(self):
        self._createBaseDB()

    def getAptsData(self):
        return self.data

    def _createBaseDB(self):
        self.data = pd.read_csv("Datasets/nyc-rolling-sales.csv")
        self.data = self.data.head(TEST_LINES)  # todo - remove! short for testing
        self._removeAptsWithNoArea()
        self.data['ADDRESS'] = self.data.apply(self._addBoroughToAddress, axis=1)

    def _removeAptsWithNoArea(self):
        self.data = self.data.loc[self.data['LAND SQUARE FEET'] != ' -  '].loc[self.data['LAND SQUARE FEET'] != '0']

    def _addBoroughToAddress(self, row):
        new_address = row['ADDRESS']  + ', NYC' + ', ' + toBorough(row['BOROUGH'])
        return new_address
        
    
