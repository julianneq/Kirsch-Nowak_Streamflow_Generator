from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from scipy.stats import norm

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

def makeReal_v_logPlots(site, tStep):
    ''''bla bla bla'''
    H = np.loadtxt('historical/' + site + '-' + tStep + '.csv', delimiter=',')
    H = H.reshape((np.shape(H)[0]*np.shape(H)[1],))
    S = np.loadtxt('synthetic/' + site + '-100x100-' + tStep + '.csv', delimiter=',')
    Hl = np.log(H)
    Sl = np.log(S)
    
    if tStep == 'monthly':
        nlags = 12 # show all lags
    elif tStep == 'daily':
        nlags = 30 # only show up to 30 lags
    
    fig = plt.figure()
    ax = fig.add_subplot(1,2,1)
    h = [None]*3
    
    for k in range(100):
      r2 = acf(S[k,:], nlags=nlags)
      h[0], = ax.step(range(nlags+1),r2, color='steelblue')
    
    # http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.stattools.acf.html
    r1, ci1 = acf(H, nlags=nlags, alpha=0.05)
    h[1], = ax.step(range(nlags+1),r1, color='k')
    h[2], = ax.step(range(nlags+1),ci1[:,0], color='k', linestyle='solid', linewidth=1)
    ax.step(range(nlags+1),ci1[:,1], color='k', linestyle='solid', linewidth=1)
    ax.set_xlim([-0.5,nlags])
    ax.set_title('Real Space')
    
    ax.legend(h, ['Synthetic', 'Historical', '95% CI'], loc='upper center')
    if tStep == 'monthly':
        ax.set_xlabel('Lag (months)')
        ax.set_ylim([-1.0,1.0])
    elif tStep == 'daily':
        ax.set_xlabel('Lag (days)')
        ax.set_ylim([0.0,1.0])
    sns.despine(left=True)  
    ax.xaxis.grid(False)
    
    ax = fig.add_subplot(1,2,2)
    
    for k in range(100):
      r2 = acf(Sl[k,:], nlags=nlags)
      h[0], = ax.step(range(nlags+1),r2, color='steelblue')
    
    r1, ci1 = acf(Hl, nlags=nlags, alpha=0.05)
    h[1], = ax.step(range(nlags+1),r1, color='k')
    h[2], = ax.step(range(nlags+1),ci1[:,0], color='k', linestyle='solid', linewidth=1)
    ax.step(range(nlags+1),ci1[:,1], color='k', linestyle='solid', linewidth=1)
    ax.set_xlim([-0.5,nlags])
    ax.set_ylim([-1.0,1.0])
    ax.set_title('Log Space')
    
    if tStep == 'monthly':
        ax.set_xlabel('Lag (months)')
        ax.set_ylim([-1.0,1.0])
    elif tStep == 'daily':
        ax.set_xlabel('Lag (days)')
        ax.set_ylim([0.0,1.0])
    sns.despine(left=True)  
    ax.xaxis.grid(False)
    
    fig.tight_layout()
    fig.savefig('figures/autocorr-' + tStep + '.pdf')
    fig.clf()

def makeMonthly_v_DailyPlots(site, space):
    ''''bla bla bla'''
    nlags = [12,30] # find correlation at all lags for months, but only up to 30 days
    
    fig = plt.figure()
    xlabels = ['Lag (months)','Lag (days)']
    tStep = ['monthly','daily']
    if space == 'real':
        title = 'Real'
    else:
        title = 'Log'
    
    for j in range(len(nlags)):
        H = np.loadtxt('historical/' + site + '-' + tStep[j] + '.csv', delimiter=',')
        H = H.reshape((np.shape(H)[0]*np.shape(H)[1],))
        S = np.loadtxt('synthetic/' + site + '-100x100-' + tStep[j] + '.csv', delimiter=',')
        if space == 'log':
            H = np.log(H)
            S = np.log(S)
        
        ax = fig.add_subplot(1,2,j+1)
        h = [None]*3
        for k in range(100):
          r2 = acf(S[k,:], nlags=nlags[j])
          h[0], = ax.step(range(nlags[j]+1),r2, color='steelblue')
        
        # http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.stattools.acf.html
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
    fig.savefig('figures/autocorr-' + space + '.pdf')
    fig.show()

makeReal_v_logPlots('qMarietta','monthly')
makeReal_v_logPlots('qMarietta','daily')
makeMonthly_v_DailyPlots('qMarietta','real')
makeMonthly_v_DailyPlots('qMarietta','log')

