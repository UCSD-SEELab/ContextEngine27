import numpy as np
import scipy
import math
from Anom import Anom
import Anomaly
import csv




inputs = []
targets = []

with open('Data.csv','rb') as f:
    reader = csv.reader(f)
    csvData = list(reader)

#Set data formats
time = [i[0] for i in csvData] 
data = [i[1] for i in csvData]

convert = 0
while (convert < len(data)):
    data[convert] = float(data[convert])
    convert = convert + 1

np.asarray(data)

mag = np.linalg.norm(data)


newData=np.array([0]*len(data))


anomalyDet = Anom (complexity = 0, numInputs = 1, outputClassifier = 0, inputClassifiers = [0], appFieldsDict = {})

for rec in data[0:1000]:
    anomalyDet.addSingleObservation([rec],0)
anomalyDet.train()
print "first train done!"
i = 0
for rec in data[1000:3200]:
    print anomalyDet.execute(rec)
    if i < 1000:
        anomalyDet.addSingleObservation([rec],0)
        i = i + 1
    else:
        i = 0
        anomalyDet.addSingleObservation([rec],0)
        anomalyDet.train()


#anomalyDet.execute(data)


