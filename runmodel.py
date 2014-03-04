# PyMC implementation of Panel 6.4 from Royle & Dorazio (2008) pp. 217
# MA MacNeil - 04.03.14

import Mbht
import sys
import os
import pdb
from pymc import MCMC, BinaryMetropolis, Metropolis, AdaptiveMetropolis
from pymc import Matplot as mp
import pdb


M = MCMC(Mbht)
#M = MCMC(models,db='sqlite',dbname='xx_dbase')
xex = 6
M.isample(10**xex, 10**xex-10**(xex-1), thin=10**(xex-4), verbose=2)
#M.isample(100000, 80000, thin=10, verbose=2)

try:
    os.mkdir('Outputs')
except OSError:
    pass
os.chdir('Outputs')
M.write_csv("zz_results.csv")
mp.plot(M)
