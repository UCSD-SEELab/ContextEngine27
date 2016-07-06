import gdp
import json
from ioClass import ioClass
import numpy as np
## This class creates a tester instance for supervised learning models.
## each input as well as output is defined with gcl log name, JSON 
## parameter in that log, and their delay from current sample. For training 
## and testing, a range of record numbers is specified.


def checkDictKeys(d):
    if 'gcl' in d and 'param' in d and 'lag' in d:
        return
    else:
        raise ValueError ('I/O dictionary does not contain required'\
                          ' keys: gclName, paramName, lag')

def collectTrace(gclHandle, param, start, stop):
    # this is the actual subscribe call
    gclHandle.multiread(start, stop-start+1)

    # timeout
    t = {'tv_sec':0, 'tv_nsec':500*(10**6), 'tv_accuracy':0.0}
    data = []
    while True:
        # This could return a None, after the specified timeout
        event = gdp.GDP_GCL.get_next_event(t)
        if event is None or event["type"] == gdp.GDP_EVENT_EOS:
            break
        datum = event["datum"]
        handle = event["gcl_handle"]
        data.append(float(json.loads(datum['data'])[param]))
    return data


class gdpSupervisedTester (object):
    def __init__(self, numInputs = None, inDicts = None, outDict = None):
        if numInputs is None:
            raise ValueError ('Number of inputs must be provided.')

        if inDicts is None:
            raise ValueError ('Input description dictionary list'\
                              ' must be provided.')
        elif len(inDicts) != numInputs:
            raise ValueError ('Length of input description dictionary'\
                              ' list and '\
                              'number of inputs mismatch: %d and %d'\
                              % (len(inTuples), numInputs))
        else:
            for d in inDicts:
                if isinstance(d, dict):
                    checkDictKeys(d)
                else:
                     raise ValueError ('Input description must be a'\
                                       ' dictionary object')

        if outDict is None:        
            raise ValueError ('Output description dictionary'\
                              ' must be provided.')
        elif isinstance(outDict, dict):
            checkDictKeys(outDict)
        else:
             raise ValueError ('Output description must be a'\
                               ' dictionary object')


        self.inObjs = []
        for d in inDicts:
            self.inObjs.append(ioClass(d['gcl'], d['param'], d['lag']))
        self.outObj = ioClass(outDict['gcl'], outDict['param'],
                              outDict['lag'])


    def collectData(self, start, stop):
        inData = []
        for inObj in self.inObjs:
            param = inObj.param
            handle = inObj.gclHandle            
            lag = inObj.lag
            trace = collectTrace(handle, param, start - lag, stop - lag)
            inData.append(trace)
    
        param = self.outObj.param
        handle = self.outObj.gclHandle            
        lag = self.outObj.lag
        outData = collectTrace(handle, param, start - lag, stop - lag)
        return np.array(inData).T, np.array(outData)
        

#        if (trainRecStart is None or trainRecStop is None or
#            testRecStart is None or testRecStop is None):  
#            raise ValueError ('Training and test record start and end fields'\
#                              ' must be provided')
#        elif trainRecStart > trainRecStop:
#            raise ValueError ('Training end record must be after training'\
#                              ' start record: %d and %d' %(trainRecStart, \
#                              trainRecStop))
#        elif testRecStart > testRecStop:
#            raise ValueError ('Test end record must be after test'\
#                              ' start record: %d and %d' %(testRecStart, \
#                              testRecStop))
