import numpy as np
import scipy
import math
import sys, os
import datetime
import time
import gdp

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python'))
sys.path.append("../python/AnomalyDetection")
## Test class path 
sys.path.insert(1, os.path.join(sys.path[0], 'gdpTestClass'))

# Import your algorithms here.
from Anom import Anom
import Anomaly
from ContextEngineBase import Complexity
## Test class import
from gdpSupervisedTester import gdpSupervisedTester
 

## For different tests, these values will vary.
complexity = Complexity.firstOrder

# Create dictionary object for each of the context engine I/Os
# each dictionary object includes: log name, JSON parameter in that log, lag
dict0 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 0}
dict4 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 4}
# Number of CE input
numInp = 1
# Instantiate gdpSupervisedTester which creates all input and 
# output IOClass objects
gdpTest = gdpSupervisedTester(numInp, [dict0], dict4)
print "Collecting training and test data from GDP"
# Use the collect data routine to fetch training data in separate lists
# for input and output
# TODO fix list - int error in large datasets.
# TODO test on larger datasets
trainRecStart = 1000
trainRecStop = 6001
batchSize = 100
numTrainingSamples = trainRecStop - trainRecStart + 1
inDataTrain, outDataTrain = gdpTest.collectData(trainRecStart, trainRecStart + batchSize)

print "Done: collecting data from GDP"

print "Beginning loading and training"
# For testing purpose. print input for test data
# each line in output corresponds to one input data field (record)
# print inDataTest

## Change the name of the algorithm to test it out.
# IMPORTANT: outputClassifier is set to 2, because output is NOT continous
algorithmTest = Anom(complexity, numInp, 0, [0], {})
timestamps = {}
# Add training data to CE object
for i in xrange(len(outDataTrain)):
    # recording time stamps before and after adding to measure load time
    firstTS = time.time()
    algorithmTest.addSingleObservation(inDataTrain[:][i], outDataTrain[i])
    secondTS = time.time()
    timestamps["load" + str(i)] = secondTS - firstTS
# Normalize the data
# TODO standard deviation
# TODO should we remember the average from last batch to normalize the next batch? because thresold computed with last batch....
avg = sum(inDataTrain) / float(len(inDataTrain))
std = np.std(inDataTrain)
data = inDataTrain
inDataTrain = [(rec - avg) / std for rec in inDataTrain]
# training CE using the added data, while the training time is measured
firstTS = time.time()
algorithmTest.train()
secondTS = time.time()

i = 0
while trainRecStart < trainRecStop:
    if algorithmTest.execute(inDataTrain[i][0]) == 1:
        print algorithmTest.execute(inDataTrain[i][0]), inDataTrain[i][0], data[i][0]
    if i < batchSize:
        i = i + 1
    else:
        i = 0
        trainRecStart = trainRecStart + batchSize
        inDataTrain, outDataTrain = gdpTest.collectData(trainRecStart, trainRecStart + batchSize)
        for j in xrange(len(outDataTrain)):
            algorithmTest.addSingleObservation(inDataTrain[:][j], outDataTrain[i])
        avg = sum(inDataTrain) / float(len(inDataTrain))
        std = np.std(inDataTrain)
        data = inDataTrain
        inDataTrain = [(rec - avg) / std for rec in inDataTrain]
        algorithmTest.train()

"""
timestamps["train"] = secondTS - firstTS
print "Done: loading and training"
print "Beginning execution"
runningTotal = 0
for executeSample in range(testRecStop - testRecStart + 1):
    # computing output of test data using trained CE (time measured)
    # Saving error for each test data.
    firstTS = time.time()
    theor = algorithmTest.execute(list(inDataTest[executeSample]))
    secondTS = time.time()
    timestamps["test" + str(executeSample)] = secondTS - firstTS
    timestamps["delta" + str(executeSample)] = \
            abs(algorithmTest.classify(outDataTest[executeSample], -1)\
                - theor)
    print algorithmTest.classify(outDataTest[executeSample], -1), theor
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
print("Normalize MAE: " + str(runningNMAE))
"""

