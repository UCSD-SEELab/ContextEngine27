import csv
import datetime
import math
import numpy as np
import sys, os
import pickle
import time

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python/Tesla'));
sys.path.insert(1, os.path.join(sys.path[0], '../python/Knn'));
sys.path.insert(1, os.path.join(sys.path[0], '../python'));

## Import your algorithms here.
from Tesla import Tesla
## from Knn import Knn
from ContextEngineBase import Complexity

## For different tests, these values will vary.
inputFilePath = "3192_clothesWasher1_0_input.csv"
outputFilePath = "3192_clothesWasher1_0_output.csv"
complexity = Complexity.firstOrder;
numTrainingSamples = 800;
numExecuteSamples = 800;
numInputsToUse = 5;

inputFile = open(inputFilePath);
outputFile = open(outputFilePath);
inputReader = csv.reader(inputFile);
outputReader = csv.reader(outputFile);

## Change the name of the algorithm to test it out.
algorithmTest = Tesla(complexity, numInputsToUse, 0, [0]*numInputsToUse, {});
teslaTimestamps = {};
knnTimestamps = {};

print(algorithmTest.complexity);
print(algorithmTest.functionOrder);

for trainingSample in range(numTrainingSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        inputs = inputRow[:numInputsToUse];
        inputs = [float(x) for x in inputs];
#        input1 = float(inputRow[0]);
#        input2 = float(inputRow[1]);
        output = float(outputRow[0]);

        firstTS = time.time();
        algorithmTest.addSingleObservation(inputs, output);
#        algorithmTest.addSingleObservation([input1, input2], output);
        secondTS = time.time();
        teslaTimestamps["load" + str(trainingSample)] = secondTS - firstTS;

firstTS = time.time();
algorithmTest.train();
secondTS = time.time();
teslaTimestamps["train"] = secondTS - firstTS;

runningActual = [];
for executeSample in range(numExecuteSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        inputs = inputRow[:numInputsToUse];
        inputs = [float(x) for x in inputs];
#        input1 = float(inputRow[0]);
#        input2 = float(inputRow[1]);
        output = float(outputRow[0]);

        firstTS = time.time();
        theor = algorithmTest.execute(inputs);
#        theor = 0 if (theor < 0.0) else theor;
#        print(str(theor) + "\t" + str(output));
#        theor = algorithmTest.execute([input1, input2]);
        secondTS = time.time();
        teslaTimestamps["test" + str(executeSample)] = secondTS - firstTS;
        teslaTimestamps["delta" + str(executeSample)] = abs(output - theor);

        runningActual.append(output);

runningActualHigh = [x for x in runningActual if x > 0];
avgActual =  sum(runningActualHigh)/(1.0*len(runningActualHigh));

netLoadingTime = 0;
for i in range(numTrainingSamples):
    netLoadingTime += teslaTimestamps["load" + str(i)];

netExecuteTime = 0;
runningMAE = 0.0;
runningRMSE = 0.0;
for i in range(numExecuteSamples):
    netExecuteTime += teslaTimestamps["test" + str(i)];
    runningMAE += teslaTimestamps["delta" + str(i)];
    runningRMSE += pow(float(teslaTimestamps["delta" + str(i)]),2);

runningMAE = runningMAE/(1.0*avgActual*numExecuteSamples);
runningRMSE = pow((runningRMSE/numExecuteSamples),0.5)/avgActual;

print("Loading time (tot): " + str(netLoadingTime) + " seconds");
print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds");
print("Training time: " + str(teslaTimestamps["train"]) + " seconds");
print("Execute time (tot): " + str(netExecuteTime) + " seconds");
print("Execute time (avg): " + str(netLoadingTime/(1.0*numExecuteSamples)) + " seconds");
print("MAE: " + str(runningMAE));
print("RMSE: " + str(runningRMSE));
print("Correlation Values: " + str(algorithmTest.getCorrelationValues()));
