#!/usr/bin/python
# coding: utf-8

from pprint import pprint
from pylab import *
from collections import defaultdict

import matplotlib.pyplot as plt


class Plotter(object):

    def __init__(self):
        self.graphs = []
        self.data_y   = defaultdict(lambda: defaultdict(list))
        self.data_x   = defaultdict(lambda: defaultdict(list))

    def add(self, title, y_values, x_values=None):
        """
        y_values = {'plus':[1, 2, 3, ..], 'minus': [1, 2, 3, ...]}
        x_values = {'plus':[1, 2, 3, ..], 'minus': [1, 2, 3, ...]}
        """
        self.data_y[title].update(y_values)
        if x_values is not None:
            self.data_x[title].update(x_values)

    def show(self):
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec

        self.fig = plt.figure(figsize=(16, 10))
        gs = gridspec.GridSpec(len(self.data_y), 1)

        # graph setting
        for idx, title in enumerate(self.data_y.keys()):
            self.graphs.append(self.fig.add_subplot(gs[idx, 0]))
            plt.title( title )

        for idx, data_dict in enumerate(self.data_y.values()):
            title = self.data_y.keys()[idx]
            sub_title_list = []
            for sub_title, data in data_dict.items():
                if self.data_x.has_key(title):
                    self.graphs[idx].plot(self.data_x[title][sub_title] , data)
                else:
                    self.graphs[idx].plot(data)

                sub_title_list.append(sub_title)

            self.graphs[idx].legend(tuple(sub_title_list), loc=3)

        plt.show()
