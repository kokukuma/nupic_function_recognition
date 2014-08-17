#!/usr/bin/python
# coding: utf-8

import random
import numpy

class function_data(object):
    """
    指定した関数のx,yデータを取得する.

    sample:
        fd = function_data()
        ftype = fd.romdom_choice()
        data = fd.get_data(ftype)

        print ftype
        for d in data:
            print d
    """
    def __init__(self):
        """
        x = 0 - 100
        y = 0 - 100
        """
        self.max_x = 100
        self.function_list = {
                'flat':  lambda x: 50.0,
                'plus':  lambda x: float(x),
                'minus': lambda x: 100-float(x),
                # 'sin':   lambda x: numpy.sin(x *  4 * numpy.pi/self.max_x) * 50 + 50,
                # 'quad':  lambda x: float(x*x)/self.max_x,
                # 'step':  lambda x: 100.0 if int(float(x)/15) % 2 == 0  else 0.0
                }

    def romdom_choice(self):
        ftype = random.choice(self.function_list.keys())
        return ftype

    def get_data(self, ftype):
        if ftype not in self.function_list.keys():
            return []
        result = []
        for x in range(self.max_x):
            y = self.function_list[ftype](x)
            result.append([float(x), y])
        return result


