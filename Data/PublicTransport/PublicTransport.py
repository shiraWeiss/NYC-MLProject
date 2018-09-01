import overpy
from Data.Apartments.Apartments import *
from Data.ExtractionUtils import *

class PublicTransport:
    def __init__(self, radius):
        self.api = overpy.Overpass()
        self.curr_radius = radius
        self.pushTransportDB(radius)
        self.loadTransportDB()

    '''
    @return - number of bus stations around the given address, inside the given radius.
    '''
    def busStopsAroundAddress(self, address, radius):
        self.curr_radius = radius
        lat, lon = fromTableAddressToCoordinates(address[0])
        query_is = "node(around:" + str(radius) + "," + str(lat) + "," + str(lon) + ")[highway=bus_stop];out;"
        result = self.api.query(query_is)
        return len(result.nodes)

    '''
    @return - number of subway stations around the given address, inside the given radius.
    '''
    def subwayStopsAroundAddress(self, address, radius):
        self.curr_radius = radius
        lat, lon = fromTableAddressToCoordinates(address[0])
        query_is = "node(around:" + str(radius) + "," + str(lat) + "," + str(lon) + ")[station = subway];out;"
        result = self.api.query(query_is)
        return len(result.nodes)

    '''
    This function takes the addresses from the main table, and runs busStopsAroundAddress
    and subwayStopsAroundAddress on every address. The results are written to a csv file
    with the prefix "transport_db" and then the radius that was set when the csv was created.
    
    This way, there is no need to run the function more than once for a specific radius.  
    '''
    def pushTransportDB(self, radius):
        name = "Data/PublicTransport/transport_db" + str(radius) + ".csv"
        try:
            pd.read_csv(name)
        except FileNotFoundError:
            addresses = Apartments.getInstance().data['ADDRESS'].to_frame()
            addresses['BUS_STOPS'] = addresses.apply(self.busStopsAroundAddress, args=(radius,), axis=1)
            addresses['SUBWAY_STOPS'] = addresses.apply(self.subwayStopsAroundAddress, args=(radius,), axis=1)
            addresses.to_csv(path_or_buf=name, index=False)
            self.curr_radius = radius

    '''
    This function loads a csv into the field 'transport_db' in the class.
    The csv that will be loaded is the one with the current radius, so in order to load
    a specific radius you can change the field "radius" before using this function, and
    get the relevant csv.
    '''
    def loadTransportDB(self):
        name = "Data/PublicTransport/transport_db" + str(self.curr_radius) + ".csv"
        try:
            self.data = pd.read_csv(name)
        except FileNotFoundError:
            print("Dor says: No transport_db with that radius in here. Run pushTransportDB() first.")

    def getData(self):
        return self.data


if __name__ == "__main__":
    pt = PublicTransport()
    pt.pushTransportDB(1000)
    # pt.curr_radius = 500
    pt.loadTransportDB()
