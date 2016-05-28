import csv
import datetime
import math
import numpy as np
import sys, os
import pickle
import time

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python/D-StreamII'));
sys.path.insert(1, os.path.join(sys.path[0], '../python'));

## Import your algorithms here.
from DStreamII import DStreamII
from ContextEngineBase import Complexity

## For different tests, these values will vary.
inputFilePath = "input.csv"
outputFilePath = "output.csv"
complexity = Complexity.firstOrder;
numTrainingSamples = 5;
numExecuteSamples = 25;

inputFile = open(inputFilePath);
outputFile = open(outputFilePath);
inputReader = csv.reader(inputFile);
outputReader = csv.reader(outputFile);

## Change the name of the algorithm to test it out.
dStreamIITest = DStreamII(0, 2, 0, [0, 0],{'gridSize': [1,1], 'gridUpperRange':[10,10], 'gridLowerRange':[0,0]});
dStreamIITimestamps = {};

for trainingSample in range(numTrainingSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        input1 = float(inputRow[0]);
        input2 = float(inputRow[1]);
        output = float(outputRow[0]);

        firstTS = time.time();
        dStreamIITest.addSingleObservation([input1, input2], output);
        secondTS = time.time();
        dStreamIITimestamps["load" + str(trainingSample)] = secondTS - firstTS;

firstTS = time.time();
dStreamIITest.train();
secondTS = time.time();
dStreamIITimestamps["train"] = secondTS - firstTS;

runningTotal = 0;
for executeSample in range(numExecuteSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        input1 = float(inputRow[0]);
        output = float(outputRow[0]);

        firstTS = time.time();
        dStreamIITest.execute([input1, input2]);
        theor = output;
        secondTS = time.time();
        dStreamIITimestamps["test" + str(executeSample)] = secondTS - firstTS;
        dStreamIITimestamps["delta" + str(executeSample)] = abs(output - theor);
        runningTotal += output;

dStreamIITest.printClusters()
avgActual = runningTotal/(1.0*numExecuteSamples);

netLoadingTime = 0;
for i in range(numTrainingSamples):
    netLoadingTime += dStreamIITimestamps["load" + str(i)];

netExecuteTime = 0;
runningMAE = 0.0;
for i in range(numExecuteSamples):
    netExecuteTime += dStreamIITimestamps["test" + str(i)];
    runningMAE += dStreamIITimestamps["delta" + str(i)];

runningMAE = runningMAE/(1.0*avgActual*numExecuteSamples);

print("Loading time (tot): " + str(netLoadingTime) + " seconds");
print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds");
print("Training time: " + str(dStreamIITimestamps["train"]) + " seconds");
print("Execute time (tot): " + str(netExecuteTime) + " seconds");
print("Execute time (avg): " + str(netLoadingTime/(1.0*numExecuteSamples)) + " seconds");
print("MAE: " + str(runningMAE));



                                                                            
