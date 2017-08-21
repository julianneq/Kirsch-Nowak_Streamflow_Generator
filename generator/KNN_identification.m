function [KNN_id, W] = KNN_identification( Z, Qpatterns, month, k )

% [KNN_id, W] = KNN_identification( Z, z )
%
% Identification of K-nearest neighbors of Z in the historical annual data
% z and computation of the associated weights W.
%
% Input:    Z = synthetic datum (scalar)
%           z = historical annual data 
%           k = number of nearest neighbors (by default k=n_year^0.5
%           according to Lall and Sharma (1996))
% Output:   KNN_id = indices of the first K-nearest neighbors of Z in the
%           the historical annual data z
%           W = nearest neighbors weights, according to Lall and Sharma
%           (1996): W(i) = (1/i) / (sum(1/i)) 
%
% MatteoG 31/05/2013

% Npatterns is the number of historical patterns used for disaggregation.
% A pattern is a sequence of ndays of daily flows, where ndays is the
% number of days in the month being disaggregated. Patterns are all
% historical sequences of length ndays beginning within 7 days before or
% after the 1st day of the month being disaggregated.
Npatterns = size(Qpatterns{month},1);
if( nargin<4 )
    K = round(sqrt(Npatterns));
else
    K = k ;
end

% nearest neighbors identification;
% only look at neighbors from the same month +/- 7 days
Nsites = size(Qpatterns{month},2);
delta = zeros([Npatterns,1]); % first and last month have 7 less possible shifts
for i=1:Npatterns
    for j=1:Nsites
            delta(i) = delta(i) + (Qpatterns{month}(i,j)-Z(1,1,j))^2;
    end
end

Y = [[1:size(delta,1)]', delta ] ;
Y_ord = sortrows(Y, 2);
KNN_id = Y_ord(1:K,1) ;

% computation of the weights
f = [1:K];
f1 = 1./f;
W = f1 ./ sum(f1) ;

end








