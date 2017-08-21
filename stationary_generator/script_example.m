
% This script shows how to use the streamflow generator available in the
% Kirsch-Nowak_Streamflow_Generator repository on a test dataset 
% (the Lower Susquehanna River basin).
%
% Copyright 2017 Matteo Giuliani, Jon Herman and Julianne Quinn
% 
% Post-doc Research Fellow at Politecnico di Milano
% matteo.giuliani@polimi.it
% http://giuliani.faculty.polimi.it
%
% Faculty Member at UC Davis
% jdherman8@gmail.com
%
% Postdoctoral Researcher at Cornell University
% jdq8@cornell.edu
%
% Please refer to README.txt for further information.
%
%
%     This code is free software: you can redistribute 
%     it and/or modify it under the terms of the GNU General Public License 
%     as published by the Free Software Foundation, either version 3 of the 
%     License, or (at your option) any later version.     
% 
%     This code is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%     GNU General Public License for more details.

%% prepare workspace
clear all
clc

% load multi-site observations of daily streamflow
Qdaily = load('./../data/Qdaily.txt');
Qdaily = Qdaily(:,1:4); % columns 4 and 5 the same; remove column 5

% make normally distributed evaporation log-normal like flows
% (monthly_gen.m takes the log of Qdaily to make all columns normally
% distributed)
Qdaily(:,4) = exp(Qdaily(:,4));
sites = {'qMarietta', 'qMuddyRun', 'qLateral', 'evapConowingo'};
Nyears = size(Qdaily,1)/365;
Nsites = size(Qdaily,2);


%% Kirsch + Nowak generation
clc
% 100 realizations of 100 years
% and then 1000 realizations of 1 year
num_realizations = [100, 1000];
num_years = [100, 1];
dimensions = {'-100x100','-1000x1'};
% directory to write output to
mkdir('./../validation/synthetic');
for k=1:2
    Qd_cg = combined_generator(Qdaily, num_realizations(k), num_years(k) );
    % back-transform evaporation
    Qd_cg(:,:,4) = log(Qd_cg(:,:,4));

    % write simulated data to file
    for i=1:Nsites
        q_ = [];
        for j=1:num_realizations(k)
            qi = nan(365*num_years(k),1);
            qi(1:size(Qd_cg,2)) = Qd_cg(j,:,i)';
            q_ = [q_ reshape(qi,365,num_years(k))];
        end
        Qd2(:,i) = reshape(q_(:),[],1);
        saveQ = reshape(Qd2(:,i), num_years(k)*365, num_realizations(k))';
        dlmwrite(['./../validation/synthetic/' sites{i} dimensions{k} '-daily.csv'], saveQ);
    end
    synMonthlyQ = convert_data_to_monthly(Qd2);
    % divide evaporation by 86400 (s/day) to get total monthly evap in mm/month
    synMonthlyQ{4} = synMonthlyQ{4}/86400;
    for i=1:Nsites
        saveMonthlyQ = reshape(synMonthlyQ{i}',12*num_years(k),num_realizations(k))';
        dlmwrite(['./../validation/synthetic/' sites{i} dimensions{k} '-monthly.csv'], saveMonthlyQ);
    end
    dlmwrite(['./../validation/synthetic/Qdaily' dimensions{k} '.csv'], Qd2);
    clear Qd2;
end