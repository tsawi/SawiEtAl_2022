"""
Created on Sat Feb 29 leap day!



updates:
    
    2020/03/03 : fixed precip time interpolation (goes for whole year!)

@author: theresa
"""

from scipy.io import loadmat

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
#%%


pathIn = '/Users/theresa/Documents/SpecUFEx/GARCIA_BundledData2007/Bundled_data_2007.mat'
pathOut = '/Users/theresa/Documents/SpecUFEx/GARCIA_BundledData2007/'


mat = loadmat(pathIn)


keys_list = mat.keys()

for keys in mat.keys():
    
    exec(f"var_{keys} = mat.get('{keys}')")





#%% lake level

lakedata = [[row.flat[0] for row in line] for line in mat['LakeLevel'][0][0]]



#%%
#
lake = list(lakedata[0])
lakediff = np.hstack((0,np.diff(lakedata[0])))
doy = list(lakedata[4])


lakedf = pd.DataFrame({"level_m":lake,
                       "lakediff_m":lakediff,
                       "doy":doy})
    
lakedf.to_csv( pathOut + "lake_data.csv")    

plt.figure(figsize=(40,4))    
plt.plot(doy,lake)

plt.figure(figsize=(40,4))
plt.plot(doy,lakediff)
plt.ylim(-.05,.05)

#%%temp
plt.figure(figsize=(40,4))    
  
tempdata = [[row.flat[0] for row in line] for line in mat['Meteor'][0][2]]
plt.plot(tempdata[2])
plt.plot(tempdata[3])
year = list(tempdata[0])
temp = list(tempdata[2])
precip = list(tempdata[3])
doy = tempdata[1] #interped from 0 to number of days
#time_interp = np.interp(time,np.arange(min(time),max(time)),np.arange(min(time),max(time)))
###extrapolate between doys:
#xlim([155,200]),grid

#plt.plot(time_interp,temp)
#plt.plot(time_interp,precip)


meteor_df = pd.DataFrame({"temp":temp,
                          "precip":precip,
                          "doy":doy})
    
meteor_df.to_csv( pathOut + "meteor_data_v2.csv")  

#
#lakedf = pd.DataFrame({"level_m":lake,
#                       "lakediff_m":lakediff,
#                       "doy":doy})
#    
#lakedf.to_csv( pathOut + "lake_data.csv")  
    
#%%strain
plt.figure(figsize=(40,4))    
  
straindata = [[row.flat[0] for row in line] for line in mat['Strain_East'][0][0]]

strain_east = []
for s in straindata:
    
    strain_east.append(s[0])


#%%



plt.plot(strain_east)
plt.ylim(0,200000)




#%%






#%%

    



#%%

    



#%%

    



#%%

    



#%%

    



#%%

    



#%%

    