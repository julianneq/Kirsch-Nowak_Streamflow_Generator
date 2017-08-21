from __future__ import division
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from scipy.stats import norm,pearsonr
from scipy import stats

def init_plotting():
    '''Sets plotting characteristics'''
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (8,4)
    plt.rcParams['font.size'] = 15
    plt.rcParams['font.family'] = 'Source Sans Pro'
    plt.rcParams['axes.labelsize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.1*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']

init_plotting()

def set_box_color(bp, color):
  '''Sets colors of boxplot elements'''
  plt.setp(bp['boxes'], color=color)
  plt.setp(bp['whiskers'], color=color, linestyle='solid')
  plt.setp(bp['caps'], color=color)
  plt.setp(bp['medians'], color='k')

# thanks to http://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
def boxplots(syn, hist, n_pairs, xticks=True, legend=True):
  '''Makes boxplots'''
  bpl = plt.boxplot(syn, positions=np.arange(1,n_pairs+1)-0.2, sym='', widths=0.3, patch_artist=True)
  bpr = plt.boxplot(hist, positions=np.arange(1,n_pairs+1)+0.2, sym='', widths=0.3, patch_artist=True)
  set_box_color(bpl, 'navy')
  set_box_color(bpr, 'indianred')

  plt.plot([], c='navy', label='Synthetic')
  plt.plot([], c='indianred', label='Historical') # remember means and stdevs here are bootstrapped
  sns.despine(left=True)  
  plt.gca().xaxis.grid(False)

  if xticks:
    points = range(1,n_pairs+1)
    plt.gca().set_xticks(points)
    plt.gca().set_xticklabels(points)
  else:
    plt.gca().set_xticks([])
  plt.gca().set_xlim([0,n_pairs+1])

  if legend:
    plt.legend(ncol=1, loc='upper right')

  plt.locator_params(axis='y', nbins=6)

# Make statistical validation plots for spatial correlation
sites = ['qMarietta', 'qMuddyRun', 'qLateral', 'evapConowingo']
evapIndices = [3]
tStep = ['-monthly', '-daily']
titleStep = ['Monthly', 'Daily']
totalSteps = [12,365]

n_bootstrap = 100
n_pairs = 6
rh = np.zeros((n_bootstrap,n_pairs))
rs = np.zeros((100,n_pairs))
rhl = np.zeros((n_bootstrap,n_pairs))
rsl = np.zeros((100,n_pairs))

# plot real space and log space side by side, with a separate plot for monthly and daily
# t = 0: monthly, t = 1: daily
for t in range(2):
  ct = 0
  for i in range(len(sites)-1):
    for j in range(i+1,len(sites)):
      site1 = sites[i]
      site2 = sites[j]
      Hi = np.loadtxt('historical/' + site1 + tStep[t] + '.csv', delimiter=',').flatten()
      Hj = np.loadtxt('historical/' + site2 + tStep[t] + '.csv', delimiter=',').flatten()
      Si = np.loadtxt('synthetic/' + site1 + '-1000x1' + tStep[t] + '.csv', delimiter=',')
      Sj = np.loadtxt('synthetic/' + site2 + '-1000x1' + tStep[t] + '.csv', delimiter=',')
      
      # convert evaporation from normal to log-normal
      if i in evapIndices:
        Hi = np.exp(Hi)
        Si = np.exp(Si)
      if j in evapIndices:
        Hj = np.exp(Hj)
        Sj = np.exp(Sj)
        
      Hil = np.log(Hi)
      Hjl = np.log(Hj)
      Sil = np.log(Si)
      Sjl = np.log(Sj)

      for k in range(n_bootstrap):
        ix = np.random.randint(len(Hi), size=(len(Hi),))
        rh[k,ct] = pearsonr(Hi[ix],Hj[ix])[0]
        rs[k,ct] = pearsonr(Si[k,:],Sj[k,:])[0]
        rhl[k,ct] = pearsonr(Hil[ix],Hjl[ix])[0]
        rsl[k,ct] = pearsonr(Sil[k,:],Sjl[k,:])[0]

      ct += 1
      print ct

  fig = plt.figure()
  ax = fig.add_subplot(1,2,1)
  boxplots(rs, rh, n_pairs, xticks=True, legend=False)
  ax.set_ylim([-1,1])
  ax.set_xlabel('Pairs of Sites')
  ax.set_title('Real Space')

  ax = fig.add_subplot(1,2,2)
  boxplots(rsl, rhl, n_pairs, xticks=True)
  ax.set_ylim([-1,1])
  ax.set_yticklabels([])
  ax.set_xlabel('Pairs of Sites')
  ax.set_title('Log Space')

  fig.tight_layout()
  fig.subplots_adjust(top=0.8)
  fig.suptitle('Pairwise Correlation at ' + titleStep[t] + ' Time Step', fontsize=16)
  fig.savefig('figures/spatial-corr-dist' + tStep[t] + '.pdf')
  fig.clf()
  
  # hypothesis testing
  pvals = np.zeros([n_pairs,2])
  for k in range(n_pairs):
    tstat = stats.ranksums(rh[:,k], rs[:,k])
    pvals[k,0] = tstat[1]
    tstat = stats.ranksums(rhl[:,k], rsl[:,k])
    pvals[k,1] = tstat[1]
    
  fig = plt.figure()
  ax = fig.add_subplot(2,1,1)
  ax.bar(np.arange(1,n_pairs+1)-0.4, pvals[:,0], facecolor='0.7', edgecolor='None')
  ax.set_xlim([0,n_pairs+1])
  ax.plot([0,14],[0.05,0.05], color='k')
  ax.set_xticks([])
  ax.set_yticks(np.arange(0.0,1.1,0.2))
  ax.set_ylabel('Rank-sum $p$\n (real space)')
    
  ax = fig.add_subplot(2,1,2)
  ax.bar(np.arange(1,n_pairs+1)-0.4, pvals[:,1], facecolor='0.7', edgecolor='None')
  ax.set_xlim([0,n_pairs+1])
  ax.plot([0,14],[0.05,0.05], color='k')
  ax.set_yticks(np.arange(0.0,1.1,0.2))
  ax.set_xlabel('Month of Year')
  ax.set_ylabel('Rank-sum $p$\n (log space)')
  
  fig.tight_layout()
  fig.subplots_adjust(top=0.8)
  fig.suptitle('Statistical Differences in Pairwise Correlation at ' + titleStep[t] + ' Time Step', fontsize=16)
  fig.savefig('figures/spatial-corr-ranksum' + tStep[t] + '.pdf')
  fig.clf()
  
