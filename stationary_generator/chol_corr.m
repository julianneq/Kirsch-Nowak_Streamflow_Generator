function U = chol_corr(Z)
% compute cholesky decomp of correlation matrix of columns of Z
% attempts to repair non-positive-definite matrices
% http://www.mathworks.com/matlabcentral/answers/6057-repair-non-positive-definite-correlation-matrix
% rank-1 update followed by rescaling to get unit diagonal entries

    R = corr(Z);
    [U,p] = chol(R);
    while p > 0 % if not positive definite, modify slightly
        k = min([min(real(eig(R))) -1*eps]);
        R = R - k*eye(size(R));
        R = R/R(1,1);
        [U,p] = chol(R);
    end
end