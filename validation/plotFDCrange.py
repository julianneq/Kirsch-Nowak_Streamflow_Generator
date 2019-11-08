'''Plots the ranges spanned by historical (black) and synthetic (gray)flow
duration curves for each year of the historical and synthetic records at all
sites. The list of sites can be changed on line 98. Indices of sites for which
the data is evaporation rather than flows can be changed on line 99.'''

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import os

# https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
def assure_path_exists(path):
    '''Creates directory if it doesn't exist'''
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

assure_path_exists(os.getcwd() + '/figures/')

def init_plotting():
    '''Sets plotting characteristics'''
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (9,7)
    plt.rcParams['font.size'] = 15
    plt.rcParams['font.family'] = 'Source Sans Pro'
    plt.rcParams['axes.labelsize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']

init_plotting()

def plotFDCrange(syntheticData, histData, sites, evapIndices):
    '''Plots the upper and lower bound of each site's FDCs under 
    all annual historical and synthetic time series'''
    n = 365
    M = np.array(range(1,n+1))
    P = (M-0.5)/n
    
    fig = plt.figure()
    for j in range(np.shape(histData)[1]):
        # load data for site j
        histData_j = histData[:,j]
        syntheticData_j = syntheticData[:,j]
        histData_newshape = (len(histData_j)//n, n)  # note: use floor division - https://stackoverflow.com/questions/42989289/python-typeerror-float-object-cannot-be-interpreted-as-an-integer
        f_hist = np.reshape(histData_j, histData_newshape)
        syntheticData_newshape = (len(syntheticData_j)//n, n)  # note: use floor division - https://stackoverflow.com/questions/42989289/python-typeerror-float-object-cannot-be-interpreted-as-an-integer
        f_syn = np.reshape(syntheticData_j, syntheticData_newshape)
        
        # calculate historical FDCs
        F_hist = np.empty(np.shape(f_hist))
        F_hist[:] = np.NaN
        for k in range(np.shape(F_hist)[0]):
            F_hist[k,:] = np.sort(f_hist[k,:],0)[::-1]
            
        # calculate synthetic FDCs
        F_syn = np.empty(np.shape(f_syn))
        F_syn[:] = np.NaN
        for k in range(np.shape(F_syn)[0]):
            F_syn[k,:] = np.sort(f_syn[k,:],0)[::-1]
            
        ax = fig.add_subplot(2,2,j+1)
        # plot min and max at each percentile
        if j in evapIndices:
            ax.plot(P,np.min(F_syn,0),c='k',label='Synthetic')
            ax.plot(P,np.max(F_syn,0),c='k',label='Synthetic')
            ax.plot(P,np.min(F_hist,0),c='#bdbdbd',label='Historical')
            ax.plot(P,np.max(F_hist,0),c='#bdbdbd',label='Historical')
            ax.set_ylabel('Rate (in/day)')
        else:
            ax.semilogy(P,np.min(F_syn,0),c='k',label='Synthetic')
            ax.semilogy(P,np.max(F_syn,0),c='k',label='Synthetic')
            ax.semilogy(P,np.min(F_hist,0),c='#bdbdbd',label='Historical')
            ax.semilogy(P,np.max(F_hist,0),c='#bdbdbd',label='Historical')
            ax.set_ylabel('Flow (cfs)')
        
        # fill between min and max to show range of FDCs
        ax.fill_between(P, np.min(F_syn,0), np.max(F_syn,0), color='k')
        ax.fill_between(P, np.min(F_hist,0), np.max(F_hist,0), color='#bdbdbd')
        ax.set_title(sites[j],fontsize=18)
        ax.tick_params(axis='both',labelsize=14)
        if j <= 1:
            ax.tick_params(axis='x',labelbottom='off')
            
        handles, labels = plt.gca().get_legend_handles_labels()
        labels, ids = np.unique(labels, return_index=True)
        handles = [handles[i] for i in ids]
        plt.grid(True,which='both',ls='-')
        
    fig.subplots_adjust(bottom=0.2,wspace=0.32)
    fig.legend(handles, labels, fontsize=18,loc='lower center',ncol=2, frameon=True)
    fig.text(0.5,0.1,'Probability of Exceedance',ha='center',fontsize=18)
    fig.savefig('figures/FDCs.pdf')
    fig.clf()
    
# plot range of flow duration curves from historical record and synthetic generation
syntheticData = np.loadtxt('./synthetic/Qdaily-1000x1.csv',delimiter=',')
histData = np.loadtxt('./../data/Qdaily.txt')
histData = histData[:,0:4] # remove last column (evaporation at Muddy Run same as Conowingo)
sites = ['Marietta', 'Muddy Run', 'Lateral Inflow', 'Evaporation']
evapIndices=[3]
plotFDCrange(syntheticData, histData, sites, evapIndices)