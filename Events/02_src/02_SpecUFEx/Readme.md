# SpecUFEx 

SpecUFEx stands for "Unsupervised Spectral Feature Extraction", an unsupervised machine learning algorithm to characterize time variations in spectral content of waveform data. We apply the method to earthquake seismograms. SpecUFEx combines probabilistic non-negative matrix factorization (NMF) and hidden Markov modeling (HMM) of spectrograms (short time Fourier transforms of waveform data) to generate "fingerprints", low dimensional representations of spectral variation through time. Both the NMF and HMM models are fit using stochastic variational inference; the method is therefore scalable to tens or hundreds of thousands of spectrograms. The resulting fingerprints can be used as features for either unsupervised (e.g. clustering) or supervised (e.g. classification) machine learning. The method is described in

Holtzman, B.K., Paté, A., Paisley, J., Waldhauser, F., Repetto, D.: Machine learning reveals cyclic changes in seismic source spectra in geysers geothermal field. Science advances 4(5) (2018)

Please cite this article if you use the package for research purposes.

Matlab code originally written by John Paisley at Columbia University. 