function Initialize( this, ...
                     complexity, ...
                     numberOfInputs, ...
                     discreteOutput, ...
                     discreteInputs, ...
                     specificFields )
%INITIALIZE Initializes the context engine with appropriate
% parameters.
% complexity: Maximum complexity of the context engine.
% numberOfInputs: Number of inputs to be used.
% discreteOutput: 0 if the output is continuous.
% discreteInputs: 0 if the inputs are continuous.
% specificFields: Key-value pairs for application specific fields.
        
    this.m_initialTrainingComplete  = false;
    this.m_trainingSuccessfull      = false;
    this.m_holdStatistics           = true;
    this.m_order                    = complexity;
    this.m_numberOfInputs           = numberOfInputs;
    
    if nargin == 3
        discreteOutput = 0;
        discreteInputs = zeros( numberOfInputs, 1 );
        specificFields = [];
    elseif nargin == 4
        discreteInputs = zeros( numberOfInputs, 1 );
        specificFields = [];
    elseif nargin == 5
        specificFields = [];
    end
    
    % We might use them sometime, currently unused.
    this.m_discreteOutput           = discreteOutput;
    this.m_discreteInputList        = discreteInputs;
    
    % Calculate index selections for each order through outer products.
    if complexity ~= 0
        randomValues = linspace( 1, 100, numberOfInputs + 1 );
        higherOrders = randomValues';
        for oIndex = 1:( complexity - 1 )
            [higherOrders, this.m_orderSelections{ oIndex }] = ...
                                    unique( higherOrders * randomValues );
        end
    end

    

    % Read TESLA specific options.
    if isa( specificFields, 'containers.Map' )
        if specificFields.isKey( 'HoldStatistics' )
            this.m_holdStatistics = specificFields('HoldStatistics');
        end
    end

    % Initialize the statistics.
    if this.m_holdStatistics
        this.m_rmseValues       = StatisticUnit();
        this.m_maeValues        = StatisticUnit();
        this.m_mbeValues        = StatisticUnit();
        this.m_stdErrValues     = StatisticUnit();
        this.ClearStatistics();
    end
end