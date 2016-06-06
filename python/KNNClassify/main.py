from scipy.io import wavfile
import csv
import numpy as np
import lpcdata
from KNNClassify  import KNNClassify 

knn = KNNClassify (complexity=0, numInputs=11, discreteOutputs=0, discreteInputs=0)

inputs = []
targets = []
with open('lpcInputTarget.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        inputs.append(map(float,row[0:11]))
        targets.append(map(int,row[11]))
inputs = np.asarray(inputs, dtype=np.float32)
targets = np.asarray(targets, dtype=np.float32)

knn.addBatchObservations(inputs,targets);

knn.train()

results = []
for i in range(1,11):
    filename='testData\\'+str(i)+'.wav'
    rate,data = wavfile.read(filename)
    l=lpcdata.lpc_ref(data,10)
    results.append(knn.execute(l)[0].item())


