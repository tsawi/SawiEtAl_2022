#!/usr/bin/env python3
# -*- coding: utf-8 -*-




import pandas as pd
import numpy as np
import datetime
import gorner_dt


def gen_catalog(key,path_Cat):
    """
    Format catalog if needed
    """


#####       #####       #####       #####       #####       #####       #####       
    if "Geysers" in key or "Parkfield" in key:
        
        cat = pd.read_csv(path_Cat, header=None,delim_whitespace=True)
        
        
        cat.columns = ['year','month','day','hour','minute','second','lat','long','depth','mag','event_ID_orig']
        
        #for index
        cat['date'] = pd.to_datetime(cat[['year','month','day','hour','minute','second']])
        
        #for plotting
        cat['datetime'] = pd.to_datetime(cat[['year','month','day','hour','minute','second']])
        
        
        # create wf ID to match on waveform filename
        cat['event_ID'] = [ str(cat['year'].iloc[i]) + '.' + \
                        str(cat['datetime'].iloc[i].dayofyear).zfill(3) + '.' + \
                        str(cat['hour'].iloc[i]).zfill(2) + \
                        str(cat['minute'].iloc[i]).zfill(2) + \
                        str(cat['second'].iloc[i]).split('.')[0].zfill(2) + '.' +\
                        str(cat['event_ID_orig'].iloc[i])    \
                        for i in range(len(cat))]
        
        
        cat = cat.set_index('date')
        
        cat.sort_values(by="event_ID") #sort cat by event IDs ~TS 2020/11/15
                
        cat_format = cat
#####       #####       #####       #####       #####       #####       #####       
    if "Gorner" in key:
        
        cat = pd.read_csv(path_Cat)
        cat['year'] = 2007
        
        cat = cat.drop(['Unnamed: 0'],axis=1)
        
        if "Cont" in key:
            cat['event_ID'] = [str(evv) for evv in cat.ID]
            
            cat = cat.drop(['Label'],axis=1)
            cat = cat.drop(['Precluster'],axis=1)
            
            
            
        else:        
            cat['event_ID'] = cat.datenum   
            

            
        date = [gorner_dt.gorner_dt(evID,key) for evID in cat.event_ID] #convert timestamp to datetime
 
        cat['date'] = date      #for indexing
        cat['datetime'] = date  # for plotting
        
        cat = cat.set_index('date')
        
        cat.sort_values(by="event_ID") #sort cat by event IDs ~TS 2020/11/15
                
        cat_format = cat        
        
        
        
        
        
        
        
#####       #####       #####       #####       #####       #####       #####       
        
    return cat_format