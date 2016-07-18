import datetime
import math
import numpy as np
import sys, os
import time
import gdp
## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python'))
sys.path.insert(1, os.path.join(sys.path[0], '../python/LinSVM'))
## Interface path 
sys.path.insert(1, os.path.join(sys.path[0], '../python/ContextEngineInterface'))

## Import your algorithms here.
from LinSVM import LinSVM
printFlag = True
timestamps = {}
# Create dictionary object for each of the context engine I/Os
# each dictionary object includes: log name, JSON parameter in that log, lag
dict0 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 0,
          'norm': 'none'}
dict1 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570008b',
          'param': 'apparent_power',
          'lag': 0,
          'norm': 'lin'}
dict2 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e5700088',
          'param': 'apparent_power',
          'lag': 0,
          'norm': 'lin'}
dict3 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570008e',
          'param': 'apparent_power',
          'lag': 0,
          'norm': 'lin'}
dict4 = {'gcl': 'edu.berkeley.eecs.bwrc.device.c098e570008f',
          'param': 'apparent_power',
          'lag': 0,
          'norm': 'lin'}
# Number of CE input
numInp = 4

interfaceDict = {"in":[dict1, dict2, dict3, dict4], 
                 "out":dict0}
# Pass Linear SVM model parameters with this dictionary
ceDict = {"interface": interfaceDict}
## Change the name of the algorithm to test it out
algorithmTest = LinSVM(numInp, 2, [0,4,2,6], ceDict)


# Instantiate gdpSupervisedTester which creates all input and 
# output IOClass objects
# gdpTest = gdpSupervisedTester(numInp, [dict1, dict2, dict3, dict3], dict0)
print "Collecting training and test data from GDP"
# Use the collect data routine to fetch training data in separate lists
# for input and output


# TODO test on larger datasets
trainRecStart = 2000
trainRecStop = 2400
numTrainingSamples = trainRecStop - trainRecStart + 1
inDataTrain, outDataTrain = algorithmTest.interface.collectData(trainRecStart, trainRecStop)
# Use the collect data routine to fetch test data in separate lists
# for input and output
testRecStart = 2401
testRecStop = 2600
numExecuteSamples = testRecStop - testRecStart + 1
inDataTest, outDataTest = algorithmTest.interface.collectData(testRecStart,testRecStop)

print "Done: collecting data from GDP"

print "Beginning loading and training"
# For testing purpose. print input for test data
# each line in output corresponds to one input data field (record)
# print inDataTest

# Add training data to CE object
for i in xrange(len(outDataTrain)):
    # recording time stamps before and after adding to measure load time
    firstTS = time.time()
    algorithmTest.addSingleObservation(inDataTrain[:][i], outDataTrain[i])
    secondTS = time.time()
    timestamps["load" + str(i)] = secondTS - firstTS

# training CE using the added data, while the training time is measured
firstTS = time.time()
algorithmTest.clusterAndTrain()
secondTS = time.time()

timestamps["train"] = secondTS - firstTS
print "Done: loading and training"
print "Beginning execution"
runningTotal = 0
for executeSample in range(testRecStop - testRecStart + 1):
    # computing output of test data using trained CE (time measured)
    # Saving error for each test data.
    firstTS = time.time()
    algoRes = algorithmTest.deNormalizeSnippet(
            algorithmTest.executeAndCluster(list(inDataTest[executeSample])),-1)
    secondTS = time.time() 
    timestamps["test" + str(executeSample)] = secondTS - firstTS
    timestamps["delta" + str(executeSample)] = \
            abs(np.asarray(algorithmTest.deNormalizeSnippet(\
                algorithmTest.classify(\
                algorithmTest.normalizeSnippet(\
                outDataTest[executeSample], -1), -1), -1))\
                - np.asarray(algoRes))
    print algorithmTest.deNormalizeSnippet(\
          algorithmTest.classify(\
          algorithmTest.normalizeSnippet(\
          outDataTest[executeSample], -1), -1), -1), \
          algoRes
    runningTotal += outDataTest[executeSample]
print "Done: execution"
# computing average of the output test data
avgActual = runningTotal/(1.0*numExecuteSamples)
# calculating the loading time of the whole training dataset
netLoadingTime = 0
for i in range(numTrainingSamples):
    netLoadingTime += timestamps["load" + str(i)];
# calculating the execution time and Normalized Mean Absolute Error
netExecuteTime = 0
runningNMAE = 0.0
for i in range(numExecuteSamples):
    netExecuteTime += timestamps["test" + str(i)]
    runningNMAE += timestamps["delta" + str(i)]
runningNMAE = runningNMAE/(1.0*avgActual*numExecuteSamples)

print("Loading time (tot): " + str(netLoadingTime) + " seconds")
print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds")
print("Training time: " + str(timestamps["train"]) + " seconds")
print("Execute time (tot): " + str(netExecuteTime) + " seconds")
print("Execute time (avg): " + str(netLoadingTime/(1.0*numExecuteSamples)) + " seconds")
print("Normalized MAE: " + str(runningNMAE))

