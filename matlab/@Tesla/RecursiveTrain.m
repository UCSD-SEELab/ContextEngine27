function RecursiveTrain( this, inputObservations, outputObservations )
%RECURSIVETRAIN Recursively trains for the given inputs.

numberOfRows = size( inputObservations, 1 );

for rowIndex = 1:numberOfRows
    % Calculate the new weights (look at the paper for details).
    newCoeff = this.m_weights - ( this.m_inverseMatrix * ( inputObservations(rowIndex,:)' * inputObservations(rowIndex,:) ) * this.m_weights ) / ...
               ( 1 + inputObservations(rowIndex,:) * this.m_inverseMatrix * inputObservations(rowIndex,:)' ) + ...
               this.m_inverseMatrix * inputObservations(rowIndex,:)' * outputObservations(rowIndex) - ...
               ( this.m_inverseMatrix * ( inputObservations(rowIndex,:)' * inputObservations(rowIndex,:) ) * this.m_inverseMatrix * inputObservations(rowIndex,:)' * outputObservations(rowIndex) ) / ...
               ( 1 + inputObservations(rowIndex,:) * this.m_inverseMatrix * inputObservations(rowIndex,:)' );

    % Calculate the new inverse matrix (look at the paper for details).
    newInverse = this.m_inverseMatrix - ( this.m_inverseMatrix * ( inputObservations(rowIndex,:)' * inputObservations(rowIndex,:) ) * this.m_inverseMatrix' ) / ...
                              ( 1 + inputObservations(rowIndex,:) * this.m_inverseMatrix * inputObservations(rowIndex,:)' );

    this.m_weights = newCoeff;
    this.m_inverseMatrix = newInverse;

    this.AddStatistics( inputObservations( rowIndex, : ), ...
                        outputObservations( rowIndex ) );
    
end

end

