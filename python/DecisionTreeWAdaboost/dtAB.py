# Wanlin Cui

import numpy as np
import math
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from ContextEngineBase import ContextEngineBase
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

## Implementation of the DecisionTree algorithm:
class DecisionTreeAB(ContextEngineBase):
    decTreeAB = None
    y_Test = np.empty([0])
    
    def __init__(self, numInputs, outputClassifier, inputClassifiers, appFieldsDict):
        ContextEngineBase.__init__(self, numInputs, outputClassifier, inputClassifiers, appFieldsDict)

        self.decTreeAB = AdaBoostClassifier(DecisionTreeClassifier(max_depth=2))
        
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
        if self.outputClassifier == 0:
            raise ValueError('Decision Tree Classifier (w/ Adaboost) model output\
                     must be defined as discrete.')
        if (self.numObservations > 0):
            #print("Training started");
            self.decTreeAB.fit(self.observationMatrix, self.outputVectorIdx);
            return True;
        else:
            print("Not enough observations to train!");
            return False;
    
    def execute(self, inputObsVector):
        if(len(inputObsVector) == self.numInputs):
            #print("Begin execute");
            #x_Test = np.vstack((self.x_Test,inputObsVector));
            x_Test = np.reshape(inputObsVector,(1,self.numInputs));
            self.y_Test = self.decTreeAB.predict(x_Test);
            return self.y_Test;
        else:
            print("Wrong dimensions, fail to execute");
            return None;

