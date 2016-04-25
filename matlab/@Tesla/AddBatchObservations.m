function AddBatchObservations( this, ...
                              inputObservations, ...
                              outputObservations )
%ADDBATCHOBSERVATIONS Adds multiple observation for training purposes.
% inputObservations: Input observations in a matrix format, where the
% number of rows are the input types and the columns are their respective
% values.
% outputObservation: A column vector for output observation values.

assert( size( inputObservations, 1 ) == this.m_numberOfInputs, ...
        'Input Observation size mismatch' );

batchSize = size( inputObservations, 2 );

assert( size( outputObservations, 1 ) == batchSize, ...
        'Output Observation size mismatch' );

this.SelectiveTrain( inputObservations, outputObservations );
end