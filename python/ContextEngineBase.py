from aenum import Enum

import math
import numpy as np
import sys
from sklearn.cluster import KMeans 
#sys.path.append("../python/Security/Encrypt/")
#from encrypt import encrypt
#from encrypt import rsaEncrypt
#sys.path.remove("../python/Security/Encrypt/")
#sys.path.append("../python/Security/Decrypt/")
#from decrypt import rsaDecrypt
#from decrypt import decrypt

class Complexity(Enum):
    firstOrder  = 1
    secondOrder = 2
    thirdOrder  = 3
    fourthOrder = 4
    fifthOrder  = 5
    


## Implementation of the context engine base class: the class inherited by other
## machine learning algorithms.
class ContextEngineBase(object):

    ## Member variables
    #  Function order - limit the highest order of the function
    complexity = Complexity.firstOrder;

    #  Number of inputs - interface for the number of input variables -
    #  defines input vector (+1 for training vector - n input, 1 output)
    numInputs = 0;

    #  Classification of the output - 0 is continuous, 1+ is # of states
    outputClassifier = 0;

    #  Classification of the inputs as an in-order list
    inputClassifiersList = [];

    #  Number of observations - a running count of the unique numbe of
    #  observations
    numObservations = 0;

    #  Additional custom algorithm-specific outputs as a key-value dictionary
    customFieldsDict = {};
    
    #  Matrix model - each row represents a new input vector
    observationMatrix = np.empty([0, 0]);

    #  Coefficient vector - the column vector representing the trained
    #  coefficients based on observations
    coefficientVector = [];

    #  Output observation vector - the column vector of recorded observations
    outputVector = [];
    
    #  Name of the file that contains the key for encryption/decryption
    key = {};   

    #  Constructor - the order and number of inputs are mandatory
    #  Parameters:
    #    complexity: an instance of the Complexity enumerated type
    #    numInputs: integer number of inputs
    #    outputClassifier: integer for discrete (#) or continuous (0) output
    #    inputClassifiers: list of integers for discrete/continuous inputs
    #    appFieldsDict: dictionary of key/value pairs of app-specific fields
    def __init__(self,
                 complexity,
                 numInputs,
                 outputClassifier,
                 inputClassifiers,
                 appFieldsDict):

        if (len(inputClassifiers) != numInputs):
            raise ValueError("The magnitude of inputClassifiers",
                             "must be the same as numInputs");
        self.complexity = complexity;
        self.numInputs = numInputs;
        self.outputClassifier = outputClassifier;
        self.inputClassifiersList = inputClassifiers;
        self.customFieldsDict = appFieldsDict;

        # Generate the blank coefficient matrix
        self.coefficientVector = np.zeros([self.numInputs,1])

        # Check for the presence of AES key in the key-value pair, and update 
        # the value of key with the keyFileName passed as argument
        if "key" in appFieldsDict:
            key = appFieldsDict.get("key")
            if len(key) != 0:
                self.key = key

        # All other matrices/vectors are left the same, as they are dependent
        # on the number of observations.

        # Check whether clustering is required in the output
        if self.outputClassifier > 0:
            self.outputClustering = KMeans(n_clusters = self.outputClassifier,\
                    random_state = 170) # change to random later on
            print ">> Output classifier with %d states defined" %self.outputClassifier

        self.inputClustering = {}
        for i in xrange(self.numInputs):
            if self.inputClassifiersList[i] > 0:
                self.inputClustering[i] = KMeans(n_clusters = \
                        self.inputClassifiersList[i], random_state = 170) # random
                print ">> Input classifier %d with %d states defined" \
                        %(i, self.inputClassifiersList[i])


    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    def addSingleObservation(self, newInputObs, newOutputObs):
        if (len(newInputObs) == self.numInputs
            and type(newOutputObs) not in (tuple, list)):

            # TODO: Replace the following code with a general implementation
            if (self.observationMatrix.shape[0] == 0):
                self.observationMatrix = np.array([newInputObs]);
                self.outputVector = np.array([newOutputObs]);
                self.numObservations = 1;
            else:
                self.observationMatrix = np.append(self.observationMatrix,\
                                                   np.array([newInputObs]),\
                                                   axis=0);
                self.outputVector = np.append(self.outputVector,\
                                              np.array([newOutputObs]),\
                                              axis=0);
                self.numObservations += 1;
        else:
            print("Wrong dimensions!");


    #  Add a set of training observations, with the newInputObsMatrix being a
    #  set of correctly-sized vectors and newOutputVector being a vector of
    #  individual values.
    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        for newInputVector in newInputObsMatrix:
            outputValue = newOutputVector.pop();
            self.addSingleObservation(newInputVector, outputValue);

      #  Returns the name of the file that contains the encrypted data, takes in 
    #  name of the file containing key and name of the file to be encrypted
    #def encrypt(self, plainTextFile):
    #    if len(self.key) != 0:
    #        rsaEncrypt(self.key);
    #        return encrypt(self.key, plainTextFile);
    #    else:
    #        return
            
    #  Returns the name of the file that contains the decrypted data, takes in 
    #  name of the file containing key and name of the file to be decrypted
    #def decrypt(self, encyptedFile):
    #    if len(self.key) != 0:
    #        rsaDecrypt(self.key);
    #        return decrypt(self.key, encyptedFile);
    #    else:   
    #        return

    #  Train the coefficients on the existing observation matrix if there are
    #  enough observations.

    def train(self):
        if (self.observationMatrix.shape[0] >= self.numNormalizedInputs):
            print("Training started");
            self.coefficientVector = \
                np.linalg.lstsq(self.observationMatrix, self.outputVector);
        else:
            print("Not enough observations to train!");
    
    def clusterAndTrain(self):
        # We add clustering functionality here.
        # Before each training, the data that is saved in observationMatrix\
        # is given to a kMeans clustering algorithm, which finds k clusters\
        # within the data and labels them accordingly. The number k is\
        # provided during initialization. Test data can also be classified\
        # according to this clustering, using the desgnated TODO function. 
        if self.outputClassifier > 0:
            # print np.asarray(self.outputVector).reshape(-1,1).reshape(-1,1)
            self.outputClustering.fit(np.asarray(self.outputVector).reshape(-1,1))
            outClust = []
            for out in self.outputVector:
                outClust.append(self.outputClustering.predict(float(out))[0])
            self.outputVector = outClust
            print outClust
        # Now we train
        self.train()

    #  Test the trained matrix against the given input observation
    def execute(self, inputObsVector):
        return np.dot(self.coefficientVector[0],inputObsVector);

    def executeAndCluster(self, inputObsVector):
        # We now execute the algorithm, and then classify the \
        # result using the same clustering criteria that was \
        # created in training. If the algorithm already outputs\
        # clustered results, execute() function may be used.
        res = float(self.execute(inputObsVector))
        return self.outputClustering.predict(np.asarray(res).reshape(-1,1))

    def classify(self, number, index):
        # this function classifies "number" based on the clustering that is\
        # performed on one of the inputs or output. The index identifies\
        # which clustering to use. -1 corresponds to output clustering,\
        # while any other number shows one of the input clusterings.
        modNumber = np.asarray(float(number)).reshape(-1, 1)
        if index == -1:
            if self.outputClassifier > 0:   # we have a clustering for output       
                return self.outputClustering.predict(modNumber)
            # TODO add error case for when clustering has not been fitted yet
            else:
                raise ValueError ("Clustering for output is undefined")
        else:
            if index in self.inputClustering: # we have a clustering for this input
                return self.inputClustering[index].predict(modNumber)
            # TODO add error case for when clustering has not been fitted yet
