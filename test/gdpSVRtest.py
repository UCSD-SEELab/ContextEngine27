import csv
import datetime
import math
import numpy as np
import sys, os
import pickle
import time
import gdp

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python'))
sys.path.insert(1, os.path.join(sys.path[0], '../python/Svr'))
## Test class path 
sys.path.insert(1, os.path.join(sys.path[0], 'gdpTestClass'))


## Import your algorithms here.
from svr import SVR
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
dict1 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 1}
dict2 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 2}
dict3 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 3}
dict4 = {'gcl': 'edu.berkeley.eecs.swarmlab.device.c098e570002b',
          'param': 'apparent_power',
          'lag': 4}
# Number of CE input
numInp = 4
# Instantiate gdpSupervisedTester which creates all input and 
# output IOClass objects
gdpTest = gdpSupervisedTester(numInp, [dict1, dict2, dict3, dict3], dict0)
print "Collecting training and test data from GDP"
# Use the collect data routine to fetch training data in separate lists
# for input and output
# TODO fix list - int error in large datasets.
# TODO test on larger datasets
trainRecStart = 100
trainRecStop = 200
numTrainingSamples = trainRecStop - trainRecStart + 1
inDataTrain, outDataTrain = gdpTest.collectData(trainRecStart, trainRecStop)
# Use the collect data routine to fetch test data in separate lists
# for input and output
testRecStart = 201
testRecStop = 240
numExecuteSamples = testRecStop - testRecStart + 1
inDataTest, outDataTest = gdpTest.collectData(testRecStart,testRecStop)

## NORMALIZATION
# TODO: Either create a method in class to do this, or make it 
# happen automatically before training.
# TODO: separate each feature's normalization!

avg = (sum(outDataTest) + sum(outDataTrain))\
        / (len(outDataTrain) + len(outDataTest))
std = np.std(np.append(outDataTest, outDataTrain))
inDataTrain = (np.asarray(inDataTrain) - float(avg)) / float(std)
inDataTest = (np.asarray(inDataTest) - float(avg)) / float(std)

# Creating classification labels from continues data
#outDataTrain = map(lambda x: int(x > avg), outDataTrain)
#outDataTest = map(lambda x: int(x > avg), outDataTest)
print "Done: collecting data from GDP"

print "Beginning loading and training"
# For testing purpose. print input for test data
# each line in output corresponds to one input data field (record)
# print inDataTest

## Change the name of the algorithm to test it out.
# IMPORTANT: outputClassifier is set to 2, because output is NOT continous
algorithmTest = SVR(complexity, numInp, 0, [0,0,0,0], {})
timestamps = {}
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
    theor = algorithmTest.execute(list(inDataTest[executeSample]))
    secondTS = time.time()
    timestamps["test" + str(executeSample)] = secondTS - firstTS
    timestamps["delta" + str(executeSample)] = \
            abs(outDataTest[executeSample] - theor)
    print outDataTest[executeSample], theor 
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

