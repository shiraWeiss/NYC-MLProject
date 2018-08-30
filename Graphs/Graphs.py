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
def graph_PredictionVsActual(y_prediction, y_actual, x_label, y_label, graph_name, train_score=None, test_score=None, more_text=None):
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
    plt.scatter(y_actual, y_prediction, s=20, edgecolor="black", c="darkorange", label="data")
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

def graph_save(fig, name):
    time = datetime.datetime.now()
    # todo : take note, if in the start of the path for 'name' there is no "Graphs/" - add it.
    name = name + '-' + str(time.day) + '-' + str(time.month)\
           + '-' + str(time.year) + '--' + str(time.hour) + str(time.minute) + '.png'
    fig.savefig(name, dpi=300)

if __name__ == '__main__':
    graph_PredictionVsActual(range(1,50), range(1,50), 'x', 'y', 'trial graph', 0.5, 0.7, 'More Details mannnn')