function InitialTrain( this, inputObservations, outputObservations )
%INITIALTRAIN Initiates the first training through matrix division.
%   Matrix division is much faster than recursive training. The initial
%   batch training should be preferred, rather than recursive training.

hermitianInput = inputObservations' * inputObservations;

if rank( hermitianInput ) ~= length( hermitianInput )
    return;
end

this.m_inverseMatrix = inv( hermitianInput );
this.m_weights = this.m_inverseMatrix * inputObservations' * outputObservations;

this.m_initialTrainingComplete = true;

this.m_trainingSuccessfull = rank( this.m_inverseMatrix ) == ...
                             length( this.m_inverseMatrix );
                         
this.AddStatistics( inputObservations, outputObservations );

end

