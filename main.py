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

    for ftype in fd.function_list.keys():
        print ftype
        data = fd.get_data(ftype)
        for x, y in data:
            input_data = {
                    'xy_value': [x, y],
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)

            # print
            input_data['ftype'] = ftype
            recogniter.print_inferences(input_data, inferences)

            tmp = inferences[ "classifier_" + recogniter.selectivity]['likelihoodsDict'][ftype]
            result[ftype].append(tmp)


    # plot write
    import numpy
    plotter.add(title='result', y_values=result)
    print '### result'
    for title , data in result.items():
        print title , " : ",
        print numpy.mean(data)

    # print evaluation summary
    recogniter.evaluation.print_summary()

    # # plot selectivity
    # selectivity = recogniter.evaluation.get_selectivity()
    # for title, data in selectivity.items():
    #     plotter.add( title = 'selectivity', y_values={title:data['y']}, x_values={title:data['x']} )

    plotter.show()


def predict_example_2(fd, recogniter):
    """
    データはランダムに選択された関数から取得してnetwrokに入力.
    関数を確率を表示する.
    """
    plotter_2    = Plotter()
    result = defaultdict(list)

    plotter_2.setting({
        'xy_value':{
            'ylim': [0,100],
            'sub_title': ['value']},
        'likelihood':{
            'ylim': [0,1],
            'sub_title': fd.function_list.keys()},
        })

    #for ftype in fd.function_list.keys():
    print '################"'
    for idx in range(100):
        ftype = fd.romdom_choice()
        data  = fd.get_data(ftype)
        for x, y in data:
            input_data = {
                    'xy_value': [x, y],
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)

            # print
            input_data['ftype'] = ftype
            recogniter.print_inferences(input_data, inferences)

            tmp = inferences[ "classifier_" + recogniter.selectivity]['likelihoodsDict']
            plotter_2.write_draw(title='xy_value',   x_value={'value': x + 100 * idx}, y_value={'value': y})
            plotter_2.write_draw(title='likelihood', x_value=dict([(sub, x + 100 * idx) for sub in tmp.keys()]),  y_value=tmp)

def main():
    fd = function_data()
    recogniter = FunctionRecogniter()

    # トレーニング
    for i in range(100):
        print i,
        for num, ftype in enumerate(fd.function_list.keys()):
            data = fd.get_data(ftype)
            for x, y in data:
                input_data = {
                        'xy_value': [x, y],
                        'ftype': ftype
                        }
                inferences = recogniter.run(input_data, learn=True)

                # print
                recogniter.print_inferences(input_data, inferences)

            recogniter.reset()

    # 予測
    predict_example(fd, recogniter)

    predict_example_2(fd, recogniter)

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
