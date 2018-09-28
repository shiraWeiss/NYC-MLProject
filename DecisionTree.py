# need to use: conda install scikit-learn
import numpy
import pandas as pd
from numpy import linspace
from numpy.ma import arange

from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from Data.ExtractionUtils import removeCols, selectCols
from Data.MainTable import MainTable
from Graphs.Graphs import graph_compareAccuracyOfDifferentParamsValues

TEST_SIZE = 0.2


class DecisionTree:

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
            self.classifiers.append(DecisionTreeRegressor(min_impurity_decrease=value, random_state=0))

        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        return self.createDecisionTreeAccuracyGraph("Min Impurity Decrease", params_values)

    def testClassifierWithMaxDepth(self, params_values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(DecisionTreeRegressor(max_depth=value, random_state=1))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)
        return self.createDecisionTreeAccuracyGraph("Max Depth", params_values)

    def testMinSamplesLeaf(self, params_values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(DecisionTreeRegressor(min_samples_leaf=value, random_state=1))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        return self.createDecisionTreeAccuracyGraph("Min Samples Leaf", params_values)

    def testClassifierWithMaxLeafNodes(self, values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in values:
            self.classifiers.append(DecisionTreeRegressor(max_leaf_nodes=value, random_state=1))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        return self.createDecisionTreeAccuracyGraph("Max Leaf Nodes", values)

    ''' 
        Comparing prediction vs actual classification. Prints the accuracy of the classifier.
    '''
    def buildWithBestParams(self, max_depth=None, min_impurity_decrease=0, min_samples_leaf=1, max_leaf_nodes=None):
        clf = DecisionTreeRegressor(max_depth=max_depth, min_impurity_decrease=min_impurity_decrease,
                                    min_samples_leaf=min_samples_leaf, max_leaf_nodes=max_leaf_nodes, random_state=1)

        clf.fit(self.training_features, self.training_prices)
        print("Accuracy for best parameters:\nTrain group: " + str(clf.score(self.training_features, self.training_prices)))
        print("Test group: " + str(clf.score(self.test_features, self.test_prices)))


if __name__ == '__main__':
    tree = DecisionTree(save=False)
    best_impurity = tree.testClassifierWithMinImpuritryDecrease([0, 25, 50, 75, 100, 150, 200, 250, 500, 1000, 1500])
    best_depth = tree.testClassifierWithMaxDepth([2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, None])
    best_num_leafs = tree.testClassifierWithMaxLeafNodes([5, 10, 15, 30, 45, 60, 75, 100, 125, 150, None])
    best_min_samples = tree.testMinSamplesLeaf([1, 2, 4, 5, 8, 10, 15, 20, 25, 30, 40, 50])
    tree.buildWithBestParams(max_depth=best_depth, min_samples_leaf=best_min_samples,
                             max_leaf_nodes=best_num_leafs,min_impurity_decrease=best_impurity)


