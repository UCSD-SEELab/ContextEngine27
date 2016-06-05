function [ rmseAll ] = PlotResults( this, options )
%PLOTRESULTS Plots the statistical results.
% option 0: All error statistics and their time evolution.
% option 1: Only cummulative time evolution of all statistics.
% option 2: Only individual training statistics.
% option 3: Only the RMSE time evolution.

if ~this.m_holdStatistics
    rmseAll = [];
    return;
end

if nargin == 1
    options = 0;
end

figure(1);

dataLength = length( this.m_rmseValues.GetData() );
x = 1:dataLength;

rmse = this.m_rmseValues.GetData();
mae = this.m_maeValues.GetData();
mbe = this.m_mbeValues.GetData();

if options ~= 2
    rmseAll = zeros( dataLength, 1 );
    maeAll = zeros( dataLength, 1 );
    mbeAll = zeros( dataLength, 1 );
    rmseAll(1) = rmse(1);
    maeAll(1) = mae(1);
    mbeAll(1) = mbe(1);
    for i = 2:dataLength
        rmseAll( i ) = sqrt( ( ( rmseAll( i - 1 ) ^ 2  * ( i - 1 ) ) +rmse( i )^2 ) / i );
        maeAll( i ) = ( maeAll( i - 1 ) * ( i - 1 ) + mae( i ) ) / i;
        mbeAll( i ) = ( mbeAll( i - 1 ) * ( i - 1 ) + mbe( i ) ) / i;
    end
end

if options == 0
    plot( x, mae, 'b', ...
          x, mae, 'r', ...
          x, mbe, 'g', ...
          x, rmseAll, '--b', ...
          x, maeAll, '.r', ...
          x, mbeAll, '.g' );
elseif options == -1
    plot( x, rmseAll, '--b', ...
          x, maeAll, '.r', ...
          x, mbeAll, '.g' );
elseif options == -2
    plot( x, rmse, 'b', ...
          x, mae, 'r', ...
          x, mbe, 'g' );
elseif options == -3
    plot( x, rmseAll, 'LineWidth', 3 );
end

if options ~= -3
    legend( 'RMSE', 'MAE', 'MBE' );
end

xlabel( 'Prediction Instance' );
ylabel( 'Error Value' );
set( gca, 'FontSize', 30 );
grid on;

end

