import csv
import datetime
import math
import numpy as np
import sys, os
import pickle
import time

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python/Tesla'));
sys.path.insert(1, os.path.join(sys.path[0], '../python/VLR'));
sys.path.insert(1, os.path.join(sys.path[0], '../python'));


## Import your algorithms here.
from Tesla import Tesla
from VLR import VLR
from ContextEngineBase import Complexity

## For different tests, these values will vary.
inputFilePath = "VLRTestInput.csv"
outputFilePath = "VLRTestOutput.csv"
complexity = Complexity.firstOrder;
numTrainingSamples = 110;
numExecuteSamples = 110;

inputFile = open(inputFilePath);
outputFile = open(outputFilePath);
inputReader = csv.reader(inputFile);
outputReader = csv.reader(outputFile);

## Change the name of the algorithm to test it out.
algorithmTest = VLR(Complexity.firstOrder, 1, 0, [0], {});
teslaTimestamps = {};
knnTimestamps = {};
vlrTimestamps = {};

for trainingSample in range(numTrainingSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        input1 = str(inputRow[0]);
        output = str(outputRow[0]);

        firstTS = time.time();
        algorithmTest.addSingleObservation([input1], output);
        secondTS = time.time();
        vlrTimestamps["load" + str(trainingSample)] = secondTS - firstTS;

firstTS = time.time();
algorithmTest.train();
secondTS = time.time();
vlrTimestamps["train"] = secondTS - firstTS;

for executeSample in range(numExecuteSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        input1 = str(inputRow[0]);
        output = str(outputRow[0]);

        firstTS = time.time();
        theor = algorithmTest.execute([input1]);
        secondTS = time.time();
        vlrTimestamps["test" + str(executeSample)] = secondTS - firstTS;
        vlrTimestamps["delta" + str(executeSample)] = 1 if theor != output else 0;
        print("Actual: " + output + " Predicted: " + theor)

netLoadingTime = 0;
for i in range(numTrainingSamples):
    netLoadingTime += vlrTimestamps["load" + str(i)];

netExecuteTime = 0;
runningMAE = 0.0;
for i in range(numExecuteSamples):
    netExecuteTime += vlrTimestamps["test" + str(i)];
    runningMAE += vlrTimestamps["delta" + str(i)];

runningMAE = runningMAE/(1.0*numExecuteSamples);

print("Loading time (tot): " + str(netLoadingTime) + " seconds");
print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds");
print("Training time: " + str(vlrTimestamps["train"]) + " seconds");
print("Execute time (tot): " + str(netExecuteTime) + " seconds");
print("Execute time (avg): " + str(netExecuteTime/(1.0*numExecuteSamples)) + " seconds");
print("MAE: " + str(runningMAE));
