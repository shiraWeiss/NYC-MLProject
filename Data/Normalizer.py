HI_ED_FACTOR = 152

class Normalizer:
    def __init__(self, main_db):
        self.main_db = main_db

    def normalizeFeatures(self):

        print("MainTable: Normalizing...")
        self.main_db['HI_ED']           = self.main_db['HI_ED'].apply(self._normHiEd)
        self.main_db['HIGH_SCHOOLS'] = self._normalizeByMaxValue('HIGH_SCHOOLS')
        self.main_db['BUS_STOPS']       = self._normalizeByMaxValue('BUS_STOPS')
        self.main_db['SUBWAY_STOPS']    = self._normalizeByMaxValue('SUBWAY_STOPS')
        self.main_db['CRIMES'] = self._normalizeByMaxValue('CRIMES')
        self.main_db['NUM_OF_PARKS'] = self._normalizeByMaxValue('NUM_OF_PARKS')
        self.main_db['AREA_OF_PARKS'] = self._normalizeByMaxValue('AREA_OF_PARKS')
        self.main_db['NOISE']           = self._inverseNormalizeByMaxValue('NOISE')
        self.main_db['HEALTH']          = self._inverseNormalizeByMaxValue('HEALTH')
        self.main_db['GALLERIES']       = self._normalizeByMaxValue('GALLERIES')
        self.main_db['MUSEUMS'] = self._normalizeByMaxValue('MUSEUMS')
        self.main_db['BUILDING_AGE'] = self._inverseNormalizeByMaxValue('BUILDING_AGE')
        self.main_db['BOROUGH'] = self._inverseNormalizeByMaxValue('BOROUGH')

        self.main_db.fillna(0, inplace=True)

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
