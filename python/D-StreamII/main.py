import numpy as np
from DStreamII import DStreamII


# D-StreamII training objects
trainer = DStreamII(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0, appFieldsDict= {'gridSize': [0.25], 'gridUpperRange':[25], 'gridLowerRange':[0]});

trainInputData = []
trainOutputData = []

# Train to determine the grid size
with open("trace.txt", mode='r') as fp:
    for line in fp:
        dataInfo = line.split()
        trainInputData.append(dataInfo)

with open("trace_obs.txt", mode='r') as fp:
    for line in fp:
        dataInfo = line.split()
        trainOutputData.append(dataInfo)
        
trainer.addBatchObservations(trainInputData, trainOutputData);

trainer.train();

inputData = []

#Execute D-Stream II clustering algorithm
with open("power_use.txt") as fp:
    for line in fp:
        dataInfo  = line.split()
        trainer.execute(dataInfo)

trainer.printClusters()
