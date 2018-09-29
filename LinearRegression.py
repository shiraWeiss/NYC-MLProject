from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd

from Data.ArtGalleries.ArtGalleries import ArtGalleries
from Data.ExtractionUtils import features
from Data.MainTable import MainTable, selectCols
from Data.Museums.Museums import Museums
from Graphs.Graphs import *
from Data.Apartments import Apartments


def predictionAndScore_andDisplay(regressor, X_train, X_test, y_train, y_test):
    print("Linear Regression: Predicting...")
    y_pred = regressor.predict(X_test)
    train_score = round(regressor.score(X_train, y_train), 4)       # 4 digits after the decimal point
    test_score = round(regressor.score(X_test, y_test), 4)          # 4 digits after the decimal point
    # generate the graph for the current experiment
    graph_PredictionVsActual(y_pred, y_test.values, 'Prediction', 'Actual Value',
                             'Linear Regression', train_score, test_score, 'No Parameters', "lightgreen")

    return y_pred, test_score, train_score

def normalizeByMaxValue(df, col):
    return df[col].apply(standardNormalize, args=(df[col].max(),)).to_frame()

def standardNormalize(score, factor):
    if factor == 0:
        return 0
    return float(score) / float(factor)


def coorelationExperiments(X, y, df, regressor):
    # Corelation examining
    estimated_coefs = pd.DataFrame(list(zip(X.columns, regressor.coef_)), columns=['features', 'esitmatedCoefficients'])
    estimated_coefs.to_csv(path_or_buf="LinearRegression_EstimatedCoefficients.csv")
    # graph_coorelation(selectCols(df, ['HIGH_SCHOOLS']), y, 'Highschools Quality (1.2km radius)', 'Apartment Price')
    # graph_coorelation(selectCols(df, ['NUM_OF_PARKS']), y, 'Number of Parks (1km radius)', 'Apartment Price')
    # graph_coorelation(selectCols(df, ['NOISE']), y, 'Amount of Noise in Apartment Area', 'Apartment Price')
    # graph_coorelation(selectCols(df, ['GALLERIES']), y, 'Number of Galleries (1km radius)', 'Apartment Price')
    # graph_coorelation(selectCols(df, ['MUSEUMS']), y, 'Number of Museums (1km radius)', 'Apartment Price')
    # graph_coorelation(selectCols(df, ['BOROUGH']), y, 'Borough', 'Apartment Price')  # todo - as histogram
    # graph_coorelation(selectCols(df, ['BUILDING_AGE']), y, 'Building Age', 'Apartment Price')


if __name__ == '__main__':
    # Get the base table
    all_data = MainTable()
    # df = all_data.getDB()

    # Split to Data and Actual results
    # X = selectCols(df, features)
    # y = df['SQR_FEET_PRICE']

    # it's better if this piece of code happens only once because it takes a long time to fit
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)
    # regressor = LinearRegression()
    # regressor.fit(X_train, y_train)

    # coorelationExperiments(X, y, df, regressor)
    # predictionAndScore_andDisplay(regressor, X_train, X_test, y_train, y_test)


