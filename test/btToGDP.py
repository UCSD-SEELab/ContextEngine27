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
dict0 = {'source': 'BT_I',
        'name': '20:91:48:A8:E4:0A',
        'param': 'temperature_celcius',
          'lag': 0,
          'norm': 'lin'}
dict1 = {'source': 'GDP_I',
        'name': 'edu.berkeley.eecs.swarmlab.device.c098e5300003',
        'param': 'temperature_celcius',
          'lag': 0,
          'norm': 'lin'}
dict4 = {'sink': 'GDP_O',
          'name': 'tCcbytv6gY0BdzvMx_JHw9ovPGwcpzvptFJiZ1k2u7Y',
          'param': 'temperature_celcius',
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
# subscribe to input log
algorithmTest.streamInputInit(0)

for i in xrange(2000):
    char = sock.recv(1)
    if char == '\r':
        j = j + 1
        print '%dth input' %j
        print data
        data = ''
    else:
        data = data + char
sock.close()
                                                                 


# Get the latest data point, extract latest recno, train on the most
# recent batch of data prior to online run.
event = gdp.GDP_GCL.get_next_event(None)
print event
batchSize = 8
trainRecStart = event['datum']['recno'] - batchSize
print "Collecting initial training data from GDP"
# Use the collect data routine to fetch training data in separate lists
# for input and output
##numTrainingSamples = trainRecStop - trainRecStart + 1
inDataTrain = algorithmTest.interface.collectDataIn(trainRecStart, trainRecStart + batchSize - 1)

# Add training data to CE object
for i in xrange(len(inDataTrain)):
    # recording time stamps before and after adding to measure load time
    firstTS = time.time()
    # NOTE change 0 passed
    algorithmTest.addSingleObservation(inDataTrain[:][i], 0)
    secondTS = time.time()
    timestamps["load" + str(i)] = secondTS - firstTS

firstTS = time.time()
algorithmTest.clusterAndTrain()
secondTS = time.time()

i = 0
while i < 100:
    newDataPoint = algorithmTest.fetchOnlineData(0)
    algorithmTest.addSingleObservation([newDataPoint], 0)
    if True: #algorithmTest.executeAndCluster(newDataPoint) == 1:
        result = int(algorithmTest.executeAndCluster([newDataPoint]))
        print result, newDataPoint
        algorithmTest.interface.outputData(str(result)+'pad')
    if i < batchSize:
        i = i + 1
    else:
        i = 0
        algorithmTest.clusterAndTrain()

