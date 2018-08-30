import overpy
from Data.ExtractionUtils import *
from Data.Apartments.Apartments import *
import pandas as pd

NO_RANK = 200

class HigherEducation:
    def __init__(self, radius):
        self.api = overpy.Overpass()
        self.geolocator = Nominatim(user_agent="higher123", timeout=20)
        self.curr_radius = radius
        self.rankings = pd.read_csv("Data/Education/uni-rank-2.csv")
        self.rankings['SHORT'] = self.rankings['UNIVERSITY'].apply(getAbbreviation)
        self.hied_db = pd.DataFrame()
        self.pushHiEdDB(radius)
        self.loadHiEdDB()

    '''
    Straight forward search in Overpass for all the universities and colleges in the initial radius around the 
    given address. 
    
    @return - a 'Result' type (from overpy) with all the nodes found.
    '''
    def allHiEdAroundAddress(self, address):
        lat, lon = addressToCoordinates(address)
        query_is = "(node(around:" + str(self.curr_radius) + "," + str(lat) + "," + str(lon) + ")[amenity=college];" \
                    "node(around:" + str(self.curr_radius) + "," + str(lat) + "," + str(lon) + ")[amenity=university];" \
                                                                                  ");out;"
        return self.api.query(query_is)

    '''
    This function searches for a given name in the UNIVERSITY column in the universities rankings
    and returns the ranking if it's found. The search is using 'contains' and not '==' for better results.
    '''
    def getRankDirectFromTable_byName(self, name):
        row = self.rankings[self.rankings['UNIVERSITY'].str.contains(name, na=False)]
        if not row.empty:
            return row['RANK'].iloc[0]
        else:
            return NO_RANK

    '''
    This function searches for a given abbreviation in the SHORT column in the universities rankings
    and returns the ranking if it's found. The search is using 'contains' and not '==' for better results.
    '''
    def getRankDirectFromTable_byShort(self, name):
        row = self.rankings[self.rankings['SHORT'].str.contains(name, na=False)]
        if not row.empty:
            return row['RANK'].iloc[0]
        else:
            return NO_RANK

    '''
    This is the main "getRank" function. If there is a match by the name recieved from Overpass - great, 
    return its rank. 
    Else, try the 'operator' field in  the node (still data from Overpass). If found, use it.
    If that didn't work - start trying to match using the abbreviation. This is a problematic and not accurate
    match, that will probably cause the feature to be a bit weak. 
    '''
    def getRankByNode(self, node):
        rank = NO_RANK

        full_name = str(node.tags.get("name"))

        # first of all, let's try to get the rank using the full name from the map. maybe we're lucky!
        by_full_name = self.getRankDirectFromTable_byName(full_name)
        if by_full_name != NO_RANK:
            rank = by_full_name

        # but... in most cases we'll get here. now let's try to get the operator from the map and use it.
        if node.tags.get("operator") is not None:
            rank = self.getRankDirectFromTable_byName(str(node.tags.get("operator")))

        short_name = getAbbreviation(full_name)
        # a lot of nodes don't have an operator field. Let's try our Abbreviations table.
        by_short_name = self.getRankDirectFromTable_byShort(short_name)
        if by_short_name != NO_RANK:
            rank = by_short_name

        # handle NYU, SUNY and CUNY
        weak_operator = self.findOperatorManually(short_name)
        by_weak = self.getRankDirectFromTable_byName(weak_operator)
        if by_weak != NO_RANK:
            rank = by_weak

        if rank == NO_RANK:
            rank = 0

        return rank

    '''
    This function uses the 'allHiEd...' function and simply chooses the intitute with the best
    ranking from the list that was found, and returns its rank.
    @return - the best rank found (in curr_radius), or NO_RANK if no match is found.
    '''
    def getBestHiEdAroundAddress(self, address):
        best_rank = NO_RANK
        all_HiEd = self.allHiEdAroundAddress(address[0])
        for inst in all_HiEd.nodes:
            curr_name = str(inst.tags.get("name"))
            # print(curr_name + ", " + getAbbreviation(curr_name) + ", Rank: " + str(self.getRankByNode(inst)))
            best_rank = min(self.getRankByNode(inst), best_rank)
        return best_rank

    '''
    Auxiliary function for matching names after using the Overpass data wasn't successful. Still needs work.
    '''
    def findOperatorManually(self, short_name):
        if short_name[:3] == 'NYU':
            return 'New York University'
        else: # todo : add SUNY and CUNY
            return short_name

    '''
    This function takes the addresses from the main table, and runs getBestHiEdAroundAddress
    on every address. The results are written to a csv file with the prefix "hied_db" 
    and then the radius that was set when the csv was created.

    This way, there is no need to run the function more than once for a specific radius.  
    '''
    def pushHiEdDB(self, radius):
        name = "Data/Education/hied_db" + str(radius) + ".csv"
        try:
            pd.read_csv(name)
        except FileNotFoundError:
            addresses = Apartments.getInstance().data['ADDRESS'].to_frame()
            addresses['HI_ED'] = addresses.apply(self.getBestHiEdAroundAddress, axis=1)
            addresses.to_csv(path_or_buf=name, index=False)
            self.curr_radius = radius

    '''
    This function loads a csv into the field 'hied_db' in the class.
    The csv that will be loaded is the one with the current radius, so in order to load
    a specific radius you can change the field "radius" before using this function, and
    get the relevant csv.
    '''
    def loadHiEdDB(self):
        name = "Data/Education/hied_db" + str(self.curr_radius) + ".csv"
        try:
            self.hied_db = pd.read_csv(name)
        except FileNotFoundError:
            print("Dor says: No hied_db with that radius in here. Run pushHiEdDB() first.")

    def getData(self):
        return self.hied_db


if __name__ == '__main__':
    hi_ed = HigherEducation(1200)
    hi_ed.curr_radius = 1500
    print(hi_ed.hied_db)
