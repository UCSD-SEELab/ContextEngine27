# Wanlin Cui
# Modified by Nima (to Wanlin: please contact me if something went wrong with the code because of this edit!)
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
import math
from sklearn import svm
from ContextEngineBase import ContextEngineBase

## Implementation of the SVR algorithm:
class SVR(ContextEngineBase):
    svrLinear = None
    y_Test = np.empty([0])

    def __init__(self, numInputs, outputClassifier, 
            inputClassifiers, appFieldsDict):
        ContextEngineBase.__init__(self, numInputs, 
                outputClassifier, inputClassifiers, appFieldsDict)
        self.numInputs = numInputs;
        self.outputClassifier = outputClassifier;
        self.inputClassifiersList = inputClassifiers;
        self.customFieldsDict = appFieldsDict;
        if 'kernel' in appFieldsDict:
            svrKernel = appFieldsDict['kernel']
        else:
            svrKernel = 'linear'
        if 'degree' in appFieldsDict:
            svrDegree = appFieldsDict['degree']
        else:
            svrDegree = 1
        self.svrLinear = svm.SVR(kernel='rbf', degree = svrDegree)

    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        if(len(newInputObsMatrix.shape) == 2 and newInputObsMatrix.shape[1] == self.numInputs
            and newOutputVector.shape[0] == newInputObsMatrix.shape[0]):
            #print("All good!");
            newOutputVector = newOutputVector.ravel();
            i = 0;
            for newInputVector in newInputObsMatrix:
                newOutputValue = newOutputVector[i];
                self.addSingleObservation(newInputVector, newOutputValue);
                i += 1;
        else:
            print("Wrong dimensions!");

    def train(self):
        if (self.numObservations > 0):
            #print("Training started");
            self.svrLinear.fit(self.observationMatrix, self.outputVector);
            return True;
        else:
            print("Not enough observations to train!");
            return False;

    def execute(self, inputObsVector):
        if(len(inputObsVector) == self.numInputs):
            #print("Begin execute");
            #x_Test = np.vstack((self.x_Test,inputObsVector));
            x_Test = np.reshape(inputObsVector,(1,self.numInputs));
            self.y_Test = self.svrLinear.predict(x_Test);
            return self.y_Test;
        else:
            print("Wrong dimensions, fail to execute");
            return None;
