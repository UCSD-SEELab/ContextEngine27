%Implementation of the context engine base class: the class inherited by 
%other machine learning algorithms.

classdef ContextEngineBase < ContextEngineBaseAbstract
    properties
        %Member variables
        %Function order - limit the highest order of the function
        complexity=uint32(Complexity.firstOrder);
        
        %Number of inputs - interface for the number of input variables -
        %defines input vector (+1 for training vector - n input, 1 output)
        numInputs=0;
        
        %Classification of the output - 0 is continuous, 1+ is # of states
        outputClassifier = 0;
        
        %Classification of the inputs as an in-order list
        inputClassifiersList = [];
        
        %Number of observations - a running count of the unique numbe of
        %observations
        numObservations = 0;
        
        %Additional custom algorithm-specific outputs as a key-value 
        %dictionary
        %TODO: Get type of key and value currently assumed char
        customFieldsDict = containers.Map('KeyType','char',...
            'ValueType','char');
        
        %Matrix model - each row represents a new input vector
        observationMatrix =[];
        
        %Coefficient vector - the column vector representing the trained
        %coefficients based on observations
        coefficientVector = [];
        
        %Output observation vector - the column vector of
        %recorded observations
        outputVector = [];
        
        % Constructor - the order and number of inputs are mandatory
        % Parameters:
        % complexity: an instance of the Complexity enumerated type
        % numInputs: integer number of inputs
        % outputClassifier: integer for discrete (#) or 
                           %continuous (0) output
        % inputClassifiers: list of integers for 
                           %discrete/continuous inputs
        % appFieldsDict: dictionary of key/value pairs of 
                           %app-specific fields
    end
    methods
        function self=Initialize(~,complexity,numInputs,...
                outputClassifier,inputClassifiers,appFieldsDict)
            if length(inputClassifiers)~=numInputs
                error('The magnitude of inputClassifiers must be the same as numInputs');
            end
            self.complexity=complexity;
            self.numInputs=numInputs;
            self.outputClassifier=outputClassifier;
            self.inputClassifiersList =inputClassifiers;
            self.customFieldsDict = appFieldsDict;
            
            %Generate the blank coefficient matrix
            self.coefficientVector =zeros(self.numInputs,1);
            
            %All other matrices/vectors are left the same, 
            %as they are dependent on the number of observations.
        end
                
        %Add a new training observation. Requirements: newInputObs must be a
        %row array of size numInputs. newOutputObs must be a single value.
        
        function self=AddSingleObservation(self,newInputObs,newOutputObs)
            if length(newInputObs)==self.numInputs
                %Only add non-duplicates
                if ~isADuplicate(self,newInputObs,newOutputObs)
                    %TODO: Replace the following code with a general implementation
                    if size(self.observationMatrix,1)==0
                        self.observationMatrix=...
                            [self.observationMatrix;newInputObs];
                        self.outputVector =...
                            [self.outputVector;newOutputObs];
                        self.numObservations = 1;
                    else
                        self.observationMatrix=...
                            [self.observationMatrix;newInputObs];
                        self.outputVector=[self.outputVector;newOutputObs];
                        self.numObservations = self.numObservations +1;
                    end
                end
            else
                print('Wrong Dimension!');
            end
        end
        
        %Add a set of training observations, with the newInputObsMatrix being a
        %set of correctly-sized vectors and newOutputVector being a vector of
        %individual values.
        function self=AddBatchObservations(self,...
                newInputObsMatrix, newOutputVector)
            for i=1:size(newInputObsMatrix,1)
                newInputVector =newInputObsMatrix(i,:);
                outputValue =newOutputVector(end-i-1);
                
                self.addSingleObservation(newInputVector, outputValue);
            end
        end
        
        %Train the coefficients on the existing observation matrix if there are
        %enough observations.
        %TODO: Check if numNormalizedInputs is same as numInputs.
        function self= Train(self)
            if size(self.observationMatrix,1) >= self.numInputs
                print('Training started');
                self.coefficientVector = ...
                    self.observationMatrix\self.outputVector;
            else
                print('Not enough observations to train!');
            end
        end
                
        %Returns True if the provided input vector and output observation already
        %exist in the observation matrix, False otherwise
        
        function tf=isADuplicate(self,inputVector,outputObs)
            for row = 1:size(self.observationMatrix,1)
                if isequal(self.observationMatrix(row,:),inputVector)...
                        && self.outputVector(row)==outputObs
                    tf=true;  
                    return
                end
            end
            tf=false;
            return
        end
        
        %Test the trained matrix against the given input observation
        function z=Execute(self, inputObsVector)
            z=self.coefficientVector(0)*inputObsVector;
        end
        
        
    end
end
