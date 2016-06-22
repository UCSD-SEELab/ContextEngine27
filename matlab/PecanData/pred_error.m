function [ error] = pred_error( yCalc1, y )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
    count = 0;
    for i =  1:numel(y)
        if yCalc1(i)>4.5
            yCalc1(i)= 1;
        else
            yCalc1(i)= 0;
        if (y(i)==yCalc1(i))
            count = count+1;
        end
    end
error = count*1.0/numel(y);
end

