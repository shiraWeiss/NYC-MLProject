from Data.Apartments.Apartments import *
from Data.Crime.Crimes import Crimes
from Data.Parks.Parks import Parks
from Data.Noise.Noise import Noise
from Data.PublicTransport.PublicTransport import PublicTransport
from Data.Education.HigherEducation import HigherEducation
from Data.Education.HighSchools import HighSchools
from Data.Health.Health import Health
from Data.ArtGalleries.ArtGalleries import ArtGalleries
from Data.Museums.Museums import Museums
from Data.BuildingAge.BuildingAge import BuildingAge

HI_ED_FACTOR = 152
HIGH_SCHOOLS_FACTOR = 100
BUS_FACTOR = 100     #  bus & subway factors are *really* subject to change
SUBWAY_FACTOR = 20  #  bus & subway factors are *really* subject to change

class MainTable:
    def __init__(self):
        self.main_db        = self._getAptsDB()
        self.crimes         = self._getCrimesDB()
        self.transport      = self._getTransportDB()
        self.hi_ed          = self._getHigherEducationDB()
        self.high_schools   = self._getHighschoolsDB()
        # self.parks          = self._getParksDB()
        self.noise          = self._getNoiseDB()
        self.health         = self._getHealthDB()
        self.galleries      = self._getGalleriesDB()
        self.museums        = self._getMuseumsDB()
        self.building_age   = self._getAgeDB()

        self.mergeAllDB()
        self._normalizeFeatures()
        self.main_csv = self.main_db.to_csv(path_or_buf="mainDB.csv", index=False)

    def getDB(self):
        return self.main_db

    def mergeAllDB(self):
        self.main_db = self.main_db.merge(self.crimes, on='ZIP CODE', how='left').fillna(value=0)
        self.main_db = self.main_db.merge(self.transport, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.hi_ed, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.high_schools, on='ADDRESS', how='left')
        # self.main_db = self.main_db.merge(self.parks, on='ADDRESS', how='left').fillna(value=0)
        self.main_db = self.main_db.merge(self.noise, on='ZIP CODE', how='left').fillna(value=0)
        self.main_db = self.main_db.merge(self.health, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.galleries, on='ADDRESS', how='left')
        self.main_db = self.main_db.merge(self.building_age, on='ADDRESS', how='left')

    def _normalizeFeatures(self):
        print("MainTable: Normalizing...")
        self.main_db['HI_ED']           = self.main_db['HI_ED'].apply(self._normHiEd)
        self.main_db['HIGH_SCHOOLS']    = self._normalizeByMaxValue('HIGH_SCHOOLS')
        self.main_db['BUS_STOPS']       = self._normalizeByMaxValue('BUS_STOPS')
        self.main_db['SUBWAY_STOPS']    = self._normalizeByMaxValue('SUBWAY_STOPS')
        self.main_db['CRIMES']          = self._normalizeByMaxValue('CRIMES')
        # self.main_db['NUM_OF_PARKS']  = self._normalizeByMaxValue('NUM_OF_PARKS')
        # self.main_db['AREA_OF_PARKS'] = self._normalizeByMaxValue('AREA_OF_PARKS')
        self.main_db['NOISE']           = self._inverseNormalizeByMaxValue('NOISE')
        self.main_db['HEALTH']          = self._inverseNormalizeByMaxValue('HEALTH')
        self.main_db['GALLERIES']       = self._normalizeByMaxValue('GALLERIES')
        self.main_db['MUSEUMS']         = self._normalizeByMaxValue('MUSEUMS')
        self.main_db['BUILDING_AGE']    = self._inverseNormalizeByMaxValue('BUILDING_AGE')

    # --------------------------------------------------------------------------------- #
    # ------------------------------------ get DBs ------------------------------------ #
    # --------------------------------------------------------------------------------- #

    def _getAptsDB(self):
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
        extractor = Museums()
        return extractor.getData()

    def _getAgeDB(self):
        print("MainTable: Initializing Buildings Age...")
        extractor = BuildingAge()
        return extractor.getData()

    # --------------------------------------------------------------------------------- #
    # ----------------------- Noramlizing functions ----------------------------------- #
    # --------------------------------------------------------------------------------- #

    def _normHiEd(self, score):
        return (HI_ED_FACTOR - float(score)) / HI_ED_FACTOR

    def _normalizeByMaxValue(self, col):
        return self.main_db[col].apply(self._standardNormalize, args=(self.main_db[col].max(),))

    def _standardNormalize(self, score, factor):
        if factor == 0:
            return 0
        return float(score) / float(factor)

    def _inverseNormalizeByMaxValue(self, col):
        return self.main_db[col].apply(self._inverseNormalize, args=(self.main_db[col].max(),))

    def _inverseNormalize(self, score, factor):
        if factor == 0:
            return 1
        return 1 - (float(score) / float(factor))
