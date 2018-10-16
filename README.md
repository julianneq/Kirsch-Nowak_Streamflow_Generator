# Kirsch-Nowak_Streamflow_Generator

By [Matteo Giuliani](http://giuliani.faculty.polimi.it), [Jon Herman](http://herman.faculty.ucdavis.edu/) and [Julianne Quinn](https://www.linkedin.com/in/julianne-quinn-411a2a13)

This repository contains code for generating correlated synthetic daily streamflow time series at multiple sites assuming stationary hydrology. Monthly flows are generated using Cholesky decomposition (see [Kirsch et al. 2013](http://ascelibrary.org/doi/abs/10.1061/(ASCE)WR.1943-5452.0000287)) and then disaggregated to daily flows by proportionally scaling daily flows from a randomly selected historical month +/- 7 days as in [Nowak et al. (2010)](http://onlinelibrary.wiley.com/doi/10.1029/2009WR008530/full).

A full description is provided in `MethodDescription.pdf` in this directory. This code was used to generate synthetic flows in the following papers:  
  
* Giuliani, M., J.D. Quinn, J.D. Herman, A. Castelletti and P.M. Reed, 2017, "Scalable multiobjective control for large-scale water resources systems under uncertainty", *IEEE Transactions on Control Systems Technology*, *99*, doi: [10.1109/TCST.2017.2705162](http://ieeexplore.ieee.org/document/7959085/).
  
* Quinn, J.D., P.M. Reed, M. Giuliani and A. Castelletti, 2017, "Rival Framings: A framework for discovering how problem formulation uncertainties shape risk management trade-offs in water resources systems", *Water Resources Research*, *53*, doi: [10.1002/2017WR020524](http://onlinelibrary.wiley.com/doi/10.1002/2017WR020524/abstract).

* Zatarain Salazar, J., P.M. Reed, J.D. Quinn, M. Giuliani and A. Castelletti, 2017, "Balancing exploration, uncertainty and computational demands in many objective reservoir optimization", *Advances in Water Resources*, *109*, 196-210, doi: [10.1016/j.advwatres.2017.09.014](https://doi.org/10.1016/j.advwatres.2017.09.014).

Licensed under the GNU Lesser General Public License.

Contents:

* `monsoonal_rescaling`: Directory containing Python code to rescale synthetic streamflows by changing the log-space mean, log-space standard deviation, and amplitudes and phase shifts of harmonics fit to the log-space annual cycle. Includes a README describing how to run the code. This method is used for the Red River basin in Vietnam in the following paper: Quinn, J.D., P.M. Reed, M. Giuliani, A. Castelletti, J.W. Oyler, R.E. Nicholas, 2018, "Exploring how changing monsoonal dynamics and human pressures challenge multi-reservoir management for flood protection, hydropower production and agricultural water supply", *Water Resources Research*, *54*, doi: [10.1029/2018WR022743](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2018WR022743).

* `data`: Directory containing example data set for the Susquehanna River Basin (for a description of the system, see Giuliani, M., J.D. Herman, A. Castellett, P.M. Reed, 2014, "Many-objective reservoir policy identification and refinement to reduce policy inertia and myopia in water management", *Water Resources Research*, *50*, doi: [10.1002/ 2013WR014700](http://onlinelibrary.wiley.com/doi/10.1002/2013WR014700/full)).

* `stationary_generator`: Directory containing MATLAB code to generate correlated synthetic daily streamflow time series at multiple sites assuming stationary hydrology. Includes a README describing how to run the code.

* `validation`: Directory containing Python code to validate performance of synthetic streamflow generator. Includes a README describing how to run the code.
