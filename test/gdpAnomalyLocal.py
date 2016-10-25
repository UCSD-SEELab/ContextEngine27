import numpy as np
import scipy
import math
import sys, os
import datetime
import time
import gdp
import demoProximity

#sys.path.insert(0, "/home/nima/src/ContextEngine27/python")
#sys.path.insert(0, "/home/nima/src/ContextEngine27/python/AnomalyDetection")
#sys.path.insert(0, "/home/nima/src/ContextEngine27/python/ContextEngineInterface")

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
dict0 = {'dir': 'in',
        'source': 'Database',
        'name': 'localgdp',
        'param_lev1': 'S1W',
        'param_lev2': None,
          'lag': 0,
          'norm': 'lin'}
dict4 = {'dir': 'in',
            'source': 'GDP_I',
            'sink': 'GDP_I',
            # 'name': 'tCcbytv6gY0BdzvMx_JHw9ovPGwcpzvptFJiZ1k2u7Y',
            'name': 'edu.berkeley.eecs.swarmlab.device.c098e5300003',
            'param_lev1': 'temperature_celcius',
            'param_lev2': None,
            'lag': 4,
            'norm': '',   
            'key': 'DgAAAOhbtHYAAAAA-Fm0diD2h36MEfB2AAAAAAAAAAA.pem',
            'password': '1234'}
# Number of CE input
numInp = 1
interfaceDict = {'in': [dict0], 
                 'out': dict4}
ceDict = {'interface': interfaceDict}
## Change the name of the algorithm to test it out.
algorithmTest = Anom(numInp, 0,[0], ceDict)

print "Collecting training and test data from GDP"
# Use the collect data routine to fetch training data in separate lists
# for input and output
# TODO test on larger datasets
trainRecStart = 500
trainRecStop = 8001
batchSize = 200
numTrainingSamples = trainRecStop - trainRecStart + 1
inDataTrain, outDataTrain = algorithmTest.interface.collectData(trainRecStart, trainRecStart + batchSize)
print inDataTrain.shape
print "Done: collecting data from Database"

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


plugIP1 = "192.168.1.46"
plugIP2 = "192.168.1.51"

dg = time.time()
startCount = dg
#algorithmTest.interface.controlPlug("75.80.49.247","9999","off")
#demoProximity.test(plugIP1,plugIP2,"off")

while trainRecStart < trainRecStop:
    if algorithmTest.executeAndCluster(data[i][0]) == 1:
        print int(algorithmTest.executeAndCluster(data[i][0])), inDataTrain[i][0], data[i][0]
#        demoProximity.test(plugIP1,plugIP2,"on")
#        algorithmTest.interface.controlPlug("192.168.1.51","9999","on")
        startCount = time.time()
    else:
        if time.time()-startCount > 1:
            startCount = time.time()
#            demoProximity.test(plugIP1,plugIP2,"off")
#            algorithmTest.interface.controlPlug("75.80.49.247","9999","off")
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
#    time.sleep(0.1)
#demoProximity.test(plugIP1,plugIP2,"off")

