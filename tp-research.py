#!/usr/bin/python
# coding: utf-8

from pprint import pprint
from pylab import *
from collections import defaultdict

from lib.function_recognition import FunctionRecogniter
from lib.function_data import function_data
from lib.plotter import Plotter


def predict_example_4(data_set, recogniter):
    result = defaultdict(lambda: defaultdict(list))
    for ftype, data in data_set.items():
        for x, y in enumerate(data):
            input_data = {
                    'xy_value': [x, y],
                    'x_value': x,
                    'y_value': y,
                    'ftype': None
                    }
            inferences = recogniter.run(input_data, learn=False)

            # debug output
            if x >= 10:
                #recogniter.layer_output(input_data, region_name="tp_region1")
                result[(x,y)][ftype] = recogniter.network.regions["tp_region1"].getOutputData("bottomUpOut").nonzero()[0]

        recogniter.reset()

    for xy_value, data in sorted(result.items(), key=lambda x: x[0]):
        non_set = (set(data['a']) | set(data['b']))  - (set(data['a']) & set(data['b']))
        on_set = (set(data['a']) & set(data['b']))
        print xy_value, len(on_set), ":", len(data['a']),len(data['b']), ":",list(non_set)[:10]



def main():
    type_a_data = [2] * 10 + [50] * 30
    type_b_data = [1] * 10 + [50] * 30

    data_set  = {'a': type_a_data, 'b':type_b_data}

    recogniter = FunctionRecogniter()

    plotter    = Plotter()
    result = defaultdict(list)
    plotter.initialize({
        'anomaly':{
            'ylim': [0,1],
            'sub_title': ['a', 'b']},
        'output-differ':{
            'ylim': [0,1],
            'sub_title': ['a', 'b']},
        'first':{
            'ylim': [0,100],
            'sub_title': ['a', 'b']},
        }, movable=True)

    # トレーニング
    for i in range(100):
        anomaly_mean = {}
        output_differ_mean = {}
        first_input = {}
        for ftype, data in data_set.items():
            tmp_anomaly = []
            tmp_output_differ = []
            first_input_cnt = 0
            for x, y in enumerate(data):
                input_data = {
                        'xy_value': [x, y],
                        'x_value': x,
                        'y_value': y,
                        'ftype': ftype
                        }
                inferences = recogniter.run(input_data, learn=True)

                # for plot
                tmp_anomaly.append(inferences['anomaly']['region1'] )
                if len(inferences["output_differ"]) == 0:
                    first_input_cnt += 1
                else:
                    tmp_output_differ.append(inferences["output_differ"]['region1'])

                # print
                #recogniter.print_inferences(input_data, inferences)
            recogniter.reset()

            # for plot
            anomaly_mean[ftype]       = sum(tmp_anomaly) / len(tmp_anomaly)
            output_differ_mean[ftype] = sum(tmp_output_differ) / len(tmp_output_differ)
            first_input[ftype] =  first_input_cnt

        plotter.write_draw(title='anomaly', x_value={'a':i, 'b':i}, y_value=anomaly_mean)
        plotter.write_draw(title='output-differ', x_value={'a':i, 'b':i}, y_value=output_differ_mean)
        plotter.write_draw(title='first', x_value={'a':i, 'b':i}, y_value=first_input)


        # 予測
        #if i % 10 == 0:
        print
        print '##################### ', i
        predict_example_4(data_set, recogniter)

    plotter.show()



if __name__ == "__main__":
    main()
