import pandas as pd

from ExtractionUtils import TEST_LINES, removeCols, removeRowsWithEmptyCol


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
        self._removeAptsWithMissingData()
        self.data['ADDRESS'] = self.data.apply(self._getFullAddress, axis=1)
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
        self.data = removeCols(self.data, 'SALE PRICE')
