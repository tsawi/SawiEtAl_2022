# An Unsupervised Machine-Learning Approach to Understanding Seismicity at an Alpine Glacier
----------


This is a repository of the code used in Sawi et al (2022, JGR in rev). 

## Acknowledgements
----------------

1 [Holtzman, B.K., Paté, A., Paisley, J., Waldhauser, F., Repetto, D.: Machine learning reveals cyclic changes in seismic source spectra in geysers geothermal field. Science advances 4(5) (2018)](https://advances.sciencemag.org/content/4/5/eaao2929)
2 [Garcia, L., Luttrell, K., Kilb, D., & Walter, F. (2019). Joint geodetic and seismic analysis of surface crevassing near a seasonal glacier-dammed lake at Gornergletscher, Switzerland. _Annals of Glaciology,_ _60_(79), 1-13. doi:10.1017/aog.2018.32](https://www.cambridge.org/core/journals/annals-of-glaciology/article/joint-geodetic-and-seismic-analysis-of-surface-crevassing-near-a-seasonal-glacierdammed-lake-at-gornergletscher-switzerland/15E026FE40EB6CA4E3FD5A4B5602E2F2)
3 Fabian
4 Sawi


## Getting started 
-----------------

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

### Preprocessing external data

You'll need to format the lake, temperature, precipitation and GPS data from [Garcia et al., 2019](https://www.cambridge.org/core/journals/annals-of-glaciology/article/joint-geodetic-and-seismic-analysis-of-surface-crevassing-near-a-seasonal-glacierdammed-lake-at-gornergletscher-switzerland/15E026FE40EB6CA4E3FD5A4B5602E2F2) (ref. 3) , all of which happens in the "GPS_preprocessing" Jupyter notebook [here](https://github.com/tsawi/SawiEtAl_2022/blob/main/Events/01_input/Garcia_data/external/GarciaEtAl_2019/src/GPS_preprocessing.ipynb).

### Preprocessing waveform data

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

### Running SpecUFEx on MATLAB



## File structure and walkthrough


* Preprocessing and SpecUFEx analysis is done in the respective project folders
* GPS preprocessing in Garcia_data/external/Garcia_etAl/src
* Run scripts in Events/02_src/ in numerical order for preprocessing
* Edit paths.py in project folder/02_src
* Figures are created in the notebooks Events/src/

