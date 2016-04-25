function [ outputResult ] = Execute( this, inputObservations )
%EXECUTE Executes the TESLA algorithm to predict the output values.
%   The function adjusts the order of the inputs and obtains the outputs
%   through matrix multiplication.

input = [ ones( size( inputObservations, 1 ), 1 ), inputObservations ];
input = this.ArrangeOrderInputList( input );

outputResult = input * this.m_weights;

end

