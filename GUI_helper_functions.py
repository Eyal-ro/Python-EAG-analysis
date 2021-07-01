from tkinter import *
from EAG_analysis_class import *
import statistics
from PIL import ImageTk, Image
from matplotlib.figure import Figure
import matplotlib
from tkinter import messagebox as mb
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

matplotlib.use('TkAgg')


def pharse_experiments_input(experiments):
    experiments = experiments.split(',')
    new_experiments = []
    indeces_to_remove = []
    for j in range(0, len(experiments)):
        if '-' in experiments[j]:
            new_experiments = new_experiments + list(
                range(int(experiments[j].split('-')[0]),
                      int(experiments[j].split('-')[1]) + 1))
            indeces_to_remove.append(j)
    for ele in sorted(indeces_to_remove, reverse=True):
        del experiments[ele]
    experiments = experiments + new_experiments
    if len(experiments) == 1:
        experiments = int(experiments[0])
    return experiments


def plot_experiments_data(experiment_list, data, channel):
    fig = Figure(figsize=(5, 5))
    plot1 = fig.add_subplot(111)
    if isinstance(experiment_list, int):
        experiment_list = str(experiment_list)
    # if len([experiment_list]) == 1:
    #     experiment_list = [experiment_list]
    for i in experiment_list:
        plot1.plot(data.values_only.loc[int(i)].loc[channel])
        plot1.set_title('Experiments', loc='center')
        plot1.axes.get_xaxis().set_visible(False)
    plot1.legend(experiment_list)
    return fig


def plot_experiments_label_data(experiment_list, labels, data, channel):
    fig = Figure(figsize=(5, 5))
    plot1 = fig.add_subplot(111)
    for i in range(len(experiment_list)):
        if isinstance(experiment_list[i], int):
            experiment_list[i] = str(experiment_list[i])
    for experiment in experiment_list:
        plot1.plot(data.getAverageOfExperiments(experiment, channel))
        plot1.axes.get_xaxis().set_visible(False)
    plot1.set_title('Labels plot channel' + str(channel), loc='center')
    plot1.legend(labels)
    return fig


def plot_blank_experiments_data(experiment_list, data):
    fig1 = Figure(figsize=(5, 5))
    plot1 = fig1.add_subplot(111)
    fig2 = Figure(figsize=(5, 5))
    plot2 = fig2.add_subplot(111)
    if isinstance(experiment_list, int):
        experiment_list = str(experiment_list)
    # if len([experiment_list]) == 1:
    #     experiment_list = [experiment_list]
    for i in experiment_list:
        plot1.plot(data.values_only.loc[int(i)].loc[1])
        plot1.get_xaxis().set_visible(False)
        plot1.set_title("Blank channel 1")
    for i in experiment_list:
        plot2.plot(data.values_only.loc[int(i)].loc[2])
        plot2.get_xaxis().set_visible(False)
        plot2.set_title("Blank channel 2")
    fig1.legend(experiment_list)
    fig2.legend(experiment_list)
    return fig1, fig2
