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
dict0 = {'source': 'GDP_I',
        'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e5300003',
        'param': 'temperature_celcius',
          'lag': 0,
          'norm': 'lin'}
dict1 = {'source': 'GDP_I',
        'gcl': 'edu.berkeley.eecs.bwrc.device.c098e530005d',
        'param': 'temperature_celcius',
          'lag': 0,
          'norm': 'lin'}
#dict2 = {'gcl': 'edu.berkeley.eecs.bwrc.device.c098e570008f',
#        'param': 'apparent_power',
#          'lag': 0,
#          'norm': 'lin'}
dict4 = {'sink': 'Console', # Console not yet defined`
        'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e5300003',
          'param': 'temperature_celcius',
          'lag': 4,
          'norm': '',
          'key': 'DgAAAOhbtHYAAAAA-Fm0diD2h36MEfB2AAAAAAAAAAA.pem',
          'password': '1234'}
# Number of CE input
numInp = 2
interfaceDict = {'in': [dict0, dict1], 
                 'out': dict4}
ceDict = {'interface': interfaceDict}
## Change the name of the algorithm to test it out.
algorithmTest = Anom(numInp, 0,[0, 0], ceDict)
# subscribe to input log
algorithmTest.streamInputInit(0)
algorithmTest.streamInputInit(1)
#algorithmTest.streamInputInit(2)
# Get the latest data point, extract latest recno, train on the most
# recent batch of data prior to online run.
i = 0
while i < 20:
    event = gdp.GDP_GCL.get_next_event(None)
    print
    print i, event
    i = i + 1

