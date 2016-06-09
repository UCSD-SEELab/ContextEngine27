function [ ind, rem_ind] = select_next(A, variable_set, index, rem_ind )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

for i = 1:numel(rem_ind)
    try_ind = [index, rem_ind(i)];
    clear input_set;
    input_set = variable_set(:,try_ind);
    [ R(i), NMAE(i) ] = get_R2( A, input_set );
end

[best_R index_R] = max(R);
[best_NMAE  index_NMAE]= min(NMAE);
ind = [index, rem_ind(index_NMAE)];
rem_ind = rem_ind(~ismember(rem_ind,ind));

if (index_NMAE == index_R)
    disp('success');
else
    disp('success');    
end

end

