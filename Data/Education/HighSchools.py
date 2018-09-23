import overpy
from Data.Apartments.Apartments import *
import pandas as pd

NO_RANK = -200

class HighSchools:
    def __init__(self, radius):
        self.curr_radius = radius
        try:
            self.high_schools_db = pd.read_csv(DATASETS_PATH + "/high_schools_db" + str(self.curr_radius) + ".csv")
            self.high_schools_db = removeCols(self.high_schools_db, ['ROW']).drop_duplicates(subset='ADDRESS', keep='first')
        except FileNotFoundError:
            self.api = overpy.Overpass()
            self.curr_radius = radius
            self.full_report = pd.read_csv("Data/Education/regents_report.csv")
            self._removeSchoolsWithNoMeanScore()
            self.merged_report = pd.DataFrame(columns=['School Name', 'Mean Expected Value'])
            self.generateMergedReport()
            self.high_schools_db = pd.DataFrame()
            self.pushHighschoolsDB(radius)
            self.loadHighschoolsDB()

    def _removeSchoolsWithNoMeanScore(self):
        self.full_report = self.full_report.loc[self.full_report['Mean Score'] != 's']

    def generateMergedReport(self):
        name = DATASETS_PATH + "/regents_merged" + str(self.curr_radius) +".csv"
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
        lat, lon = fromTableAddressToCoordinates(address)
        if lat == 0 and lon == 0:
            return 0
        query_is = "node(around:" + str(self.curr_radius) + "," + str(lat) + "," + str(lon) + ")[amenity=school];out;"
        return self.api.query(query_is)

    def getMeanFromTable(self, name):
        row = self.merged_report[self.merged_report['School Name'].str.contains(name, na=False)]
        if not row.empty:
            return row['Mean Expected Value'].iloc[0]
        else:
            return NO_RANK

    def getMeanByNode(self, node):
        rank = NO_RANK
        name = str(node.tags.get("name"))

        by_name = self.getMeanFromTable(name)
        if by_name != NO_RANK:
            rank = by_name

        public = self.findPublic(name)
        by_public = self.getMeanFromTable(public)
        if by_public != NO_RANK:
            rank = by_public

        if rank == NO_RANK:
            closest_school = self.schoolByMatch(name, 90)
            if closest_school is not None:
                by_closest = self.getMeanFromTable(closest_school)
                if by_closest != NO_RANK:
                    rank = by_closest

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
            best_rank = max(self.getMeanByNode(inst), best_rank)
        return best_rank

    def pushHighschoolsDB(self, radius):
        name = "Data/Education/high_schools_db" + str(radius) + ".csv"
        try:
            pd.read_csv(name)
        except FileNotFoundError:
            addresses = Apartments.getInstance().data['ADDRESS'].to_frame()
            addresses['HIGH_SCHOOLS'] = addresses.apply(self.getBestHighschoolsAroundAddress, axis=1)
            addresses.to_csv(path_or_buf=name, index=False)
            self.curr_radius = radius


    def loadHighschoolsDB(self):
        name = DATASETS_PATH + "/high_schools_db" + str(self.curr_radius) + ".csv"
        try:
            self.high_schools_db = pd.read_csv(name)
            self.high_schools_db = removeCols(self.high_schools_db, ['ROW']).drop_duplicates(subset='ADDRESS', keep='first')
        except FileNotFoundError:
            print("Dor says: No high_schools_db with that radius in here. Run pushHighschoolsDB() first.")

    def getData(self):
        return self.high_schools_db

    def schoolByMatch(self, in_school, match_percent):
        max_match = 0
        max_school = str()
        for t_school in self.merged_report['School Name']:
            curr_match = substringMatchPercentage(t_school, in_school)
            if curr_match > max_match:
                max_match = curr_match
                max_school = t_school

        if max_match > match_percent:
            return max_school
        else:
            return None