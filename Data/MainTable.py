from Data.Apartments.Apartments import *
from Data.Crime.Crimes import Crimes
from Data.Normalizer import Normalizer
from Data.Parks.Parks import Parks
from Data.Noise.Noise import Noise
from Data.PublicTransport.PublicTransport import PublicTransport
from Data.Education.HigherEducation import HigherEducation
from Data.Education.HighSchools import HighSchools
from Data.Health.Health import Health
from Data.ArtGalleries.ArtGalleries import ArtGalleries
from Data.Museums.Museums import Museums
from Data.BuildingAge.BuildingAge import BuildingAge


class MainTable:
    def __init__(self):
        try:
            self.main_db = pd.read_csv("mainDB.csv")
        except FileNotFoundError:
            self._extractAllDatasets()
            self._mergeAllDB()
            Normalizer(self.main_db).normalizeFeatures()
            self.main_db = selectCols(self.main_db, all_filters)
            self.main_db = self.main_db.to_csv(path_or_buf="mainDB.csv", index=False)

    def _extractAllDatasets(self):
        print("Extractnig all Datasets...")
        self.main_db = self._getApartmentsDB()

        self.crimes = self._getCrimesDB()
        self.transport      = self._getTransportDB()
        self.hi_ed          = self._getHigherEducationDB()
        self.high_schools   = self._getHighschoolsDB()
        self.parks = self._getParksDB()
        self.noise          = self._getNoiseDB()
        self.health         = self._getHealthDB()
        self.galleries      = self._getGalleriesDB()
        self.museums = self._getMuseumsDB()
        self.building_age = self._getAgeDB()

    def _mergeAllDB(self):
        print("Merging all Datasets...")
        self.main_db = self.main_db.merge(self.crimes, on='ZIP CODE', how='left')
        self.main_db = self.main_db.merge(self.transport, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.hi_ed, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.high_schools, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.parks, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.noise, on='ZIP CODE', how='left')
        self.main_db = self.main_db.merge(self.health, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.galleries, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.museums, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.building_age, on='ADDRESS', how='left')

        self.main_db = self.main_db.fillna(value=0)
        print("Finished merging")


    # --------------------------------------------------------------------------------- #
    # ------------------------------------ get DBs ------------------------------------ #
    # --------------------------------------------------------------------------------- #

    def getDB(self):
        return self.main_db[self.main_db['SQR_FEET_PRICE'] >= 150]

    def _getApartmentsDB(self):
        print("MainTable: Initializing Apartments...")
        extractor = Apartments.getInstance()
        return extractor.getData()

    def _getCrimesDB(self):
        print("MainTable: Initializing Crimes...")
        extractor = Crimes()
        return extractor.getData()

    def _getTransportDB(self):
        print("MainTable: Initializing Transport...")
        extractor = PublicTransport(1000)
        return extractor.getData()

    def _getParksDB(self):
        print("MainTable: Initializing Parks...")
        extractor = Parks(radius=1, min_area=100)
        return extractor.getData()

    def _getHigherEducationDB(self):
        print("MainTable: Initializing Higher Education...")
        extractor = HigherEducation(1200)
        return extractor.getData()

    def _getHighschoolsDB(self):
        print("MainTable: Initializing High Schools...")
        extractor = HighSchools(1200)
        return extractor.getData()

    def _getNoiseDB(self):
        print("MainTable: Initializing Noise...")
        extractor = Noise()
        return extractor.getData()

    def _getHealthDB(self):
        print("MainTable: Initializing Health...")
        extractor = Health()
        return extractor.getData()

    def _getGalleriesDB(self):
        print("MainTable: Initializing Galleries...")
        extractor = ArtGalleries()
        return extractor.getData()

    def _getMuseumsDB(self):
        print("MainTable: Initializing Museums...")
        extractor = Museums(1)
        return extractor.getData()

    def _getAgeDB(self):
        print("MainTable: Initializing Buildings Age...")
        extractor = BuildingAge()
        return extractor.getData()

if __name__ == '__main__':
    main_table = MainTable()
