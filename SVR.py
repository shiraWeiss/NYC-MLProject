from sklearn import svm
from sklearn.model_selection import train_test_split

from Data.ExtractionUtils import features
from Data.MainTable import MainTable, selectCols
from Graphs.Graphs import graph_multipleExperiments_compareParameterEffect

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def multipleExperimentsFindingBestC(X, y, initial_c, final_c):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    train_scores_dict = {}
    test_scores_dict = {}
    for c in frange(float(initial_c), float(final_c), 50000000):
        regressor = svm.SVR(kernel='linear', C=c)
        regressor.fit(X_train, y_train)
        train_score = regressor.score(X_train, y_train)
        test_score = regressor.score(X_test, y_test)
        train_scores_dict[c] = train_score
        test_scores_dict[c] = test_score
    graph_multipleExperiments_compareParameterEffect(train_scores_dict, test_scores_dict, 'SVR', 'C')

if __name__ == '__main__':
    # Get the base table
    all_data = MainTable()
    df = all_data.getDB()

    # Split to Data and Actual results
    X = selectCols(df, features)
    y = df['SQR_FEET_PRICE']

    # it's better if this piece of code happens only once because it takes a long time to fit
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    regressor = svm.SVR(kernel='linear', C=1e7)
    regressor.fit(X_train, y_train)
    train_score = regressor.score(X_train, y_train)
    test_score = regressor.score(X_test, y_test)
    print("SVR basic test: Training score: " + str(train_score) + ", Test score: " + str(test_score))