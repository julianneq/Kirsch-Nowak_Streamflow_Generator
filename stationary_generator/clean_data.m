% This loads the mat files and combines the Q (cfs) time series into one
% txt file. Removes leap years by averaging with the prior date.

clc; clear all;
datadir = './../data/';
files = { 'qMarietta_1932-2001.csv', 'qMuddyRun_1932-2001.csv', ...
    'qLateral_1932-2001.csv', 'evapConowingo_1932-2001.csv', ...
    'evapMuddyRun_1932-2001.csv'};
hist_data = [];

% load the historical data
for i=1:length(files)
    M{i} = load([datadir  files{i}]);
end

% find indices of leap years
% this is specific to the Susquehanna, not general
leaps = 60:365*3+366:365*(2001-1932+1)+ceil(2001-1932)/4;
all = 1:1:365*(2001-1932+1)+ceil(2001-1932)/4+1;
non_leaps = setdiff(all,leaps);

Qfinal = zeros(length(non_leaps),length(files));

for i=1:length(files)
    Q = M{i};
    Qfinal(:,i) = Q(non_leaps);
end

dlmwrite('./../data/Qdaily.txt', Qfinal, ' ');

% reshape into nyears x 365 and nyears x 12 for daily and monthly 
% statistical validation figures
Qfinal_monthly = convert_data_to_monthly(Qfinal);
% divide evaporation by 86400 (s/day) to get total monthly evap in in/month
Qfinal_monthly{4} = Qfinal_monthly{4}/86400;
Qfinal_monthly{5} = Qfinal_monthly{5}/86400;

% create directories to write files to
mkdir('./../validation/historical');
for i=1:length(files)
   q_nx365 = reshape(Qfinal(:,i),365, [])';
   dlmwrite(['./../validation/historical/' files{i}(1:(length(files{i})-14)) '-daily.csv'], q_nx365);
   dlmwrite(['./../validation/historical/' files{i}(1:(length(files{i})-14)) '-monthly.csv'], Qfinal_monthly{i}); 
end
