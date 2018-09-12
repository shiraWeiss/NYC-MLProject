# need to use: conda install scikit-learn
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor
from Data.ExtractionUtils import removeCols
from Data.MainTable import MainTable

TEST_SIZE = 0.25
CLASSIFIER = 0
DATA = 1
PRICE_LEVEL_SIZE = 1000

class DecisionTree:
    def __init__(self):
        self.data = MainTable().getDB()
        self.data = removeCols(self.data, 'ADDRESS')    # not a numeric feature - not relevant
        self._getDecisionTreeAccuracy()

    def _getDecisionTreeAccuracy(self):
        clf = DecisionTreeRegressor()
        training_set, test_set = train_test_split(self.data, test_size=TEST_SIZE)
        num_features = len(self.data.columns) - 1  # num of features without the apartment's price

        # separate data to apartments features (without prices) and apartments prices
        training_features = training_set.iloc[:, :num_features]
        training_prices = training_set.loc[:, 'SQR_FEET_PRICE']
        test_features = test_set.iloc[:, :num_features]
        test_prices = test_set.loc[:, 'SQR_FEET_PRICE']

        clf = clf.fit(training_features, training_prices)

        # Comparing prediction vs actual classification:
        training_accuracy = clf.score(training_features, training_prices)
        test_accuracy = clf.score(test_features, test_prices)
        print("training accuracy: " + str(training_accuracy) + ", test acc: " + str(test_accuracy))

if __name__ == '__main__':
    tree = DecisionTree()