function [ outputResult ] = ExecuteAndLearn( this, ...
                                             inputObservations, ...
                                             actualOutput, ...
                                             learnFromOutput )
%EXECUTEANDLEARN Executes the inputs and either improves based on the given
%outputs or adds the results to the statistics if it is enabled.

outputResult = this.Execute( inputObservations );

if nargin == 4
    if learnFromOutput
        this.AddBatchObservations( inputObservations, actualOutput )
    else
        this.AddStatistics( inputObservations, actualOutput );
    end
elseif nargin == 3
    this.AddStatistics( inputObservations, actualOutput );
end

end

