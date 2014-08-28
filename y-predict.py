#!/usr/bin/python
# coding: utf-8

from pprint import pprint
from pylab import *
from collections import defaultdict

from lib.function_recognition import FunctionRecogniter
from lib.function_data import function_data
from lib.plotter import Plotter

def predict_example(fd, recogniter, image_prefix="", ftypes=[]):
    """
    全ての関数から得たデータをnetwrokに入力, 関数を予測する.
    最終的に, 関数毎の平均正解率と入力に対する正解率を表示する.
    neuronの選択性が得られているかを表示.

    """
    plotter    = Plotter()
    result = defaultdict(list)
    plotter.initialize({
        'xy_value':{
            'ylim': [0,100],
            'sub_title': ['value', 'predict']},
        }, movable=False)

    if len(ftypes) == 0:
        ftypes = fd.function_list.keys()

    for ftype in ftypes:
        data = fd.get_data(ftype, error_var=1)
        label = fd.get_label(ftype)
        y_predict = 0
        for x, y in data:
            input_data = {
                    'xy_value': [x, y],
                    'x_value': x,
                    'y_value': y,
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)
            pprint(inferences)


            # print
            input_data['ftype'] = label
            #recogniter.print_inferences(input_data, inferences)

            # for plot
            plotter.write(title="xy_value", x_value={'value': x, 'predict': x}, y_value={'value': y, 'predict': y_predict})
            y_predict = inferences[ "classifier_" + recogniter.selectivity]['best']['value']

        plotter.show(save_dir='./docs/images/multi_layer/', file_name=image_prefix+ftype+'.png')
        plotter.reset()


def main():
    import random
    import numpy

    fd = function_data()
    recogniter = FunctionRecogniter()

    # トレーニング
    #for learn_layer in [['region1', 'region2'], ['region3']]:
    for learn_layer in [['region1'], ['region2'] ]:
        for i in range(25):
            print i
            for num, ftype in enumerate(fd.function_list.keys()):
                data  = fd.get_data(ftype, error_var=1)
                label = fd.get_label(ftype)
                for x, y in data:
                    input_data = {
                            'xy_value': [x, y],
                            'x_value': x,
                            'y_value': y,
                            'ftype': label
                            }

                    inferences = recogniter.run(input_data, learn=True, learn_layer=learn_layer)

                    # print
                    recogniter.print_inferences(input_data, inferences)

                recogniter.reset()

    # 予測
    predict_example(fd, recogniter, image_prefix="layer-")

if __name__ == "__main__":
    main()
