% parse_data
close all
clear all
%% Reading input data sets
% home_id = 2814;
appliance_list = [ 'refrigerator1', 'microwave1', 'use', 'bathroom1', 'oven1']; %   REFENRENCE LIST
file_selected_homes  = fopen('selected_homes.txt', 'r');
home_list = fscanf(file_selected_homes, '%d');
for j = 1: length(home_list)
    home_id = home_list(j);
    
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
    
% ouputfile
    out = zeros(size(mic));
    
% Ground truth set up base parameters
    mean_mic = mean (mic);
    num_obs = min([length(mic) length(ref) length(use) length(bath) length(oven)]);
    for i = 1:num_obs
        if ( (mic(i,1) >= mean_mic && ref(i,1) >= mean(ref) && ...
                 oven(i,1) >= mean(oven) && bath(i,1) >= mean(bath)) ...
                 && (use(i,1) >= mean(use)) )
            out(i,1) = 1;
        end
    end
    f = strcat(num2str(home_id),'_activity');
    save (f, 'out');

end 
% plot_weights
% count = 0;
% for i=1:length(out)
%     if(out(i)==1)
%         count = count+1;
%         
%     end
% end

% if (mic(i,1) >= mean_mic || ref(i,1) >= mean(ref)|| ...
%                 use(i,1) >= mean(use) || oven(i,1) >= mean(oven) ... 
%                 || bath(i,1) >= mean(bath))