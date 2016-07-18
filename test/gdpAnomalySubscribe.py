import numpy as np
import scipy
import math
import sys, os
import datetime
import time
import gdp

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python'))
sys.path.insert(1, os.path.join(sys.path[0], '../python/AnomalyDetection'))
## Interface path
sys.path.insert(1, os.path.join(sys.path[0], '../python/ContextEngineInterface'))

# Import your algorithms here.
from Anom import Anom
import Anomaly
printFlag = True
timestamps = {}
# Create dictionary object for each of the context engine I/Os
# each dictionary object includes: log name, JSON parameter in that log, lag
dict0 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 0,
          'norm': 'lin'}
dict4 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 4,
          'norm': ''}
# Number of CE input
numInp = 1
interfaceDict = {'in': [dict0], 
                 'out': dict4}
ceDict = {'interface': interfaceDict}
## Change the name of the algorithm to test it out.
algorithmTest = Anom(numInp, 0,[0], ceDict)
# subscribe to input log
algorithmTest.streamInputInit(0)
event = gdp.GDP_GCL.get_next_event(None)
print event 
print "Collecting training and test data from GDP"
# Use the collect data routine to fetch training data in separate lists
# for input and output
# TODO test on larger datasets
trainRecStart = 1000
trainRecStop = 4001
batchSize = 200
numTrainingSamples = trainRecStop - trainRecStart + 1
inDataTrain, outDataTrain = algorithmTest.interface.collectData(trainRecStart, trainRecStart + batchSize)
print "Done: collecting data from GDP"

print "Beginning loading and training"
# Add training data to CE object
for i in xrange(len(outDataTrain)):
    # recording time stamps before and after adding to measure load time
    firstTS = time.time()
    algorithmTest.addSingleObservation(inDataTrain[:][i], outDataTrain[i])
    secondTS = time.time()
    timestamps["load" + str(i)] = secondTS - firstTS

firstTS = time.time()
algorithmTest.clusterAndTrain()
secondTS = time.time()

data = inDataTrain
i = 0
while trainRecStart < trainRecStop:
    if algorithmTest.executeAndCluster(data[i][0]) == 1:
        print int(algorithmTest.executeAndCluster(data[i][0])), inDataTrain[i][0], data[i][0]
    if i < batchSize:
        i = i + 1
    else:
        i = 0
        trainRecStart = trainRecStart + batchSize
        inDataTrain, outDataTrain = algorithmTest.interface.collectData(trainRecStart, trainRecStart + batchSize)
        for j in xrange(len(outDataTrain)):
            algorithmTest.addSingleObservation(inDataTrain[:][j], outDataTrain[i])
        data = inDataTrain
        algorithmTest.clusterAndTrain()

