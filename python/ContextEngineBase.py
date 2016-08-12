from aenum import Enum
import math
import numpy as np
import sys
from sklearn.cluster import KMeans 
sys.path.append("ContextEngineInterface")
from CEInterface import ceInterface

#sys.path.append("../python/Security/Encrypt/")
#from encrypt import encrypt
#from encrypt import rsaEncrypt
#sys.path.remove("../python/Security/Encrypt/")
#sys.path.append("../python/Security/Decrypt/")
#from decrypt import rsaDecrypt
#from decrypt import decrypt


## Implementation of the context engine base class: the class inherited by other
## machine learning algorithms.
class ContextEngineBase(object):
    ## Member variables
    #  Function order - limit the highest order of the function
    # complexity = Complexity.firstOrder

    #  Number of inputs - interface for the number of input variables -
    #  defines input vector (+1 for training vector - n input, 1 output)
    numInputs = 0

    #  Classification of the output - 0 is continuous, 1+ is # of states
    outputClassifier = 0

    #  Classification of the inputs as an in-order list
    inputClassifiersList = []

    #  Number of observations - a running count of the unique numbe of
    #  observations
    numObservations = 0

    #  Additional custom algorithm-specific outputs as a key-value dictionary
    customFieldsDict = {}
    
    #  Matrix model - each row represents a new input vector
    observationMatrix = np.empty([0, 0])
    observationMatrixIdx = np.empty([0, 0])

    #  Coefficient vector - the column vector representing the trained
    #  coefficients based on observations
    coefficientVector = []

    #  Output observation vector - the column vector of recorded observations
    outputVector = []
    outputVectorIdx = []
    #outputVectorNorm = []

    #  Name of the file that contains the key for encryption/decryption
    key = {}

    #  Constructor - the order and number of inputs are mandatory
    #  Parameters:
    #    numInputs: integer number of inputs
    #    outputClassifier: integer for discrete (#) or continuous (0) output
    #    inputClassifiers: list of integers for discrete/continuous inputs
    #    appFieldsDict: dictionary of key/value pairs of app-specific fields
    def __init__(self,
                 numInputs,
                 outputClassifier,
                 inputClassifiers,
                 appFieldsDict):

        if (len(inputClassifiers) != numInputs):
            raise ValueError("The magnitude of inputClassifiers",
                             "must be the same as numInputs")
        #self.complexity = complexity
        self.numInputs = numInputs
        self.outputClassifier = outputClassifier
        self.inputClassifiersList = inputClassifiers
        self.customFieldsDict = appFieldsDict

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
        # Interface (i.e., GDP log info for IO)
        if "interface" in appFieldsDict:
            inDicts = appFieldsDict["interface"]["in"]
            outDict = appFieldsDict["interface"]["out"]
            self.interface = ceInterface (numInputs, inDicts, outDict)
        else:
            raise ValueError("Interface dictionary must be provided")

    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    def addSingleObservation(self, newInputObs, newOutputObs):
        if (len(newInputObs) == self.numInputs
            and type(newOutputObs) not in (tuple, list)):

            # TODO: Replace the following code with a general implementation
            if (self.observationMatrix.shape[0] == 0):
                self.observationMatrix = np.array([newInputObs])
                self.outputVector = np.array([newOutputObs])
                self.numObservations = 1
            else:
                self.observationMatrix = np.append(self.observationMatrix,\
                                                   np.array([newInputObs]),\
                                                   axis=0)
                self.outputVector = np.append(self.outputVector,\
                                              np.array([newOutputObs]),\
                                              axis=0)
                self.numObservations += 1
        else:
            print("Wrong dimensions!")


    #  Add a set of training observations, with the newInputObsMatrix being a
    #  set of correctly-sized vectors and newOutputVector being a vector of
    #  individual values.
    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        for newInputVector in newInputObsMatrix:
            outputValue = newOutputVector.pop()
            self.addSingleObservation(newInputVector, outputValue)

      #  Returns the name of the file that contains the encrypted data, takes in 
    #  name of the file containing key and name of the file to be encrypted
    #def encrypt(self, plainTextFile):
    #    if len(self.key) != 0:
    #        rsaEncrypt(self.key)
    #        return encrypt(self.key, plainTextFile)
    #    else:
    #        return
            
    #  Returns the name of the file that contains the decrypted data, takes in 
    #  name of the file containing key and name of the file to be decrypted
    #def decrypt(self, encyptedFile):
    #    if len(self.key) != 0:
    #        rsaDecrypt(self.key)
    #        return decrypt(self.key, encyptedFile)
    #    else:   
    #        return

    #  Train the coefficients on the existing observation matrix if there are
    #  enough observations.

    def train(self):
        if (self.observationMatrix.shape[0] >= self.numNormalizedInputs):
            print("Training started")
            self.coefficientVector = \
                np.linalg.lstsq(self.observationMatrix, self.outputVector)
        else:
            print("Not enough observations to train!")
    
    def clusterAndTrain(self):
        # We add normalization and clustering functionality here.
        # Before each training, the data that is saved in observationMatrix\
        # normalized using the method specified in initialization, and then it \
        # is given to a kMeans clustering algorithm, which finds k clusters\
        # within the data and labels them accordingly. The number k is\
        # provided during initialization. Test data can also be classified\
        # according to this clustering, using "classify" function.
        self.normalizeData()
        # output clustering
        if self.outputClassifier > 0:
            # print np.asarray(self.outputVector).reshape(-1,1).reshape(-1,1)
            self.outputClustering.fit(np.asarray(self.outputVector).reshape(-1,1))
            outClust = []
            for out in self.outputVector:
                outClust.append(self.outputClustering.predict(float(out))[0])
            self.outputVectorIdx = outClust
            self.outputVector = [self.outputClustering.cluster_centers_[c][0]\
                    for c in outClust]
        # Input clustering
        self.observationMatrixIdx = np.copy(self.observationMatrix)
        for i in xrange(self.numInputs):
            if self.inputClassifiersList[i] > 0:
                snip = map(lambda d: d[i], self.observationMatrix)
                self.inputClustering[i].fit(np.asarray(snip).reshape(-1,1))
                j = 0
                for rec in self.observationMatrixIdx:
                    clust = self.inputClustering[i].predict(float(rec[i]))[0]
                    self.observationMatrixIdx[j][i] = clust
                    self.observationMatrix[j][i] = \
                        self.inputClustering[i].cluster_centers_[clust]
                    j = j + 1

        # Now we train using normalized and clustered data
        self.train()

    #  Test the trained matrix against the given input observation
    def execute(self, inputObsVector):
        return np.dot(self.coefficientVector[0],inputObsVector)

    def executeAndCluster(self, inputObsVector, idx = None):
        # We now execute the algorithm, and then classify the \
        # result using the same clustering criteria that was \
        # created in training. If the algorithm requires clustered\
        # inputs, the clustering is performed here.
        # Normalize and cluster input before calling execute (if necessary):
        normInp = self.normalizeInputRec(inputObsVector)
        if self.numInputs == 1 and self.inputClassifiersList[0] > 0:
            inputObsVector = self.inputClustering[0].\
                    cluster_centers_[self.inputClustering[0].\
                    predict(float(inputObsVector))][0][0]
        else:
            for i in xrange(self.numInputs):
                if self.inputClassifiersList[i] > 0:
                    inputObsVector[i] = self.inputClustering[i].\
                            cluster_centers_[self.inputClustering[i].
                            predict(float(inputObsVector[i]))][0][0]
        res = float(self.execute(normInp))
        # Return cluster centroid if output is         if self.outputClassifier > 0:
        if self.outputClassifier > 0:
            return self.outputClustering.cluster_centers_[self.outputClustering\
                    .predict(float(res))][0][0]
        else:
            return res

    def classify(self, number, index):
        # this function classifies "number" based on the clustering that is\
        # performed on one of the inputs or output. The index identifies\
        # which clustering to use. -1 corresponds to output clustering,\
        # while any other number shows one of the input clusterings.
        modNumber = np.asarray(float(number)).reshape(-1, 1)
        if index == -1 and self.outputClassifier > 0:
            if self.outputClassifier > 0:   # we have a clustering for output       
                return self.outputClustering.cluster_centers_[\
                        self.outputClustering.predict(modNumber)][0][0]
            # TODO add error case for when clustering has not been fitted yet
            else:
                raise ValueError ("Clustering for output is undefined")
        elif index in self.inputClustering: # we have a clustering for this input
            return self.outputClustering.cluster_centers_[\
                   self.inputClustering[index].predict(modNumber)][0][0]
            # TODO add error case for when clustering has not been fitted yet
        else:
            return number

    # normalize (zero mean and divide by standard deviation) for each
    # of inputs or 
    def normalizeData(self):
        # output normalization:
        # Linear normlization, zero-mean and divide by std
        if self.interface.outObj.norm == 'lin':
            avg = np.mean(self.outputVector)
            std = np.std(self.outputVector)
            self.outputVector = [(r - avg) / std for r in self.outputVector]
            self.interface.outObj.normParam = {'avg': avg, 'std': std}
        else:
            self.outputVector = self.outputVector
        # input normalization
        for i in xrange(self.numInputs):
            inObj = self.interface.inObjs[i]
            if inObj.norm == 'lin':
                # Extracting the i'th input to normalize
                inSnippet = map(lambda d: d[i], self.observationMatrix)
                avg = np.mean(inSnippet)
                std = np.std(inSnippet)
                normInp = [(r - avg) / std for r in inSnippet]
                self.updateSingleInputSnippet(normInp, i)
                self.interface.inObjs[i].normParam = {'avg': avg, 'std': std}
            i = i + 1

    def normalizeSnippet(self, snip, idx):
        if idx == -1:
            if self.interface.outObj.norm == 'lin':
                avg = self.interface.outObj.normParam['avg']
                std = self.interface.outObj.normParam['std']
            else:
                avg = float(0)
                std = float(1)
        elif idx < numInputs:
            if self.interface.inObjs[idx].norm == 'lin':
                avg = self.interface.inObjs[idx].normParam['avg']
                std = self.interface.inObjs[idx].normParam['std']
            else:
                avg = float(0)
                std = float(1)
        else:
            raise ValueError ("Index out of bound: idx > numInputs")

        if type(snip) == np.float64:
            return (snip - avg) / std
        else:
            return [(r - avg) / std for r in snip]

    def deNormalizeSnippet(self, snip, idx):
        if idx == -1:
            if self.interface.outObj.norm == 'lin':
                avg = self.interface.outObj.normParam['avg']
                std = self.interface.outObj.normParam['std']
            else:
                avg = float(0)
                std = float(1)
        elif idx < numInputs:
            if self.interface.inObjs[idx].norm == 'lin':
                avg = self.interface.inObjs[idx].normParam['avg']
                std = self.interface.inObjs[idx].normParam['std']
            else:
                avg = float(0)
                std = float(1)
        else:
            raise ValueError ("Index out of bound: idx > numInputs")
        if type(snip) != np.ndarray or type(snip) != list:
            return snip * std + avg
        else:
            return [f * std + avg for f in snip]

    def normalizeInputRec(self, rec):
        # only 1 input
        if type(rec) == np.float64:
            avg = self.interface.inObjs[0].normParam['avg']
            std = self.interface.inObjs[0].normParam['std']
            rec = (rec - avg) / std
            return rec
        # several inputs
        if len(rec) == self.numInputs:
            for i in xrange(self.numInputs):
                if self.interface.inObjs[i].norm == 'lin':
                    avg = self.interface.inObjs[i].normParam['avg']
                    std = self.interface.inObjs[i].normParam['std']
                    rec[i] = (rec[i] - avg) / std
            return rec
        else:
            raise ValueError ("Record Length does not match numInputs")
    # TODO make this faster
    def updateSingleInputSnippet(self, snippet, idx):
        if len(self.observationMatrix) != len(snippet):
            raise ValueError ("Input update data snippet does not match the\
                    number of observed data")
        else:
            j = 0
            for rec in self.observationMatrix:
                rec[idx] = snippet[j]
                j = j + 1
    
    def streamInputInit (self, idx):
        if idx == -1:
            raise ValueError ('Subscription is not defined for output.')
        if idx >= self.numInputs:
            raise ValueError ('Subscription index out of bound (idx > numInputs).')
        self.interface.inObjs[idx].subscribe()
        return

    def fetchOnlineData (self, idx):
        if idx == -1:
            raise ValueError ('Subscription is not defined for output.')
        if idx >= self.numInputs:
            raise ValueError ('Subscription index out of bound (idx > numInputs).')
        return self.interface.inObjs[idx].getNextData()
