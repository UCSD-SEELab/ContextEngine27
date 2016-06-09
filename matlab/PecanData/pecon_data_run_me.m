% parse_data
close all
clear all
%% Reading input data sets
% num_inputs = 4;
fileID = fopen ('corr.txt','a');
appliance_list = {  'microwave1', 'refrigerator1', 'use', 'bathroom1', 'oven1'}; %   REFENRENCE LIST
% R_all = [R_mic, R_ref, R_use, R_bath, R_oven]
f  = fopen('selected_homes1.txt', 'r');
% f  = fopen('other_homes.txt', 'r');
home_list = fscanf(f, '%d');
for j = 1: length(home_list)
    close all;
    
    fileID = fopen ('results1.txt','a');
%     home_id = 5357;
    home_id = home_list(j);
    R_all = [];
    % k3 = importdata('../traces/kitch_out3.dat');
    % k2 = importdata('../traces/kitch_out2.dat');
    % oven = importdata('../traces/oven01.dat');
    % stove = importdata('../traces/stove.dat');

    file_name = strcat(num2str(home_id),'_activity.mat');
    A = importdata(file_name);

    file_name = strcat(num2str(home_id),'_power_values_microwave1.csv');
    [mic, mic_time] = xlsread(file_name);

    file_name = strcat(num2str(home_id),'_power_values_refrigerator1.csv');
    [ref, ref_time] = xlsread(file_name);

    file_name = strcat(num2str(home_id),'_power_values_use.csv');
    [use, use_time] = xlsread(file_name);

    file_name = strcat(num2str(home_id),'_power_values_bathroom1.csv');
    [bath, bath_time] = xlsread(file_name);

    file_name = strcat(num2str(home_id),'_power_values_oven1.csv');
    [oven, oven_time] = xlsread(file_name);

    fprintf(fileID, 'for Hose ID %s\n',num2str(home_id) );
    %% Generating Input Set
    num_inputs = 5;
    num_obs = size (A,1);
    clear input_set;
    input_set = [mic(1:num_obs) ref(1:num_obs) use(1:num_obs) ...
        bath(1:num_obs) oven(1:num_obs)];
    [ R, NMAE ] = get_R2( A, input_set);
    fprintf(fileID, 'The overall value of R is: %f\n',R );
    fprintf(fileID, 'The overall value of NMAE is: %f\n',NMAE );

    %% separtrate tests Microwave
    % Microwave

    num_obs = size (A,1);
    clear input_set;
    input_set = [mic(1:num_obs)];
    [ R_mic, NMAE ] = get_R2( A, input_set );
    % for i = 1:numel(y)
    %     denom(i) = (y(i)-mean(y)).^2;
    % end
    % for i = 1:numel(y)
    %     num(i) = (y(i)-yCalc(i)).^2;
    % end
    R_all(end+1)=R_mic;
    fprintf(fileID, 'The value of R for mic is: %f\n',R_mic );
    fprintf(fileID, 'The value of NMAE for mic is: %f\n',NMAE );
    %% Refrigerator
    num_obs = size (A,1);
    clear input_set;
    input_set = [ref(1:num_obs)];
    [ R_ref, NMAE ] = get_R2( A, input_set );
    R_all(end+1)=R_ref;
    fprintf(fileID, 'The value of R for ref is: %f\n',R_ref );
    fprintf(fileID, 'The value of NAME for ref is: %f\n',NMAE );

    %% use
    num_obs = size (A,1);
    clear input_set;
    input_set = [use(1:num_obs)];
    [ R_use, NMAE ] = get_R2( A, input_set );
    R_all(end+1)=R_use;
    fprintf(fileID, 'The value of R for use is: %f\n',R_use );
    fprintf(fileID, 'The value of NMAE for use is: %f\n',NMAE );
    %% Bath
    num_obs = size (A,1);
    clear input_set;
    input_set = [bath(1:num_obs)];
    [ R_bath, NMAE ] = get_R2( A, input_set );
    R_all(end+1)=R_bath;
    fprintf(fileID, 'The value of R for bath is: %f\n',R_bath );
    fprintf(fileID, 'The value of NMAE for bath is: %f\n',NMAE );
    %% Oven 
    num_obs = size (A,1);
    clear input_set;
    input_set = [oven(1:num_obs)];
    [ R_oven, NMAE ] = get_R2( A, input_set );
    R_all(end+1)=R_oven;
    fprintf(fileID, 'The value of R for oven is: %f\n',R_oven );
    fprintf(fileID, 'The value of NMAE for oven is: %f\n',NMAE );
    %% Selected set of inputs 
    % Compile all R values
    %R_all = [R_mic, R_ref, R_use, R_bath, R_oven]
    num_inputs = 5;
    num_obs = size (A,1);
    variable_set = [mic(1:num_obs),ref(1:num_obs), use(1:num_obs), ...
        bath(1:num_obs), oven(1:num_obs)];
    [ ~ , index] = max(R_all);
    clear input_set;
    input_set = variable_set(:,index);
    rem_ind = 1:num_inputs; rem_ind = rem_ind(rem_ind~=index);  
    [ R, NMAE ] = get_R2( A, input_set );
    fprintf(fileID, 'The selected set of R is for set from house : %f\n',R );
    fprintf(fileID, 'The selected set of NMAE is for set from house : %f\n',NMAE );

    [selected_index] = select_best_inputs(A, variable_set, index, rem_ind);
    fprintf(fileID, 'The selected set Input appliances are : %s, %s, %s\n', ...
    appliance_list{selected_index(1)}, appliance_list{selected_index(2)}, ...
    appliance_list{selected_index(3)} );
    fprintf('\n\n\n');

end
%%
fclose(fileID);
