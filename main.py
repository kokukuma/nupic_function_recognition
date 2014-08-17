#!/usr/bin/python
# coding: utf-8

from pprint import pprint
from pylab import *
from collections import defaultdict

from lib.function_recognition import FunctionRecogniter
from lib.function_data import function_data
from lib.plotter import Plotter

def main():
    fd = function_data()
    recogniter = FunctionRecogniter()
    plotter    = Plotter()

    # トレーニング
    for i in range(50):
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


    # 予測1
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

    # plot selectivity
    selectivity = recogniter.evaluation.get_selectivity()
    for title, data in selectivity.items():
        plotter.add( title = 'selectivity', y_values={title:data['y']}, x_values={title:data['x']} )

    plotter.show()



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
