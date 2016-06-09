function [ selected_index ] = select_best_inputs( A, variable_set, index, rem_ind)
%Choose the best inputs
%   Detailed explanation goes here
% variable_set = [mic(1:num_obs),ref(1:num_obs), use(1:num_obs), ...
%     bath(1:num_obs), oven(1:num_obs)];

while (numel(rem_ind))
    [index, rem_ind] = select_next( A, variable_set, index, rem_ind);
end

selected_index = index;
end

