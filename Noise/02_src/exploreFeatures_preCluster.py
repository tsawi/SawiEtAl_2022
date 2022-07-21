#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 02:17:24 2022

Explore features of noise catalog

@author: theresasawi
"""


import h5py


import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
# this will close any existing hdf5 _open_files
# if we use while statements, we won't have to do this
import tables
tables.file._open_files.close_all()
sys.path.append('./functions')


import paths


sys.path.append('.')
sys.path.append('/Users/theresasawi/Documents/SpecUFEx_v1/BB_Gorner_Event_Redo_v2/02_src/functions')

from functions2 import getFeatures_Explore_preCluster

#%%


event_dir = '/Users/theresasawi/Documents/SpecUFEx_v1/BB_Gorner_Event_Redo_v2/'


# key = sys.argv[1]
key_orig = 'BB_Gorner_Cont_Redo' #'CC_Gorner_Cont_J5_noProc_01'#'BB_Gorner_Cont_05_b'#"BB_Gorner_Event_J5_02"

key = 'BB_Gorner_Cont_Redo_v2' #'CC_Gorner_Cont_J5_noProc_01'#'BB_Gorner_Cont_05_b'#"BB_Gorner_Event_J5_02"
print(key)



## =============================================


#%% load project variables: names and paths

pN = paths.returnp(key)
print(pN)

# pathClusCat = path_proj + f"principalDf_full_{mode}_Kopt{Kopt}.csv"


projNameN        = pN['projName']
datasetIDN       = pN['datasetID']
projNameN        = pN['projName']
station         = pN['station']
channel         = pN['channel']


path_top        = pN['path_top']
path_projN       = pN['path_proj']
outfile_nameN    = pN['outfile_name']
dataFile_nameN   = pN['dataFile_name']
path_WFN         = pN['path_WF']
path_CatN        = pN['path_Cat'] #original, raw catalog
subCatalog_NameN = f"{dataFile_nameN}_Sgrams_Subcatalog.hdf5"


pathACMN         = f'{path_top}{projNameN}/03_output/{station}/SpecUFEx_output/step2_NMF/'
pathSTMN         = f'{path_top}{projNameN}/03_output/{station}/SpecUFEx_output/step4_stateTransMats/'
pathEBN          = f'{path_top}{projNameN}/02_src/02_SpecUFEx/EB.mat'
pathElnBN          = f'{path_top}{projNameN}/02_src/02_SpecUFEx/ElnB.mat'
pathWN        = path_projN + '02_src/02_SpecUFEx/out.DictGain.mat' 



# pathClusCatN = path_projN + f"principalDf_full_{mode}_Kopt{KoptN}.csv"
dataH5_pathN = path_projN + dataFile_nameN

pathFig = '../05_reports/figures/'
pathFigSupp = '../05_reports/supp_figures/'
pathAuxData = '../01_input/data/processed/Garcia/'
#%% get params


with h5py.File(path_projN + dataFile_nameN,'r') as dataFile:

    lenDataN = dataFile['processing_info/'].get('lenData')[()]
    fsN = dataFile['spec_parameters/'].get('fs')[()]
    
    # fminN = 
    npersegN = dataFile['spec_parameters/'].get('nperseg')[()]
    noverlapN = dataFile['spec_parameters/'].get('noverlap')[()]
    nfftN = dataFile['spec_parameters/'].get('nfft')[()]


    fmaxN = dataFile['spec_parameters/'].get('fmax')[()]
    fmaxN = np.ceil(fmaxN)
    fminN = dataFile['spec_parameters/'].get('fmin')[()]
    fminN = np.floor(fminN)    
    fSTFTN = dataFile['spec_parameters/'].get('fSTFT')[()]
    tSTFTN = dataFile['spec_parameters/'].get('tSTFT')[()]
    
    sgram_modeN = dataFile['spec_parameters/'].get('mode')[()].decode('utf-8')
    scalingN = dataFile['spec_parameters/'].get('scaling')[()].decode('utf-8')
    
    
fsN = int(np.ceil(fsN))
winLen_SecN = float(npersegN / fsN)




#%% load catalog

Kopt = 3
KoptN = 4

## # # we prefer to read the catalogs originally created  .... 
cat00N = pd.read_csv(event_dir + f'/01_input/data/interim/{key_orig}_noise_k{KoptN}.csv')


cat00N['event_ID'] = [int(evv) for evv in cat00N.event_ID]

#why two the same?? not sure : / 



#%% get features


df = getFeatures_Explore_preCluster(cat00N,dataH5_pathN,station,channel,fminN,fmaxN,fsN,nfftN)





#%% plot results



plt.plot(df.SC,ls='none',marker='.')
plt.figure()
plt.plot(df.log10P2P,ls='--',marker='.')

#%%




