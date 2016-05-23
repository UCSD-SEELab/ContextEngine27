import csv
import datetime
import math
import numpy as np
import os.path
import pickle
import time

from Tesla import Tesla

class PecanStreetCE():

    def __init__(self, funcOrder=3, numOfInputs=2, numHistoryStates=0):
        self.inputData = []
        self.outputData = []
        self.flexCE = Tesla(order=funcOrder, numInputs=(numOfInputs+numHistoryStates));
        self.aggregatedError = 0.0;
        self.aggregatedCount = 0;
        self.errorNumerator = 0.0;
        self.errorDenominator = 0;
        self.predictedList = [];
        self.actualList = [];
        self.testSetPredictedList = [];
        self.testSetActualList = [];
        self.numInputs = numOfInputs;
        self.numHistoryStates = numHistoryStates;

    def runTesla(self, csvFilepath):
        with open(csvFilepath) as csvFile:
            reader = csv.reader(csvFile);
            i = 0;
            for row in reader:
                inputList = [];
                historyList = [];
                outputValue = 0.0;

                if (i != 0 and i < self.numHistoryStates):
                    self.predictedList.append(0.0);
                    self.actualList.append(float(row[self.numInputs]));  
                elif (i != 0):
                    # Append the appropriate number of values from the CSV file to the input list.
                    for j in range(0,self.numInputs):
                        inputList.append(float(row[j]));

                    # Generate a list of history states to append to the inputs
                    for k in range(0, self.numHistoryStates):
                        historyList.append(-1-k);

                    # Append the history state as an additional inputs.
                    inputList += historyList;
                    outputValue = float(row[self.numInputs]);

                    self.inputData.append(inputList);
                    self.outputData.append(outputValue);

                if (i >= self.numHistoryStates and i <= 17500):
                    self.flexCE.addSingleObservation(inputList,
                                                     outputValue);
                    # Append garbage data to predicted, since this is training.
                    self.predictedList.append(0.0);
                    self.actualList.append(outputValue);

                elif (i > 17500 and i <= 35000):
                    predicted = self.flexCE.test(inputList);
                    if (predicted < 0):
                        predicted = 0.0;
                    actual = outputValue;

                    self.aggregatedError += pow(actual-predicted, 2);
                    self.aggregatedCount += 1;

#                    print(str(actual), "\t", str(predicted))
                    self.errorNumerator += abs((actual-predicted));
                    self.errorDenominator += 1;

                    self.predictedList.append(predicted);
                    self.actualList.append(actual);
                    self.testSetPredictedList.append(predicted);
                    self.testSetActualList.append(actual);

                elif (i > 35000):
                    print(str(time.clock()));
                    break;

                if (i == 17500):
                    print("Training data loaded");
                    startTime = time.clock()
                    self.flexCE.train();
                    elapsedTime = time.clock() - startTime;
                    print("CE trained, elapsed time:",
                          str(elapsedTime));
                    print(str(time.clock()));
                i+=1;

clotheswasher = PecanStreetCE();
clotheswasher.runTesla("../../traces/PecanStreet/traces/93/93.clotheswasher1.training.csv");
clotheswasherMean = (sum(clotheswasher.testSetActualList)/float(len(clotheswasher.testSetActualList)));
print(str(pow(clotheswasher.aggregatedError/clotheswasher.aggregatedCount,0.5)), ":",
           str(clotheswasherMean));
print("Error: ",
      str((pow(clotheswasher.aggregatedError/clotheswasher.aggregatedCount,0.5)/clotheswasherMean)),
      "\n");
print("Error: ",
      str(clotheswasher.errorNumerator/(clotheswasherMean*clotheswasher.errorDenominator)),
      "\n");

##clotheswasher = PecanStreetCE(numHistoryStates=4);
##clotheswasher.runTesla("../../traces/PecanStreet/traces/93/93.clotheswasher1.training.csv");
##clotheswasherMean = (sum(clotheswasher.testSetActualList)/float(len(clotheswasher.testSetActualList)));
##print(str(pow(clotheswasher.aggregatedError/clotheswasher.aggregatedCount,0.5)), ":",
##           str(clotheswasherMean));
##print("Error: ",
##      str((pow(clotheswasher.aggregatedError/clotheswasher.aggregatedCount,0.5)/clotheswasherMean)),
##      "\n");
##print("Error: ",
##      str(clotheswasher.errorNumerator/(clotheswasherMean*clotheswasher.errorDenominator)),
##      "\n");

