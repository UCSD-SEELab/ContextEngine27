function [ newInputList ] = ArrangeOrderInputList( this, ...
                                                   inputObservations )
%ARRANGEORDERINPUTLIST Arranges high order inputs for multiple items.

numberOfRows = size( inputObservations, 1 );
newInputList = zeros( numberOfRows, this.GetOrderLength() );

for rowIndex = 1:numberOfRows
    newInputList( rowIndex, : ) = this.ArrangeOrderInput( ...
                                        inputObservations( rowIndex, : ) );
end

end

