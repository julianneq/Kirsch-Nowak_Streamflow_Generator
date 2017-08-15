from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from scipy.stats import norm


def init_plotting():
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (5, 3)
    plt.rcParams['font.size'] = 13
    plt.rcParams['font.family'] = 'Source Sans Pro'
    plt.rcParams['axes.labelsize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']

init_plotting()

# from: http://www.real-statistics.com/correlation/two-sample-hypothesis-testing-correlation/
# two-tailed Z test
def fisher_test(r1, r2, n1, n2):
  # fix number of samples: http://www.ltrr.arizona.edu/~dmeko/notes_9.pdf
  # "effective" sample size (Mitchell et al. 1966)
  lags = np.arange(len(r1))
  n1 = n1*(1-r1[1])/(1+r1[1])-lags-3
  n2 = n2*(1-r2[1])/(1+r2[1])-lags-3

  r1 = np.arctanh(r1)
  r2 = np.arctanh(r2) # fisher transformation
  s = np.sqrt(1/n1 + 1/n2)
  Z = np.abs(r1-r2)/s
  p = 2*(1 - norm.cdf(Z))
  return p


def makeReal_v_logPlots(tStep):
    site = 'tabu'
    H = np.loadtxt('historical/'+site+'-' + tStep + '.csv', delimiter=',')
    H = H.reshape((np.shape(H)[0]*np.shape(H)[1],))
    S = np.loadtxt('synthetic/'+site+'-100x100-' + tStep + '.csv', delimiter=',')
    #S5 = np.loadtxt('synthetic-n5/'+site+'.csv', delimiter=',') 
    Hl = np.log(H)
    Sl = np.log(S)
    
    k = 2
    if tStep == 'monthly':
        nlags = 12
    elif tStep == 'daily':
        nlags = 365
    
    fig = plt.figure()
    ax = fig.add_subplot(1,2,1)
    h = [None]*3
    
    for k in range(100):
      r2 = acf(S[k,:], nlags=nlags)
      h[0], = ax.step(range(nlags+1),r2, color='steelblue')
    
    # for k in range(100):
    #   r2 = acf(S5[k,:], nlags=nlags)
    #   h[0], = plt.step(range(nlags+1),r2, color='steelblue')
    
    # http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.stattools.acf.html
    r1, ci1 = acf(H, nlags=nlags, alpha=0.05)
    h[1], = ax.step(range(nlags+1),r1, color='k')
    h[2], = ax.step(range(nlags+1),ci1[:,0], color='k', linestyle='solid', linewidth=1)
    ax.step(range(nlags+1),ci1[:,1], color='k', linestyle='solid', linewidth=1)
    ax.set_xlim([-0.5,nlags])
    ax.set_ylim([-1.0,1.0])
    ax.set_title('Real Space')
    
    
    ax.legend(h, ['Synthetic', 'Historical', '95% CI'], loc='upper center')
    if tStep == 'monthly':
        ax.set_xlabel('Lag (months)')
    elif tStep == 'daily':
        ax.set_xlabel('Lag (days)')
    # plt.ylabel('ACF')
    # plt.title('Real Space')
    sns.despine(left=True)  
    ax.xaxis.grid(False)
    
    # plt.plot([0,nlags],[0,0], color='k', linestyle='--', linewidth=2)
    
    
    # This test rejects for a lot of lags -- not good. 
    # it's because the "sample size" is so big, is that right??
    # p = fisher_test(r1, r2, len(H), len(S[k,:]))
    # print p
    # how straight-up do we want to be here?
    
    
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
    
    
    # plt.legend(h, ['Synthetic', 'Historical', '95% CI'])
    if tStep == 'monthly':
        ax.set_xlabel('Lag (months)')
    elif tStep == 'daily':
        ax.set_xlabel('Lag (days)')
    ax.set_yticklabels([])
    # plt.ylabel('ACF')
    # plt.plot([0,nlags],[0,0], color='k', linestyle='--', linewidth=2)
    # plt.title('Log Space')
    sns.despine(left=True)  
    ax.xaxis.grid(False)
    
    
    fig.tight_layout()
    fig.set_size_inches([9.8125, 4.3])
    #fig.savefig('autocorr-' + tStep + '.png')
    #fig.savefig('autocorr-' + tStep + '.svg')
    fig.savefig('autocorr-' + tStep + '.pdf')
    fig.show()

