import sys, os
import math
import numpy as np
import csv
import subprocess

sys.path.insert(1, os.path.join(sys.path[0], '..'));
                
from ContextEngineBase import *

scriptCaller = "../../c/aes/aes.exe";
inputFileParam = "-i";
outputFileParam = "-o";
inputTrace = "input.csv";
outputTrace = "output.csv";

## Implementation of the TESLA algorithm: map input variables to output
## observations
class Tesla(ContextEngineBase):

    # Input and output observations tracker
    inputObs = {};
    outputObs = [];
    #  Constructor - the order and number of inputs are mandatory
    def __init__(self,
                 complexity,
                 numInputs,
                 outputClassifier,
                 inputClassifiers,
                 appFieldsDict):
        super(Tesla, self).__init__(complexity,
                     numInputs,
                     outputClassifier,
                     inputClassifiers,
                     appFieldsDict);

        # Keep track of the observations seen so far.
        for i in range(0, len(self.numInputs)):
            self.inputObs[i] = [];

    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    def addSingleObservation(self, newInputObs, newOutputObs):
        if (len(newInputObs) == self.numInputs
            and type(newOutputObs) not in (tuple, list)):
            for i in range(0, len(newInputObs)):
                self.inputObs[i].append(newInputObs[i]);

            self.outputObs.append[newOutputObs];

        else:
            print("Wrong dimensions! Expected ",
                  str(self.numInputs),
                  ", got ",
                  str(len(newInputObs)));


    #  Add a set of training observations, with the newInputObsMatrix being a
    #  set of correctly-sized vectors and newOutputVector being a vector of
    #  individual values.
    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        for newInputVector in newInputObsMatrix:
            outputValue = newOutputVector.pop();
            self.addSingleObservation(newInputVector, outputValue);

    #  Train the coefficients on the existing observation matrix if there are
    #  enough observations.
    def train(self):
        with open(inputTrace, 'w') as csvFile:
            inputCSVWriter = csv.writer(csvFile, quoting=csv.QUOTE_MINIMAL);
            for i in range(0, len(self.outputObs)):
                inputRow = [];
                for key in self.inputObs:
                    inputRow.append(self.inputObs[key][i]);
                inputCSVWriter.writerow(inputRow);
        with open(outputTrace, 'w') as csvFile:
            outputCSVWriter = csv.writer(csvFile, quoting=csv.QUOTE_MINIMAL);
            for i in range(0, len(self.outputObs)):
                outputCSVWriter.writerow([self.outputObs[i]]);
        
    #  Test the trained matrix against the given input observation
    def execute(self, inputObsVector):
        with open(inputTrace, 'a') as csvFile:
            inputCSVWriter = csv.writer(csvFile, quoting=csv.QUOTE_MINIMAL);
            inputCSVWriter.writerow(inputObsVector);
        
        return subprocess.run(args=[scriptCaller,
                                    inputFileParam,
                                    inputTrace,
                                    outputFileParam,
                                    outputTrace],
                              stdout=subprocess.PIPE);
