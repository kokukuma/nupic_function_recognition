#!/usr/bin/python
# coding: utf-8

from pprint import pprint
from pylab import *
from collections import defaultdict

from collections import deque

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# TODO: setting/write_drawを追加してぐちゃぐちゃになったから, 一回整理する.

class Plotter(object):

    def __init__(self):
        self.graphs = []
        self.xdata     = defaultdict(lambda: defaultdict(list))
        self.ydata     = defaultdict(lambda: defaultdict(list))
        self.initialized = False
        self.plots  = defaultdict(lambda: defaultdict(list))

        self.settings = None

    def write(self, title, y_value, x_value=None):
        """
        for non-movable

        y_values = {'plus':1, 'minus': 1}
        x_values = {'plus':1, 'minus': 1}
        """
        for key, value in y_value.items():
            self.ydata[title][key].append(value)

        if x_value is not None:
            for key, value in x_value.items():
                self.xdata[title][key].append(value)
        else:
            for key, value in y_value.items():
                self.xdata[title][key].append(len(self.xdata[title][key]))

    def reset(self):
        self.graphs = []
        self.plots  = defaultdict(lambda: defaultdict(list))
        self.xdata  = defaultdict(lambda: defaultdict(list))
        self.ydata  = defaultdict(lambda: defaultdict(list))
        self.initialize(self.settings, self.movable)

    def add(self, title, y_values, x_values=None):
        """
        for non-movable

        y_values = {'plus':[1, 2, 3, ..], 'minus': [1, 2, 3, ...]}
        x_values = {'plus':[1, 2, 3, ..], 'minus': [1, 2, 3, ...]}
        """
        self.ydata[title].update(y_values)
        if x_values is not None:
            self.xdata[title].update(x_values)
        else:
            self.xdata[title].update(dict([(subt, range(len(values))) for subt,values in y_values.items()]))


    def show(self):
        """
        for non-movable
        """

        if self.movable:
            plt.ioff()
            plt.show()
            return

        for idx, title in enumerate(self.settings.keys()):
            for sub_title in self.settings[title]['sub_title']:
                self.plots[title][sub_title].set_xdata(self.xdata[title][sub_title])
                self.plots[title][sub_title].set_ydata(self.ydata[title][sub_title])

            self.graphs[idx].legend(tuple(self.settings[title]['sub_title']), loc=3)
            self.graphs[idx].relim()
            self.graphs[idx].autoscale_view(True, True, True)

        plt.show()



    def initialize(self, settings, movable=False ):
        self.settings = settings
        self.movable = movable

        self.fig = plt.figure(figsize=(16, 10))
        gs = gridspec.GridSpec(len(settings), 1)


        WINDOW = 100
        if movable:
            plt.ion()

        # graph setting
        for idx, title in enumerate(settings.keys()):
            self.graphs.append(self.fig.add_subplot(gs[idx, 0]))
            if settings[title].has_key('ylim'):
                plt.ylim( settings[title]['ylim'] )
            plt.title( title )

        for idx, title in enumerate(settings.keys()):
            for sub_title in settings[title]['sub_title']:
                if movable:
                    self.xdata[title][sub_title] = deque([0.0] * WINDOW, maxlen=WINDOW)
                    self.ydata[title][sub_title] = deque([0.0] * WINDOW, maxlen=WINDOW)

                self.plots[title][sub_title],  = self.graphs[idx].plot(self.xdata[title][sub_title], self.ydata[title][sub_title])
            self.graphs[idx].legend(tuple(settings[title]['sub_title']), loc=3)

        plt.tight_layout()
        self.initialized = True

    def write_draw(self, title, y_value, x_value=None):
        """
        for movable

        y_values = {'plus':1, 'minus': 1}
        x_values = {'plus':1, 'minus': 1}
        """


        for key, value in y_value.items():
            self.ydata[title][key].append(value)


        if x_value is not None:
            for key, value in x_value.items():
                self.xdata[title][key].append(value)
        else:
            self.xdata[title][key].append(len(self.xdata[title][key]))


        # update
        for idx, title in enumerate(self.settings.keys()):
            for sub_title in self.settings[title]['sub_title']:
                self.plots[title][sub_title].set_xdata(self.xdata[title][sub_title])
                self.plots[title][sub_title].set_ydata(self.ydata[title][sub_title])

            self.graphs[idx].legend(tuple(self.settings[title]['sub_title']), loc=3)
            self.graphs[idx].relim()
            self.graphs[idx].autoscale_view(True, True, True)

        plt.draw()
        return plt


