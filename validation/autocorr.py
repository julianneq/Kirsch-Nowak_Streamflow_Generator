'''Plots the autocorrelation function (acf) and 95\% confidence intervals for
the historical flows at Marietta (black), as well as the realizations from the
synthetic flows (blue). This is done for up to 12 lags at a monthly time step
and 30 lags at a daily time step. The site whose acf is plotted can be changed
on line 39.'''

from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from scipy.stats import norm
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
    plt.rcParams['figure.figsize'] = (10, 4)
    plt.rcParams['font.size'] = 15
    plt.rcParams['font.family'] = 'Source Sans Pro'
    plt.rcParams['axes.labelsize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']

init_plotting()

site = 'qMarietta'
space = ['log','real']
xlabels = ['Lag (months)','Lag (days)']
tStep = ['monthly','daily']
nlags = [12,30] # find correlation at all lags for monthly data, but only up to 30 days for daily data

for i in range(len(space)):
    fig = plt.figure()
    if space[i] == 'real':
        title = 'Real'
    else:
        title = 'Log'
    
    for j in range(len(nlags)):
        H = np.loadtxt('historical/' + site + '-' + tStep[j] + '.csv', delimiter=',')
        H = H.reshape((np.shape(H)[0]*np.shape(H)[1],))
        S = np.loadtxt('synthetic/' + site + '-100x100-' + tStep[j] + '.csv', delimiter=',')
        if space[i] == 'log':
            H = np.log(H)
            S = np.log(S)
        
        ax = fig.add_subplot(1,2,j+1)
        h = [None]*3
        for k in range(100):
          r2 = acf(S[k,:], nlags=nlags[j])
          h[0], = ax.step(range(nlags[j]+1),r2, color='steelblue')
        
        # http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.stattools.acf.html
        # plot autocorrelation function
        r1, ci1 = acf(H, nlags=nlags[j], alpha=0.05)
        h[1], = ax.step(range(nlags[j]+1),r1, color='k')
        h[2], = ax.step(range(nlags[j]+1),ci1[:,0], color='k', linestyle='solid', linewidth=1)
        ax.step(range(nlags[j]+1),ci1[:,1], color='k', linestyle='solid', linewidth=1)
        ax.set_xlim([-0.5,nlags[j]])
        if tStep[j] == 'monthly':
            ax.set_ylim([-1.0,1.0])
        else:
            ax.set_ylim([0.0,1.0])
        
        if j == 0:
            ax.legend(h, ['Synthetic', 'Historical', '95% CI'], loc='upper center')
        
        ax.set_xlabel(xlabels[j])
        sns.despine(left=True)  
        ax.xaxis.grid(False)
    
    fig.tight_layout()
    fig.subplots_adjust(top=0.85)
    fig.suptitle(title + ' Space Autocorrelation',fontsize=16)    
    fig.savefig('figures/autocorr-' + space[i] + '.pdf')
    fig.show()

