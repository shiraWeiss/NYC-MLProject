# need to use: conda install scikit-learn
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from Data.ExtractionUtils import removeCols, selectCols
from Data.MainTable import MainTable
from Graphs.Graphs import graph_compareAccuracyOfDifferentParamsValues

TEST_SIZE = 0.25
CLASSIFIER = 0
DATA = 1
PRICE_LEVEL_SIZE = 1000

class DecisionTree:
    def __init__(self):
        self.data = MainTable().getDB()
        training_set, test_set = train_test_split(self.data, test_size=TEST_SIZE)
        # separate data to apartments features (without prices) and apartments prices
        self.training_features = removeCols(training_set, ['SQR_FEET_PRICE'])
        self.test_features = removeCols(test_set, ['SQR_FEET_PRICE'])
        self.training_prices = selectCols(training_set, ['SQR_FEET_PRICE'])
        self.test_prices = selectCols(test_set, ['SQR_FEET_PRICE'])

    '''
    Create the classifier based on the mainDB. This function splits the data to training and test groups,
    and creates the classifier which is based on these groups.
    '''
    def testClassifierWithMinImputiryDecrease(self, params_values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(DecisionTreeRegressor(min_impurity_decrease=value, random_state=0))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)


        self.createDecisionTreeAccuracyGraph("Min Impurity Decrease", params_values)


    def testClassifierWithMaxDepth(self, params_values):
        # create classifiers with different parameters according to the test input
        for value in params_values:
            self.classifiers.append(DecisionTreeRegressor(max_depth=value, random_state=0))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)
        self.createDecisionTreeAccuracyGraph("Max Depth", params_values)


    def testlLogisticRegression(self, values):
        classifier = LogisticRegression(random_state=0)
        classifier.fit(self.training_features, self.training_prices)
        self.createDecisionTreeAccuracyGraph("forest", values)



    def testClassifierWithMaxLeafNodes(self, values):
        self.classifiers = []
        # create classifiers with different parameters according to the test input
        for value in values:
            self.classifiers.append(DecisionTreeRegressor(max_depth=value, random_state=0))
        # fit the classifiers
        for i in range(len(self.classifiers)):
            self.classifiers[i] = self.classifiers[i].fit(self.training_features, self.training_prices)

        self.createDecisionTreeAccuracyGraph("Max Leaf Nodes", values)

        ''' 
            Comparing prediction vs actual classification. Prints the accuracy of the classifier.
            '''

    def createDecisionTreeAccuracyGraph(self, test_name, params_values):
        # print("Accuracy for " + test_name + ":")
        # for i in range(len(params_values)):
        #     training_accuracy = self.classifiers[i].score(self.training_features, self.training_prices)
        #     test_accuracy = self.classifiers[i].score(self.test_features, self.test_prices)
        #     print("For value " + str(params_values[i]) + ": training accuracy=" + str(training_accuracy) + ", test acc=" + str(test_accuracy))
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        training_accuracy = []
        test_accuracy = []
        for i in range(len(params_values)):
            training_accuracy.append(self.classifiers[i].score(self.training_features, self.training_prices))
            test_accuracy.append(self.classifiers[i].score(self.test_features, self.test_prices))

        graph_compareAccuracyOfDifferentParamsValues(params_values, training_accuracy, test_accuracy, test_name)

if __name__ == '__main__':

    tree = DecisionTree()
    tree.testClassifierWithMinImputiryDecrease([0, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55])
    tree.testClassifierWithMaxDepth([None, 4, 5, 6, 10, 15, 20, 50 , 100, 500])
    tree.testClassifierWithMaxLeafNodes([None, 5, 10, 25, 50, 75, 100, 500, 1000])

    # tree.testlLogi    sticRegression([None])