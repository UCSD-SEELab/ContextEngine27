#!/usr/local/bin/python2.7

import argparse as ap
import cv2
import re
import imutils 
import numpy as np
import os
import operator
import time
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from pyimagesearch.helpers import sliding_window
from multiprocessing import Process, Queue

# Load the classifier, class names, scaler, number of clusters and vocabulary 
clf, classes_names, stdSlr, k, voc = joblib.load("bof.pkl")

# Get the path of the testing set
parser = ap.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
#group.add_argument("-t", "--testingSet", help="Path to testing Set")
group.add_argument("-i", "--image", help="Path to image")
parser.add_argument('-v',"--visualize", action='store_true')
args = vars(parser.parse_args())

# Get the path of the testing image(s) and store them in a list
image_paths = []
#if args["testingSet"]:
#    test_path = args["testingSet"]
#    try:
#        testing_names = os.listdir(test_path)
#    except OSError:
#        print "No such directory {}\nCheck if the file exists".format(test_path)
#        exit()
#    for testing_name in testing_names:
#        dir = os.path.join(test_path, testing_name)
#        class_path = imutils.imlist(dir)
#        image_paths+=class_path
#else:
image_paths = [args["image"]]
    
# Create feature extraction and keypoint detector objects
fea_det = cv2.xfeatures2d.SURF_create()

step_size = 5 # sampling density
win_size = [30, 45, 75, 135]

# List where all the descriptors are stored
#des_list = []

def predictor(im, w, queue):
    global fea_det
    global step_size
    global k
    global voc
    global clf
    global classes_names
    global stdSlr
    global image_paths
    best = 0
    for (x_pt, y_pt, window) in sliding_window(im, stepSize=16, windowSize=(w,w)):
        if window.shape[0] != w or window.shape[1] != w:
            continue
        kpts = [cv2.KeyPoint(x, y, step_size) for y in range(0, window.shape[0], step_size)
                                              for x in range(0, window.shape[1], step_size)]
        (kpts, des) = fea_det.compute(window, kpts) # compute dense descriptors
        des = whiten(des)
        test_features = np.zeros((len(image_paths), k), "float32")
        words, L2distance = vq(des, voc)
        for wd in words:
            test_features[0][wd] += 1
        nbr_occurences = np.sum( (test_features > 0) * 1, axis = 0)
        idf = np.array(np.log((1.0*len(image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')
        test_features = stdSlr.transform(test_features)
        probs = np.array(clf.predict_proba(test_features))
        ind = np.argmax(probs)
        max_prob = np.max(probs)
        if max_prob > best:
            predictions = (classes_names[ind], max_prob)
            best = max_prob
            #print(predictions)
    queue.put(predictions)

cv2.namedWindow("Window", cv2.WINDOW_NORMAL)
for image_path in image_paths:
    if image_path.endswith('.db'):
        continue
    im = cv2.imread(image_path)
    if im is None:
        print "No such file {}\nCheck if the file exists".format(image_path)
        exit()
    begintime = time.time()
    ground_truth = []
    path_list = re.split('/', image_path)
    for c in classes_names:
        if c in path_list:
            ground_truth.append(c)
            break

    queue = Queue()
    p0 = Process(target=predictor, args=(im,win_size[0],queue,))
    p1 = Process(target=predictor, args=(im,win_size[1],queue,))
    p2 = Process(target=predictor, args=(im,win_size[2],queue,))
    p3 = Process(target=predictor, args=(im,win_size[3],queue,))

    p3.start()
    p2.start()
    p1.start()
    p0.start()

    p3.join()
    p2.join()
    p1.join()
    p0.join()

    predictions = queue.get()
    while not queue.empty():
        p = queue.get()
        if p[1] > predictions[1]:
            predictions = p

#        for (x_pt, y_pt, window) in sliding_window(im, stepSize=16, windowSize=(w, w)):
#            if window.shape[0] != w or window.shape[1] != w:
#                continue
#            kpts = fea_det.detect(im)
#            kpts = [cv2.KeyPoint(x, y, step_size) for y in range(0, window.shape[0], step_size)
#                                   for x in range(0, window.shape[1], step_size)] # detect kpts
#            (kpts, des) = fea_det.compute(window, kpts) # compute dense features
#            des_list.append((image_path, des))   
    
# Stack all the descriptors vertically in a numpy array
#descriptors = des_list[0][1]
#for image_path, descriptor in des_list[1:]:
#    descriptors = np.vstack((descriptors, descriptor)) 

#print("stacking success")
#descriptors = whiten(descriptors) # whiten features
#            des = whiten(des)
# Calculate histogram of features
#            test_features = np.zeros((len(image_paths), k), "float32") # bag of words for each image
#start_marker = 0
#for i in xrange(len(image_paths)):
#    end_marker = start_marker + len(des_list[i][1])
#    words, L2distance = vq(descriptors[start_marker:end_marker], voc) # hard quantization!!!
#    words, L2distance = vq(des_list[i][1], voc) # hard quantization!!!
#    start_marker = end_marker
#            words, L2distance = vq(des, voc)
#            for wd in words:
#                test_features[wd] += 1

#print("quantizing success")
# Perform Tf-Idf vectorization
#            nbr_occurences = np.sum( (test_features > 0) * 1, axis = 0)
#            idf = np.array(np.log((1.0*len(image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')

#print("if-Idf vectorization success")
# Scale the features
#            test_features = stdSlr.transform(test_features)

#print("scaling success")
# Perform the predictions with probability estimates
#            probs = np.array(clf.predict_proba(test_features))
#            ind = np.argmax(probs)
#            max_prob = np.max(probs)
            #predictions =  [classes_names[i] for i in clf.predict_proba(test_features)]
#            if max_prob > best:
#                predictions = (classes_names[ind], max_prob)
#                best = max_prob
                #print(predictions)
    endtime = time.time()

#print("SVM prediction success")
# Visualize the results, if "visualize" flag set to true by the user
            #clone = im.copy()
            #cv2.rectangle(clone, (x_pt, y_pt), (x_pt + w, y_pt + w), (0, 255, 0), 2)
            #cv2.imshow("Window", clone)
            #key = cv2.waitKey(1) & 0xFF
            #if key == ord('q'):
            #    break
            #time.sleep(0.025)

#if args["visualize"]:
#    for image_path, prediction in zip(image_paths, predictions):
#        image = cv2.imread(image_path)
#        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
#        pt = (0, 3 * image.shape[0] // 4)
#        cv2.putText(image, prediction, pt ,cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0])
#        cv2.imshow("Image", image)
#        cv2.waitKey(3000)

# Validate
correct_count = 0
#for i in xrange(len(predictions)):
if predictions[0] == ground_truth[0]:
	correct_count = 1
#acc = float(correct_count)/float(len(predictions))
#print("Accuracy: %f" %acc)
#print("Ground truth is %s" %ground_truth[0])
#print("Final prediction is %s" %predictions[0])
print(correct_count)
#print(endtime - begintime) # in sec
cv2.destroyAllWindows()
