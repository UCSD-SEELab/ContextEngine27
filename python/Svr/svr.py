# Wanlin Cui

import numpy as np
import math
from sklearn.svm import SVR
from ContextEngineBase import ContextEngineBase
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

## Implementation of the SVR algorithm:
class SVR(ContextEngineBase):

    def __init__(self, complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict):
		ContextEngineBase.__init__(self,complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict)
		self.svrLinear = SVR(kernel='rbf');

    def train(self):
		if (self.numObservations > 0):
			#print("Training started");
			self.svrLinear.fit(self.x_Obs, self.y_Obs);
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
