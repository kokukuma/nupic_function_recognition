#!/usr/bin/python
# coding: utf-8

from pprint import pprint
from pylab import *
from collections import defaultdict

from lib.function_recognition import FunctionRecogniter
from lib.function_data import function_data
from lib.plotter import Plotter

def predict_example(fd, recogniter):
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
            'sub_title': ['value']},
        'likelihood':{
            'ylim': [0,1],
            'sub_title': fd.function_list.keys()},
        }, movable=False)

    for ftype in fd.function_list.keys():
        print ftype
        data = fd.get_data(ftype)
        for x, y in data:
            input_data = {
                    'xy_value': [x, y],
                    'x_value': x,
                    'y_value': y,
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)

            # print
            input_data['ftype'] = ftype
            recogniter.print_inferences(input_data, inferences)

            # for result summary
            tmp = inferences[ "classifier_" + recogniter.selectivity]['likelihoodsDict'][ftype]
            result[ftype].append(tmp)

            # for plot
            plotter.write(title="xy_value", x_value={'value': x}, y_value={'value': y})
            plotter.write(title="likelihood", y_value=inferences[ "classifier_" + recogniter.selectivity]['likelihoodsDict'])

        plotter.show()
        plotter.reset()


    # write result summary
    import numpy
    print '### result'
    for title , data in result.items():
        print title , " : ",
        print numpy.mean(data)

    # print evaluation summary
    for name in recogniter.dest_resgion_data.keys():
        print '### ', name
        recogniter.evaluation.print_summary()



def predict_example_2(fd, recogniter):
    """
    データはランダムに選択された関数から取得してnetwrokに入力.
    関数を確率を表示する.
    """
    plotter_2    = Plotter()
    result = defaultdict(list)

    plotter_2.initialize({
        'xy_value':{
            'ylim': [0,100],
            'sub_title': ['value']},
        'likelihood':{
            'ylim': [0,1],
            'sub_title': fd.function_list.keys()},
        }, movable=True)

    #for ftype in fd.function_list.keys():
    print '################"'
    for idx in range(100):
        ftype = fd.romdom_choice()
        data  = fd.get_data(ftype)
        for x, y in data:
            input_data = {
                    'xy_value': [x, y],
                    'x_value': x,
                    'y_value': y,
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)

            # print
            input_data['ftype'] = ftype
            recogniter.print_inferences(input_data, inferences)

            tmp = inferences[ "classifier_" + recogniter.selectivity]['likelihoodsDict']
            plotter_2.write_draw(title='xy_value',   x_value={'value': x + 100 * idx}, y_value={'value': y})
            plotter_2.write_draw(title='likelihood', x_value=dict([(sub, x + 100 * idx) for sub in tmp.keys()]),  y_value=tmp)


def predict_example_3(fd, recogniter):
    """
    各層の統計的特徴を比較する.

    1. 各層のclassifier結果のgraph表示.
    2.

    """
    plotter    = Plotter()
    result = defaultdict(lambda: defaultdict(list))
    plotter.initialize({
        'selectivity_center':{
            'ylim': [0,100],
            'sub_title': recogniter.dest_resgion_data.keys() },
        'selectivity_outside':{
            'ylim': [0,100],
            'sub_title': recogniter.dest_resgion_data.keys() },
        'xy_value':{
            'ylim': [0,100],
            'sub_title': ['value']},
        'likelihood':{
            'ylim': [0,1],
            'sub_title': recogniter.dest_resgion_data.keys() },
        }, movable=False)

    for ftype in fd.function_list.keys():
        print ftype
        data = fd.get_data(ftype)
        for x, y in data:
            input_data = {
                    'xy_value': [x, y],
                    'x_value': x,
                    'y_value': y,
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)

            # print
            input_data['ftype'] = ftype
            recogniter.print_inferences(input_data, inferences)

            # for result summary
            for name in recogniter.dest_resgion_data.keys():
                tmp = inferences[ "classifier_" + name ]['likelihoodsDict'][ftype]
                result[name][ftype].append(tmp)

            # for plot
            plotter.write(title="xy_value", x_value={'value': x}, y_value={'value': y})
            tmp = {}
            for name in recogniter.dest_resgion_data.keys():
                class_name = "classifier_" + name
                tmp[name] = inferences[class_name]['likelihoodsDict'][ftype]
            plotter.write(title="likelihood", y_value=tmp)

        # for plot
        x_tmp = {}
        y_tmp = {}
        for name in recogniter.dest_resgion_data.keys():
            x_tmp[name] = recogniter.evaluation[name].get_selectivity()[ftype]['x']
            y_tmp[name] = recogniter.evaluation[name].get_selectivity()[ftype]['y']
        plotter.add(title="selectivity_center", x_values=x_tmp, y_values=y_tmp)

        x_tmp2 = {}
        y_tmp2 = {}
        for name in recogniter.dest_resgion_data.keys():
            x_tmp2[name] = recogniter.evaluation_2[name].get_selectivity()[ftype]['x']
            y_tmp2[name] = recogniter.evaluation_2[name].get_selectivity()[ftype]['y']
        plotter.add(title="selectivity_outside", x_values=x_tmp2, y_values=y_tmp2)

        plotter.show()
        plotter.reset()


    # write result summary
    import numpy
    print '### result'
    for name, datas in result.items():
        print '#### ', name
        for title ,data in datas.items():
            print title , " : ",
            print numpy.mean(data)

    # print evaluation summary
    for name in recogniter.dest_resgion_data.keys():
        print '### ', name
        recogniter.evaluation[name].print_summary()



def main():
    fd = function_data()
    recogniter = FunctionRecogniter()

    # トレーニング
    for i in range(50):
        print i,
        for num, ftype in enumerate(fd.function_list.keys()):
            data = fd.get_data(ftype)
            for x, y in data:
                input_data = {
                        'xy_value': [x, y],
                        'x_value': x,
                        'y_value': y,
                        'ftype': ftype
                        }
                inferences = recogniter.run(input_data, learn=True)

                # print
                recogniter.print_inferences(input_data, inferences)

            recogniter.reset()

            # for x, y in reversed(data):
            #     input_data = {
            #             'xy_value': [x, y],
            #             'x_value': x,
            #             'y_value': y,
            #             'ftype': ftype
            #             }
            #     inferences = recogniter.run(input_data, learn=True)
            #
            #     # print
            #     recogniter.print_inferences(input_data, inferences)

    # 予測
    #predict_example(fd, recogniter)

    #predict_example_2(fd, recogniter)

    predict_example_3(fd, recogniter)

    # # 予測2, fixed-sin
    # import numpy
    # print
    # print "fiexed-sin"
    # fd.function_list['sin'] = lambda x: numpy.sin(x * 2 * numpy.pi/fd.max_x) * 50 + 50
    # data = fd.get_data('sin')
    # for x, y in data:
    #     input_data = {
    #             'xy_value': [x, y]
    #             }
    #     inferences = recogniter.predict(input_data)
    #     print 'sin', inferences['best']['value'], inferences['best']['prob'], inferences["anomaly"]
    #
    #
    # # 予測3, fixed-sin
    # print
    # print "fiexed-sin"
    # fd.function_list['sin'] = lambda x: numpy.sin(x * 4 * numpy.pi/fd.max_x) * 30 + 50
    # data = fd.get_data('sin')
    # for x, y in data:
    #     input_data = {
    #             'xy_value': [x, y]
    #             }
    #     inferences = recogniter.predict(input_data)
    #     print 'sin', inferences['best']['value'], inferences['best']['prob'], inferences["anomaly"]

if __name__ == "__main__":
    main()
