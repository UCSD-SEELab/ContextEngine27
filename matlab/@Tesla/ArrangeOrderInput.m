function [ arrangedInput ] = ArrangeOrderInput( this, inputObservation )
%ARRANGEORDERINPUT Creates a high order input list from given input
%observations. This method uses outer product to produce higher order
%elements.

arrangedInput = inputObservation';
for orderIndex = 1:( this.m_order - 1 )
    arrangedInput = ( arrangedInput * inputObservation );
    arrangedInput = arrangedInput( this.m_orderSelections{ orderIndex } );
end

if this.m_order == 0
    arrangedInput = 1;
end

end

