import overpy
from ExtractionUtils import *
from Apartments.Apartments import Apartments
import pandas as pd

class HighSchools:
    def __init__(self, radius):
        self.api = overpy.Overpass()
        self.geolocator = Nominatim(user_agent="highschools123", timeout=20)
        self.curr_radius = radius
        self.full_report = pd.read_csv\
            ("C:/Users/lenovo/PycharmProjects/NYC-Data/Education/regents_report.csv").head(100) # todo - removeeeee
        self._removeSchoolsWithNoMeanScore()
        # self.pushHighschoolsEdDB(radius)
        # self.loadHighschoolsEdDB()
        self.merged_report = pd.DataFrame(columns=['School Name', 'Mean Expected Value'])
        self.generateMergedReport()

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


if __name__ == '__main__':
    hs = HighSchools(1000)
    print(hs.merged_report)