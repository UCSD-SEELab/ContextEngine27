#!/usr/bin/env python

import sys, os
import csv
import time
import numpy as np
import math
from openalpr import Alpr
import cv2

sys.path.insert(1, os.path.join(sys.path[0], '..'));

from ContextEngineBase import ContextEngineBase

class ALPR(ContextEngineBase):

	# Input observation array
	x_Obs = np.empty([0]);

	# Output observation array
	y_Obs = np.empty([0]);

	# Trained classifier
	alpr = None;

	# Top n highest confidence predictions
	n = 5

	def __init__(self, complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict):
		ContextEngineBase.__init__(self,complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict)
		#self.discreteOutputs = discreteOutputs;
		#3sself.discreteInputs = discreteInputs;
		self.x_Obs = np.empty([0,numInputs]);
		#self.x_Test = np.empty([0,numInputs]);
		self.alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data")
		if not self.alpr.is_loaded():
        		print("Error loading OpenALPR")
        		sys.exit(1)
		self.alpr.set_top_n(self.n)
		self.alpr.set_default_region("va")

	#  Add a new training observation. Requirements: newInputObs must be a
	#  row array of size numInputs. newOutputObs must be a single value.
	def addSingleObservation(self, newInputObs, newOutputObs): 
		# No training needed for OpenALPR classifier
		if (len(newInputObs) == self.numInputs and type(newOutputObs) not in (tuple, list)):
			self.x_Obs = np.vstack((self.x_Obs,newInputObs));
			self.y_Obs = np.append(self.y_Obs, newOutputObs);
			self.numObservations += 1;
		else:
			print("Wrong dimensions!");

	#  Add a set of training observations, with the newInputObsMatrix being a
	#  list of video paths, where the row magnitude must match numInputs,
	#  and the column magnitude must match the number of observations.
	#  and newOutputVector being a column vector of license plate strings
	def addBatchObservations(self, newInputObsMatrix, newOutputVector):
		# No training needed for OpenALPR classifier
		if(newInputObsMatrix.shape[1] == self.numInputs
			and newOutputVector.shape[0] == newInputObsMatrix.shape[0]):
			newOutputVector = newOutputVector.ravel();
			i = 0;
			for newInputVector in newInputObsMatrix:
				newOutputValue = newOutputVector[i];
				self.addSingleObservation(newInputVector, newOutputValue);
				i += 1;
		else:
			print("Wrong dimensions!");

	#  Training
	def train(self):
		# No training needed for OpenALPR classifier
		if (self.numObservations > 0):
 			return True;
		else:
			return False;

	#  Execute the trained classifier against the given input observation
	#  inputObsVector is a path to the video file
	def execute(self, inputObsVector):
		if(len(inputObsVector) == self.numInputs):
    		#x_Test = np.vstack((self.x_Test,inputObsVector));
			x_Test = np.reshape(inputObsVector,(1,self.numInputs));
			y_Test = self.predict(x_Test);
			return y_Test;
		else:
			print("Wrong dimensions, fail to execute");
			return None;

	def predict(self, x_Test):
		cap = cv2.VideoCapture(x_Test[0][0])
		if not cap.isOpened():
			print("vid open error")
			cap.open()
		fps = 25
		timedelta = 0
		detectCounter = [0]
		detectCounter[0] = 0
		plates_list = np.empty([0, self.n])
		while(cap.isOpened()):
			ret, frame = cap.read()
			if (detectCounter[0] < fps*timedelta):
				detectCounter[0] += 1
				continue
			detectCounter[0] = 0
			if ret:
				pretime = time.time()
				ret, enc = cv2.imencode("*.bmp", frame)
				results = self.alpr.recognize_array(bytes(bytearray(enc)))
				posttime = time.time()
				plates = np.empty([1,self.n], dtype='a5')
				for s in range(0, self.n):
					plates[0][s] = ""
				for plate in results['results']:
					i = 0
                        		for candidate in plate['candidates']:
                                		platenum = candidate['plate'].encode('ascii','ignore')
						plates[0][i] = platenum
						i += 1
                		timedelta = posttime - pretime # in seconds
				plates_list = np.vstack((plates_list, plates))
			else:
				break
		return plates_list;
