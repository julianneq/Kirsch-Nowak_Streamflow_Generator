from __future__ import division
import numpy as np
from fitHarmonics import fitHarmonics
import math
import os

# https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
def assure_path_exists(path):
    '''Creates directory if it doesn't exist'''
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def MonsoonalRescaling(sites, k, evapIndices):

    nSites = len(sites)
    
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    nMonths = len(daysPerMonth)
    dayOfYear = [0]*(nMonths+1)
    for i in range(nMonths):
        dayOfYear[i+1] = dayOfYear[i] + daysPerMonth[i]
    
    # calculate historical mean and standard deviation of log of monthly flows
    HistoricalDailyQ = np.loadtxt('../data/Qdaily.txt')
    # make normally distributed evaporation log-normal like flows
    for index in evapIndices:
        HistoricalDailyQ[:,index] = np.exp(HistoricalDailyQ[:,index])

    meanMatrix = np.zeros([nSites,nMonths])
    stdMatrix = np.zeros([nSites,nMonths])
    for i in range(nSites):
        HistoricalMonthlyQ = convert_data_to_monthly(HistoricalDailyQ[:,i],daysPerMonth)
        LogQ = np.log(HistoricalMonthlyQ)
        meanMatrix[i,:] = np.mean(LogQ,0)
        stdMatrix[i,:] = np.std(LogQ,0,ddof=1)
        
    # fit harmonics to each site's flows
    modelCoeffs = np.zeros([nSites,2*len(k)])
    intercepts = np.zeros(nSites)
    for i in range(nSites):
        intercepts[i] = np.mean(meanMatrix[i,:])
        #de-mean before fitting model
        y = meanMatrix[i,:] - intercepts[i]
        modelCoeffs[i,:] = fitHarmonics(np.arange(1,13,1),k,y,nMonths)

    # Latin hypercube samples of uncertain streamflow parameters in 'uncertain_params.txt'
    LHsamples = np.loadtxt('LHsamples.txt')
    nScenarios = np.shape(LHsamples)[0]
    
    # calculate rescaled flows
    for i in range(nSites):
        DailyFlows = np.loadtxt('../validation/synthetic/' + sites[i] + '-1000x1-daily.csv',delimiter=',')
        # make normally distributed evaporation log-normal like flows
        if i in evapIndices:
            DailyFlows = np.exp(DailyFlows)
            
        LogMonthlyZ, P = calcLogMonthlyZ(DailyFlows, dayOfYear, meanMatrix[i,:], stdMatrix[i,:])
        for j in range(nScenarios):
            meanMultipliers, stdMultipliers = calcMultipliers(LHsamples[j,0], LHsamples[j,1], [LHsamples[j,2], LHsamples[j,4]],\
                [LHsamples[j,3], LHsamples[j,5]], modelCoeffs[i,:], intercepts[i], nMonths)
            NewMonthlyQ = calcNewMonthlyQ(LogMonthlyZ, meanMultipliers, stdMultipliers, meanMatrix[i,:], stdMatrix[i,:])
            NewDailyQ = calcNewDailyQ(NewMonthlyQ, P, dayOfYear, daysPerMonth)
            # convert evaporation back to real-space
            if i in evapIndices:
                NewDailyQ = np.log(NewDailyQ)

            np.savetxt('./rescaledFlows/' + sites[i] + '_Sample' + str(j+1) + '.csv',NewDailyQ, fmt='%.3f', delimiter=',')
    
    return None
    
def convert_data_to_monthly(Q, daysPerMonth):

    Nyears = int(len(Q)/365)
    Nmonths = len(daysPerMonth)
    Qmonthly = np.zeros([Nyears,Nmonths])
    
    for year in range(Nyears):
        for month in range(Nmonths):        
            start = year*365 + sum(daysPerMonth[0:month])
            # mean daily flow rate each month
            Qmonthly[year,month] = np.mean(Q[start:start+daysPerMonth[month]])
    
    return Qmonthly
    
