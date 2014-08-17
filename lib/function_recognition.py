#!/usr/bin/python
# coding: utf-8


import numpy
import json
import itertools
import copy

from collections import defaultdict
from collections import OrderedDict

from nupic.algorithms.anomaly import computeAnomalyScore
from nupic.encoders import MultiEncoder
from nupic.algorithms.anomaly import computeAnomalyScore
from nupic.encoders import MultiEncoder
from nupic.engine import Network

import lib.create_network as cn



class FunctionRecogniter():

    def __init__(self):

        self.run_number = 0

        # for classifier
        self.classifier_encoder_list = {}
        self.classifier_input_list   = {}
        self.prevPredictedColumns    = {}

        self.selectivity = "region1"

        # net structure
        self.net_structure = OrderedDict()
        self.net_structure['sensor1'] = ['region1']
        # self.net_structure['sensor2'] = ['region2']
        # self.net_structure['sensor3'] = ['region3']
        # self.net_structure['region1'] = ['region4']
        # self.net_structure['region2'] = ['region4']

        # sensor change params
        self.sensor_params = {
                'sensor1': {
                    'xy_value': {
                        'maxval': 100.0,
                        'minval':  0.0
                        },
                    },
                # 'sensor2': {
                #     'xy_value': {
                #         'maxval': 80.0,
                #         'minval': 20.0
                #         },
                #     },
                # 'sensor3': {
                #     'xy_value': {
                #         'maxval': 100.0,
                #         'minval':  40.0
                #         },
                #     },
                }

        # region change params
        self.dest_resgion_data = {
                'region1': {
                    'SP_PARAMS':{
                        "columnCount": 2024,
                        "numActiveColumnsPerInhArea": 20,
                        },
                    'TP_PARAMS':{
                        "cellsPerColumn": 16
                        },
                    },
                # 'region2': {
                #     'TP_PARAMS':{
                #         "cellsPerColumn": 8
                #         },
                #     },
                # 'region3': {
                #     'TP_PARAMS':{
                #         "cellsPerColumn": 8
                #         },
                #     },
                # 'region4': {
                #     'SP_PARAMS':{
                #         "inputWidth": 2024 * (4 + 8)
                #         },
                #     'TP_PARAMS':{
                #         "cellsPerColumn": 16
                #         },
                #     },
                 }

        self._createNetwork()


        # for evaluate netwrok accuracy
        self.evaluation = NetworkEvaluation()


    def _addRegion(self, src_name, dest_name, params):

        sensor     =  src_name
        sp_name    = "sp_" + dest_name
        tp_name    = "tp_" + dest_name
        class_name = "class_" + dest_name

        try:
            self.network.regions[sp_name]
            self.network.regions[tp_name]
            self.network.regions[class_name]

            self.network.link(sensor, sp_name, "UniformLink", "")

        except Exception as e:
            # sp
            self.network.addRegion(sp_name, "py.SPRegion", json.dumps(params['SP_PARAMS']))
            self.network.link(sensor, sp_name, "UniformLink", "")

            # tp
            self.network.addRegion(tp_name, "py.TPRegion", json.dumps(params['TP_PARAMS']))
            self.network.link(sp_name, tp_name, "UniformLink", "")

            # class
            self.network.addRegion( class_name, "py.CLAClassifierRegion", json.dumps(params['CLASSIFIER_PARAMS']))
            self.network.link(tp_name, class_name, "UniformLink", "")

            encoder = MultiEncoder()
            encoder.addMultipleEncoders(params['CLASSIFIER_ENCODE_PARAMS'])
            self.classifier_encoder_list[class_name]  = encoder
            self.classifier_input_list[class_name]    = tp_name

    def _initRegion(self, name):
        sp_name = "sp_"+ name
        tp_name = "tp_"+ name
        class_name = "class_"+ name

        # setting sp
        SP = self.network.regions[sp_name]
        SP.setParameter("learningMode", True)
        SP.setParameter("anomalyMode", True)

        # setting tp
        TP = self.network.regions[tp_name]
        TP.setParameter("topDownMode", False)
        TP.setParameter("learningMode", True)
        TP.setParameter("inferenceMode", True)
        TP.setParameter("anomalyMode", False)

        # classifier regionを定義.
        classifier = self.network.regions[class_name]
        classifier.setParameter('inferenceMode', True)
        classifier.setParameter('learningMode', True)


    def _createNetwork(self):

        def deepupdate(original, update):
            """
            Recursively update a dict.
            Subdict's won't be overwritten but also updated.
            """
            for key, value in original.iteritems():
                if not key in update:
                    update[key] = value
                elif isinstance(value, dict):
                    deepupdate(value, update[key])
            return update




        self.network = Network()

        # sensor
        for sensor_name, change_params in self.sensor_params.items():
            self.network.addRegion(sensor_name, "py.RecordSensor", json.dumps({"verbosity": 0}))
            sensor = self.network.regions[sensor_name].getSelf()

            # set encoder
            params = deepupdate(cn.SENSOR_PARAMS, change_params)
            encoder = MultiEncoder()
            encoder.addMultipleEncoders( params )
            sensor.encoder         = encoder

            # set datasource
            sensor.dataSource      = cn.DataBuffer()


        # network
        print 'create network ...'
        for source, dest_list in self.net_structure.items():
            for dest in dest_list:
                change_params = self.dest_resgion_data[dest]
                params = deepupdate(cn.PARAMS, change_params)

                if source in self.sensor_params.keys():
                    sensor = self.network.regions[source].getSelf()
                    params['SP_PARAMS']['inputWidth'] = sensor.encoder.getWidth()
                    self._addRegion(source, dest, params)
                else:
                    self._addRegion("tp_" + source, dest, params)

        # initialize
        print 'initializing network ...'
        self.network.initialize()
        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            self._initRegion(name)


        # TODO: 1-3-1構造で, TPのセル数をむやみに増やすことは逆効果になるのでは?

        return


    def run(self, input_data, learn=True):
        """
        networkの実行.
        学習したいときは, learn=True, ftypeを指定する.
        予測したいときは, learn=False, ftypeはNoneを指定する.
        学習しているときも, 予測はしているがな.

        input_data = {'xy_value': [1.0, 2.0], 'ftype': 'sin'}
        """

        self.enable_learning_mode(learn)
        self.run_number += 1

        # calc encoder, SP, TP
        for sensor_name in self.sensor_params.keys():
            self.network.regions[sensor_name].getSelf().dataSource.push(input_data)
        self.network.run(1)
        #self.layer_output(input_data)
        #self.debug(input_data)


        # learn classifier
        inferences = {}
        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            class_name = "class_" + name
            inferences['classifier_'+name]   = self._learn_classifier_multi(class_name, actValue=input_data['ftype'], pstep=0)

        # anomaly
        inferences["anomaly"] = self._calc_anomaly()

        # selectivity
        if input_data['ftype'] is not None and inferences["anomaly"][self.selectivity] < 0.7:
        #if input_data['ftype'] is not None and input_data['xy_value'][0] > 40 and input_data['xy_value'][0] < 60:
            tp_bottomUpOut = self.network.regions[ "tp_" + self.selectivity ].getOutputData("bottomUpOut").nonzero()[0]
            self.evaluation.save_cell_activity(tp_bottomUpOut, input_data['ftype'])

        return inferences


    def _learn_classifier_multi(self, region_name, actValue=None, pstep=0):
        """
        classifierの計算を行う.

        直接customComputeを呼び出さずに, network.runの中でやりたいところだけど,
        計算した内容の取り出し方法がわからない.
        """

        # TODO: networkとclassifierを完全に切り分けたいな.
        #       networkでは, sensor,sp,tpまで計算を行う.
        #       その計算結果の評価/利用は外に出す.

        classifier     = self.network.regions[region_name]
        encoder        = self.classifier_encoder_list[region_name].getEncoderList()[0]
        class_input    = self.classifier_input_list[region_name]
        tp_bottomUpOut = self.network.regions[class_input].getOutputData("bottomUpOut").nonzero()[0]
        #tp_bottomUpOut = self.network.regions["TP"].getSelf()._tfdr.infActiveState['t'].reshape(-1).nonzero()[0]

        if actValue is not None:
            bucketIdx = encoder.getBucketIndices(actValue)[0]
            classificationIn = {
                    'bucketIdx': bucketIdx,
                    'actValue': actValue
                    }
        else:
            classificationIn = {'bucketIdx': 0,'actValue': 'no'}
        clResults = classifier.getSelf().customCompute(
                recordNum=self.run_number,
                patternNZ=tp_bottomUpOut,
                classification=classificationIn
                )

        inferences= self._get_inferences(clResults, pstep, summary_tyep='sum')

        return inferences

    def _get_inferences(self, clResults, steps, summary_tyep='sum'):
        """
        classifierの計算結果を使いやすいように変更するだけ.
        """

        likelihoodsVec = clResults[steps]
        bucketValues   = clResults['actualValues']

        likelihoodsDict = defaultdict(int)
        bestActValue = None
        bestProb = None

        if summary_tyep == 'sum':
            for (actValue, prob) in zip(bucketValues, likelihoodsVec):
                likelihoodsDict[actValue] += prob
                if bestProb is None or likelihoodsDict[actValue] > bestProb:
                    bestProb = likelihoodsDict[actValue]
                    bestActValue = actValue

        elif summary_tyep == 'best':
            for (actValue, prob) in zip(bucketValues, likelihoodsVec):
                if bestProb is None or prob > bestProb:
                    likelihoodsDict[actValue] = prob
                    bestProb = prob
                    bestActValue = actValue

        return {'likelihoodsDict': likelihoodsDict, 'best': {'value': bestActValue, 'prob':bestProb}}


    def _calc_anomaly(self):
        """
        各層のanomalyを計算
        """

        score = 0
        anomalyScore = {}
        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            sp_bottomUpOut = self.network.regions["sp_"+name].getOutputData("bottomUpOut").nonzero()[0]
            if self.prevPredictedColumns.has_key(name):
                score = computeAnomalyScore(sp_bottomUpOut, self.prevPredictedColumns[name])
            #topdown_predict = self.network.regions["TP"].getSelf()._tfdr.topDownCompute().copy().nonzero()[0]
            topdown_predict = self.network.regions["tp_"+name].getSelf()._tfdr.topDownCompute().nonzero()[0]
            self.prevPredictedColumns[name] = copy.deepcopy(topdown_predict)

            anomalyScore[name] = score

        return anomalyScore

    def reset(self):
        """
        reset sequence
        """
        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            self.network.regions["tp_"+name].getSelf().resetSequenceStates()

    def enable_learning_mode(self, enable):
        """
        各層のSP, TP, ClassifierのlearningModeを変更
        """
        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            self.network.regions["sp_"+name].setParameter("learningMode", enable)
            self.network.regions["tp_"+name].setParameter("learningMode", enable)
            self.network.regions["class_"+name].setParameter("learningMode", enable)


    def print_inferences(self, input_data, inferences):
        """
        計算結果を出力する
        """

        print "%10s, %10s, %5s" % (
                int(input_data['xy_value'][0]),
                int(input_data['xy_value'][1]),
                input_data['ftype']),

        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            print "%5s," % (inferences['classifier_'+name]['best']['value']),

        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            print "%10.6f," % (inferences['classifier_'+name]['likelihoodsDict'][input_data['ftype']]),

        for name in set( itertools.chain.from_iterable( self.net_structure.values() )):
            print "%5s," % (str(inferences["anomaly"][name])),
        print

    # def layer_output(self, input_data):
    #     sensorRegion = self.network.regions["sensor"]
    #     SPRegion = self.network.regions["SP"]
    #     TPRegion = self.network.regions["TP"]
    #     SP2Region = self.network.regions["SP2"]
    #     TP2Region = self.network.regions["TP2"]
    #     print
    #     print "####################################"
    #     print
    #     print "==== Input ===="
    #     print input_data['xy_value']
    #     print
    #     print "==== EC layer ===="
    #     print "output:     ", sensorRegion.getOutputData("dataOut").nonzero()[0][:10]
    #     print
    #     print "==== SP layer ===="
    #     print "input:  ", SPRegion.getInputData("bottomUpIn").nonzero()[0][:10]
    #     print "output: ", SPRegion.getOutputData("bottomUpOut").nonzero()[0][:10]
    #     print
    #     print "==== TP layer ===="
    #     print "input:  ", TPRegion.getInputData("bottomUpIn").nonzero()[0][:10]
    #     print "output: ", TPRegion.getOutputData("bottomUpOut").nonzero()[0][:10]
    #     print
    #     print "==== SP2 layer ===="
    #     print "input:  ", SP2Region.getInputData("bottomUpIn").nonzero()[0][:10]
    #     print "output: ", SP2Region.getOutputData("bottomUpOut").nonzero()[0][:10]
    #     print
    #     print "==== TP2 layer ===="
    #     print "input:  ", TP2Region.getInputData("bottomUpIn").nonzero()[0]
    #     print "output: ", TP2Region.getOutputData("bottomUpOut").nonzero()[0]
    #     print
    #     print "==== Predict ===="
    #     print TPRegion.getSelf()._tfdr.topDownCompute().copy().nonzero()[0][:10]
    #     print
    #
    # def debug(self, input_data):
    #     TPRegion = self.network.regions["TP2"]
    #     tp_output = TPRegion.getOutputData("bottomUpOut").nonzero()[0]
    #     #print tp_output
    #
    #     if 5 in tp_output:
    #         print input_data['xy_value']


