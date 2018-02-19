from __future__ import division
import numpy as np
import math
import statsmodels.api as sm

def fitHarmonics(t, k, y, T):
    # k is a vector specifying which harmonics to include in the fit
    # Y is the data being fit
    # T is the length of one period
    # no intercept is included in the model

    # fit to 12 data points (monthly averages)
    X = np.zeros([len(t),2*len(k)])
    for j in range(len(k)):
        for i in range(len(t)):
            X[i,2*j] = np.cos(2*math.pi*k[j]*t[i]/T)
            X[i,2*j+1] = np.sin(2*math.pi*k[j]*t[i]/T)
    
    model = sm.OLS(y,X).fit()

    return model.params