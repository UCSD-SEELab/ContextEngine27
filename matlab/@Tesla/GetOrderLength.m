function [ orderLength ] = GetOrderLength( this )
%GETORDERLENGTH Calculate length of the resulting higher order input length.

orderLength = length( this.ArrangeOrderInput( rand( 1, ...
                                                    this.m_numberOfInputs + 1 ) ) );

end

