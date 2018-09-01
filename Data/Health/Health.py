from Data.Apartments.Apartments import *
from geopy.distance import distance
from Data.ExtractionUtils import *

class Health:
    def __init__(self):
        self.data = pd.read_csv('Data/Health/Health_Facility_General_Information.csv')
        self.data = removeRowsWithEmptyCol(self.data, 'Facility Latitude')
        self.data = removeRowsWithEmptyCol(self.data, 'Facility Longitude')
        self.pushHealthDB()
        self.loadHealthDB()

    def getData(self):
        return self.data

    def closestHealthToAddress(self, address):
        in_coords = fromTableAddressToCoordinates(address[0])  # change to 'in_coords = addressToCoordinates(address[0])' after loacl testing
        if in_coords == (0, 0):
            return 0
        min_dist = 10000
        for curr_lat, curr_lon in zip(self.data['Facility Latitude'], self.data['Facility Longitude']):
            curr_coord = (curr_lat, curr_lon)
            curr_dist = distance(curr_coord, in_coords)
            min_dist = min(min_dist, curr_dist)
        return str(min_dist)[:-2]  #  removing the 'km' letters added in the end of the distance

    def pushHealthDB(self):
        name = "Data/Health/health_db.csv"
        try:
            pd.read_csv(name)
        except FileNotFoundError:
            addresses = Apartments.getInstance().data['ADDRESS'].to_frame()
            addresses['HEALTH'] = addresses.apply(self.closestHealthToAddress, axis=1)
            addresses.to_csv(path_or_buf=name, index=False)

    def loadHealthDB(self):
        name = "Data/Health/health_db.csv"
        try:
            self.data = pd.read_csv(name)
        except FileNotFoundError:
            print("Dor says: No transport_db with that radius in here. Run pushHealthDB() first.")


if __name__ == '__main__':
    h = Health()
    print(h.closestHealthToAddress('153 AVENUE B, NYC, Manhattan'))