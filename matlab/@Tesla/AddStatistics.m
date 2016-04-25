function AddStatistics( this, inputObservations, actualOutputs )
%ADDSTATISTICS Adds historical statistics if the option is enabled.
% inputObservations: Input observations used for training
% actualOutputs: Output observations used for training

if this.m_holdStatistics
    [rmse, mae, mbe, stdErr] = RMSE( inputObservations * this.m_weights, ...
                                     actualOutputs );
    this.m_rmseValues.AddData( rmse );
    this.m_maeValues.AddData( mae );
    this.m_mbeValues.AddData( mbe );
    this.m_stdErrValues.AddData( stdErr );
end

end

