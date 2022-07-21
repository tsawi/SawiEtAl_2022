#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 08:44:43 2021


Create catalog and folder of icequake events


~ Read catalog of all events (in proj folder)
~ make list of events with depth <100m
~ [[list of events only within footprint?]]
~ remove those w 2 peaks
~ copy those waveforms to project folder



@author: theresasawi
"""
#%%

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import sys
import os
from shutil import copyfile

sys.path.append('../')
import paths


sys.path.append('./functions')
import gorner_dt as gorner_dt


import random 
from matplotlib import pyplot as plt

import obspy.signal.filter
#import peak_detector_fcn as pkdetect
#import savitzky_golay as savitzky_golay
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import plot_trigger
from scipy.signal import find_peaks



import random
sys.path.append('./functions')
import os

import gen_catalog
plt.rcParams.update({'font.size': 16})

#%%

# maxDepth= 50 #m #V1
maxDepth= 50 #m #V2
buff = 0 #m outside of array extent


key = "BB_Gorner_Event_Redo_v2"
print(key)



plotWF = False

# chanNum = 12 # station J5 SHZ
chanNum = 21 # station J5 SHZ

takeSample = False
Nsub = 100 #size of sample
    
    


#%%

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

path_WF_fig     = p['path_WF_fig']

path_WF_reject_fig     = path_WF_fig + '01_rejects/'


# path_WF_fig = '/Users/theresasawi/Documents/SpecUFEx_v1/BB_Gorner_Event_J5/01_input/J5/figures/01_waveforms'

path_all_WF     = "/Users/theresasawi/Documents/gorner_2007_all/waveforms_all/"
# path_Cat_orig   = f"/Users/theresasawi/Documents/SpecUFEx_v1/{key}/Gorner_Catalog_orig.csv"
path_Cat_orig   = '/Users/theresasawi/Documents/gorner_2007_all/labeled_datasets/Gorner_Catalog.csv'

#%% get map boundaries
stn = pd.read_csv("/Users/theresasawi/Documents/gorner_2007_all/stnlst.csv",
                  header=None,
                  names=['name','X','Y','Elevation','dX','dY','Depth'])


buffer = [-buff,buff,-buff,buff]

bounds = [min(stn.X), max(stn.X), min(stn.Y), max(stn.Y)]

map_lim_mat = np.mat(bounds)+np.mat(buffer)
map_lim = np.array(map_lim_mat)[0]


#%% remove catalog enties below maxDepth, outside map_lim



#format original catalog, and save
cat_orig = gen_catalog.gen_catalog(key,path_Cat_orig)


print(len(cat_orig))
#%% get fraction of hour (for analyzing time of day)
hourFrac = []

for xx in range(len(cat_orig)):
            hourFrac.append(float(cat_orig.datetime.iloc[xx].hour) + float(cat_orig.datetime.iloc[xx].minute/60))


cat_orig['hourFrac']=hourFrac

# find fraction of year (for ben!)





#%% map bounds



cat_orig = cat_orig.where(cat_orig.X_m >= map_lim[0])
cat_orig = cat_orig.where(cat_orig.X_m <= map_lim[1])
cat_orig = cat_orig.where(cat_orig.Y_m >= map_lim[2])
cat_orig = cat_orig.where(cat_orig.Y_m <= map_lim[3])

cat_bounded = cat_orig.dropna()

print(f'{len(cat_bounded)} events in map bounds')




#%% date bounds (after June 10, which is when basals start)

# cat_orig = cat_orig.where(cat_orig.datenum >= 70610000000)
cat_orig = cat_orig.where(cat_orig.datenum >= 70614000000).dropna()#2022/07/15

cat_bounded = cat_orig.dropna()

print(f'{len(cat_bounded)} events in date bounds')

#%%

cat_final = cat_bounded.where(cat_bounded.Depth_m <= maxDepth).dropna()




print(f'{len(cat_final)} events above {maxDepth}m depth')
plt.hist(cat_final.Depth_m,bins=100,label=f'N={len(cat_final)} icequakes \n max depth = {maxDepth}m ',color='k')
plt.legend()
# plt.savefig(path_proj + 'depthHist_maxDepth{maxDepth}.png')

print(len(cat_final))








#%% take random sample 

if takeSample:
    random.seed(0)
    evID_list = random.sample(list(cat_final.event_ID),k=Nsub)
else:
    evID_list = list(cat_final.event_ID)

#%%

dp = 0 #count double peaks
le = 0 # count loading errors


evID_keep = []

for evv in evID_list:
    
    
    fileName = path_all_WF  + '0' + str(evv)[0:-2] + '.gse2' 
    
    try:
        st = obspy.read(fileName)
        tr = st[chanNum]
        data = tr.data
        
        lenData = len(data)
        
    
        thrup = 7.5 #upper threshold sta/lta
        stalta = classic_sta_lta(data, 50, 400) #sta/lta; 
        
        peaks, _ = find_peaks(stalta, height=thrup, distance = 250)
        
        
    
    
        if len(peaks)<=1:# and np.max(noiseData) >= 5*np.mean(np.abs(noiseData)):
            
            evID_keep.append(evv)
            
            if plotWF:
                fig = plt.figure()#figsize=(10,10))
                
                
                fig.add_subplot(211)
                plt.plot(data)
                plt.ylabel('velocity')    
                plt.xticks([])
                
                    
                ax = fig.add_subplot(212)    
                plt.plot(stalta)
                plt.plot(peaks,stalta[peaks],'o')
                ax.hlines(thrup,color='r',linestyle='--',linewidth=1,xmin=0,xmax=lenData)
                plt.xlabel('Samples')
                plt.ylabel('STA/LTA')
                
                plt.savefig(path_WF_fig + str(evv)[0:-2] + '.png')
            
            
        else:
            dp += 1
            print('double peak ', dp)
            
                
        
            if plotWF:
                fig = plt.figure()#figsize=(10,10))
                
                
                fig.add_subplot(211)
                plt.plot(data)
            
                    
                ax = fig.add_subplot(212)    
                plt.plot(stalta)
                plt.plot(peaks,stalta[peaks],'o')
                ax.hlines(thrup,color='r',linestyle='--',linewidth=1,xmin=0,xmax=lenData)
                
                plt.savefig(path_WF_reject_fig + str(evv)[0:-2] + '_reject.png')
          
    except:
        le += 1
        print('loading error : ValueError: second must be in 0..59')
        pass

            
        #%%

print(len(evID_keep), ' events kept')
print(le+dp+len(evID_keep), ' = ' , len(evID_list), '?')
print(le+dp+len(evID_keep) == len(evID_list))

#%%
evID_keep_str = evID_keep

evID_keep_df = pd.DataFrame({'event_ID':evID_keep})


#%%

cat_final2 = cat_final.merge(evID_keep_df)

print('cat_final2', len(cat_final2))
print('evID_keep', len(evID_keep))


cat_final2['date_index'] = cat_final2.datetime


cat_final2 = cat_final2.set_index('date_index')
#%% save catalog

cat_final2.to_csv(path_Cat)


#%% plot map by datetime

fig = plt.figure(figsize=(10,10))

fig.add_subplot(111,aspect='equal')
# Define your mappable for colorbar creation
sm = plt.cm.ScalarMappable(cmap='viridis', 
                           norm=plt.Normalize(vmin=cat_final2.index.min().value,
                                              vmax=cat_final2.index.max().value))
sm._A = []  


im = plt.scatter(cat_final2.X_m, cat_final2.Y_m, label=f'N={len(cat_final2)}',s=1,c=cat_final2.datetime)

plt.scatter(stn.X, stn.Y, label='stations',marker='^',color='orange')
cbar = plt.colorbar(sm,label='Date, 2007',shrink=.8);
cbar.ax.set_yticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%b %d'))

plt.xticks(size=12)
plt.yticks(size=12)
plt.xlabel('easting (m)')
plt.ylabel('northing (m)')
plt.savefig(path_proj + f'simple_event_map_datetime.png')

#%% plot map by hourfrac


fig = plt.figure(figsize=(10,10))

fig.add_subplot(111,aspect='equal')

sm = plt.cm.ScalarMappable(cmap='viridis', 
                           norm=plt.Normalize(vmin=cat_final2.hourFrac.min(),
                                              vmax=cat_final2.hourFrac.max()))
sm._A = []  



im = plt.scatter(cat_final2.X_m, cat_final2.Y_m, label=f'N={len(cat_final)}',s=1,c=cat_final2.hourFrac)

plt.scatter(stn.X, stn.Y, label='stations',marker='^',color='orange')
cbar = plt.colorbar(sm,label='Hour of day',shrink=.8);

plt.xticks(size=12)
plt.yticks(size=12)
plt.xlabel('easting (m)')
plt.ylabel('northing (m)')

plt.tight_layout()
plt.savefig(path_proj + 'simple_event_map_hourFrac.png')


#%%



plt.hist(cat_final2.hourFrac,bins=24*3,label=f'N={len(cat_final2)}',color='k',density=False)
plt.legend()

plt.xlabel('UTC hour of day')
plt.ylabel('Number of events')

plt.savefig(path_proj + 'hourlyHist_allEvents.png')



#%% plot map by depth

fig = plt.figure(figsize=(10,10))

fig.add_subplot(111,aspect='equal')
# Define your mappable for colorbar creation
sm = plt.cm.ScalarMappable(cmap='viridis', 
                           norm=plt.Normalize(vmin=cat_final2.Depth_m.min(),
                                              vmax=cat_final2.Depth_m.max()))
sm._A = []  

# df.plot(legend=False, colormap='viridis', figsize=(12,10));






im = plt.scatter(cat_final2.X_m, cat_final2.Y_m, label=f'N={len(cat_final2)}',s=1,c=cat_final2.Depth_m)

plt.scatter(stn.X, stn.Y, label='stations',marker='^',color='orange')
# plt.legend(loc='upper right', bbox_to_anchor=(1.8,1))
# plt.title('Gorner Glacier, Summer 2007')
cbar = plt.colorbar(sm,label='Depth (m)',shrink=0.8);
# Change the numeric ticks into ones that match the x-axis
# cbar.ax.set_yticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%h'))

plt.xticks(size=12)
plt.yticks(size=12)
plt.xlabel('easting (m)')
plt.ylabel('northing (m)')
plt.tight_layout()

plt.savefig(path_proj + f'simple_event_map_depth_max{maxDepth}m.png')

# plt.close()
#%% plot map by elevation


fig = plt.figure(figsize=(10,10))

fig.add_subplot(111,aspect='equal')
# Define your mappable for colorbar creation
sm = plt.cm.ScalarMappable(cmap='viridis', 
                           norm=plt.Normalize(vmin=cat_final2.Elevation_m.min(),
                                              vmax=cat_final2.Elevation_m.max()))
sm._A = []  

# df.plot(legend=False, colormap='viridis', figsize=(12,10));






im = plt.scatter(cat_final2.X_m, cat_final2.Y_m, label=f'N={len(cat_final2)}',s=1,c=cat_final2.Elevation_m)

plt.scatter(stn.X, stn.Y, label='stations',marker='^',color='orange')
# plt.legend(loc='upper right', bbox_to_anchor=(1.8,1))
# plt.title('Gorner Glacier, Summer 2007')
cbar = plt.colorbar(sm,label='Elevation (m)',shrink=0.8);
# Change the numeric ticks into ones that match the x-axis
# cbar.ax.set_yticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%h'))

plt.xticks(size=12)
plt.yticks(size=12)
plt.xlabel('easting (m)')
plt.ylabel('northing (m)')
plt.tight_layout()

plt.savefig(path_proj + f'simple_event_map_Elevation_m.png')










#%% copy waveforms to file




for evv in evID_keep:
    
    pathIn = path_all_WF  + '0' + str(evv)[0:-2] + '.gse2' 
    pathOut = path_WF  + '0' + str(evv)[0:-2] + '.gse2' 

    copyfile(pathIn, pathOut)










#%%











#%%