def calcLogMonthlyZ(DailyFlows, dayOfYear, meanVector, stdVector):
    
    MonthlyQ = np.zeros([np.shape(DailyFlows)[0],len(dayOfYear)-1])
    LogMonthlyQ = np.zeros([np.shape(DailyFlows)[0],len(dayOfYear)-1])
    allP = [] # nested list of proportion matrices: [year 1, year 2, ...], where year1 = [month 1, month2 ..., month12]
    for i in range(np.shape(DailyFlows)[0]):
        annualP = [] # inner List of proportion matrices each month of year i
        for j in range(len(dayOfYear)-1):
            # calculate mean daily flow rate each month
            MonthlyQ[i,j] = np.mean(DailyFlows[i,dayOfYear[j]:dayOfYear[j+1]])
            # calculate proportion of monthly flow on each day
            annualP.append(DailyFlows[i,dayOfYear[j]:dayOfYear[j+1]]/ \
                np.sum(DailyFlows[i,dayOfYear[j]:dayOfYear[j+1]]))
                        
        allP.append(annualP)
            
    # calculate total monthly flow in log space
    LogMonthlyQ = np.log(MonthlyQ)
    
    # standardize log of monthly flows
    LogMonthlyZ = np.zeros(np.shape(LogMonthlyQ))
    for j in range(np.shape(LogMonthlyQ)[1]):
        LogMonthlyZ[:,j] = (LogMonthlyQ[:,j] - meanVector[j])/stdVector[j]
    
    return LogMonthlyZ, allP
    
def calcMultipliers(meanM, stdM, Cfactors, phiShifts, coeffs, intercept, T):
    
    K = int(len(coeffs)/2)
    C = np.zeros(K)
    phi = np.zeros(K)
    for k in range(K):
        C[k] = np.sqrt(coeffs[2*k]**2 + coeffs[2*k+1]**2)
        if coeffs[2*k] > 0:
            phi[k] = np.arctan(coeffs[2*k+1]/coeffs[2*k])
        elif coeffs[2*k] < 0:
            phi[k] = np.arctan(coeffs[2*k+1]/coeffs[2*k]) + math.pi
        else:
            phi[k] = math.pi/2
        
    y1 = np.zeros(T)
    y2 = np.zeros(T)
    for t in range(T):
        y1[t] = y1[t] + intercept
        y2[t] = y2[t] + intercept
        for k in range(K):
            y1[t] = y1[t] + C[k]*np.cos((2*math.pi*(k+1)*(t+1)/T)-phi[k])
            y2[t] = y2[t] + C[k]*Cfactors[k]*np.cos((2*math.pi*(k+1)*(t+1)/T)-(phi[k]-phiShifts[k]))
    
    meanMultipliers = meanM * y2 / y1    
    stdMultipliers = stdM * np.ones(len(meanMultipliers))
    
    return meanMultipliers, stdMultipliers
    
def calcNewMonthlyQ(LogMonthlyZ, meanMultipliers, stdMultipliers, meanVector, stdVector):
    
    NewLogMonthlyQ = np.zeros(np.shape(LogMonthlyZ))
    for i in range(np.shape(NewLogMonthlyQ)[0]):
        # unstandardize flows with multiplier adjustment
        NewLogMonthlyQ[i,:] = meanVector*meanMultipliers + LogMonthlyZ[i,:]*stdVector*stdMultipliers
        
    # convert log space flows to real space
    NewMonthlyQ = np.exp(NewLogMonthlyQ)
    
    return NewMonthlyQ
    
def calcNewDailyQ(NewMonthlyQ, P, dayOfYear, daysPerMonth):
    
    NewDailyQ = np.zeros([np.shape(NewMonthlyQ)[0],dayOfYear[-1]])
    for i in range(np.shape(NewDailyQ)[0]):
        for j in range(len(dayOfYear)-1):
            NewDailyQ[i,dayOfYear[j]:dayOfYear[j+1]] = P[i][j]*NewMonthlyQ[i,j]*daysPerMonth[j]
    
    return NewDailyQ
    
assure_path_exists(os.getcwd() + '/rescaledFlows/')

sites = ['qMarietta', 'qMuddyRun', 'qLateral', 'evapConowingo']
k = [1,2] # which harmonics to fit to annual cycle - this is fitting the first two (changing this will require other changes in this code and `uncertain_params.txt`)
evapIndices = [3]
MonsoonalRescaling(sites, k, evapIndices)
