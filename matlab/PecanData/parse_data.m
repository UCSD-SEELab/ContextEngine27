% parse_data
close all
%% Reading input data sets
num_inputs = 4;

k3 = importdata('../traces/kitch_out3.dat');
% figure;
% A = k3;
% plot (A(:,1),A(:,2));

A = importdata('../traces/activity.dat');
% figure;
% plot (B(:,1), B(:,2));

k2 = importdata('../traces/kitch_out2.dat');
% figure;
% A = k2;
% plot (A(:,1),A(:,2));

oven = importdata('../traces/oven01.dat');
% figure;
% A = oven01;
% plot (A(:,1),A(:,2));

stove = importdata('../traces/stove.dat');
% figure;
% A = stove;
% plot (A(:,1),A(:,2));
 
%% Generating Input Set
num_inputs = 2;
input_set = zeros(size(A,1), num_inputs);
for i=1:size(activity,1)
    if (activity(i,1)==k3(i,1))
%         input_set(i,:) = [k3(i,2), k2(i,2), oven(i,2), stove(i,2)];
%           input_set(i,:) = [oven(i,2)];
           input_set(i,:) = [k3(i,2), k2(i,2)];
    end
        
end
clear weights
weights = TeslaTrain( input_set, A(:,2), 1 );
