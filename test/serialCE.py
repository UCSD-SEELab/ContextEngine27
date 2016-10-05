import numpy as np
#import scipy
import math
import sys, os
import datetime
import time

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python'))
sys.path.insert(1, os.path.join(sys.path[0], '../python/AnomalyDetection'))
## Interface path
sys.path.insert(1, os.path.join(sys.path[0], '../python/ContextEngineInterface'))
print os.getpid()
# Import your algorithms here.
from Anom import Anom
import Anomaly
printFlag = True
timestamps = {}
# Create dictionary object for each of the context engine I/Os
# each dictionary object includes: log name, JSON parameter in that log, lag
dict0 = {'dir': 'in',
        'source': 'SER_I',
        #'name': 'edu.berkeley.eecs.swarmlab.device.c098e5300003',
        #'name': 'edu.berkeley.eecs.bwrc.device.c098e530005d',
        'name': '/dev/ttyACM0',
        #'param_lev1': 'temperature_celcius',
        #'param_lev2': None,
        'param_lev1': 'raw',
        'param_lev2': 'S1W',
          'lag': 0,
          'norm': 'lin'}
dict4 = {'dir': 'out',
          'sink': 'DRONE',
          'name': 'http://192.168.1.37:5000/launch',
          'param_lev1': None,
          'param_lev2': None,
          'lag': 0,
          'norm': '',
          }
dict5 = {'dir': 'out',
          'sink': 'GDP_O',
          'name': 'tCcbytv6gY0BdzvMx_JHw9ovPGwcpzvptFJiZ1k2u7Y',
          'param_lev1': 'raw',
          'param_lev2': 'S1A',
          'lag': 4,
          'norm': '',
          'key': 'DgAAAOhbtHYAAAAA-Fm0diD2h36MEfB2AAAAAAAAAAA.pem',
          'password': '1234'}
# Number of CE input
numInp = 1
interfaceDict = {'in': [dict0], 
                 'out': dict5}
ceDict = {'interface': interfaceDict}


## Change the name of the algorithm to test it out.

## TODO ERROR HAPPENS HERE!
algorithmTest = Anom(numInp, 0,[0], ceDict)

# subscribe to input log
#algorithmTest.streamInputInit(0)
algorithmTest.interface.writeDataToInputPort(0, '{"msg":"cmd","usb":1}')

batchSize =3 
trained = 0

i = 0
while 1:
    #print i
    newDataPoint = algorithmTest.fetchOnlineData(0)
    if newDataPoint != None:
        algorithmTest.addSingleObservation([float(newDataPoint)], 0)
        if trained == 1: #algorithmTest.executeAndCluster(newDataPoint) == 1:
            result = int(algorithmTest.executeAndCluster([newDataPoint]))
            #print result, newDataPoint
            algorithmTest.interface.outputData(str(result))
        if i < batchSize:
            i = i + 1
        else:
            i = 0
            algorithmTest.clusterAndTrain()
            trained = 1

