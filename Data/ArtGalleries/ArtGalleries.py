from Data.Apartments.Apartments import *
from geopy.distance import distance
from Data.ExtractionUtils import *

class ArtGalleries:
    def __init__(self):
        self.data = pd.read_csv('Data/ArtGalleries/ART_GALLERY.csv')
        # self.pushHealthDB()
        # self.loadHealthDB()

