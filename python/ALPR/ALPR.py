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

    # Trained classifier
    alpr = None;

    # Top n highest confidence predictions
    n = 5

    def __init__(self, complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict):
        ContextEngineBase.__init__(self,complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict)
        self.alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data")
        if not self.alpr.is_loaded():
            print("Error loading OpenALPR")
            sys.exit(1)
        self.alpr.set_top_n(self.n)
        self.alpr.set_default_region("va")

    #  Execute the trained classifier against the given test sample
    #  inputObsVector is a path to the video file
    def execute(self, inputObsVector):
        if(len(inputObsVector) == self.numInputs):
            y_Test = self.predict(inputObsVector);
            return y_Test;
        else:
            print("Wrong dimensions, fail to execute");
            return None;

    #  Grabs frames and returns top n predictions per frame.
    def predict(self, x_Test):
        cap = cv2.VideoCapture(x_Test[0])
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
