function SelectiveTrain( this, inputObservations, outputObservations )
%SELECTIVETRAIN Trains the coefficients, either recursively or initially.

inputObservations = inputObservations';

inputObservations = [ ones( size( inputObservations, 1 ), 1 ), inputObservations ];
inputObservations = this.ArrangeOrderInputList( inputObservations );

if this.m_initialTrainingComplete
    this.RecursiveTrain( inputObservations, outputObservations );
else
    this.InitialTrain( inputObservations, outputObservations );
end

end

