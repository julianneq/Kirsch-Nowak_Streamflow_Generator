function Qgen = monthly_main( hist_data, nR, nY )

Nyears = size(hist_data,1)/365;
Nsites = size(hist_data,2);

% from daily to monthly
Qh = convert_data_to_monthly(hist_data) ; 

% initialization of the output
for k=1:Nsites
    qq{k} = zeros(nR, nY*12);
end

% generation
for r=1:nR
    Qs = monthly_gen(Qh, nY);
    for k=1:Nsites
        qq{k}(r,:) = reshape(Qs{k}',1,[]);
    end
end

% output matrix
Qgen = nan(nR,nY*12,Nsites) ;
for k=1:Nsites
    Qgen(:,:,k)= qq{k} ;
end

end

