import csv
import datetime
import math
import numpy as np
import sys, os
import pickle
import time
import Levenshtein

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python/Tesla'));
sys.path.insert(1, os.path.join(sys.path[0], '../python/ALPR'));
sys.path.insert(1, os.path.join(sys.path[0], '../python'));


## Import your algorithms here.
from Tesla import Tesla
from ALPR import ALPR
from ContextEngineBase import Complexity

## For different tests, these values will vary.
inputFilePath = "ALPRTestInput.csv"
outputFilePath = "ALPRTestOutput.csv"
complexity = Complexity.firstOrder;
numTrainingSamples = 0;
numExecuteSamples = 2;

inputFile = open(inputFilePath);
outputFile = open(outputFilePath);
inputReader = csv.reader(inputFile);
outputReader = csv.reader(outputFile);

## Change the name of the algorithm to test it out.
algorithmTest = ALPR(Complexity.firstOrder, 1, 0, [0], {});
teslaTimestamps = {};
knnTimestamps = {};
alprTimestamps = {};

#for trainingSample in range(numTrainingSamples):
#    inputRow = next(inputReader);
#    outputRow = next(outputReader);
#    if (len(inputRow) > 0):
#        input1 = str(inputRow[0]);
#        output = str(outputRow[0]);

#        firstTS = time.time();
#        algorithmTest.addSingleObservation([input1], output);
#        secondTS = time.time();
#        alprTimestamps["load" + str(trainingSample)] = secondTS - firstTS;

#firstTS = time.time();
#algorithmTest.train();
#secondTS = time.time();
#alprTimestamps["train"] = secondTS - firstTS;

runningTotal = 0;
frames = 0
for executeSample in range(numExecuteSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        input1 = str(inputRow[0]);
        output = str(outputRow[0]);

        firstTS = time.time();
        theor = algorithmTest.execute([input1]);
        secondTS = time.time();
        alprTimestamps["test" + str(executeSample)] = secondTS - firstTS;
        print(theor)
        print("\n")
        for i in range(0, len(theor)):
            s = 0
            dist_list = []
            if theor[i][0] != "":
                frames += 1
            while s < 5 and theor[i][s] != "":
                dist_list.append(Levenshtein.distance(theor[i][s], output))
                s += 1
            if dist_list:
                runningTotal += min(dist_list)
        #alprTimestamps["delta" + str(executeSample)] = abs(output - theor);

#netLoadingTime = 0;
#for i in range(numTrainingSamples):
#    netLoadingTime += alprTimestamps["load" + str(i)];

netExecuteTime = 0;
#runningMAE = 0.0;
for i in range(numExecuteSamples):
    netExecuteTime += alprTimestamps["test" + str(i)];
    #runningMAE += alprTimestamps["delta" + str(i)];

#print("Loading time (tot): " + str(netLoadingTime) + " seconds");
#print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds");
#print("Training time: " + str(alprTimestamps["train"]) + " seconds");
print("Execute time (tot): " + str(netExecuteTime) + " seconds");
print("Execute time (avg): " + str(netExecuteTime/(1.0*numExecuteSamples)) + " seconds");
print("LED (avg): " + str(float(runningTotal)/float(frames)));
