# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "y_value",
      "fieldType": "float",
      "maxValue": 100.0,
      "minValue": 0.0
    },
    {
      "fieldName": "function_type",
      "fieldType": "int",
    }
  ],
  "streamDef": {
    "info": "function_type",
    "version": 1,
    "streams": [
      {
        "info": "Rec Center",
        "source": "file://function_data.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      0
    ],
    "predictedField": "function_type"
  },
  "iterationCount": -1,
  "swarmSize": "large"
}
