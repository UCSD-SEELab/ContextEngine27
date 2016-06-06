from openalpr import Alpr
from threading import Thread
from multiprocessing import Process
from multiprocessing.sharedctypes import Value
from ctypes import c_double
import threading
import argparse
import time
import numpy as np
import cv2
import sys
import Levenshtein
import csv
with open('VQ_KT_AGH_PARKING_LOT.csv', 'rb') as f:
    reader = csv.reader(f)
    plates_list = map(tuple, reader)

alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

n = 5
alpr.set_top_n(n)
alpr.set_default_region("va")

filepath = "/media/pi/F794-4B38/agh_src1_hrc0.avi"
src = filepath[24:28]
cap = cv2.VideoCapture(filepath)
#cap = cv2.VideoCapture("/media/pi/F794-4B38/agh_src1_hrc11.flv")
if not cap.isOpened():
    print("vid open error")
    cap.open()
#[item for item in plates_list if item[0] == src]

#resX = 240
#resY = 180
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('test.avi',fourcc, 20.0, (resX, resY))

fps = 25
detectCounter = [0]
#results = alpr.recognize_file("/media/pi/F794-4B38/ea7the.jpg")
#img = cv2.imread("/home/pi/ea7the.jpg", 0)
detectCounter[0] = 0
timedelta = Value(c_double, 0)
frame_count = Value(c_double, 0)
total_dist = Value(c_double, 0)
def predictor(frame):
    pretime = time.time()
    ret, enc = cv2.imencode("*.bmp", frame)
    results = alpr.recognize_array(bytes(bytearray(enc)))
    posttime = time.time()
    for plate in results['results']:
        with frame_count.get_lock():
            frame_count.value += 1
        dist_list = []
        for candidate in plate['candidates']:
            platenum = candidate['plate'].encode('ascii','ignore')
            print(platenum)
            print('Confidence: %f' %candidate['confidence'])
            #predist = time.time()
            dist = Levenshtein.distance("KMI77EV", platenum)
            #postdist = time.time()
            #print(postdist - predist)
            dist_list.append(dist)
            print('Edit distance: %d' %dist)
            print('\n')
        with total_dist.get_lock():
            total_dist.value += min(dist_list)
    timedelta.value = posttime - pretime # in seconds
    #print(timedelta)
    #cv2.waitKey(0)

#print('Initialization end')
#sys.exit(1)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
i = 0
begintime = time.time()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    if (detectCounter[0] < fps*timedelta.value):
        detectCounter[0] += 1
        continue
    detectCounter[0] = 0
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if i == 0:
            t0 = Process(target=predictor, args=(gray,))
            t0.start()
        if i == 1:
            t1 = Process(target=predictor, args=(gray,))
            t1.start()
        if i == 2:
            t2 = Process(target=predictor, args=(gray,))
            t2.start()
        if i == 3:
            t3 = Process(target=predictor, args=(gray,))
            t3.start()
        i += 1
        if i > 3:
            i = 0
            if t0 is None:
                print("t0 null")
            t0.join()
            if t1 is None:
                print("t1 null")
            t1.join()
            if t2 is None:
                print("t2 null")
            t2.join()
            if t3 is None:
                print("t3 null")
            t3.join()
        
#       pretime = time.time()
#       ret, enc = cv2.imencode("*.bmp", gray)
#       results = alpr.recognize_array(bytes(bytearray(enc)))
#       posttime = time.time()
#       for plate in results['results']:
#           frame_count += 1
#           dist_list = []
#           for candidate in plate['candidates']:
#               platenum = candidate['plate'].encode('ascii','ignore')
#               print(platenum)
#               print('Confidence: %f' %candidate['confidence'])
                #predist = time.time()
#               dist = Levenshtein.distance("KMI77EV", platenum)
                #postdist = time.time()
                #print(postdist - predist)
#               dist_list.append(dist)
#               print('Edit distance: %d' %dist)
#               print('\n')
#           total_dist += min(dist_list)
#       timedelta = posttime - pretime # in seconds
    #   print(timedelta)
    #   cv2.waitKey(0)
    else:
        break
    #out.write(frame)
t0.join()
t1.join()
t2.join()
t3.join()
endtime = time.time()
totalexectime = endtime - begintime # in seconds
#print(total_dist.value)
#print(frame_count.value)
avg_LED = total_dist.value / frame_count.value
print("Average LED: %f" %avg_LED)
print("Total exec time in sec: %f" %totalexectime)
#with open("LED_n" + str(n) + ".csv", 'wb') as f:
#   writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#   writer.writerow([avg_LED, totalexectime])

#alpr.unload()
cap.release()
cv2.destroyAllWindows()
