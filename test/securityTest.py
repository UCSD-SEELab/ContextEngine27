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

## For different tests, these values will vary.
inputFilePath = "DStreamIITestInput.csv"
outputFilePath = "DStreamIITestOutput.csv"
numTrainingSamples = 30;
numExecuteSamples = 100;

inputFile = open(inputFilePath);
outputFile = open(outputFilePath);
inputReader = csv.reader(inputFile);
outputReader = csv.reader(outputFile);

## Change the name of the algorithm to test it out.
dStreamIITest = DStreamII(0, 2, 0, [0, 0],{'gridSize': [1,1], 'gridUpperRange':[10,10], 'gridLowerRange':[0,0], 'key':'AESKEY'});
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

firstTS = time.time();
encryptedFile = dStreamIITest.encrypt(inputFilePath)
secondTS = time.time();
dStreamIITimestamps["encrypt"] = secondTS - firstTS;

firstTS = time.time();
decryptedFile = dStreamIITest.decrypt(inputFilePath+"EncryptOut.csv")
secondTS = time.time();
dStreamIITimestamps["decrypt"] = secondTS - firstTS;

netLoadingTime = 0;
for i in range(numTrainingSamples):
    netLoadingTime += dStreamIITimestamps["load" + str(i)];

netExecuteTime = 0;
runningMAE = 0.0;
for i in range(numExecuteSamples):
    netExecuteTime += dStreamIITimestamps["test" + str(i)];
    runningMAE += dStreamIITimestamps["delta" + str(i)];

runningMAE = runningMAE/(1.0*avgActual*numExecuteSamples);

encryptTime = dStreamIITimestamps["encrypt"];

decryptTime = dStreamIITimestamps["decrypt"];

print("Loading time (tot): " + str(netLoadingTime) + " seconds");
print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds");
print("Training time: " + str(dStreamIITimestamps["train"]) + " seconds");
print("Execute time (tot): " + str(netExecuteTime) + " seconds");
print("Execute time (avg): " + str(netLoadingTime/(1.0*numExecuteSamples)) + " seconds");
print("MAE: " + str(runningMAE));
print("Encrypt time (tot): " + str(encryptTime) + "seconds");
print("Decrypt time (tot): " + str(decryptTime) + "seconds");



                                                                            
