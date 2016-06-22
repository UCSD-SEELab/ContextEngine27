% parse_data
close all
%% Reading input data sets
% num_inputs = 4;

% k3 = importdata('../Data/9585_power_values_use');
[a, b] = xlsread('..\Data\5652_power_values_use.csv');

c = datenum(b);
plot (a);

