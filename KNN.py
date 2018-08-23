from Data.MainTable import MainTable
import sklearn

field_filters = ['CRIMES',
                 'HI_ED',
                 'HIGH_SCHOOLS',
                 'BUS_STOPS',
                 'SUBWAY_STOPS',
                 'NUM_OF_PARKS',
                 'AREA_OF_PARKS' ]

if __name__ == '__main__':
    all_data = MainTable()
    df = all_data.getDB()
    df = df.loc[field_filters]
    print("hola mochacho")

