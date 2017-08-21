function Qs = monthly_gen(Q_historical, num_years, p, n)
    
    % Input error checking
    if iscell(Q_historical)
        npoints = length(Q_historical);
    else
        error(['Q_historical must be a cell array ' ...
               'containing one or more 2-D matrices.']);
    end
    
    nQ_historical = length(Q_historical{1}(:,1));
    for i=2:npoints
        if length(Q_historical{i}(:,1)) ~= nQ_historical
            error('All matrices in Q_historical must be the same size.');
        end
    end
        
    num_years = num_years+1; % this adjusts for the new corr technique
    if nargin == 2
        nQ = nQ_historical;
    elseif nargin == 4
        n = n-1; % (input n=2 to double the frequency, i.e. repmat 1 additional time)
        nQ = nQ_historical + floor(p*nQ_historical+1)*n;
    else
        error('Incorrect number of arguments.');
    end
    Random_Matrix = randi(nQ, num_years, 12);
    
    for k=1:npoints
        Q_matrix = Q_historical{k};
        if nargin == 4
            temp = sort(Q_matrix);
            append = temp(1:ceil(p*nQ_historical),:); % find lowest p% of values for each month
            Q_matrix = vertcat(Q_matrix, repmat(append, n, 1));
        end
        logQ = log(Q_matrix);

        monthly_mean = zeros(1,12);
        monthly_stdev = zeros(1,12);
        Z = zeros(nQ, 12);

        for i=1:12
            monthly_mean(i) = mean(logQ(:,i));
            monthly_stdev(i) = std(logQ(:,i));
            Z(:,i) = (logQ(:,i) - monthly_mean(i)) / monthly_stdev(i);
        end
        Z_vector = reshape(Z',1,[]);
        Z_shifted = reshape(Z_vector(7:(nQ*12-6)),12,[])';

        % The correlation matrices should use the historical Z's
        % (the "appended years" do not preserve correlation)
        U = chol_corr(Z(1:nQ_historical,:));
        U_shifted = chol_corr(Z_shifted(1:nQ_historical-1,:));

        for i=1:12
            Qs_uncorr(:,i) = Z(Random_Matrix(:,i), i);
        end
        
        Qs_uncorr_vector = reshape(Qs_uncorr(:,:)',1,[]);
        Qs_uncorr_shifted(:,:) = reshape(Qs_uncorr_vector(7:(num_years*12-6)),12,[])';
        Qs_corr(:,:) = Qs_uncorr(:,:)*U;
        Qs_corr_shifted(:,:) = Qs_uncorr_shifted(:,:)*U_shifted;

        Qs_log(:,1:6) = Qs_corr_shifted(:,7:12);
        Qs_log(:,7:12) = Qs_corr(2:num_years,7:12);

        for i=1:12
            Qsk(:,i) = exp(Qs_log(:,i)*monthly_stdev(i) + monthly_mean(i));
        end
        
        Qs{k} = Qsk;
    end
    
end
