from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor

from Data.MainTable import MainTable, removeCols, selectCols, features
from Graphs.Graphs import graph_compareAccuracyOfDifferentParamsValues, graph_paramTuning

TEST_SIZE = 0.2
N_ESTIMATORS = 100

class RandomForest:

    def __init__(self, save):
        self.save = save
        self.data = MainTable().getDB()
        training_set, test_set = train_test_split(self.data, test_size=TEST_SIZE)
        # separate data to apartments features (without prices) and apartments prices
        self.training_features = removeCols(training_set, ['SQR_FEET_PRICE'])
        self.test_features = removeCols(test_set, ['SQR_FEET_PRICE'])
        self.training_prices = selectCols(training_set, ['SQR_FEET_PRICE'])
        self.test_prices = selectCols(test_set, ['SQR_FEET_PRICE'])

        self.all_data_without_prices = removeCols(self.data, ['SQR_FEET_PRICE'])
        self.all_data_only_prices = selectCols(self.data, ['SQR_FEET_PRICE'])

    def createDecisionTreeAccuracyGraph(self, test_name, params_values):
        training_accuracy = []
        test_accuracy = []
        best = -1000
        best_param = 0
        for i in range(len(params_values)):
            training_accuracy.append(self.classifiers[i].score(self.training_features, self.training_prices))
            test_accuracy.append(self.classifiers[i].score(self.test_features, self.test_prices))
            if test_accuracy[i] > best:
                best_param = params_values[i]

        graph_compareAccuracyOfDifferentParamsValues(params_values, training_accuracy, test_accuracy, test_name, self.save)

        return best_param

    '''
    Create the classifier based on the mainDB. This function splits the data to training and test groups,
    and creates the classifier which is based on these groups.
    '''

    def testClassifierWithMinImpuritryDecrease(self, params_values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(RandomForestRegressor(n_estimators=N_ESTIMATORS, min_impurity_decrease=value, random_state=0))

        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        return self.createDecisionTreeAccuracyGraph("Min Impurity Decrease", params_values)

    def testClassifierWithMaxDepth(self, params_values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(RandomForestRegressor(n_estimators=N_ESTIMATORS, max_depth=value, random_state=1))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)
        return self.createDecisionTreeAccuracyGraph("Max Depth", params_values)

    def testMinSamplesLeaf(self, params_values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(RandomForestRegressor(n_estimators=N_ESTIMATORS, min_samples_leaf=value, random_state=1))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        return self.createDecisionTreeAccuracyGraph("Min Samples Leaf", params_values)

    def testClassifierWithMaxLeafNodes(self, values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in values:
            self.classifiers.append(RandomForestRegressor(n_estimators=N_ESTIMATORS, max_leaf_nodes=value, random_state=1))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        return self.createDecisionTreeAccuracyGraph("Max Leaf Nodes", values)

    ''' 
        Comparing prediction vs actual classification. Prints the accuracy of the classifier.
    '''
    def buildWithBestParams(self, max_depth=None, min_impurity_decrease=0, min_samples_leaf=1, max_leaf_nodes=None):
        train_score_sum = 0
        test_score_sum = 0
        for i in range(10):
            clf = RandomForestRegressor(n_estimators=100, max_depth=max_depth, min_impurity_decrease=min_impurity_decrease,
                                    min_samples_leaf=min_samples_leaf, max_leaf_nodes=max_leaf_nodes, random_state=1)
            clf.fit(self.training_features, self.training_prices)
            train_score_sum += clf.score(self.training_features, self.training_prices)
            test_score_sum += clf.score(self.test_features, self.test_prices)

        print("Accuracy for best parameters:\nTrain group: " + str(train_score_sum/10))
        print("Test group: " + str(test_score_sum/10))



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

        tot_train_score    = 0
        tot_test_score     = 0
        n = 5
        for i in range(1,n):
            regressor = RandomForestRegressor(n_estimators=N_ESTIMATORS, min_impurity_decrease=200)
            regressor.fit(X_train, y_train)

            tot_train_score += regressor.score(X_train, y_train)
            tot_test_score += regressor.score(X_test, y_test)

        train_scores_dict[p] = tot_train_score / n
        test_scores_dict[p] = tot_test_score / n
    graph_paramTuning(train_scores_dict, test_scores_dict, 'Tuning ' + param_name + 'with Desicion Trees', param_name)


def parksParamTuning():
    train_scores_dict = {}
    test_scores_dict = {}
    radius_list = [0.5, 1]
    area_list = [100, 200]
    for radius in radius_list:
        for area in area_list:
            file_name = "_parksRadius" + str(radius) + "_area" + str(area)
            all_data = MainTable(extra=file_name)
            df = all_data.getDB()
            # Split to Data and Actual results
            X = selectCols(df, features)
            y = df['SQR_FEET_PRICE']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            tot_train_score = 0
            tot_test_score = 0
            n = 5
            for i in range(0, n):
                regressor = RandomForestRegressor(n_estimators=N_ESTIMATORS, min_impurity_decrease=200)
                regressor.fit(X_train, y_train)

                tot_train_score += regressor.score(X_train, y_train)
                tot_test_score += regressor.score(X_test, y_test)

            train_scores_dict["radius " + str(radius) + "\narea " + str(area)] = tot_train_score / n
            test_scores_dict["radius " + str(radius) + "\narea " + str(area)] = tot_test_score / n
    graph_paramTuning(train_scores_dict, test_scores_dict, 'Tuning parks radius and area with Desicion Trees', 'Parks radius and area')


if __name__ == '__main__':
    tree = RandomForest(save=False)
    best_impurity = tree.testClassifierWithMinImpuritryDecrease([0, 25, 50, 75, 100, 150, 200, 250, 500, 1000, 1500])
    best_depth = tree.testClassifierWithMaxDepth([2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, None])
    best_num_leafs = tree.testClassifierWithMaxLeafNodes([5, 10, 15, 30, 45, 60, 75, 100, 125, 150, None])
    best_min_samples = tree.testMinSamplesLeaf([1, 2, 4, 5, 8, 10, 15, 20, 25, 30, 40, 50])
    tree.buildWithBestParams(max_depth=best_depth, min_samples_leaf=best_min_samples,
                             max_leaf_nodes=best_num_leafs,min_impurity_decrease=best_impurity)

    parksParamTuning()
    paramTuning('_galleries_db', [0.2, 0.5, 1, 2, 3], 'Galleries radius (km) ')
    paramTuning('_museums_db', [0.2, 0.5, 1, 2, 3], 'Museums radius (km) ')