def makeMonthly_v_DailyPlots(space):
    site = 'tabu'
    k = 2
    nlags = [12,365]
    
    fig = plt.figure()
    titles = ['Monthly Autocorrelation','Daily Autocorrelation']
    xlabels = ['Lag (months)','Lag (days)']
    tStep = ['monthly','daily']
    
    for j in range(len(nlags)):
        H = np.loadtxt('historical/'+site+'-' + tStep[j] + '.csv', delimiter=',')
        H = H.reshape((np.shape(H)[0]*np.shape(H)[1],))
        S = np.loadtxt('synthetic/'+site+'-100x100-' + tStep[j] + '.csv', delimiter=',')
        if space == 'log':
            H = np.log(H)
            S = np.log(S)
        
        ax = fig.add_subplot(1,2,j+1)
        h = [None]*3
        for k in range(100):
          r2 = acf(S[k,:], nlags=nlags[j])
          h[0], = ax.step(range(nlags[j]+1),r2, color='steelblue')
        
        # for k in range(100):
        #   r2 = acf(S5[k,:], nlags=nlags)
        #   h[0], = plt.step(range(nlags+1),r2, color='steelblue')
        
        # http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.stattools.acf.html
        r1, ci1 = acf(H, nlags=nlags[j], alpha=0.05)
        h[1], = ax.step(range(nlags[j]+1),r1, color='k')
        h[2], = ax.step(range(nlags[j]+1),ci1[:,0], color='k', linestyle='solid', linewidth=1)
        ax.step(range(nlags[j]+1),ci1[:,1], color='k', linestyle='solid', linewidth=1)
        ax.set_xlim([-0.5,nlags[j]])
        ax.set_ylim([-1.0,1.0])
        ax.set_title(titles[j])
        
        if j == 0:
            ax.legend(h, ['Synthetic', 'Historical', '95% CI'], loc='upper center')
        
        ax.set_xlabel(xlabels[j])
        # plt.ylabel('ACF')
        # plt.title('Real Space')
        sns.despine(left=True)  
        ax.xaxis.grid(False)
    
    fig.tight_layout()
    fig.set_size_inches([9.8125, 4.3])
    fig.savefig('autocorr-' + space + '.pdf')
    fig.savefig('autocorr-' + space + '.png')
    fig.savefig('autocorr-' + space + '.svg')
    fig.show()

makeReal_v_logPlots('monthly')
makeReal_v_logPlots('daily')
makeMonthly_v_DailyPlots('real')
makeMonthly_v_DailyPlots('log')

# the "real" correlograms from scipy are below:

# ax = plt.subplot(2,2,1)
# plot_acf(H[start:], lags=nlags, ax=ax)
# plt.ylabel('Autocorrelation')
# plt.title('Historical, real space')
# plt.tight_layout()


# ax = plt.subplot(2,2,2)
# plot_acf(S[k,start:], lags=nlags, ax=ax)
# plt.title('Synthetic, real space')
# plt.tight_layout()

# ax = plt.subplot(2,2,3)
# plot_acf(Hl[start:], lags=nlags, ax=ax)
# plt.xlabel('lag (weeks)')
# plt.ylabel('Autocorrelation')
# plt.title('Historical, log space')
# plt.tight_layout()


# ax = plt.subplot(2,2,4)
# plot_acf(Sl[k,start:], lags=nlags, ax=ax)
# plt.xlabel('lag (weeks)')
# plt.title('Synthetic, log space')
# plt.tight_layout()

# plt.show()

