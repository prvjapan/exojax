import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jax.numpy as jnp
from jax import random

dat=pd.read_csv("../tutorial/spectrum.txt",delimiter=",",names=("wav","flux"))
#data generated by Forward modeling.ipynb
wavd=dat["wav"].values
flux=dat["flux"].values
nusd=jnp.array(1.e8/wavd[::-1])
sigmain=0.05
norm=40000
nflux=flux/norm+np.random.normal(0,sigmain,len(wavd))


from exojax.spec.lpf import xsmatrix
from exojax.spec.exomol import gamma_exomol
from exojax.spec.hitran import SijT, doppler_sigma, gamma_natural, gamma_hitran
from exojax.spec.hitrancia import read_cia, logacia
from exojax.spec.rtransfer import rtrun, dtauM, dtauCIA, nugrid
from exojax.spec import planck, response
from exojax.spec.lpf import xsvector
from exojax.spec import molinfo
from exojax.utils.constants import RJ, pc, Rs, c


# The model is almost same as the forward modeling, but we will infer here Rp, RV, MMR_CO, T0, alpha, and Vsini. 
# In[7]:


from exojax.spec import rtransfer as rt
NP=100
Parr, dParr, k=rt.pressure_layer(NP=NP)
Nx=1500
nus,wav,res=nugrid(np.min(wavd)-5.0,np.max(wavd)+5.0,Nx,unit="AA")

R=100000.
beta=c/(2.0*np.sqrt(2.0*np.log(2.0))*R)

molmassCO=molinfo.molmass("CO")
mmw=2.33 #mean molecular weight
mmrH2=0.74
molmassH2=molinfo.molmass("H2")
vmrH2=(mmrH2*mmw/molmassH2) #VMR

Mp = 33.2 #fixing mass...

# Loading the molecular database of CO and the CIA
# In[8]:





#reference pressure for a T-P model                                             
Pref=1.0 #bar
ONEARR=np.ones_like(Parr)
ONEWAV=jnp.ones_like(nflux)


import jax.numpy as jnp
from jax import random
from jax import vmap, jit

import numpyro.distributions as dist
import numpyro
from numpyro.infer import MCMC, NUTS
from numpyro.infer import Predictive
from numpyro.diagnostics import hpdi


# In[14]:


smalla=1.0
smalldiag=smalla**2*jnp.identity(NP)


# Now we write the model, which is used in HMC-NUTS.

# In[15]:


def modelcov(t,tau,a):
    fac=1.e-5
    Dt = t - jnp.array([t]).T
    amp=a
    K=amp*jnp.exp(-(Dt)**2/2/(tau**2))+amp*fac*jnp.identity(NP)
    return K


# In[16]:


ZEROARR=jnp.zeros_like(Parr)
ONEARR=jnp.ones_like(Parr)

lnParr=jnp.log10(Parr)


# In[17]:

def comp_Tarr(okey):
    okey,key=random.split(okey)
    lnsT = numpyro.sample('lnsT', dist.Uniform(3.0,5.0),rng_key=key)
#    lnsT=4.0
    sT=10**lnsT
    okey,key=random.split(okey)
    lntaup =  numpyro.sample('lntaup', dist.Uniform(0,1),rng_key=key)
#    lntaup=0.5
    taup=10**lntaup    
    cov=modelcov(lnParr,taup,sT)

    okey,key=random.split(okey)
    T0 =  numpyro.sample('T0', dist.Uniform(800,1500),rng_key=key)
    okey,key=random.split(okey)
    Tarr=numpyro.sample("Tarr", dist.MultivariateNormal(loc=ONEARR, covariance_matrix=cov),rng_key=key)+T0

    #lnT0=3.0 #1000K
    #lnTarr=numpyro.sample("Tarr", dist.MultivariateNormal(loc=lnT0*ONEARR, covariance_matrix=cov),rng_key=key)
    #Tarr=10**lnTarr
    return Tarr

okey=random.PRNGKey(20)
for i in range(0,100):
    okey,key=random.split(okey)
    Tarr=comp_Tarr(key)
    print(np.sum(Tarr))
    plt.plot(Tarr,Parr,alpha=0.4)
plt.yscale("log")
#plt.xscale("log")

plt.gca().invert_yaxis()
plt.show()
    