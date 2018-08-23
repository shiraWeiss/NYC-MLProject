from Apartments.Apartments import Apartments
from Crime.Crimes import Crimes
from Parks.Parks import Parks
from PublicTransport.PublicTransport import PublicTransport
from Education.HigherEducation import HigherEducation
from Education.HighSchools import HighSchools

HI_ED_FACTOR = 152
HIGH_SCHOOLS_FACTOR = 100
BUS_FACTOR = 100     #  bus & subway factors are *really* subject to change
SUBWAY_FACTOR = 20  #  bus & subway factors are *really* subject to change

class MainTable:
    def __init__(self):
        self.main_db = self._getAptsDB()
        self.crimes = self._getCrimesDB()
        self.transport = self._getTransportDB()
        self.hi_ed = self._getHigherEducationDB()
        self.high_schools = self._getHighschoolsDB()
        self.parks = self._getParksDB()

        self.mergeAllDB()
        self._normalizeFeatures()

    def getDB(self):
        return self.main_db

    def mergeAllDB(self):
        #  merge the crimes table
        self.main_db = self.main_db.merge(self.crimes, on='ZIP CODE', how='left').fillna(value=0)
        self.main_db = self.main_db.merge(self.transport, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.hi_ed, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.high_schools, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.parks, on='ADDRESS', how='left').fillna(value=0)

    def _getAptsDB(self):
        extractor = Apartments()
        return extractor.getAptsData()

    def _getCrimesDB(self):
        extractor = Crimes()
        return extractor.getData()

    def _getTransportDB(self):
        extractor = PublicTransport(1000)
        return extractor.getData()

    def _getParksDB(self):
        extractor = Parks(radius=1, min_area=100)
        return extractor.getData()

    def _getHigherEducationDB(self):
        extractor = HigherEducation(1200)
        return extractor.getData()

    def _getHighschoolsDB(self):
        extractor = HighSchools(1200)
        return extractor.getData()

    def _normalizeFeatures(self):
        self.main_db['HI_ED'] = self.main_db['HI_ED'].apply(self._normHiEd)
        self.main_db['HIGH_SCHOOLS'] = self._normalizeByMaxValue('HIGH_SCHOOLS')
        self.main_db['BUS_STOPS'] = self.main_db['BUS_STOPS'].apply(self._standardNormalize, args=(BUS_FACTOR,))
        self.main_db['SUBWAY_STOPS'] = self.main_db['SUBWAY_STOPS'].apply(self._standardNormalize, args=(BUS_FACTOR,))
        self.main_db['CRIMES'] = self._normalizeByMaxValue('CRIMES')
        self.main_db['NUM_OF_PARKS'] = self._normalizeByMaxValue('NUM_OF_PARKS')
        self.main_db['AREA_OF_PARKS'] = self._normalizeByMaxValue('AREA_OF_PARKS')

    def _normalizeByMaxValue(self, col):
        return self.main_db[col].apply(self._standardNormalize, args=(self.main_db[col].max(),))

    def _normHiEd(self, score):
        return (HI_ED_FACTOR - float(score)) / HI_ED_FACTOR

    def _standardNormalize(self, score, factor):
        if factor == 0:
            return 0
        return float(score) / float(factor)

    # TODO : normalize Crime, Parks (after it's added to the main_db)

if __name__ == "__main__":
    creator = MainTable()
    print(creator.getDB())
