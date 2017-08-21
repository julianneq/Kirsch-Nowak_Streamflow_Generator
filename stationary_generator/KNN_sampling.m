function [py, yearID] = KNN_sampling( KNN_id, indices, Wcum, Qdaily, month )

% py = KNN_sampling( KKN_id, Wcum, P )
%
% Selection of one KNN according to the probability distribution defined by
% the weights W.
%
% Input:    KNN_id = indices of the first K-nearest neighbors
%           Wcum = cumulated probability for each nearest neighbor
%           P = proportion matrix
% Output:   py = selected proportion vector corresponding to the sampled
%           year
%
% MatteoG 31/05/2013

%Randomly select one of the k-NN using the Lall and Sharma density
%estimator
r = rand ;
Wcum = [0, Wcum] ;
for i = 1:length(Wcum)-1
    if (r > Wcum(i)) && (r <= Wcum(i+1))
        KNNs = i ;
    end
end
yearID = KNN_id( KNNs ) ;

% concatenate last 7 days of last year before first 7 days of first year
% and first 7 days of first year after last 7 days of last year
nrows = size(Qdaily,1);
Qdaily = [Qdaily(nrows-7:nrows,:); Qdaily; Qdaily(1:8,:)];

% shift historical data to get nearest neighbor corresponding to yearID
year = indices(yearID,1);
k = indices(yearID,2);
shifted_Qdaily = Qdaily(k:k+nrows-1,:);

DaysPerMonth = [31 28 31 30 31 30 31 31 30 31 30 31];
start = 365*(year-1) + sum(DaysPerMonth(1:(month-1)))+1;
dailyFlows = shifted_Qdaily(start:start+DaysPerMonth(month)-1,:);

py = zeros(size(dailyFlows));
for i=1:size(Qdaily,2)
    py(:,i) = dailyFlows(:,i)/sum(dailyFlows(:,i));
end

end