#!/usr/bin/python
# coding: utf-8

from lib.function_data import function_data
from lib.plotter import Plotter

def main():
    fd = function_data()
    plotter    = Plotter()

    plotter.initialize({
        'xy_value':{
            'ylim': [0,100],
            'sub_title': fd.function_list.keys()},
        }, movable=False)
    for i in range(1):
        for num, ftype in enumerate(fd.function_list.keys()):
            data  = fd.get_data(ftype, error_var=0)
            for x, y in data:
                plotter.write(title="xy_value", x_value={ftype: x}, y_value={ftype: y})
    plotter.show(save_dir='./docs/images/multi_layer/', file_name='target_function.png')


if __name__ == "__main__":
    main()
