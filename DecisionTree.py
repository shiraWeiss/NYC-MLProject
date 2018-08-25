# need to use: conda install scikit-learn
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from Data.ExtractionUtils import removeCols

TEST_SIZE = 0.25
CLASSIFIER = 0
DATA = 1
PRICE_LEVEL_SIZE = 5000

class DecisionTree:
    def __init__(self):
        self.data = pd.read_csv("Data/mainDB.csv")
        self.data = removeCols(self.data, 'ADDRESS')    # not a numeric feature - not relevant
        self._changePricesToCatagories()    # float numbers can't be classifications
        self._getDecisionTreeAccuracy()

    '''
    For the decision tree the classifications should be categories, not float numbers (prices).
    This functions splits the apartments prices into ranges
    '''
    def _changePricesToCatagories(self):
        self.data['SQR_FEET_PRICE'] = self.data['SQR_FEET_PRICE'].apply(lambda price: self._toCatagory(price))

    def _getDecisionTreeAccuracy(self):
        id3 = DecisionTreeClassifier(criterion="entropy")
        training_set, test_set = train_test_split(self.data, test_size=TEST_SIZE)
        num_features = len(self.data.columns) - 1  # num of features without the apartment's price

        # separate data to apartments features (without prices) and apartments prices
        training_features = training_set.iloc[:, :num_features]
        training_prices = training_set.loc[:, 'SQR_FEET_PRICE']
        test_features = test_set.iloc[:, :num_features]
        test_prices = test_set.loc[:, 'SQR_FEET_PRICE']

        id3 = id3.fit(training_features, training_prices)
        training_prediction = id3.predict(training_features)
        test_prediction = id3.predict(test_features)

        # Comparing prediction vs actual classification:
        training_accuracy = accuracy_score(training_prices, training_prediction)
        test_accuracy = accuracy_score(test_prices, test_prediction)
        print("training accuracy: " + str(training_accuracy) + ", and test acc:" + str(test_accuracy))

    def _toCatagory(self, price):
        count = 0
        min_price = self.data['SQR_FEET_PRICE'].min()
        max_price = self.data['SQR_FEET_PRICE'].max()
        categories = range(int(min_price), int(max_price), PRICE_LEVEL_SIZE)
        for category in categories:
            if price <= category:
                return count
            count += 1
        return count

if __name__ == '__main__':
    tree = DecisionTree()