function [ R, NMAE ] = get_R2( A, input_set )
%Calculation of R^2
%   Detailed explanation goes here

% num_inputs = 3;
% num_obs = size (A,1);
% clear input_set;
% input_set = [mic(1:num_obs) bath(1:num_obs) ...
%      oven(1:num_obs)];

clear weights
weights = TeslaTrain( input_set, A, 1 );
clear b1
clear x
clear yCalc1
b1 = weights;
x = ones(length(A),1);
x = [ x input_set];
% yCalc1 = x*b1;
% y = A;
ypred = x*b1;
yCalc = (ypred(:)-min(ypred)) / (max(ypred)-min(ypred));
y = A;
for i = 1:numel(yCalc)
    if(yCalc(i))>mean(yCalc)
        yCalc(i) = 1;
    else
        yCalc(i) = 0;
    end
end
R = 1 - (sum((y - yCalc).^2))/(sum((y - mean(y(y~=0))).^2));
NMAE =  ( sum ( abs( ( (y-yCalc)/mean(y(y~=0)) ) ) ) )/numel(y);

end