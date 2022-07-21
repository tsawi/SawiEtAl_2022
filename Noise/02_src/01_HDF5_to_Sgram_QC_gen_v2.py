#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:01:47 2020

@author: theresasawi


Run after "wf_to_H5.py"
Read waveform data from HDF5 file, create .mat spectrograms for SpecUFEx




INPUT:
    HDF5 with waveform data, metadata, etc

OUTPUT:
    .mat Spectrograms in folder
    Add spectrograms AND parameters to HDF5
    spectrogram images



Updates:
    
    12/09/2020 : Plot avg spectra reintroducted with vert lines for fmin, fmax

    11/17/2020 : Sgrams in H5 file now, using generator

    11/13/2020 : paths.py integrated

    10/29/2020 : loglog and DB in spectra and spectrograms
                 little fixes ~TS



@author: theresasawi
"""
# ===================================================
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

import gen_sgram_QC
import getSpecParams
sys.path.append('../')
import paths

#%%

# key = sys.argv[1]
key = 'BB_Gorner_Cont_Redo_v6' #'CC_Gorner_Cont_J5_noProc_01'#'BB_Gorner_Cont_05_b'#"BB_Gorner_Event_J5_02"
print(key)



random.seed(0)


## =============================================
## Flags for this run:

# take sample for tuning plotting sgrams
takeSample = False
Nsub = 5 #size of sample
  

plotAvg=False ## if plotting avg, don't trim. But DO TRIM for final dataset! 
trim=True# ##neater, less readable way : trim = 0**plotAvg



saveMat = True #set true to save folder of .mat files
saveFig = False
saveCat = True

## =============================================


#%% load project variables: names and paths

p = paths.returnp(key)
print(p)

projName        = p['projName']
datasetID       = p['datasetID']
projName        = p['projName']
station         = p['station']
channel         = p['channel']
path_top        = p['path_top']
path_proj       = p['path_proj']
outfile_name    = p['outfile_name']
dataFile_name   = p['dataFile_name']
pathFig         = p['pathFig']
path_WF         = p['path_WF']
path_Cat        = p['path_Cat']
subCatalog_Name = p['subCatalog_Name']
path_sgram      = p['path_sgram']



if saveFig:
    path_sgram_fig     = p['path_sgram_fig']
else:
    path_sgram_fig     = False



#%% load H5 file, create spectrogram parameters group


with h5py.File(path_proj + dataFile_name,'r+') as fileLoad:


    #% tune spectrogram parameters
    
    
    # fmin, fmax, winLen_Sec, fracOverlap, nfft = getSpecParams.getSpecParams(key)
    
    fmin = 1
    fmax = 80
    winLen_Sec =  1.1
    fracOverlap =  1/4  
    nfft =  2**12
    
    # ## sampling rate, Hz
    fs = np.ceil(fileLoad['processing_info/'].get('sampling_rate_Hz')[()])
    
    # ##number of datapoints
    lenData = fileLoad['processing_info/'].get('lenData')[()]
    
    ##spectrogram parameters, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
    nperseg = int(winLen_Sec*fs) #datapoints per window segment
    noverlap = nperseg*fracOverlap  #fraction of window overlapped
    
    #padding must be longer than n per window segment
    if nfft < nperseg:
        nfft = nperseg*64
        print("nfft too short; changing to ", nfft)
    
    
    mode='magnitude'
    scaling='spectrum'
    
    
    #% save sgram parameters in H5 file
    
    if 'spec_parameters' in fileLoad.keys():
        del fileLoad["spec_parameters"]
    
    spec_parameters_group  = fileLoad.create_group(f"spec_parameters")
    
    
    spec_parameters_group.clear()
    spec_parameters_group.create_dataset(name= 'fs', data=fs)
    spec_parameters_group.create_dataset(name= 'lenData', data=lenData)
    spec_parameters_group.create_dataset(name= 'nperseg', data=nperseg)
    spec_parameters_group.create_dataset(name= 'noverlap', data=noverlap)
    spec_parameters_group.create_dataset(name= 'nfft', data=nfft)
    spec_parameters_group.create_dataset(name= 'mode', data=mode)
    spec_parameters_group.create_dataset(name= 'scaling', data=scaling)
    # spec_parameters_group.create_dataset(name= 'sgram_medians', data=sgram_medians)
    spec_parameters_group.create_dataset(name= 'fmin', data=fmin)
    spec_parameters_group.create_dataset(name= 'fmax', data=fmax)
    

    
    #%  Load catalog IDs from project H5 file, can take random subsample
    
    
    cat_load = fileLoad['catalog']
    
    evID_list_full = [cat_load['event_ID'][i].decode('UTF-8') for i in range(len(cat_load['event_ID']))]
    
    
    if takeSample:
        random.seed(0)
        evID_list = random.sample(evID_list_full,k=Nsub)
    else:
        evID_list = evID_list_full
    
    
    evID_list.sort() #2020/11/15 sort by event_ID   TS
    
    
    print(len(evID_list))
    
    
    
    
    
    #% creat H5 file with sgrams and subcatalog
    
    
    with h5py.File(path_proj + subCatalog_Name,mode='a') as sub_catalog_h5:
        sub_catalog_h5.clear()
        
    #% save sgram parameters in H5 file
    
        if 'spec_parameters' in sub_catalog_h5.keys():
            del sub_catalog_h5["spec_parameters"]
        
        spec_parameters_group2  = sub_catalog_h5.create_group(f"spec_parameters")
        
        
        spec_parameters_group2.clear()
        spec_parameters_group2.create_dataset(name= 'fs', data=fs)
        spec_parameters_group2.create_dataset(name= 'lenData', data=lenData)
        spec_parameters_group2.create_dataset(name= 'nperseg', data=nperseg)
        spec_parameters_group2.create_dataset(name= 'noverlap', data=noverlap)
        spec_parameters_group2.create_dataset(name= 'nfft', data=nfft)
        spec_parameters_group2.create_dataset(name= 'mode', data=mode)
        spec_parameters_group2.create_dataset(name= 'scaling', data=scaling)
        # spec_parameters_group.create_dataset(name= 'sgram_medians', data=sgram_medians)
        spec_parameters_group2.create_dataset(name= 'fmin', data=fmin)
        spec_parameters_group2.create_dataset(name= 'fmax', data=fmax)
            
        sgram_group             = sub_catalog_h5.create_group("sgrams")
        sgram_normConst_group   = sub_catalog_h5.create_group("sgram_normConst")
        
        
        
        #%load and save sgram data
        
        evID_list_QCd = []
        spectra_for_avg=[]
        
        ### ### ### CREATE GENERATOR ### ### ###
        gen_sgram = gen_sgram_QC.gen_sgram_QC(key,
                                        evID_list=evID_list,
                                        h5File=fileLoad, #h5 data file
                                        station=station,
                                        channel=channel,
                                        trim=trim, #trim to min and max freq
                                        saveMat=saveMat, #set true to save folder of .mat files
                                        sgramOutfile=path_sgram, #path to save .mat files
                                        figOutfile=path_sgram_fig) #path to save sgram figures
        
        
        
    
        
        
        n=0
        while n <= len(evID_list): ## not sure a better way to execute this? But it works
        
            try:   #catch generator "stop iteration" error
        
                #sgram == STFT
                #sgram, sgramMedian, evID,fSTFT,tSTFT, n = next(gen_sgram) #next() command updates generator
                sgram, sgramMedian, evID,fSTFT,tSTFT, n, evID_BADones = next(gen_sgram) #next() command updates generator
        
        
                if not evID in sgram_group:
                    sgram_group.create_dataset(name= evID, data=sgram)
                if not evID in sgram_normConst_group:
                    sgram_normConst_group.create_dataset(name= evID, data=sgramMedian)
        
                evID_list_QCd.append(evID)
        
        
                if plotAvg:
                    spectra_for_avg.append(sgram)  ##only do before trim=True
                #
        
            except StopIteration: #handle generator error
                break
        
        print('N events in evID_list_QCd:', len(evID_list_QCd))
        print('N events in evID_BADones:', len(evID_BADones))
        #%
        
        spec_parameters_group.create_dataset(name= 'fSTFT', data=fSTFT)
        spec_parameters_group.create_dataset(name= 'tSTFT', data=tSTFT)
        spec_parameters_group2.create_dataset(name= 'fSTFT', data=fSTFT)
        spec_parameters_group2.create_dataset(name= 'tSTFT', data=tSTFT)        
        
        
        #%  put catalog of sgrams into sgram subcatalog group
        if saveCat: 
        #============make pandas DF from H5===================================#
            cat_temp_df = pd.DataFrame()
            
            for column in cat_load.keys():
                exec(f"cat_temp_df['{column}']=fileLoad['catalog/{column}'][:]")
            
            
            #% decoding note working!!  TS - 11/30/2020
            # evID_decode = [cat_temp_df.event_ID.iloc[i].decode('UTF-8') for i in range(len(cat_temp_df))]
            # evID_decode = [str(cat_temp_df.event_ID.iloc[i]).split("'")[1] for i in range(len(cat_temp_df))]
            # evID_decode = [str('a) for i in range(len(cat_temp_df))]
            #%
            # cat_temp_df['event_ID'] =cat_temp_df['event_ID'].astype('str')
            
            
            # cat_temp_df['event_ID']= [cat_temp_df.event_ID.iloc[i].decode('UTF-8') for i in range(len(cat_temp_df))]
            #
            #% weird that I have to do this ;;;  TS - 11/30/2020
            cat_temp_df['event_ID2'] = cat_temp_df['event_ID'].str.decode("utf-8")
            cat_temp_df = cat_temp_df.drop(columns='event_ID',axis=1)
            cat_temp_df['event_ID'] = cat_temp_df['event_ID2']
            cat_temp_df = cat_temp_df.drop(columns='event_ID2')
            
            #%
            
            #==================make subcatalog, mergerd on sgram IDs==========================#
            sub_catalog_df = cat_temp_df[cat_temp_df['event_ID'].isin(evID_list_QCd)]
            sub_catalog_df = sub_catalog_df.sort_values(by="event_ID")
            
            
            #=======================================================#
            # BH added this to match other structure
            subcat_grp = sub_catalog_h5.create_group('catalog')
            
            for key in sub_catalog_df.keys():  #subcatalog_sf is correctly sorted
                # BH changed: name= '{key}' to name= '{catalog/key}' to match catalog restructured
                # for reading in to Clustering codes
                #exec(f"sub_catalog_h5.create_dataset(name= '{catalog/key}', data=sub_catalog.{catalog/key})")
                if key == "event_ID":
                    subcat_grp.create_dataset(name='event_ID',data=np.array(sub_catalog_df['event_ID'],dtype='S'))
                else:
                    exec(f"subcat_grp.create_dataset(name= '{key}', data=sub_catalog_df.{key})")
            
            
    

#%%

# sub_catalog_h5.close()

# fileLoad.close()


# print("done!")


#%%
###put this into module
# date = [pd.to_datetime(sub_catalog_df.datetime.iloc[i].decode('UTF-8')) for i in range(len(sub_catalog_df))]
# # sub_catalog_df['date'] = date
# # sub_catalog_df = sub_catalog_df.set_index('date')

#%%

# =================plot avg spectra==========================

#% Plot average and std of spectra
alpha = 0.5
if plotAvg:
    fig, axes = plt.subplots()
    # axes.loglog(fSTFT,np.mean(spectra_for_avg,axis=0),lw=2,c='k')
    # axes.loglog(fSTFT,np.mean(spectra_for_avg,axis=0)+np.std(spectra_for_avg,axis=0),c='grey',alpha=alpha)
    # axes.loglog(fSTFT,np.mean(spectra_for_avg,axis=0)-np.std(spectra_for_avg,axis=0),c='grey',alpha=alpha)

    axes.loglog(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1),lw=2,c='k')
    axes.loglog(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1)+np.mean(np.std(spectra_for_avg,axis=0),axis=1),c='grey',alpha=alpha)
    axes.loglog(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1)-np.mean(np.std(spectra_for_avg,axis=0),axis=1),c='grey',alpha=alpha)

    
    axes.set_title(f'Average of spectra (+/- 1 std), N = {Nsub}')
    axes.set_xlabel(f'Frequency (Hz)')
    axes.set_ylabel(f'power/median(power) [dB]')
    
    axes.axvline(x=fmin,label='min frequency')
    axes.axvline(x=fmax,label='max frequency')
    axes.axvline(x=1/winLen_Sec,color='r',label='STFT window size')    
    
    plt.savefig(path_proj + 'avg_spectra_trim.png')
    plt.legend()
    plt.show()

print('FINISHED QUALITY CONTROL')
print('Length of evID_list_QCd = '+str(len(evID_list_QCd)))




#%%

#%%
#%%
#%% check size of existing mat
import scipy.io as scio

mat = scio.loadmat('/Users/theresasawi/Documents/SpecUFEx_v1/BB_Gorner_Cont_Final_v10_J8/01_input/J8/specMats/70614010658.mat')

s = mat.get('STFT')
t = mat.get('tSTFT')
f = mat.get('fSTFT')

#%%

print(t.size, f.size,s.size)

print(tSTFT.size, fSTFT.size,sgram.size)






#%%



#%%











