% ploting weights
% figure
% plot(weights);
b1 = weights;
x = ones(length(A),1);
x = [ x input_set];
ypred = x*b1;
yCalc = (ypred(:)-min(ypred)) / (max(ypred)-min(ypred));
% y = A(:,2);

for i = 1:numel(yCalc)
    if(yCalc(i))>mean(yCalc)
        yCalc(i) = 1;
    else
        yCalc(i) = 0;
    end
end
y = A;
[error NMSE]  = pred_error(yCalc, y)


R = 1 - sum((y - yCalc1).^2)/sum((y - mean(y)).^2)
VIF = 1/1-(R^2);

correct = 0;
for i = 1: numel(yCalc)
    if (yCalc(i) == y(i))
        correct = correct+1;
    end
end
correct