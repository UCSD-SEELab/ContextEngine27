function [ weights ] = TeslaTrain( inputSet, observations, order )
%TESLATRAIN Uses TESLA to train and obtain the coefficients.
%   inputSet is an MxN matrix where M represents the number of observations
%   and N represents the number of input types. This means that each row of
%   inputSet contains the values of every input type for a single
%   observation. observations is an Mx1 vector representing the observed
%   values. The number of observations must match the number of rows of
%   inputSet. order is the Taylor expansion order to be used in TESLA.
%
% As an example, if the user wants to train the gender observations to age
% and height inputs, the input set must be [age1,height1;age2,height2...]
% and observations must be [gender1; gender2...]. The function obtains the
% TESLA coefficients for any order from 0 to 3. The coefficients can then
% be used to make predictions using the TeslaPredict function.

if length(observations) ~= numel(observations)
    error('Observation set must be a single column vector');
end

observations = observations(:);

numberOfObservations = length(observations);

if size(inputSet,1)*size(inputSet,2) ~= numel(inputSet)
    error('Input value set must be 1-D or 2-D');
end

if numberOfObservations == size(inputSet,1)
    % Don't change anything
elseif numberOfObservations == size(inputSet,2)
    % take the transpose
    warning('Input set is transposed. Each column must represent an input type!');
    inputSet = inputSet';
else
    error('Number of observations and input values don''t match');
end

numberOfInputTypes = size(inputSet,2);

if order == 0
    trainingInputSet = ones(numberOfObservations,1);
    weights = trainingInputSet\observations;
elseif order == 1
    trainingInputSet = [ones(numberOfObservations,1), inputSet];
    weights = trainingInputSet\observations;
elseif order == 2
    crossInputIndices = combnk(1:numberOfInputTypes,2);
    crossInputSet = zeros(numberOfObservations, size(crossInputIndices,1));
    for crossObservationIndex = 1:size(crossInputIndices,1)
        crossInputSet(:,crossObservationIndex) = prod(inputSet(:,crossInputIndices(crossObservationIndex,:)),2);
    end
    trainingInputSet = [ones(numberOfObservations,1), inputSet, inputSet.^2, crossInputSet];
    weights = trainingInputSet\observations;
elseif order == 3
    crossInputIndices = combnk(1:numberOfInputTypes,2);
    crossInputIndices21 = [crossInputIndices(:,1), crossInputIndices];
    crossInputIndices12 = [crossInputIndices(:,2), crossInputIndices];
    crossInputSet = zeros(numberOfObservations, size(crossInputIndices,1));
    crossInputSet21 = zeros(numberOfObservations, size(crossInputIndices,1));
    crossInputSet12 = zeros(numberOfObservations, size(crossInputIndices,1));
    for crossObservationIndex = 1:size(crossInputIndices,1)
        crossInputSet(:,crossObservationIndex) = prod(inputSet(:,crossInputIndices(crossObservationIndex,:)),2);
        crossInputSet21(:,crossObservationIndex) = prod(inputSet(:,crossInputIndices21(crossObservationIndex,:)),2);
        crossInputSet12(:,crossObservationIndex) = prod(inputSet(:,crossInputIndices12(crossObservationIndex,:)),2);
    end
    
    crossInputIndices3 = combnk(1:numberOfInputTypes,3);
    crossInputSet3 = zeros(numberOfObservations, size(crossInputIndices3,1));
    for crossObservationIndex = 1:size(crossInputIndices3,1)
        crossInputSet3(:,crossObservationIndex) = prod(inputSet(:,crossInputIndices3(crossObservationIndex,:)),2);
    end    
    trainingInputSet = [ones(numberOfObservations,1), inputSet, inputSet.^2, inputSet.^3, crossInputSet, crossInputSet21, crossInputSet12, crossInputSet3];
    weights = trainingInputSet\observations;
else
    error('Higher orders are not implemented yet');
end
end

