#!/usr/bin/python
# coding: utf-8

from nupic.encoders import MultiEncoder
PARAMS = {
    "SP_PARAMS": {
        "spVerbosity": 0,
        "spatialImp": "cpp",
        "globalInhibition": 1,
        "columnCount": 2024,
        "inputWidth": 0,             # set later
        "numActiveColumnsPerInhArea": 20,
        "seed": 1956,
        "potentialPct": 0.8,
        "synPermConnected": 0.1,
        "synPermActiveInc": 0.05,
        "synPermInactiveDec": 0.0005,
        "maxBoost": 2.0,
    },
    "TP_PARAMS": {
        "verbosity": 0,
        "columnCount": 2024,
        "cellsPerColumn": 32,
        # "cellsPerColumn": 70,
        #"cellsPerColumn": 100,
        "inputWidth": 2024,
        "seed": 1960,
        "temporalImp": "cpp",
        "newSynapseCount": 20,
        "maxSynapsesPerSegment": 32,
        "maxSegmentsPerCell": 128,
        "initialPerm": 0.21,
        "permanenceInc": 0.2,
        "permanenceDec": 0.1,
        #"permanenceDec": 0.0001,
        "globalDecay": 0.0,
        "maxAge": 0,
        "minThreshold": 12,
        "activationThreshold": 16,
        "outputType": "normal",
        "pamLength": 1,
    },

    "CLASSIFIER_PARAMS": {
        "clVerbosity": 0,
        "alpha": 0.005,
        "steps": "0"
    },

    "CLASSIFIER_ENCODE_PARAMS": {
        "ftype": {
            "type": "CategoryEncoder",
            "fieldname": u"ftype",
            "name": u"ftype",
            "categoryList": ['plus', 'minus', 'flat', 'sin', 'quad', 'step'],
            "forced": True,
            "w": 7,
            },
    },

}


"""
you need delete [:] at l.298
repos/nupic/build/release/lib/python2.7/site-packages/nupic/regions/RecordSensor.py

https://github.com/numenta/nupic/issues/727
"""
SENSOR_PARAMS = {
    "xy_value": {
        #"type": "SimpleVectorEncoder",
        "clipInput": True,
        "type": "VectorEncoderOPF",
        "dataType": "float",
        "n": 200,
        "w": 21,
        "length": 2,
        "fieldname": u"xy_value",
        "name": u"xy_value",
        "maxval": 100.0,
        "minval": 0.0,
    },
    "x_value": None,
    "y_value": None,
}


# def createScalarEncoder():
#     encoder = MultiEncoder()
#     encoder.addMultipleEncoders({
#         "y_value": {
#             'clipInput': False,
#             "type": "ScalarEncoder",
#             "fieldname": u"y_value",
#             "name": u"y_value",
#             "maxval": 100.0,
#             "minval": 0.0,
#             'n': 100,
#             "w": 21,
#             },
#         })
#     return encoder

class DataBuffer(object):
    def __init__(self):
        self.stack = []

    def push(self, data):
        assert len(self.stack) == 0
        data = data.__class__(data)
        self.stack.append(data)

    def getNextRecordDict(self):
        assert len(self.stack) > 0
        return self.stack.pop()


