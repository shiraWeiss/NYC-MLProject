import overpy
from Data.Apartments.Apartments import *
from Data.ExtractionUtils import *
from overpy.exception import OverpassGatewayTimeout, OverpassTooManyRequests

class PublicTransport:
    def __init__(self, radius):
        try:
            self.data = pd.read_csv(DATASETS_PATH + "/transport_db" + str(self.curr_radius) + ".csv")
        except FileNotFoundError:
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
        if lat == 0 and lon == 0:
            return 0
        query_is = "node(around:" + str(radius) + "," + str(lat) + "," + str(lon) + ")[highway=bus_stop];out;"
        result = self.api.query(query_is)
        return len(result.nodes)



    '''
    @return - number of subway stations around the given address, inside the given radius.
    '''
    def subwayStopsAroundAddress(self, address, radius):
        self.curr_radius = radius
        lat, lon = fromTableAddressToCoordinates(address[0])
        if lat == 0 and lon == 0:
            return 0
        query_is = "node(around:" + str(radius) + "," + str(lat) + "," + str(lon) + ")[station = subway];out;"
        try:
            result = self.api.query(query_is)
            return len(result.nodes)
        except overpy.exception.OverpassTooManyRequests:
            return self.subwayStopsAroundAddress(address, radius)

    '''
    This function takes the addresses from the main table, and runs busStopsAroundAddress
    and subwayStopsAroundAddress on every address. The results are written to a csv file
    with the prefix "transport_db" and then the radius that was set when the csv was created.
    
    This way, there is no need to run the function more than once for a specific radius.  
    '''
    def pushTransportDB(self, radius):
        self.curr_radius = radius
        name = "Data/PublicTransport/transport_db" + str(radius) + ".csv"
        try:
            pd.read_csv(name)
        except FileNotFoundError:
            addresses = Apartments.getInstance().getData()[['ADDRESS', 'ROW']]  # .to_frame()
            addresses['BUS_STOPS'] = None
            addresses['SUBWAY_STOPS'] = None
            i = 0
            max_line = 0
            try:
                for line in addresses.iterrows():
                    line_index = line[0]
                    line_data = line[1]
                    addresses['BUS_STOPS'][line_index] = self.busStopsAroundAddress(line_data['ADDRESS'], radius)
                    addresses['SUBWAY_STOPS'][line_index] = self.subwayStopsAroundAddress(line_data['ADDRESS'], radius)
                    i += 1
                    max_line = max(int(line_data['ROW']), max_line)
                print("Did " + str(i) + "lines with Overpass. Max line from the original csv is line number " + str(
                    max_line))
                addresses.to_csv(path_or_buf=name, index=False)
            except (OverpassGatewayTimeout, OverpassTooManyRequests):
                print("Too many requests :(\nDid " + str(
                    i) + " lines with Overpass. Max line from the original csv is line number " + str(
                    max_line))
                addresses.to_csv(path_or_buf=name, index=False)



    '''
    This function loads a csv into the field 'transport_db' in the class.
    The csv that will be loaded is the one with the current radius, so in order to load
    a specific radius you can change the field "radius" before using this function, and
    get the relevant csv.
    '''
    def loadTransportDB(self):
        self.data = pd.read_csv(DATASETS_PATH + "/transport_db" + str(self.curr_radius) + ".csv")

    def getData(self):
        return self.data
