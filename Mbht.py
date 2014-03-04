# PyMC implementation of Panel 6.4 from Royle & Dorazio (2008) pp. 217
# MA MacNeil - 04.03.14

import sys
import os
from pymc import *
import numpy as np
import pdb
from data import *




# Covariate priors
a0 = Uniform('a0', lower=-10, upper=10, value=0.0)
a1 = Uniform('a1', lower=-10, upper=10, value=0.0)
a2 = Uniform('a2', lower=-10, upper=10, value=0.0)
a3 = Uniform('a3', lower=-10, upper=10, value=0.0)

# Mass mean
mu = Uniform('mu', lower=-10, upper=10, value=0.3)
# Mass SD
sigma_0 = Uniform('sigma_0', lower=0, upper=100, value=1.2)
# Mass precision
tau_0 = Lambda('tau_0', lambda sd=sigma_0: sd**-2)
# Imputed masses for agumented group
iMass = Normal('Mass', mu=mu, tau=tau_0, value=mass, observed=True, trace=False)
# Detection model
phi = Lambda('phi', lambda a0=a0, a1=a1, a2=a2, a3=a3, M=iMass: invlogit(a0*(1-prevcap)+a1*prevcap+a2*lagY+a3*M), trace=False)

# P(presence) for augmented groups
psi = Uniform('psi', lower=0, upper=1, value=0.5)
# Occupancy state for agumented group
Z = Bernoulli('Z', p=psi, value=sighted, trace=False)

# Detection given presence
muY = Lambda('muY', lambda z=Z,p=phi: (z*p.T).T, trace=False)

# Likelihood
Yi = Bernoulli('Yi', p=muY, value=Y, observed=True)

# Posterior estimate for population size
N = Lambda('N', lambda z=Z: sum(z))






