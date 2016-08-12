import gdp
from ioClass import ioClass
import numpy as np
## This class creates a tester instance for supervised learning models.
## each input as well as output is defined with gcl log name, JSON 
## parameter in that log, and their delay from current sample. For training 
## and testing, a range of record numbers is specified.


def checkDictKeys(d):
    if 'gcl' in d and 'param' in d and 'lag' in d and 'norm' in d:
        return
    else:
        raise ValueError ('I/O dictionary does not contain required'\
                          ' keys: gclName, paramName, lag, norm')



class ceInterface(object):
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
                    # TODO create a more general dictionary key check
                    # checkDictKeys(d)
                    if 'source' not in d:
                        raise ValueError ('Input dictionaries must'\
                                'contain source')
                else:
                     raise ValueError ('Input description must be a'\
                                       ' dictionary object')

        if outDict is None:        
            raise ValueError ('Output description dictionary'\
                              ' must be provided.')
        elif isinstance(outDict, dict):
            # TODO create a more general dictionary key check
            # checkDictKeys(outDict)
            if 'sink' not in outDict:
                raise ValueError ('Output Dictionary must contain sink')
            # TODO error for pasword and key missing
        else:
             raise ValueError ('Output description must be a'\
                               ' dictionary object')


        self.inObjs = []
        for d in inDicts:
            self.inObjs.append(ioClass(d['source'], d['name'], 
                            d['param'], d['lag'], d['norm']))
        self.outObj = ioClass(outDict['sink'], outDict['name'], 
                              outDict['param'], outDict['lag'], 
                              outDict['norm'], outDict['key'],
                              outDict['password'])


    def collectData(self, start, stop):
        inData = []
        for inObj in self.inObjs:
            trace = inObj.readLog(start, stop)
            inData.append(trace)
    
        outData = self.outObj.readLog(start, stop)
        # Change this line to accomodate different data types
        return np.array(inData).T, np.array(outData)
    
    # TODO function: collectDataByTime(self, timeStart, timeStop, timeStep)
    def collectDataByTime(self, timeStart, timeStop, timeStep):
        pass

    def collectDataIn(self, start, stop):
        inData = [] 
        for inObj in self.inObjs:
            trace = inObj.readLog(start, stop)
            inData.append(trace)
        return np.array(inData).T

    def outputData(self, data):
        self.outObj.write(data)

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
