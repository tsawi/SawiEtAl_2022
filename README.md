# An Unsupervised Machine-Learning Approach to Understanding Seismicity at an Alpine Glacier

By Theresa Sawi, Ben Holtzman, Meredith Nettles, Fabian Walter and John Paisley



This is a repository of the code used in Sawi et al (2022, JGR in rev). 

## Acknowledgements


1. SpecUFEx (machine learning) code is introduced here: **[Holtzman, B.K., Paté, A., Paisley, J., Waldhauser, F., Repetto, D.: Machine learning reveals cyclic changes in seismic source spectra in geysers geothermal field. Science advances 4(5) (2018)](https://advances.sciencemag.org/content/4/5/eaao2929)**

2. Lake, precipitation, temperature, and GPS data come from this paper: Garcia, L., Luttrell, K., Kilb, D., & Walter, F. (2019). **Joint geodetic and seismic analysis of surface crevassing near a seasonal glacier-dammed lake at Gornergletscher, Switzerland. _Annals of Glaciology,_ _60_(79), 1-13. [doi:10.1017/aog.2018.32](https://www.cambridge.org/core/journals/annals-of-glaciology/article/joint-geodetic-and-seismic-analysis-of-surface-crevassing-near-a-seasonal-glacierdammed-lake-at-gornergletscher-switzerland/15E026FE40EB6CA4E3FD5A4B5602E2F2)**

3. Seismic data and original paper on their analysis are here: **Walter, F. (2009). Seismic activity on Gornergletscher during Gornersee outburst floods. _Dissertation_, _31_(1–2), 14–27. https://doi.org/10.1007/BF03322148**

4. This code supports the paper by Sawi et al., (2022, _JGR, in review_)


## Getting started 


Seismic data can be accessed through the Swiss Seismological Service [website]( http://eida.ethz.ch/). However, for ease of use we have also compiled the waveforms used in this study in Zenodo repositories. Icequake waveforms can be found [here]( https://zenodo.org/record/7007378#.Y3Io94LMKbg),  and noise records [here](https://zenodo.org/record/6913695#.Y3Io-oLMKbg).

After downloading waveforms from the links above, copy waveforms into respective folders for events and noise. Icequake ("event") waveforms go in:
```
SawiEtAl_2022/Events/01_input/J8/
```
Likewise, noise records go here:

```
SawiEtAl_2022/Noise/01_input/J8/
```
### MATLAB Dependency
This project was performed on MATLAB version 2018b, though will likely work on other similar releases. SpecUFEx is now available free and open source from  https://github.com/Specufex/specufex.



### Installation

 Clone the github repository 
```
git clone https://github.com/tsawi/SawiEtAl_2022.git
```

## Preprocessing external data

You'll need to format the lake, temperature, precipitation and GPS data from [Garcia et al., 2019](https://www.cambridge.org/core/journals/annals-of-glaciology/article/joint-geodetic-and-seismic-analysis-of-surface-crevassing-near-a-seasonal-glacierdammed-lake-at-gornergletscher-switzerland/15E026FE40EB6CA4E3FD5A4B5602E2F2) (ref. 3) , all of which happens in the "GPS_preprocessing" Jupyter notebook [here](https://github.com/tsawi/SawiEtAl_2022/blob/main/Events/01_input/Garcia_data/external/GarciaEtAl_2019/src/GPS_preprocessing.ipynb).

## Preprocessing waveform data

Change the "path_top" to your local computer at:
```
SawiEtAl_2022/Events/02_src/paths.py
```
and:
```
SawiEtAl_2022/Events/02_src/paths.py
```
Preprocessing and SpecUFEx analysis is done in the respective project folders. Simply run the scripts in found at numerical order 
1. ~~00_getGornerIcequakes.py~~ (we already downloaded this data) 
2.  00b_waveforms_to_HDF5.py (this converts waveforms to [HDF5](https://www.hdfgroup.org/solutions/hdf5/) format used in this study)
3. 01_HDF5_to_Sgram_QC_gen_v2.py (This generates spectrograms and saves them both to an HDF5 file, and writes them out to MATLAB .m files. )

## Running SpecUFEx via MATLAB
MATLAB scripts are found in this folder (or the comparable folder for "Noise"):
```
SawiEtAl_2022/Events/02_src/02_SpecUFEx/
```

Simply run the scripts in numerical order.


## Clustering and visualizing SpecUFEx results 

Jupyter notebooks doing the clustering analysis and post-clustering visualizations can be found here:
```
SawiEtAl_2022/Events/02_src/
```
Simply run the Jupyter notebooks in numerical order

1. plotFigures1-4.ipynb
2. plotFigures5_6_11_12.ipynb
3. plotFigures7-10.ipynb



