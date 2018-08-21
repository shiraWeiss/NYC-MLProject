from Apartments.Apartments import Apartments
from Crime.Crimes import Crimes
from Parks.Parks import Parks
from PublicTransport.PublicTransport import PublicTransport
from Education.HigherEducation import HigherEducation
from Education.HighSchools import HighSchools


class MainTable:
    def __init__(self):
        self.main_db = self._getAptsDB()
        self.crimes = self._getCrimesDB()
        self.transport = self._getTransportDB()
        self.hi_ed = self._getHigherEducationDB()
        self.high_schools = self._getHighschoolsDB()
        # other data bases... and than:

    def getDB(self):
        return self.main_db

    def mergeAllDB(self):
        #  merge the crimes table
        self.main_db = self.main_db.merge(self.crimes, on='ZIP CODE', how='left')
        self.main_db = self.main_db.merge(self.transport, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.hi_ed, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.high_schools, on='ADDRESS', how='left')

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


if __name__ == "__main__":
    creator = MainTable()
    creator.mergeAllDB()
    print(creator.getDB())
