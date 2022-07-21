#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 18:50:05 2021

CONVERT CATALOG AND FINGERPRINT .MAT FILES TO H% FILES FOR SOMMMMEEE REASON :) :) 


1) copy waveforms to H5 by evID and print figs
2) copy sgrams to H5 by evID and print figs
3) convert events to datetime -- add to catalog by evID
4) copy Fprints to H5 by evID
5) copy ACM to H5 by evID 


@author: theresasawi
"""


#%%

import h5py
import numpy as np
import glob
import sys
# import obspy
# import random
sys.path.append('./functions')
import gorner_dt
import os
import datetime
# import gen_wf_from_folder
# import gen_catalog
from scipy.io import loadmat

sys.path.append('../')
import paths
import tables
tables.file._open_files.close_all()

#%%


key = "BB_Gorner_Cont_Redo_v6"
# key = "BB_Gorner_Cont_Final_v10_J8"
# key = "ErtaAle_08"
# key = "BB_Gorner_Event_J5_02"

print(key)

p = paths.returnp(key)
print(p)

projName        = p['projName']
datasetID       = p['datasetID']
projName        = p['projName']
station         = p['station']
channel         = p['channel']
path_top        = p['path_top']
path_proj       = p['path_proj']

dataFile_name   = p['dataFile_name']

outfile_name    = p['outfile_name']
path_Cat        = p['path_Cat']


path_WF         = p['path_WF']
path_WF_fig     = p['path_WF_fig']
path_sgram      = p['path_sgram']
path_sgram_fig  = p['path_sgram_fig']

pathFP          = p['pathFP']
pathACM         = p['pathACM']
pathSTM         = p['pathSTM']


#%%


if os.path.exists(path_proj + outfile_name):
  os.remove(path_proj + outfile_name)


#%% make H5 file
# Files are a kind of "group"; they serve as the root group
with h5py.File(path_proj + outfile_name,'a') as h5file:
    
    
    
    processing_group = h5file.create_group("processing_info")
    processing_group.create_dataset(name= "lenData", data=5001)
    processing_group.create_dataset(name= "sampling_rate", data=1000)


###   ###   ###   ###   ###   ###   ###   ###   
###   ###   ###   ###   ###   ###   ###   ###        
### add sgrams, ACM, STM, Fprints
    out_group               = h5file.create_group("SpecUFEX_output")

    sgram_group             = h5file.create_group("sgrams")
    sgram_parameters_group  = h5file.create_group("spec_parameters") 
    ACM_group               = h5file.create_group("SpecUFEX_output/ACM")
    Xpwr_group              = h5file.create_group("SpecUFEX_output/ACM_Xpwr") 
    gain_group              = h5file.create_group("SpecUFEX_output/ACM_gain") 
    STM_group               = h5file.create_group("SpecUFEX_output/STM")
    fprint_group            = h5file.create_group("SpecUFEX_output/fprints")
    
    
    evID_list = []
    datetime_list = []
    
    file_list = glob.glob(path_sgram + '*.mat')
    file_list.sort() # sort file list chronologically
    
    for i, s in enumerate(file_list):
        
        if i%500==0:
            print(f"{i}/{len(glob.glob(path_sgram + '*.mat'))}")
            
            
        evID = s.split('/')[-1].split('.')[0]
        
        if 'ErtaAle' in key:
            datt = str(evID)[0:14]
 
            
            timestamp = datetime.datetime(
                 int( datt[0:4]),
                 int( datt[4:6]),
                 int( datt[6:8]),
                 int( datt[8:10]),
                 int( datt[10:12]),
                 int( datt[12:14]
                     ))
            
            
        elif "Gorner"  in key: #TS 2021/02/07 for J5 events
            datt = str(evID)
            timestamp = datetime.datetime(
                             int('200' + datt[0]),
                             int( datt[1:3]),
                             int( datt[3:5]),
                             int( datt[5:7]),
                             int( datt[7:9]),
                             int( datt[9:11])
                              )
            
            
        else:
            datt = str(evID)[1:]
            
            timestamp = datetime.datetime(
                             int('200' + datt[0]),
                             int( datt[1:3]),
                             int( datt[3:5]),
                             int( datt[5:7]),
                             int( datt[7:9]),
                             int( datt[9:11]))
                         
        evID_list.append(evID)
        datetime_list.append(timestamp)
        
        if '05' in key:
            mat = loadmat(f"{path_sgram}{evID}.sac.mat")
        else:
            mat = loadmat(f"{path_sgram}{evID}.mat")
        
        sgram = mat.get('STFT')[0]
        sgram_group.create_dataset(name=evID,data=sgram)

        
        if i == 0: ## save sgram parameters
        
            if '05' not in key:        
                tSTFT = mat.get('tSTFT')[0]        
                fSTFT = mat.get('fSTFT')[0]
                nfft = mat.get('nfft')[0][0]
                nperseg = mat.get('nperseg')[0][0]
                fs = np.ceil(mat.get('fs'))[0][0]
                
            
                sgram_parameters_group.create_dataset(name='tSTFT',data=tSTFT)
                sgram_parameters_group.create_dataset(name='fSTFT',data=fSTFT)
                sgram_parameters_group.create_dataset(name='nfft',data=nfft)
                sgram_parameters_group.create_dataset(name='nperseg',data=nperseg)
                sgram_parameters_group.create_dataset(name='fs',data=fs)   
                
    
            else:
                tSTFT = mat.get('tSTFT')[0]        
                fSTFT = mat.get('fSTFT')[0]
                nfft = mat.get('Nfft')[0][0]
                nperseg = mat.get('WinLen')[0][0]
                fs = np.ceil(mat.get('sr'))[0][0]                
            
                sgram_parameters_group.create_dataset(name='tSTFT',data=tSTFT)
                sgram_parameters_group.create_dataset(name='fSTFT',data=fSTFT)
                sgram_parameters_group.create_dataset(name='nfft',data=nfft)
                sgram_parameters_group.create_dataset(name='nperseg',data=nperseg)
                sgram_parameters_group.create_dataset(name='fs',data=fs)   
            
            
            
        
        ##### ACMs
        mat = loadmat(f'{pathACM}out.{evID}.mat')
        H = mat.get('H') 
        Xpwr = mat.get('Xpwr')                
        gain = mat.get('gain')                
               
        ACM_group.create_dataset(name=evID,data=H) #ACM
        Xpwr_group.create_dataset(name=evID,data=Xpwr) #diff for each data

        if i == 0:         
            gain_group.create_dataset(name='gain',data=gain) #same for all data
        
        ##### STMs
        mat = loadmat(f"{pathSTM}out.{evID}.mat")
        gam = mat.get('gam')                
        STM_group.create_dataset(name=evID,data=gam)


        ##### Fprints
        if '05' in key:
            mat = loadmat(f"{pathFP}out.{evID}.sac.mat")
        else:
            mat = loadmat(f"{pathFP}out.{evID}.mat")

        fprint = mat.get('A2')                
        fprint_group.create_dataset(name=evID,data=fprint)        
        
        
###   ###   ###   ###   ###   ###   ###   ###   
###   ###   ###   ###   ###   ###   ###   ###        
### add datetimes
    catalog_group    = h5file.create_group("catalog")        
    catalog_group.create_dataset(name='event_ID',data=np.array(evID_list,dtype='S'))
    catalog_group.create_dataset(name='datetime',data=np.array(datetime_list,dtype='S'))        




    


#%%


#%%


