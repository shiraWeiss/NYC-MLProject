import time
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import datetime
import numpy as np

'''
This function creates a graph that compares prediction vs actual value with a scatter of points.
The X axis represents the predictions, and the Y axis represents the actual values.
The closer your points are to the line y=x, the better.

@:param: y_prediction, y_actual : 
        The prices to compare, prediction vs. reality.
        ~ Note that they should both be either from TESTS or from TRAINING! 
          Don't mix those up because the arrays need to be in the same size.
@:param: x_label, y_label, graph_name : 
        Lables for the graph.
@:param: train_score, test_score :
        Optional. If provided, displays the given scores in a textbox.
@:param: more_text :
        Optional. Provide some more text to be displayed on the graph in a textbox.
'''


def graph_PredictionVsActual(y_prediction, y_actual, x_label, y_label, graph_name, train_score=None, test_score=None,
                             more_text=None, color = None):
    print("Graph: Plotting...")
    # text boxes
    fig, ax = plt.subplots()
    if train_score is not None:
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = 'train score: ' + str(train_score) + ', test score: ' + str(test_score)
        plt.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                 verticalalignment='top', bbox=props)
        plt.text(0.05, 0.88, more_text, transform=ax.transAxes, fontsize=8,
                 verticalalignment='top', bbox=props)

    # the actual data
    if color is None:
        color = "darkorange"
    plt.scatter(y_actual, y_prediction, s=20, edgecolor="black", c=color, label="data")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(graph_name)

    # add the line y = x
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]
    # now plot both limits against eachother
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    ax.set_aspect('equal')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    graph_save(fig, 'PredictionVsActual')
    plt.show()

'''
Print accuracy for different parameters
@:param: x_label, y_label, graph_name :
    labels for the graph.
@:params: x_values, train_scores, test_scores:
    x values are the different parameters values that we want to show on the graph
    train_scores/test_scores are the accuracy score of the train/test group
@: param: more_text:
    can add additional text that will be printed on the graph
'''
def graph_compareAccuracyOfDifferentParamsValues(x_values, train_scores, test_scores, graph_name, save, more_text=''):
    train_scores = [ float('%.2f' % num) for num in train_scores]
    test_scores = [ float('%.2f' % num) for num in test_scores]

    ind = np.arange(len(x_values))  # the x locations for the groups
    fig, ax = plt.subplots(figsize=(10,8))
    width = 0.35  # the width of the bars

    train_bars = ax.bar(ind - width / 2, train_scores, width, color='LightGreen', label='Training Accuracy')
    test_bars = ax.bar(ind + width / 2, test_scores, width, color='Green', label='Test Accuracy')
    # make each X value is showed on the graph
    ax.set_xticklabels(x_values)
    ax.set_xticks(ind)
    plt.xlabel(graph_name + ' value')
    ax.set_ylabel('Accuracy Score')

    ax.legend()
    plt.title(graph_name + ' - training scores vs. test scores')
    _addBarValue(train_bars, train_scores, ax)
    _addBarValue(test_bars, test_scores, ax)
    if save == True:
        graph_save(fig, graph_name)
    plt.show()

def _addBarValue(bars, scores, ax, xpos='center'):
    """
    Attach a text label above each bar in *bars*, displaying its height.

    *xpos* indicates which side to place the text. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(score), ha=ha[xpos], va='bottom')

def graph_save(fig, name):
    time = datetime.datetime.now()
    # todo : take note, if in the start of the path for 'name' there is no "Graphs/" - add it.
    name = name + '-' + str(time.day) + '-' + str(time.month) \
           + '-' + str(time.year) + '--' + str(time.hour) + str(time.minute) + str(time.second)+ '.png'
    fig.savefig(name, dpi=300)

def graph_coorelation(x, y, x_label, y_label):
    name = 'Relationship between ' + x_label + ' and ' + y_label
    fig = figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')
    plt.scatter(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(name)
    name = 'LinearRegression/coorelation_graph_' + x_label + '_-_' + y_label
    graph_save(fig, name)

def graph_multipleExperiments_compareParameterEffect(train_scores_dict, test_scores_dict, algorithm_name, param_name):
    train_values    = list(train_scores_dict.values())
    train_keys      = list(train_scores_dict.keys())
    fig, ax = plt.subplots()
    plt.plot(train_keys, train_values, label='Training Accuracy', marker='o', color='peachpuff')

    test_values     = list(test_scores_dict.values())
    test_keys       = list(test_scores_dict.keys())
    plt.plot(test_keys, test_values, label='Test Accuracy', marker='o', color='greenyellow')

    plt.xlabel(param_name)
    plt.ylabel('Accuracy')
    plt.title(algorithm_name)
    plt.legend(loc='upper left')
    plt.show()
    name = algorithm_name + '_checking_param_' + param_name
    graph_save(fig, name)

def graph_multipleExperiments_compareParameterEffect_meanScores(mean_scores_dict, algorithm_name, param_name):
    train_values    = list(mean_scores_dict.values())
    train_keys      = list(mean_scores_dict.keys())
    fig, ax = plt.subplots()
    plt.plot(train_keys, train_values, label='Average Accuracy', marker='o', color='lime')

    plt.xlabel(param_name)
    plt.ylabel('Accuracy')
    plt.title(algorithm_name)
    plt.legend(loc='upper left')
    plt.show()
    name = algorithm_name + '_checking_param_' + param_name
    graph_save(fig, name)

def graph_paramTuning(train_scores_dict, test_scores_dict, algorithm_name, param_name):
    train_values    = list(train_scores_dict.values())
    train_keys      = list(train_scores_dict.keys())
    fig, ax = plt.subplots()
    plt.plot(train_keys, train_values, label='Training Accuracy', marker='o', color='peachpuff')

    test_values     = list(test_scores_dict.values())
    test_keys       = list(test_scores_dict.keys())
    plt.plot(test_keys, test_values, label='Test Accuracy', marker='o', color='greenyellow')

    plt.xlabel(param_name)
    plt.ylabel('Accuracy')
    plt.title(algorithm_name)
    plt.legend(loc='upper left')
    plt.show()
    name = algorithm_name + '_tuning_param_' + param_name
    # graph_save(fig, name) #todo not save for submission