dishwasher = PecanStreetCE();
dishwasher.runTesla("../../traces/PecanStreet/traces/93/93.dishwasher1.training.csv");
dishwasherMean = (sum(dishwasher.testSetActualList)/float(len(dishwasher.testSetActualList)));
print(str(pow(dishwasher.aggregatedError/dishwasher.aggregatedCount,0.5)), ":",
           str(dishwasherMean));
print("Error: ",
      str((pow(dishwasher.aggregatedError/dishwasher.aggregatedCount,0.5)/dishwasherMean)),
      "\n");
print("Error: ",
      str(dishwasher.errorNumerator/(dishwasherMean*dishwasher.errorDenominator)),
      "\n");

dryer = PecanStreetCE();
dryer.runTesla("../../traces/PecanStreet/traces/93/93.dryer1.training.csv");
dryerMean = (sum(dryer.testSetActualList)/float(len(dryer.testSetActualList)));
print(str(pow(dryer.aggregatedError/dryer.aggregatedCount,0.5)), ":",
           str(dryerMean));
print("Error: ",
      str((pow(dryer.aggregatedError/dryer.aggregatedCount,0.5)/dryerMean)),
      "\n");
print("Error: ",
      str(dryer.errorNumerator/(dryerMean*dryer.errorDenominator)),
      "\n");

microwave = PecanStreetCE();
microwave.runTesla("../../traces/PecanStreet/traces/93/93.microwave1.training.csv");
microwaveMean = (sum(microwave.testSetActualList)/float(len(microwave.testSetActualList)));
print(str(pow(microwave.aggregatedError/microwave.aggregatedCount,0.5)), ":",
           str(microwaveMean));
print("Error: ",
      str((pow(microwave.aggregatedError/microwave.aggregatedCount,0.5)/microwaveMean)),
      "\n");
print("Error: ",
      str(microwave.errorNumerator/(microwaveMean*microwave.errorDenominator)),
      "\n");

oven = PecanStreetCE();
oven.runTesla("../../traces/PecanStreet/traces/93/93.oven1.training.csv");
ovenMean = (sum(oven.testSetActualList)/float(len(oven.testSetActualList)));
print(str(pow(oven.aggregatedError/oven.aggregatedCount,0.5)), ":",
           str(ovenMean));
print("Error: ",
      str((pow(oven.aggregatedError/oven.aggregatedCount,0.5)/ovenMean)),
      "\n");
print("Error: ",
      str(oven.errorNumerator/(ovenMean*oven.errorDenominator)),
      "\n");

##
##secondStage = PecanStreetCE(funcOrder=1, numOfInputs=5);
##for i in range(0, len(clotheswasher.outputData)-1):
##    inputList = [clotheswasher.outputData[i],
##                 dishwasher.outputData[i],
##                 dryer.outputData[i],
##                 microwave.outputData[i],
##                 oven.outputData[i]];
##    outputValue = clotheswasher.outputData[i] + \
##                  dishwasher.outputData[i] + \
##                  dryer.outputData[i] + \
##                  microwave.outputData[i] + \
##                  oven.outputData[i];
##
##    if (i <= 17499):
##        secondStage.flexCE.addSingleObservation(inputList, outputValue);
##    elif (i > 17499 and i <= 34999):
##        predictedInputList = [clotheswasher.predictedList[i],
##                 dishwasher.predictedList[i],
##                 dryer.predictedList[i],
##                 microwave.predictedList[i],
##                 oven.predictedList[i]]
##        predicted = secondStage.flexCE.test(predictedInputList);
##        actual = outputValue;
##
##        secondStage.aggregatedError += pow(actual - predicted, 2);
##        secondStage.aggregatedCount += 1;
##
##        secondStage.predictedList.append(predicted);
##        secondStage.actualList.append(actual);
##    elif (i > 34999):
##        print(str(time.clock()));
##        break;
##    
##    if (i == 17499):
##        print("Training data loaded");
##        startTime = time.clock()
##        secondStage.flexCE.train();
##        elapsedTime = time.clock() - startTime;
##        print("CE trained, elapsed time:",
##              str(elapsedTime));
##        print(str(time.clock()));
##
##secondStageMean = (sum(secondStage.actualList)/float(len(secondStage.actualList)));
##print("Accuracy: ",
##      str(100.0-pow((secondStage.aggregatedError/secondStage.aggregatedCount),0.5)*100.0),
##      "\n");
##
##
##
##singleStage = PecanStreetCE(numOfInputs=6);
##singleStage.runTesla("../../traces/PecanStreet/traces/93/93.all.training.csv");
##singleStageMean = (sum(singleStage.actualList)/float(len(singleStage.actualList)));
##print("Accuracy: ",
##      str(100.0-pow((singleStage.aggregatedError/singleStage.aggregatedCount),0.5)*100.0),
##      "\n");
##
