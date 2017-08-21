# Kirsch-Nowak_Streamflow_Generator Validation
This directory contains Python code for validating the performance of the synthetic streamflow generator.

Contents:
`autocorr.py`: Plots the autocorrelation function (acf) and 95\% confidence intervals for the historical flows at Marietta (black), as well as the realizations from the synthetic flows (blue). This is done for up to 12 lags at a monthly time step and 30 lags at a daily time step. The site whose acf is plotted can be changed on line 39.

`monthly-moments.py`: Makes boxplots of bootstrapped historical monthly flows (pink) and synthetic monthly flows (blue) as well as their means and standard deviations at Marietta. Also plots p-values from rank-sum test for differences in the median between historical and synthetic flows and from Levene's test for differences in the variance between historical and synthetic flows. The site being plotted can be changed on line 76.

`plotFDCrange.py`: Plots the ranges spanned by historical (black) and synthetic (gray)flow duration curves for each year of the historical and synthetic records at all sites. The list of sites can be changed on line 98. Indices of sites for which the data is evaporation rather than flows can be changed on line 99.

`spatial-corr.py`: Makes boxplots of pairwise spatial correlations in bootstrapped historical (pink) and synthetic (blue) monthly flows. Also plots p-values from rank-sum test for differences in the median between historical and synthetic flows. The list of sites can be changed on line 75. Indices of sites for which the data is evaporation rather than flows can be changed on line 76.