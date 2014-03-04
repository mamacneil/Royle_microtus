# PyMC implementation of Panel 6.4 from Royle & Dorazio (2008) pp. 217
# MA MacNeil - 04.03.14

import sys
import os
import pdb
import numpy as np
from pymc import Matplot as mp
from pymc import rnormal
import pandas as pd




# Import data
data = pd.read_csv('microtus.csv')

# Observed
Y = data[['k1','k2','k3','k4','k5']]
# Number of observed individuals
Nobs = np.shape(Y)[0]
# Number of capture occasions
K = np.shape(Y)[1]

# Agumentation size
Nz = 125
# Augmented data
Y = Y.append(pd.DataFrame(np.zeros(Nz*K).reshape(Nz,K),columns=['k1','k2','k3','k4','k5']))
Y = np.array(Y)

# Observed individuals
sighted = Y.sum(axis=1)>0
# Unobserved individuals
no_sightings = np.array([i for i,x in enumerate(sighted) if not x])

# Standardize masses
massx = (data.mass-np.mean(data.mass))/np.sqrt(np.var(data.mass))
# Individual masses with missing values
missing_mass = np.array([x for x in np.array(massx)]+[-999]*Nz)
massx = np.array([[x]*K for x in missing_mass])
mass = np.ma.masked_equal(massx, -999)

# Number of observed and unobserved individuals
Naug = np.shape(Y)[0]

# Indicator for previously captured
first = np.array([None]*Naug)
prevcap = np.zeros(Naug*K).reshape(Naug,K)
for i in range(Naug-Nz):
    first[i] = [x for x in Y[i,]].index(1)
    if first[i]<K:
        prevcap[i,(first[i]+1):] = 1

# Lagged indicator for previous capture
lagY = np.zeros(Naug*K).reshape(Naug,K)
for i in range(Naug):
    lagY[i,1:] = Y[i,:(K-1)]

