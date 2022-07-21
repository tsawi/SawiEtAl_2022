#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import obspy

import numpy

def rescale(data,minn,maxx):
    return( -1 +  ( ( data - data.min() ) * (maxx-minn)  )  / (data.max() - data.min()))



def gen_wf_from_folder(folderPaths,lenData,key,saveFig=False,path_WF_fig='.'):
    
    """
    data : waveform data
    wfID : unique ID on waveform file
    timestamp : time from waveform ID (arrival time vs event time?)        
    """
    

    Nkept=0 # count number of files kept
    Nerr = 0 # count file loading error
    NwrongLen = 0
    
    

    for i, pathIn in enumerate(folderPaths):

        try: #catch loading errors

            stream = obspy.read(pathIn)
            stream.detrend('demean')


            if "Gorner" in key:
                # print(True)
                data_detrend = stream[0].data


                data_scale = rescale(data_detrend,-1,1)

                data = data_scale - data_scale.mean()
                
                evID = pathIn.split('/')[-1].split('.')[0][1:]

                
                # evID = pathIn  ## was used for non-Cont gorner data? TS 12/14/20
                # timestamp = gorner_dt(evID)


            else:

                print("Key not found! Update this file::  ./functions/gen_wf_from_folder.py")
                # data = stream.data
                break


            if len(data)==lenData: #checking for errant filelengths


                yield data, evID, Nkept, pathIn
                
                if i%100==0:
                    print(f"{i}/{len(folderPaths)}")
                
                if saveFig:
                    stream[0].plot(outfile=path_WF_fig + 'waveform_' + evID + '.png')



                Nkept += 1
            else:
                NwrongLen += 1
                print(NwrongLen, ' data wrong length')




        except ValueError: #some of the data are corrupt; unloadable
            Nerr +=1
            print(Nerr, ". File ", pathIn, " unloadable")

            pass
