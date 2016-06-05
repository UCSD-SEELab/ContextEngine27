function AddSingleObservation( this, ...
                               inputObservations, ...
                               outputObservation )
%ADDSINGLEOBSERVATION Adds a single observation for training purposes.
% inputObservations: Input observations in a column list.
% outputObservation: A single output observation value.

assert( size( inputObservations, 1 ) == this.m_numberOfInputs, ...
        'Input Observation size mismatch' );
    
assert( size( outputObservation, 1 ) == 1, ...
        'Single Output Observation expected' );

this.SelectiveTrain( inputObservations, outputObservation );

end