import numpy as np
import math

## Implementation of the TESLA algorithm: map input variables to output
## observations
class Tesla:

    ## Member variables
    #  Function order - limit the highest order of the function
    functionOrder = 1;

    #  Number of inputs - interface for the number of input variables -
    #  defines input vector (+1 for training vector - n input, 1 output)
    numInputs = 0;

    #  Number of normalized inputs - this is the number of inputs needed,
    #  corrected for the order.
    #  e.g. 1st order == numInputs, 2nd order == numInputs^2, etc.
    numNormalizedInputs = 0;

    #  Number of observations - a running count of the unique numbe of
    #  observations
    numObservations = 0;

    #  Matrix model - each row represents a new input vector
    observationMatrix = np.empty([0, 0]);

    #  Coefficient vector - the column vector representing the trained
    #  coefficients based on observations
    coefficientVector = [];

    #  Output observation vector - the column vector of recorded observations
    outputVector = [];
    

    #  Constructor - the order and number of inputs are mandatory
    def __init__(self, order, numInputs):
        self.functionOrder = order;
        self.numInputs = numInputs;
        self.numNormalizedInputs = \
            int(math.factorial(self.numInputs+order)/\
            (math.factorial(order)*math.factorial(self.numInputs)));
    
        # Generate the blank coefficient matrix
        self.coefficientVector = np.zeros([self.numNormalizedInputs,1])

        # All other matrices/vectors are left the same, as they are dependent
        # on the number of observations.

    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    def addSingleObservation(self, newInputObs, newOutputObs):
        if (len(newInputObs) == self.numInputs
            and type(newOutputObs) not in (tuple, list)):
#            print("All good!");

            # Prepend 1, to represent the unity coefficients
            newInputObs.insert(0, 1);

            # Generate the total number of input sets based on function order
            # (the normalized input set)
            normalizedInputObs = self.generateNormalizedInputs(newInputObs);

            # Only add non-duplicates
            if (not self.isADuplicate(normalizedInputObs, newOutputObs)):
                # TODO: Replace the following code with a general implementation
                if (self.observationMatrix.shape[0] == 0):
                    self.observationMatrix = np.array([normalizedInputObs]);
                    self.outputVector = np.array([newOutputObs]);
                    self.numObservations = 1;
                else:
                    self.observationMatrix = np.append(self.observationMatrix,\
                                                       np.array([normalizedInputObs]),\
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
            self.addSingleObservation(newInputVector, newInputObsMatrix);

    #  Generate the normalized inputs based on function order
    def generateNormalizedInputs(self, inputObs):
        normalizedInputObs = [];
        if (self.functionOrder == 1):
            return inputObs;
        elif (self.functionOrder == 2):
            for i in range(0, len(inputObs)):
                for j in range(0, i+1):
                    normalizedInputObs.append(inputObs[i]*inputObs[j]);
        elif (self.functionOrder == 3):
            for i in range(0, len(inputObs)):
                for j in range(0, i+1):
                    for k in range(0, j+1):
                        normalizedInputObs.append(inputObs[i]*inputObs[j]*inputObs[k]);

        return normalizedInputObs;


    #  Train the coefficients on the existing observation matrix if there are
    #  enough observations.
    def train(self):
        if (self.observationMatrix.shape[0] >= self.numNormalizedInputs):
            print("Training started");
            self.coefficientVector = \
                np.linalg.lstsq(self.observationMatrix, self.outputVector);
        else:
            print("Not enough observations to train!");
    
    #  Returns True if the provided input vector and output observation already
    #  exist in the observation matrix, False otherwise
    def isADuplicate(self, normalizedInputVector, outputObs):
        for row in range(0, self.observationMatrix.shape[0]):
            if (np.array_equal(self.observationMatrix[row], normalizedInputVector) \
               and self.outputVector[row] == outputObs):
                return True;
        return False;

    #  Test the trained matrix against the given input observation
    def test(self, inputObsVector):
        inputObsVector.insert(0, 1);
        inputObsNPVector = np.array(self.generateNormalizedInputs(inputObsVector));
        return np.dot(self.coefficientVector[0],inputObsNPVector);
