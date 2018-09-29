from Data.Apartments.Apartments import *

class Noise:
    def __init__(self):
        self.data = pd.read_csv("Data/Noise/party_in_nyc.csv")
        self.data = self.data.loc[self.data['ZIP CODE'].apply(str) != '83.0']  #  removing weird zipcode error
        self.groupReoccuringComplaints()

    def groupReoccuringComplaints(self):
        # group complaints by similar lon & lat
        group_lonlat = pd.DataFrame(
            {'NOISE': self.getData().groupby(['Latitude', 'Longitude', 'ZIP CODE']).size()}).reset_index()
        # remove locations with only one complaint
        group_lonlat = group_lonlat.loc[group_lonlat['NOISE'].apply(str) != '1']
        # group by zipcode
        self.data = pd.DataFrame({'NOISE': group_lonlat.groupby(['ZIP CODE']).size()}).reset_index()

    def getData(self):
        return self.data

if __name__ == '__main__':
    ns = Noise()
    print('kaki')