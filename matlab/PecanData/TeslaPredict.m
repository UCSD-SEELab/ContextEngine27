function [ prediction ] = TeslaPredict( weights, order, inputVector )
%TESLAPREDICT Predicts the output values using TESLA.
%   weights are the TESLA coefficients found preferably by the TeslaTrain
%   function. order is the Taylor expansion order to be used. inputVector
%   is either a vector representing the values for all input types as a
%   single row or a matrix obtained by combining multiple rows to obtain
%   the TESLA response for multiple cases at once.
%
% As an example if there are two input types, age and height, and the order
% to be used is 2, the user can predict a single person by calling
% TeslaPredict(weights,2,[ageValue,heightValue]). If the user wishes to
% predict multiple people at once (for performance improvement compared to
% an external for loop) TeslaPredict(weights,2,[age1,height1;age2,height2])
%
% The order used for training the weights must exactly match the order used
% for prediction. To use a different order, retrain the weights.

if nargin == 2
    if order ~= 0
        error('Input values required');
    else
        inputVector = [];
    end
end

if numel(weights) ~= length(weights)
    error('Weights must be a 1-D Vector. Use TeslaTrain() function');
end

weights = weights(:);

numberOfQueries = size(inputVector,1);
numberOfInputTypes = size(inputVector,2);

if order == 0
    if length(weights) ~= 1
        error('Weight - Order mismatch');
    end
    if numberOfQueries == 0
        prediction = weights;
    else
        prediction = weights * ones(numberOfQueries,1);
    end
elseif order == 1
    if length(weights) ~= numberOfInputTypes + 1
        error('Weight - Order mismatch');
    end
    trainingInputSet = [ones(numberOfQueries,1), inputVector];
    prediction = trainingInputSet * weights;
elseif order == 2
    crossInputIndices = combnk(1:numberOfInputTypes,2);
    
    if length(weights) ~= size(crossInputIndices,1) + 2 * numberOfInputTypes + 1
        error('Weight - Order mismatch');
    end
    
    crossInputSet = zeros(numberOfQueries, size(crossInputIndices,1));
    for crossObservationIndex = 1:size(crossInputIndices,1)
        crossInputSet(:,crossObservationIndex) = prod(inputVector(:,crossInputIndices(crossObservationIndex,:)),2);
    end
    trainingInputSet = [ones(numberOfQueries,1), inputVector, inputVector.^2, crossInputSet];
    prediction = trainingInputSet * weights;
elseif order == 3
    crossInputIndices = combnk(1:numberOfInputTypes,2);
    crossInputIndices3 = combnk(1:numberOfInputTypes,3);
    
    if length(weights) ~= length(crossInputIndices3) + 3 * size(crossInputIndices,1) + 3 * numberOfInputTypes + 1
        error('Weight - Order mismatch');
    end
    
    crossInputIndices21 = [crossInputIndices(:,1), crossInputIndices];
    crossInputIndices12 = [crossInputIndices(:,2), crossInputIndices];
    crossInputSet = zeros(numberOfQueries, size(crossInputIndices,1));
    crossInputSet21 = zeros(numberOfQueries, size(crossInputIndices,1));
    crossInputSet12 = zeros(numberOfQueries, size(crossInputIndices,1));
    for crossObservationIndex = 1:size(crossInputIndices,1)
        crossInputSet(:,crossObservationIndex) = prod(inputVector(:,crossInputIndices(crossObservationIndex,:)),2);
        crossInputSet21(:,crossObservationIndex) = prod(inputVector(:,crossInputIndices21(crossObservationIndex,:)),2);
        crossInputSet12(:,crossObservationIndex) = prod(inputVector(:,crossInputIndices12(crossObservationIndex,:)),2);
    end
    
    crossInputSet3 = zeros(numberOfQueries, size(crossInputIndices3,1));
    for crossObservationIndex = 1:size(crossInputIndices3,1)
        crossInputSet3(:,crossObservationIndex) = prod(inputVector(:,crossInputIndices3(crossObservationIndex,:)),2);
    end    
    trainingInputSet = [ones(numberOfQueries,1), inputVector, inputVector.^2, inputVector.^3, crossInputSet, crossInputSet21, crossInputSet12, crossInputSet3];
    prediction = trainingInputSet * weights;
else
    error('Higher orders are not implemented yet');
end

end

