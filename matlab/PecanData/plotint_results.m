% Result plots 
R = [2.15717537155324e-06; 2.4742e-05; 2.4848e-05; 1.6402e-04];
y = ['Kitchen_data3'; 'Kitchen_data2',; 'oven'; 'stove'];
figure
plot (R);
% rotateXLabels(gca, 45);
set (gca,'XTickLabel',['Kitchen_data3', 'Kitchen_data2', 'oven', 'stove']);
