from Data.Apartments.Apartments import *

class BuildingAge:
    def __init__(self):
        self.apts = Apartments.getInstance()
        self.addAgeToApts()

    def calcAgeOfApartment(self, apt_row_from_table):
        year_built = apt_row_from_table[1]
        return 2017 - year_built

    def addAgeToApts(self):
        addresses = self.apts.getData()[['ADDRESS', 'YEAR BUILT']]
        addresses['BUILDING_AGE'] = addresses.apply(self.calcAgeOfApartment, axis=1)
        self.data = addresses.drop_duplicates(subset='ADDRESS', keep='first')

    def getData(self):
        return self.data

