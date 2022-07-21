#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 21:01:15 2020


@author: theresasawi
"""

#%%

import h5py
import numpy as np
import glob
import sys
import obspy
import random
sys.path.append('./functions')
import os
import pandas as pd
import gen_wf_from_folder
import gen_catalog

sys.path.append('../')
import paths
import tables
tables.file._open_files.close_all()

#%% load project variables: names and paths
# key = sys.argv[1]
# key = "GeysersNW_TS_mac1"
# key = 'BB_Gorner_Cont_05_b'#"BB_Gorner_Event_J5_02"


key = 'BB_Gorner_Event_Redo_v2'
saveFig = False


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
path_WF_fig     = p['path_WF_fig']
path_WF         = p['path_WF']
path_Cat        = p['path_Cat']

#%%

if os.path.exists(path_proj + dataFile_name):
  os.remove(path_proj + dataFile_name)


#%%

takeSample  = 0
Nsub        = 5

#%% read list of waveform files and sort by filename
## VERY IMPORTANT your filenames start with the date, and so are sorted chronologically


wf_list_full    = glob.glob(path_WF + '*')
wf_list_full.sort() # sort file list chronologically
print(wf_list_full[0:Nsub])



#%%  create random subsample of files

if takeSample:
    random.seed(0)

    #now no replacement ~TS 10/29/2020
    wf_list = random.sample(wf_list_full,k=Nsub)
    wf_list.sort()

    print(len(wf_list), " waveforms sampled \n \n")


else:
    wf_list = wf_list_full


#%% read and format catalog

if "Event" in key:
    cat = pd.read_csv(path_Cat)
else:
    cat = gen_catalog.gen_catalog(key,path_Cat)

#%% get processing info from waveform metadata

### WILL NEED TO CHANGE BY PROJECT


for path in wf_list:
    st = obspy.read(path)
    # BH added detrend 10-31-2020:
    st.detrend()

    sampling_rate = st[0].stats.sampling_rate
    # instr_response =
    station_info = f"{st[0].stats.network}.{st[0].stats.station}.{st[0].stats.location}.{st[0].stats.channel}."
    calib = st[0].stats.calib
    lenData = len(st[0].data)
    _format = st[0].stats._format




#%% make H5 file
# Files are a kind of "group"; they serve as the root group
with h5py.File(path_proj + dataFile_name,'a') as h5file:
    
    waveforms_group  = h5file.create_group("waveforms")
    station_group = h5file.create_group(f"waveforms/{station}")
    channel_group = h5file.create_group(f"waveforms/{station}/{channel}")


    wf_path_group  = h5file.create_group("waveform_filepaths")

    #% load and save wf data
    
    
    ### ### ### CREATE GENERATOR ### ### ###
    gen_wf = gen_wf_from_folder.gen_wf_from_folder(folderPaths=wf_list,
                                                   lenData=lenData,
                                                   key=key,
                                                   path_WF_fig=path_WF_fig,
                                                   saveFig=saveFig) 
    
    
    #catch error: duplicate entries
    dupl_evID = 0
    dupl_evID_list = []
    
    evID_keep = [] #for trimming catalog
    wf_path_keep = []
    
    n=0
    while n <= len(wf_list): ## not sure a better way to execute this? But it works
    
        try:   #catch generator "stop iteration" error
    
    
            #these all defined in generator at top of script
            wf, evID, n, pathIn = next(gen_wf) #next() command updates generator
            
            # if "Gorner" in key: ##whyyyyy what up w this bug!
            #     evID = pathIn.split('/')[-1].split('.')[-2][1:]
    
    
    
            # if evID not in group, add dataset to wf group
            if evID not in channel_group:
                channel_group.create_dataset(name= evID, data=wf)
                evID_keep.append(evID)
                wf_path_group.create_dataset(name= evID, data=pathIn)
            elif evID in channel_group:
                dupl_evID += 1
                dupl_evID_list.append(evID)
    
    
        except StopIteration: #handle generator error
            break
    



#%%


#%% create catalog of only wavefiles in folder (original catalog has more events)



cat_wf = cat[cat['event_ID'].isin(evID_keep)]


cat_wf.sort_values(by="event_ID") #2020/11/15 sort by event_ID   TS

print(len(cat), " events in catalog")
print(len(wf_list), " waveforms in filelist")
print(len(evID_keep), " waveforms successfully loaded")
print(len(cat_wf), " waveforms in working catalog")

print(len(dupl_evID_list), " duplicate evIDs found: \n", dupl_evID_list)
print(len(cat_wf), " waveforms matched with catalog entries -- this is our final number of data!")

    
    #%% fill H5 file
with h5py.File(path_proj + dataFile_name,'a') as h5file:

    # del h5file['catalog']
    # del h5file['processing_info']
    catalog_group    = h5file.create_group("catalog")
    processing_group = h5file.create_group("processing_info")

##clear group for testing
    
    for col in cat_wf.columns:
        if col == 'datetime':
            catalog_group.create_dataset(name='datetime',data=np.array(cat_wf['datetime'],dtype='S'))
        elif col == 'event_ID':
            catalog_group.create_dataset(name='event_ID',data=np.array(cat_wf['event_ID'],dtype='S'))
        elif col == 'date_index':
            catalog_group.create_dataset(name='date_index',data=np.array(cat_wf['date_index'],dtype='S'))
        else:
            exec(f"catalog_group.create_dataset(name='{col}',data=cat_wf.{col})")
    
    

    processing_group.clear()
    
    processing_group.create_dataset(name= "sampling_rate_Hz", data=sampling_rate)#,dtype='S')
    processing_group.create_dataset(name= "station_info", data=station_info)
    processing_group.create_dataset(name= "calibration", data=calib)#,dtype='S')
    processing_group.create_dataset(name= "orig_formata", data=_format)#,dtype='S')
    # processing_group.create_dataset(name= "instr_response", data=instr_response)#,dtype='S')
    processing_group.create_dataset(name= "lenData", data=lenData)#,dtype='S')
    






#%%

print("done-zo!")
# not sure if this is necessary-- ?  it is! ~TS
h5file.close()



#%%
