import overpy
from ExtractionUtils import *
from Apartments.Apartments import Apartments
import pandas as pd

NO_RANK = -200

class HighSchools:
    def __init__(self, radius):
        self.api = overpy.Overpass()
        self.geolocator = Nominatim(user_agent="highschools123", timeout=20)
        self.curr_radius = radius
        self.full_report = pd.read_csv("Education/regents_report.csv").head(100) # todo - removeeeee
        self._removeSchoolsWithNoMeanScore()
        self.merged_report = pd.DataFrame(columns=['School Name', 'Mean Expected Value'])
        self.generateMergedReport()
        self.high_schools_db = pd.DataFrame()
        self.pushHighschoolsDB(radius)
        self.loadHighschoolsDB()

    def _removeSchoolsWithNoMeanScore(self):
        self.full_report = self.full_report.loc[self.full_report['Mean Score'] != 's']

    def generateMergedReport(self):
        name = "C:/Users/lenovo/PycharmProjects/NYC-Data/Education/regents_merged" + str(self.curr_radius) +".csv"
        try:
            self.merged_report = pd.read_csv(name)
        except FileNotFoundError:
            for school in self.full_report['School Name']:
                if school in self.merged_report['School Name'].values:
                    continue

                all_school_registries = self.full_report.loc[self.full_report['School Name'] == school]
                school_tot_mean = getExpectedValue(all_school_registries['Mean Score'],
                                                   all_school_registries['Total Tested'])
                df = pd.DataFrame([(school, school_tot_mean)], columns=['School Name',
                                                                        'Mean Expected Value'])
                self.merged_report = self.merged_report.append(df, ignore_index=True)

            self.merged_report.to_csv(path_or_buf=name, index=False)

    '''
    Straight forward search in Overpass for all the schools in the initial radius around the 
    given address. 

    @return - a 'Result' type (from overpy) with all the nodes found.
    '''
    def allSchoolsAroundAddress(self, address):
        lat, lon = addressToCoordinates(address)
        query_is = "node(around:" + str(self.curr_radius) + "," + str(lat) + "," + str(lon) + ")[amenity=school];out;"
        print(query_is)
        return self.api.query(query_is)

    def getMeanFromTable(self, name):
        row = self.merged_report[self.merged_report['School Name'].str.contains(name, na=False)]
        if not row.empty:
            return row['Mean Expected Value'].iloc[0]
        else:
            return NO_RANK

    def getMeanByNode(self, node):
        rank = NO_RANK

        by_name = self.getMeanFromTable(str(node.tags.get("name")))
        if by_name != NO_RANK:
            rank = by_name

        public = self.findPublic(str(node.tags.get("name")))
        by_public = self.getMeanFromTable(public)
        if by_public != NO_RANK:
            rank = by_public

        if rank == NO_RANK:
            rank = 0

        return rank


    def findPublic(self, in_name):
        for t_name in self.merged_report['School Name']:
            if int(getOnlyNumbers(in_name)) - int(getOnlyNumbers(t_name)) == 0:
                return t_name
        return in_name

    def getBestHighschoolsAroundAddress(self, address):
        best_rank = NO_RANK
        all = self.allSchoolsAroundAddress(address[0])
        for inst in all.nodes:
            curr_name = str(inst.tags.get("name"))
            # print(curr_name + ", " + getAbbreviation(curr_name) + ", Rank: " + str(self.getRankByNode(inst)))
            best_rank = max(self.getMeanByNode(inst), best_rank)
        return best_rank

    def pushHighschoolsDB(self, radius):
        name = "Education/high_schools_db" + str(radius) + ".csv"
        try:
            pd.read_csv(name)
        except FileNotFoundError:
            addresses = Apartments().data['ADDRESS'].to_frame()
            addresses['HIGH_SCHOOLS'] = addresses.apply(self.getBestHighschoolsAroundAddress, axis=1)
            addresses.to_csv(path_or_buf=name, index=False)
            self.curr_radius = radius
        else:
            return


    def loadHighschoolsDB(self):
        name = "C:/Users/lenovo/PycharmProjects/NYC-Data/Education/high_schools_db" + str(self.curr_radius) + ".csv"
        try:
            self.high_schools_db = pd.read_csv(name)
        except FileNotFoundError:
            print("Dor says: No high_schools_db with that radius in here. Run pushHighschoolsDB() first.")

    def getData(self):
        return self.high_schools_db

if __name__ == '__main__':
    hs = HighSchools(5000)
    # print(hs.merged_report)
    print(hs.high_schools_db)