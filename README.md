# exojax
 [![License](https://img.shields.io/github/license/HajimeKawahara/exojax)](https://github.com/HajimeKawahara/exojax/blob/develop/LICENSE)
 [![Docs](https://img.shields.io/badge/docs-exojax-brightgreen)](http://secondearths.sakura.ne.jp/exojax/)
 [![arxiv](https://img.shields.io/badge/arxiv-2105.14782-blue)](http://arxiv.org/abs/2105.14782)
 
Auto-differentiable line-by-line spectral modeling of exoplanets/brown dwarfs using JAX. Read [the docs](http://secondearths.sakura.ne.jp/exojax) 🐕. 

<img src="https://user-images.githubusercontent.com/15956904/119144463-a5cba180-ba83-11eb-8a26-687075d43883.png" Titie="exojax" Width=850px>
 
## Functions

<details open><summary>Voigt Profile :heavy_check_mark: </summary>

```python3
from exojax.spec import voigt
nu=numpy.linspace(-10,10,100)
voigt(nu,1.0,2.0) #sigma_D=1.0, gamma_L=2.0
```

</details>

<details><summary>Cross Section using HITRAN/HITEMP/ExoMol :heavy_check_mark: </summary>
 
```python
from exojax.spec import AutoXS
nus=numpy.linspace(1900.0,2300.0,200000,dtype=numpy.float64) #wavenumber (cm-1)
autoxs=AutoXS(nus,"ExoMol","CO") #using ExoMol CO (12C-16O). HITRAN and HITEMP are also supported.  
xsv=autoxs.xsection(1000.0,1.0) #cross section for 1000K, 1bar (cm2)
```

 <img src="https://user-images.githubusercontent.com/15956904/111430765-2eedf180-873e-11eb-9740-9e1a313d590c.png" Titie="exojax auto cross section" Width=850px> 
 
<details><summary> Do you just want to plot the line strength? </summary>

```python
ls=autoxs.linest(1000.0,1.0) #line strength for 1000K, 1bar (cm)
plt.plot(autoxs.mdb.nu_lines,ls,".")
```

autoxs.mdb is the [moldb.MdbExomol class](http://secondearths.sakura.ne.jp/exojax/exojax/exojax.spec.html#exojax.spec.moldb.MdbExomol) for molecular database. Here is a entrance to a deeper level. exojax is more flexible in the way it calculates the molecular lines. 🐈 Go to [the docs](http://secondearths.sakura.ne.jp/exojax) for the deeper level.  

</details>
 
 </details>

<details><summary>Emission Spectrum :heavy_check_mark: </summary>

```python
from exojax.spec.rtransfer import nugrid
from exojax.spec import AutoRT
nus,wav,res=nugrid(1900.0,2300.0,200000,"cm-1")
Parr=numpy.logspace(-8,2,100) #100 layers from 10^-8 bar to 10^2 bar
Tarr = 500.*(Parr/Parr[-1])**0.02    
autort=AutoRT(nus,1.e5,2.33,Tarr,Parr) #g=1.e5 cm/s2, mmw=2.33
autort.addcia("H2-H2",0.74,0.74)       #CIA, mmr(H)=0.74
autort.addcia("H2-He",0.74,0.25)       #CIA, mmr(He)=0.25
autort.addmol("ExoMol","CO",0.01)      #CO line, mmr(CO)=0.01
F=autort.rtrun()
```

<img src="https://user-images.githubusercontent.com/15956904/116488770-286ea000-a8ce-11eb-982d-7884b423592c.png" Titie="exojax auto \emission spectrum" Width=850px> 

<details><summary>Are you an observer? </summary>
 
```python
nusobs=numpy.linspace(1900.0,2300.0,10000,dtype=numpy.float64) #observation wavenumber bin (cm-1)
F=autort.spectrum(nusobs,100000.0,20.0,0.0) #R=100000, vsini=10km/s, RV=0km/s
```
 
  <img src="https://user-images.githubusercontent.com/15956904/116488769-273d7300-a8ce-11eb-8da1-661b23215c26.png" Titie="exojax auto \emission spectrum for observers" Width=850px> 

 </details>

If you want to customize the model, see [here](http://secondearths.sakura.ne.jp/exojax/tutorials/forward_modeling.html).

</details>

<details><summary>HMC-NUTS of Emission Spectra :heavy_check_mark: </summary>

To fit a spectrum model to real data, you need to know a little more about exojax. See [here](http://secondearths.sakura.ne.jp/exojax/tutorials/reverse_modeling.html).

 
  <img src="https://github.com/HajimeKawahara/exojax/blob/master/documents/tutorials/results.png">

🥥 HMC-NUTS modeling of a brown dwarf, [Luhman 16 A](https://en.wikipedia.org/wiki/Luhman_16) using exojax.  See [here](http://secondearths.sakura.ne.jp/exojax/tutorials/fitbd.html) for an example of the Bayes inference using the real spectrum.
 
</details>

<details><summary>Clouds :white_check_mark: </summary> Only for brave users. </details>

<details><summary>HMC-NUTS of Transmission Spectra :x: </summary>Not supported yet. </details>

## Installation

```
pip install exojax
```

or

```
python setup.py install
```

<details><summary> Note on installation w/ GPU support</summary>

:books: You need to install CUDA, NumPyro, JAX w/ NVIDIA GPU support, and cuDNN. 

- NumPyro

exojax supports NumPyro >0.5.0, which enables [the forward differentiation of HMC-NUTS](http://num.pyro.ai/en/latest/mcmc.html#numpyro.infer.hmc.NUTS). Please check the required JAX version by NumPyro. In May 2021, it seems the recent version of [NumPyro](https://github.com/pyro-ppl/numpyro) requires jaxlib>=0.1.62 (see [setup.py](https://github.com/pyro-ppl/numpyro/blob/master/setup.py) of NumPyro for instance). 

- JAX

Check you cuda version:

```
nvcc -V
```

Install such as

```
pip install --upgrade "jax[cuda111]"  -f https://storage.googleapis.com/jax-releases/jax_releases.html
```

This is the case for cuda11.1 to 11.4. Visit [here](https://github.com/google/jax) for the details.

- cuDNN

For instance, get .deb from NVIDIA and install such as

```
sudo dpkg -i libcudnn8_8.2.0.53-1+cuda11.3_amd64.deb
```

cuDNN is used for to compute the astronomical/instrumental response for the large number of wave number grid (exojax.spec.response). Otherwise, we do not use it. 

</details>

## References

- Kawahara, Kawashima, Masuda, Crossfield, Parker, van den Bekerom (2021) under review: [arXiv:2105.14782](http://arxiv.org/abs/2105.14782)

## License

🐈 Copyright 2020-2021 [Hajime Kawahara](http://secondearths.sakura.ne.jp/en/index.html) and contributors. exojax is publicly available under the MIT license. Under development since Dec. 2020.
