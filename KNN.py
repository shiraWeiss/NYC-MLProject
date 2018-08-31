from Data.MainTable import MainTable
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from Graphs.Graphs import *

all_filters = [  'CRIMES',
                 'HI_ED',
                 'HIGH_SCHOOLS',
                 'BUS_STOPS',
                 'SUBWAY_STOPS',
                 'NUM_OF_PARKS',
                 'AREA_OF_PARKS',
                 'SQR_FEET_PRICE',
                 'NOISE',
                 'HEALTH' ]

features =    [  'CRIMES',
                 'HI_ED',
                 'HIGH_SCHOOLS',
                 'BUS_STOPS',
                 'SUBWAY_STOPS',
                 'NUM_OF_PARKS',
                 'AREA_OF_PARKS',
                 'NOISE',
                 'HEALTH' ]

def getKNNPredictionAndScore_andDisplay(X, y, n, algorithm, weights):
    print("KNN: Predicting...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42,
                                                        algorithm = algorithm, weights = weights)
    regressor = neighbors.KNeighborsRegressor(n_neighbors = n)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    train_score = regressor.score(X_train, y_train)
    test_score = regressor.score(X_test, y_test)
    # generate the graph for the current experiment
    details = 'Algorithm: ' + algorithm + ', Weights: ' + weights
    graph_PredictionVsActual(y_pred, y_test.values, 'Prediction', 'Actual Value',
                             'KNN Regression (with k=' + str(n) +')', train_score, test_score, details)

    return y_pred, test_score, train_score

def getKNNPredictionAndScore(X, y, n, algorithm, weights):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42,
                                                        algorithm = algorithm, weights = weights)
    regressor = neighbors.KNeighborsRegressor(n_neighbors = n)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    train_score = regressor.score(X_train, y_train)
    test_score = regressor.score(X_test, y_test)
    return y_pred, test_score, train_score


if __name__ == '__main__':
    # Get the base table
    all_data = MainTable()
    df = all_data.getDB()
    df = df[all_filters]

    # Split to Data and Actual results
    X = df[features]
    y = df['SQR_FEET_PRICE']

    # Get predictions and display them
    getKNNPredictionAndScore_andDisplay(X, y, 5, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 5, 'auto', 'distance')
    getKNNPredictionAndScore_andDisplay(X, y, 7, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 7, 'auto', 'distance')
    getKNNPredictionAndScore_andDisplay(X, y, 10, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 10, 'auto', 'distance')
    getKNNPredictionAndScore_andDisplay(X, y, 15, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 15, 'auto', 'distance')
    getKNNPredictionAndScore_andDisplay(X, y, 30, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 30, 'auto', 'distance')
    getKNNPredictionAndScore_andDisplay(X, y, 65, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 65, 'auto', 'distance')
    getKNNPredictionAndScore_andDisplay(X, y, 100, 'auto', 'uniform')
    getKNNPredictionAndScore_andDisplay(X, y, 100, 'auto', 'distance')
