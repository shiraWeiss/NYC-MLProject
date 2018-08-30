# need to use: conda install scikit-learn
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor
from Data.ExtractionUtils import removeCols

TEST_SIZE = 0.25
CLASSIFIER = 0
DATA = 1
PRICE_LEVEL_SIZE = 1000

class DecisionTree:
    def __init__(self):
        self.data = pd.read_csv("Data/mainDB.csv")
        self.data = removeCols(self.data, 'ADDRESS')    # not a numeric feature - not relevant
        self._getDecisionTreeAccuracy()

    # '''
    # For the decision tree the classifications should be categories, not float numbers (prices).
    # This functions splits the apartments prices into ranges
    # '''
    # def _changePricesToCatagories(self):
    #     self.data['SQR_FEET_PRICE'] = self.data['SQR_FEET_PRICE'].apply(lambda price: self._toCatagory(price))

    def _getDecisionTreeAccuracy(self):
        # clf = DecisionTreeRegressor() todo: basic version
        clf = DecisionTreeRegressor(max_depth=100, max_features=2, min_samples_leaf=10)
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