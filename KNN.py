from Data.MainTable import MainTable
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

all_filters = [  'CRIMES',
                 'HI_ED',
                 'HIGH_SCHOOLS',
                 'BUS_STOPS',
                 'SUBWAY_STOPS',
                 'NUM_OF_PARKS',
                 'AREA_OF_PARKS',
                 'SQR_FEET_PRICE' ]

features =    [  'CRIMES',
                 'HI_ED',
                 'HIGH_SCHOOLS',
                 'BUS_STOPS',
                 'SUBWAY_STOPS',
                 'NUM_OF_PARKS',
                 'AREA_OF_PARKS' ]



if __name__ == '__main__':
    all_data = MainTable()
    df = all_data.getDB()
    df = df[all_filters]

    X = df[features]
    y = df['SQR_FEET_PRICE']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)

    regressor = neighbors.KNeighborsRegressor()
    regressor.fit(X_train, y_train)

    accuracy = regressor.score(X_test, y_test)

    print("KNN accuracy: " + str(accuracy))

