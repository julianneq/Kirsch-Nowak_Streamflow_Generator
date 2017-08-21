# Kirsch-Nowak_Streamflow_Generator
This repository contains code for generating correlated synthetic daily streamflow time series at multiple sites assuming stationary hydrology. Monthly flows are generated using Cholesky decomposition (see [Kirsch et al. 2013](http://ascelibrary.org/doi/abs/10.1061/(ASCE)WR.1943-5452.0000287)) and then disaggregated to daily flows by proportionally scaling daily flows from a randomly selected historical month +/- 7 days as in [Nowak et al. (2010)](http://onlinelibrary.wiley.com/doi/10.1029/2009WR008530/full).

A full description is provided in `MethodDescription.pdf` in this directory. This code was used to generate the synthetic flows used in the following paper: Quinn, J.D., P.M. Reed, M. Giuliani and A. Castelletti, "Rival Framings: A framework for discovering how problem formulation uncertainties shape risk management trade-offs in water resources systems", *Water Resources Research*, *53*, doi: [10.1002/2017WR020524](http://onlinelibrary.wiley.com/doi/10.1002/2017WR020524/abstract). See that paper's supporting information for details on the methods and a statistical validation of the generator's performance.

Licensed under the GNU Lesser General Public License.

Contents:

* `data`: Directory containing example data set for the Susquehanna River Basin

* `generator`: Directory containing MATLAB code to generate correlated synthetic daily streamflow time series at multiple sites assuming stationary hydrology. Includes a README describing how to run the code.

* `validation`: Directory containing Python code to validate performance of synthetic streamflow generator. Includes a README describing how to run the code.