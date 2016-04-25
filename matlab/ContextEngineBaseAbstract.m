classdef ContextEngineBaseAbstract < handle
    %CONTEXTENGINEBASEAbstract Base class for any Context Engine
    %   The class should be inherited by any Context Engine implementation
    %   that wishes to change all functionalities, such as the mechanishm
    %   for the addition of data points.
    
    properties
    end
    
    methods ( Abstract, Access = 'public' )
        %INITIALIZE Initializes the context engine with appropriate
        % parameters.
        % complexity: Maximum complexity of the context engine.
        % numberOfInputs: Number of inputs to be used.
        % discreteOutput: 0 if the output is continuous.
        % discreteInputs: 0 if the inputs are continuous.
        % specificFields: Key-value pairs for application specific fields.
        Initialize( this, ...
                    complexity, ...
                    numberOfInputs, ...
                    discreteOutput, ...
                    discreteInputs, ...
                    specificFields );
        
        %ADDSINGLEOBSERVATION Adds a single observation for training purposes.
        % inputObservations: Input observations in a column list.
        % outputObservation: A single output observation value.        
        AddSingleObservation( this, ...
                              inputObservations, ...
                              outputObservation );
        
        %ADDBATCHOBSERVATIONS Adds multiple observation for training purposes.
        % inputObservations: Input observations in a matrix format, where the
        % number of rows are the input types and the columns are their respective
        % values.
        % outputObservation: A row vector for output observation values
        AddBatchObservations( this, ...
                              inputObservations, ...
                              outputObservations );
                          
        [ trainingResult ] = Train( this );
        
        [ outputResult ] = Execute( this, inputObservations );
    end
    
end

