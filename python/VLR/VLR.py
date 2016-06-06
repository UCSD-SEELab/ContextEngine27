#!/usr/bin/env python

import sys, os
import csv
import time
import numpy as np
import math
import cv2
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn import cluster
from sklearn.externals import joblib
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler
sys.path.insert(1, os.path.join(sys.path[0], '..'));
from ContextEngineBase import ContextEngineBase

class VLR(ContextEngineBase):

    # Input observation array of descriptors
    x_Obs = [];

    # Output observation array
    y_Obs = [];

    # Feature extractor from keypoints
    fea_det = None;

    # Sampling density
    step_size = 5;

    # For k-means clustering
    k = 300;

    # Codebook of words
    voc = None;

    # SVM Classifier
    clf = None;

    # Scalar
    stdSlr = None;

    # Class labels
    classes_names = None;

    # Output observation array in numeric format
    image_classes = [];

    def __init__(self, complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict):
        ContextEngineBase.__init__(self,complexity, numInputs, outputClassifier, inputClassifiers, appFieldsDict)
        self.fea_det = cv2.xfeatures2d.SURF_create();
        self.numObservations = 0;
        self.classes_names = os.listdir("../python/VLR/dataset/")
        if True in appFieldsDict:
            self.clf, self.classes_names, self.stdSlr, self.k, self.voc = joblib.load("../python/VLR/bof.pkl")

    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    #  Load the image, detect keypoints, and extract dense-SIFT features.
    def addSingleObservation(self, newInputObs, newOutputObs): 
        if (len(newInputObs) == self.numInputs and type(newOutputObs) not in (tuple, list)):
            im = cv2.imread(newInputObs[0]);
            if im is None:
                print(newInputObs[0])
                sys.exit(1)
            kpts = [cv2.KeyPoint(x, y, self.step_size) for y in range(0, im.shape[0], self.step_size)
                                   for x in range(0, im.shape[1], self.step_size)] # detect kpts
            (kpts, des) = self.fea_det.compute(im, kpts) # compute dense features
            self.x_Obs.append((newInputObs[0], des));
            self.y_Obs.append(newOutputObs);
            self.numObservations += 1;
            self.image_classes.append(self.classes_names.index(newOutputObs));
        else:
            print("Wrong dimensions!");

    #  Add a set of training observations, with the newInputObsMatrix being a
    #  list of image paths, where the row magnitude must match numInputs,
    #  and the column magnitude must match the number of observations.
    #  and newOutputVector being a column vector of ground-truth labels.
    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        if(newInputObsMatrix.shape[1] == self.numInputs
            and newOutputVector.shape[0] == newInputObsMatrix.shape[0]):
            i = 0;
            for newInputVector in newInputObsMatrix:
                newOutputValue = newOutputVector[i];
                self.addSingleObservation(newInputVector, newOutputValue);
                i += 1;
        else:
            print("Wrong dimensions!");

    #  Stack the descriptors and whiten the features.
    def preprocess(self):
        descriptors = self.x_Obs[0][1];
        for image_path, descriptor in self.x_Obs[1:]:
            descriptors = np.vstack((descriptors, descriptor))
        print("preprocessing success")
        return whiten(descriptors)

    def softassign(self, descriptors):
        im_features = np.zeros((1, self.k), "float32")
        for i in range(len(descriptors)):
            descriptor = descriptors[i]
            s = 0
            temp = np.zeros((1, self.k), "float32")
            for j in range(self.k):
                dist = np.linalg.norm(descriptor - self.voc[j])
                s += dist
                temp[0][j] = dist
            for m in range(self.k):
                im_features[0][m] += 1.0 - temp[0][m]/s
        return im_features

    #  Quantize feature descriptors against the vocabulary of words i.e. constructing
    #  a BoW for each image, perform Tf-Idf vectorization, and scale the words.
    def quantize(self, descriptors):
        # Calculate the histogram of features
        im_features = np.zeros((self.numObservations, self.k), "float32") # bag of words for each image
        start_marker = 0
        for i in xrange(self.numObservations):
            end_marker = start_marker + len(self.x_Obs[i][1])
            #words, L2distance = vq(descriptors[start_marker:end_marker], self.voc) # hard quantization!
            im_features[i] = self.softassign(descriptors[start_marker:end_marker])
            start_marker = end_marker
            #for wd in words:
            #    im_features[i][wd] += 1
        print("quantizing success")
        # Perform Tf-Idf vectorization
        nbr_occurences = np.sum( (im_features > 0) * 1, axis = 0)
        idf = np.array(np.log((1.0*self.numObservations+1) / (1.0*nbr_occurences + 1)), 'float32')
        print("Tf-Idf vectorization success")
        # Scaling the words
        self.stdSlr = StandardScaler().fit(im_features)
        im_features = self.stdSlr.transform(im_features)
        print("scaling success")
        return im_features

    #  Training
    def train(self):
        if (self.numObservations > 0):
            descriptors = self.preprocess();
            #self.voc, variance = kmeans(descriptors, self.k) # codebook generation
            k_means = cluster.KMeans(n_clusters=self.k, n_init=1)
            k_means.fit(descriptors)
            self.voc = k_means.cluster_centers_.squeeze()
            if len(self.voc) != self.k:
                print("generate codebook fail " + str(len(self.voc)))
                sys.exit(1)
            print("generate codebook success")
            im_features = self.quantize(descriptors)
            # Train the linear SVM
            self.clf = LinearSVC()
            self.clf.fit(im_features, np.array(self.image_classes))
            print("SVM training success")
            # Save the SVM
            joblib.dump((self.clf, self.classes_names, self.stdSlr, self.k, self.voc), "../python/VLR/bof.pkl", compress=3)
            print("SVM saved")

        else:
            return False;

    #  Execute the trained classifier against the given test sample.
    #  inputObsVector is a path to the image file
    def execute(self, inputObsVector):
        if(len(inputObsVector) == self.numInputs):
            x_Test = [];
            im = cv2.imread(inputObsVector[0]);
            if im is None:
                print(inputObsVector[0])
                sys.exit(1)
            kpts = [cv2.KeyPoint(x, y, self.step_size) for y in range(0, im.shape[0], self.step_size)
                                   for x in range(0, im.shape[1], self.step_size)] # detect kpts
            (kpts, des) = self.fea_det.compute(im, kpts) # compute dense features
            des = whiten(des) # whiten features
            test_features = np.zeros((1, self.k), "float32") # bag of words
            test_features = self.softassign(des)
            #words, L2distance = vq(des, self.voc) # hard quantize
            #for wd in words:
            #    test_features[0][wd] += 1
            nbr_occurences = np.sum( (test_features > 0) * 1, axis = 0)
            idf = np.array(np.log((1.0*1+1) / (1.0*nbr_occurences + 1)), 'float32')
            test_features = self.stdSlr.transform(test_features)
            predictions = [self.classes_names[i] for i in self.clf.predict(test_features)]
            return predictions[0]
        else:
            print("Wrong dimensions, fail to execute");
            return None;


