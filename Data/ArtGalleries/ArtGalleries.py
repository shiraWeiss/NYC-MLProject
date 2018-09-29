from Data.Apartments.Apartments import *
from geopy.distance import geodesic
from Data.ExtractionUtils import *

class ArtGalleries:
    def __init__(self, radius):
        print("init Galleries with radius" + str(radius))
        self.loadGalleriesDB(radius)

    '''
    Load the galleries DB from csv, or create it if necessary
    '''
    def loadGalleriesDB(self, radius):
        try:
            self.data = pd.read_csv(DATASETS_PATH + "/galleries_db" + str(radius) + ".csv")
        except FileNotFoundError:
            self.pushGalleriesDB(radius)

    '''
    Create the galleries DB and save it to CSV
    '''
    def pushGalleriesDB(self, radius):
        self.galleries = self._extractGalleriesData()
        self.data = pd.read_csv("Data/Datasets/nyc-rolling-sales-coord.csv") # .head(TEST_LINES) # todo use the Apartments instead
        self.data['GALLERIES'] = self.data.apply(self._countGalleriesInRadius, args=(radius,), axis=1)
        self.data.to_csv(path_or_buf= DATASETS_PATH + "/galleries_db" + str(radius) + ".csv", index=False)


    def _extractGalleriesData(self):
        galleries = pd.read_csv("Data/ArtGalleries/ART_GALLERY.csv")
        galleries = galleries # .head(TEST_LINES)  # todo remove!! short only for testing
        galleries = self._getGalleriesCoords(galleries)
        return galleries



    def _getGalleriesCoords(self, galleries):
        galleries = galleries['the_geom']
        # get from 'the_geom' only the coordinate
        galleries = galleries.apply(lambda geom: re.match(r"POINT \((.* .*)\)", geom).group(1))
        # the coordinates are in flipped order, so flip them back
        galleries = galleries.apply(lambda coord: coord.split(' ')[::-1])
        galleries = galleries.apply(pd.Series)
        galleries.columns = ['LAT', 'LON']
        return galleries

    def _countGalleriesInRadius(self, apartment_location, radius):
        counter = 0
        for galleries_row in self.galleries.iterrows():
            gallery_coord = galleries_row[1]['LAT'], galleries_row[1]['LON']
            apartment_coord = apartment_location['LAT'], apartment_location['LON']
            if apartment_coord == (0, 0): return 0      #   not to insert noise to the table
            dist = geodesic(apartment_coord, gallery_coord).kilometers
            if dist <= radius:
                counter += 1
        return counter


    def getData(self):
        return self.data


if __name__ == '__main__':
    glr = ArtGalleries()
    print(glr.getData())
