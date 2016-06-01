#!/usr/local/bin/python2.7

import argparse as ap
import cv2
import imutils 
import numpy as np
import os
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-t", "--trainingSet", help="Path to Training Set", required="True")
args = vars(parser.parse_args())

# Get the training classes names and store them in a list
train_path = args["trainingSet"]
training_names = os.listdir(train_path)

# Get all the path to the images and save them in a list
# image_paths and the corresponding label in image_paths
image_paths = []
image_classes = []
class_id = 0
for training_name in training_names:
    dir = os.path.join(train_path, training_name)
    class_path = imutils.imlist(dir)
    image_paths+=class_path
    image_classes+=[class_id]*len(class_path)
    class_id+=1

# Create feature extraction and keypoint detector objects
fea_det = cv2.xfeatures2d.SURF_create()

# List where all the descriptors are stored
des_list = []
step_size = 5

for image_path in image_paths:
	if image_path.endswith('.db'):
		continue
	im = cv2.imread(image_path)
#    kpts = fea_det.detect(im)
	if im is None:
		print(image_path)
	kpts = [cv2.KeyPoint(x, y, step_size) for y in range(0, im.shape[0], step_size) 
                                   for x in range(0, im.shape[1], step_size)] # detect kpts
	(kpts, des) = fea_det.compute(im, kpts) # compute dense features
#	(kpts, des) = fea_det.detectAndCompute(im, None)
	if des is None:
		print("des is null")
	des_list.append((image_path, des))   
	    
# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]
for image_path, descriptor in des_list[1:]:
    descriptors = np.vstack((descriptors, descriptor))  

print("stacking success")
# Perform k-means clustering
k = 300
descriptors = whiten(descriptors) # whiten features
voc, variance = kmeans(descriptors, k, 1) 

print("generate codebook success")
# Calculate the histogram of features
im_features = np.zeros((len(image_paths), k), "float32") # bag of words for each image
start_marker = 0
for i in xrange(len(image_paths)):
    end_marker = start_marker + len(des_list[i][1])
    words, L2distance = vq(descriptors[start_marker:end_marker], voc) # hard quantization!!!
#    words, L2distance = vq(des_list[i][1], voc) # hard quantization!!!
    start_marker = end_marker
    for w in words:
        im_features[i][w] += 1

print("quantizing success")
# Perform Tf-Idf vectorization
nbr_occurences = np.sum( (im_features > 0) * 1, axis = 0)
idf = np.array(np.log((1.0*len(image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')

print("if-Idf vectorization success")
# Scaling the words
stdSlr = StandardScaler().fit(im_features)
im_features = stdSlr.transform(im_features)

print("scaling success")
# Train the Linear SVM
#clf = LinearSVC()
clf = SVC(1.0, 'rbf', 3, 'auto', 0.0, True, True)
clf.fit(im_features, np.array(image_classes))

print("SVM training success")
# Save the SVM
joblib.dump((clf, training_names, stdSlr, k, voc), "bof.pkl", compress=3)    
    
print("SVM saved")
