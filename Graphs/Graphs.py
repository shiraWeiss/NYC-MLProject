import matplotlib.pyplot as plt
import datetime


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
'''
def graph_PredictionVsActual(y_prediction, y_actual, x_label, y_label, graph_name, train_score=None, test_score=None):
    print("Graph: Plotting...")

    # for the text box
    fig, ax = plt.subplots()
    if train_score is not None:
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = 'train score: ' + str(train_score) + ', test score: ' + str(test_score)
        plt.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                                                verticalalignment='top', bbox=props)
    # the actual data
    plt.scatter(y_actual, y_prediction, s=20, edgecolor="black", c="darkorange", label="data")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(graph_name)
    graph_save(fig)
    plt.show()

def graph_save(fig):
    time = datetime.datetime.now()
    name = 'Graph/PredictionVsActual-' + str(time.day) + '-' + str(time.month)\
           + '-' + str(time.year) + '--' + str(time.hour) + str(time.minute) + '.png'
    fig.savefig(name, dpi=300)

if __name__ == '__main__':
    graph_PredictionVsActual(range(1,50), range(1,50), 'x', 'y', 'trial graph', 0.5, 0.7)