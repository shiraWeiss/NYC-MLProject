from Data.MainTable import MainTable
from sklearn import neighbors
from sklearn.model_selection import train_test_split, cross_validate, KFold
from Graphs.Graphs import *
from Data.ExtractionUtils import *

def predictionAndScore_plusDisplayGraph(X, y, n, algorithm = 'auto', weights = 'distance'):
    print("KNN: Predicting...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    regressor = neighbors.KNeighborsRegressor(n_neighbors = n, algorithm = algorithm, weights = weights)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    train_score = round(regressor.score(X_train, y_train), 4)       # 4 digits after the decimal point
    test_score = round(regressor.score(X_test, y_test), 4)          # 4 digits after the decimal point
    # generate the graph for the current experiment
    details = 'Algorithm: ' + algorithm + ', Weights: ' + weights
    graph_PredictionVsActual(y_pred, y_test.values, 'Prediction', 'Actual Value',
                             'KNN Regression (with k=' + str(n) +')', train_score, test_score, details)

    return y_pred, test_score, train_score

def predictionAndScore(X, y, n, algorithm = 'auto', weights = 'distance'):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    regressor = neighbors.KNeighborsRegressor(n_neighbors = n)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    train_score = regressor.score(X_train, y_train)
    test_score = regressor.score(X_test, y_test)
    return y_pred, test_score, train_score

def multipleExperimentsFindingBestK(X, y, initial_k, final_k):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    train_scores_dict = {}
    test_scores_dict = {}
    for k in range(int(initial_k), int(final_k)):
        regressor = neighbors.KNeighborsRegressor(n_neighbors = k)
        regressor.fit(X_train, y_train)
        train_score = regressor.score(X_train, y_train)
        test_score = regressor.score(X_test, y_test)
        train_scores_dict[k] = train_score
        test_scores_dict[k] = test_score
    graph_multipleExperiments_compareParameterEffect(train_scores_dict, test_scores_dict, 'KNN', 'K')

def crossValidateWithValidationGroup(X, y, X_train, X_test, y_test, knn_regressor, n):
    kf = KFold(n_splits=n, random_state=None, shuffle=False)
    total = 0
    for train_index, test_index in kf.split(X_train):
        X_train_vgroup = X.iloc[train_index]
        X_test_vgroup = X.iloc[test_index]
        y_train_vgroup = y.iloc[train_index]
        y_test_vgroup = y.iloc[test_index]

        knn_regressor.fit(X_train_vgroup, y_train_vgroup)
        train_score = knn_regressor.score(X_train_vgroup, y_train_vgroup)
        test_score = knn_regressor.score(X_test_vgroup, y_test_vgroup)
        actual_score = knn_regressor.score(X_test, y_test)
        total += actual_score

        print("train_score: " + str(train_score) + ",\ttest_score: " + str(test_score) + ",\tACTUAL: " + str(actual_score))

    return total / n

def findingBestN_crossValidation(X, y, X_train, X_test, y_test, knn_regressor, init_n, final_n):
    mean_score_dict = {}
    for n in range(init_n, final_n, 2):
        print("n: " + str(n) + "...")
        mean_score_dict[n] = crossValidateWithValidationGroup(X, y, X_train, X_test, y_test, knn_regressor, n)
    graph_multipleExperiments_compareParameterEffect_meanScores(mean_score_dict, 'KNN', 'n = number of splits')

def paramTuning(file_name, param_values_list, param_name):
    train_scores_dict = {}
    test_scores_dict = {}
    for p in param_values_list:
        # Get the base table
        all_data = MainTable(extra = file_name + str(p))
        df = all_data.getDB()

        # Split to Data and Actual results
        X = selectCols(df, features)
        y = df['SQR_FEET_PRICE']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        regressor = neighbors.KNeighborsRegressor(n_neighbors=16)
        regressor.fit(X_train, y_train)

        train_score = regressor.score(X_train, y_train)
        test_score = regressor.score(X_test, y_test)

        train_scores_dict[p] = train_score
        test_scores_dict[p] = test_score
    graph_paramTuning(train_scores_dict, test_scores_dict, 'KNN', param_name)

if __name__ == '__main__':
    # # Get the base table
    # all_data = MainTable()
    # df = all_data.getDB()
    #
    # # Split to Data and Actual results
    # X = selectCols(df, features)
    # y = df['SQR_FEET_PRICE']

    paramTuning('_galleries_db', [0.2, 0.5, 1, 2, 3, 4, 5], 'Galleries radius (km)')
    # paramTuning('_museums_db', [0.2, 0.5, 1, 2, 3], 'Museums radius (km)')
    # y_pred, test_score, train_score = predictionAndScore(X, y, 16)

    # Cross validation
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    # knn_regressor = neighbors.KNeighborsRegressor(n_neighbors=16)
    # cv_results = cross_validate(knn_regressor, X_train, y_train, cv=3, return_train_score=True)

    # findingBestN_crossValidation(X, y, X_train, X_test, y_test, knn_regressor, 2, 40)