# plot daily and monthly side by side, with a separate plot for each space (real vs. log)
space = ['-real','-log']
titleSpace = ['Real','Log']
for k in range(len(space)):
    fig = plt.figure()
    for t in range(len(tStep)):
        ct = 0
        for i in range(len(sites)-1):
          for j in range(i+1,len(sites)):
            site1 = sites[i]
            site2 = sites[j]
            Hi = np.loadtxt('historical/' + site1 + tStep[t] + '.csv', delimiter=',').flatten()
            Hj = np.loadtxt('historical/' + site2 + tStep[t] + '.csv', delimiter=',').flatten()
            Si = np.loadtxt('synthetic/' + site1 + '-1000x1' + tStep[t] + '.csv', delimiter=',') 
            Sj = np.loadtxt('synthetic/' + site2 + '-1000x1' + tStep[t] + '.csv', delimiter=',') 
            
            if k == 1:
                if i in evapIndices:
                    Hi = np.exp(Hi)
                    Si = np.exp(Si)
                if j in evapIndices:
                    Hj = np.exp(Hj)
                    Sj = np.exp(Sj)
                Hi = np.log(Hi)
                Hj = np.log(Hj)
                Si = np.log(Si)
                Sj = np.log(Sj)
        
            for n in range(n_bootstrap):
              ix = np.random.randint(len(Hi), size=(len(Hi),))
              rh[n,ct] = pearsonr(Hi[ix],Hj[ix])[0]
              rs[n,ct] = pearsonr(Si[n,:],Sj[n,:])[0]
        
            ct += 1
            print ct
        
        ax = fig.add_subplot(1,2,t+1)
        if t == 0:
            boxplots(rs, rh, n_pairs, xticks=True, legend=False)
        else:
            boxplots(rs, rh, n_pairs, xticks=True)
            
        ax.set_ylim([-1,1])
        ax.set_xlabel('Pairs of Sites')
        ax.set_title(titleStep[t] + ' Spatial Correlation')
        
        if t == 1:
            ax.set_yticklabels([])
            
        # hypothesis testing
        pvals = np.zeros([n_pairs,2])
        for m in range(n_pairs):
            tstat = stats.ranksums(rh[:,m], rs[:,m])
            pvals[m,t] = tstat[1]
        
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)
    fig.suptitle(titleSpace[k] + ' Space Pairwise Correlation', fontsize=16)
    fig.savefig('figures/spatial-corr-dist' + space[k] + '.pdf')
    fig.clf()
      
    fig = plt.figure()
    ax = fig.add_subplot(2,1,1)
    ax.bar(np.arange(1,n_pairs+1)-0.4, pvals[:,0], facecolor='0.7', edgecolor='None')
    ax.set_xlim([0,n_pairs+1])
    ax.plot([0,14],[0.05,0.05], color='k')
    ax.set_xticks([])
    ax.set_yticks(np.arange(0.0,1.1,0.2))
    ax.set_ylabel('Rank-sum $p$\n (Monthly)')
        
    ax = fig.add_subplot(2,1,2)
    ax.bar(np.arange(1,n_pairs+1)-0.4, pvals[:,1], facecolor='0.7', edgecolor='None')
    ax.set_xlim([0,n_pairs+1])
    ax.plot([0,14],[0.05,0.05], color='k')
    ax.set_yticks(np.arange(0.0,1.1,0.2))
    ax.set_xlabel('Pairs of Sites')
    ax.set_ylabel('Rank-sum $p$\n (Daily)')
      
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)
    fig.suptitle('Statistical Differences in Pairwise Correlation', fontsize=16)
    fig.savefig('figures/spatial-corr-ranksum' + space[k] + '.pdf')
    fig.clf()