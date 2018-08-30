import overpy
from Data.Apartments.Apartments import *
from Data.ExtractionUtils import *

class Commercial:
    def __init__(self, radius):
        self.api = overpy.Overpass()
        self.curr_radius = radius
        # self.pushTransportDB(radius)
        # self.loadTransportDB()

    def commercialPresenceAroundAddress(self, address, radius):
        self.curr_radius = radius
        lat, lon = addressToCoordinates(address)
        query_is = "area(around:" + str(radius) + "," + str(lat) + "," + str(lon) + ")[landuse=commercial];out;"
        print(query_is)
        result = self.api.query(query_is)
        return len(result.areas)

if __name__ == '__main__':
    com = Commercial(1000)
    print(com.commercialPresenceAroundAddress('153 AVENUE B,  NYC, Manhattan', 1000))