class NetworkEvaluation(object):
    def __init__(self):
        self.cell_activity = defaultdict(lambda: defaultdict(int))

    def get_fired_rate(self):
        """
        セルの平均発火数/STD
        """
        fire_count  = []
        for cell, activity in self.cell_activity.items():
            fire_count.append(sum([x for x in activity.values()]))
        return numpy.mean(fire_count) , numpy.std(fire_count)

    def get_selectivity(self):
        """
        選択性
        """
        selectivity  = defaultdict(lambda: defaultdict(int))

        mean, _ = self.get_fired_rate()

        for cell, activity in self.cell_activity.items():
            if sum(activity.values()) >= mean:
                for label, data in activity.items():
                    if not data == 0:
                        select_value = float(data) / sum(activity.values())
                        selectivity[label][int(select_value * 100)] += 1

        result  = defaultdict(lambda: defaultdict(list))
        for label, data in selectivity.items():
            result[label]['x'] = data.keys()
            result[label]['y'] = data.values()

        return result

    def get_selectivity_sum(self):
        """
        選択性summary
        """
        cell_count  = len(self.cell_activity)
        selectivity = self.get_selectivity()

        result = {}
        for label, data in selectivity.items():
            result[label] = sum([ rate * count for rate, count in zip(data['x'], data['y'])]) / cell_count

        return result


    def save_cell_activity(self, tp_cell_activity, label):
        """
        cellのアクティブ情報を保存

        classifierでも同じような個とやってるはずだからそっちからデータ取りたかったが,
        C++側で実装されていて, 直接アクセスできない.
        そっち側あまり修正したくないので, 自分で保存する.
        """
        for cell in tp_cell_activity:
            self.cell_activity[cell][label] += 1

    def print_summary(self):
        mean, std = self.get_fired_rate()
        print
        print '### mean/std'
        print 'mean : ', mean
        print 'std : ', std

        rate = self.get_selectivity_sum()
        print
        print "### selectivity"
        print "plus  : ", rate['plus']
        print "minus : ", rate['minus']
        print "flat  : ", rate['flat']
        print
