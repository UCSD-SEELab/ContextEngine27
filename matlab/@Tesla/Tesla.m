classdef Tesla < ContextEngineBaseAbstract
    %TESLA Taylor Expanded Solar Analog Forecasting algorithm
    %implementation.
    % This is the implementation of the TESLA algorithm using the Context
    % Engine base class.
    
    properties( SetAccess = 'private' )
        % Model order of TESLA
        m_order;
        
        % Weights of each coefficient.
        m_weights;
        
        % Inverse matrix of $$A^{T}A$$ for recursive calculation.
        m_inverseMatrix;
        
        % Number of input types.
        m_numberOfInputs;
        
        % Boolean to indicate the success of training.
        m_trainingSuccessfull;
        
        % Boolean to indicate that the initial training is complete.
        m_initialTrainingComplete;
        
        % The indices to be selected from each outer product at each order.
        m_orderSelections;
        
        % Indicates whether the output is continuous (0) or not (~0).
        m_discreteOutput;
        
        % Indicates whether the inputs are continuous (0) or not (~0).
        m_discreteInputList;
        
        % Boolean to indicate whether to hold statistics.
        m_holdStatistics;
        
        % Root mean square statistics.
        m_rmseValues;
        
        % Mean Absolute Error statistics.
        m_maeValues;
        
        % Mean Bias Error statistics.
        m_mbeValues;
        
        % Standard Error statistics.
        m_stdErrValues;
    end
    
    methods
        %TESLA Empty Constructor
        function this = Tesla()
        end
        
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
        
        %ADDSINGLEOBSERVATION Adds a single observation for training
        % purposes.
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
             
        %TRAIN No effect on Tesla for now. Training is done at every observation
        % addition.
        [ trainingResult ] = Train( this );
        
        %EXECUTE Executes the TESLA algorithm to predict the output values.
        %   The function adjusts the order of the inputs and obtains the outputs
        %   through matrix multiplication.
        [ outputResult ] = Execute( this, inputObservations );
        
        %EXECUTEANDLEARN Executes the inputs and either improves based on the given
        %outputs or adds the results to the statistics if it is enabled.
        [ outputResult ] = ExecuteAndLearn( this, ...
                                            inputObservations, ...
                                            actualOutputs, ...
                                            learnFromOutput );
        
        %CLEARSTATISTICS Clears all Statistics
        ClearStatistics( this );
        
        %PLOTRESULTS Plots the statistical results.
        % option 0: All error statistics and their time evolution.
        % option 1: Only cummulative time evolution of all statistics.
        % option 2: Only individual training statistics.
        % option 3: Only the RMSE time evolution.
        [rmseAll] = PlotResults( this, options );
    end
    
    methods( Access = 'private' );
        %ARRANGEORDERINPUT Creates a high order input list from given input
        %observations. This method uses outer product to produce higher order
        %elements.
        newInput = ArrangeOrderInput( this, inputObservation );
        
        %ARRANGEORDERINPUTLIST Arranges high order inputs for multiple items.
        newInputList = ArrangeOrderInputList( this, inputObservations );
        
        %GETORDERLENGTH Calculate length of the resulting higher order input length.
        outputLength = GetOrderLength( this );
        
        %ADDSTATISTICS Adds historical statistics if the option is enabled.
        % inputObservations: Input observations used for training
        % actualOutputs: Output observations used for training
        AddStatistics( this, inputObservations, actualOutputs );
        
        %SELECTIVETRAIN Trains the coefficients, either recursively or initially.
        SelectiveTrain( this, inputObservations, outputObservations );
        
        %INITIALTRAIN Initiates the first training through matrix division.
        %   Matrix division is much faster than recursive training. The initial
        %   batch training should be preferred, rather than recursive training.
        InitialTrain( this, inputObservations, outputObservations );
        
        %RECURSIVETRAIN Recursively trains for the given inputs.
        RecursiveTrain( this, inputObservations, outputObservations );
    end
    
end

