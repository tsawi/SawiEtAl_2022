#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:48:20 2020

@author: theresasawi
"""
import numpy as np
import os

import scipy as sp
import scipy.io as spio
import scipy.signal

from matplotlib import pyplot as plt


evID_BADones = []

def gen_sgram_QC(key,evID_list,h5File,station,channel,trim=True,saveMat=False,sgramOutfile='.',figOutfile=0):

    # ===========================
    # The  QC loop:
    # ===========================


    fs          = h5File['spec_parameters/'].get('fs')[()]
    nperseg     = h5File['spec_parameters/'].get('nperseg')[()]
    noverlap    = h5File['spec_parameters/'].get('noverlap')[()]
    nfft        = h5File['spec_parameters/'].get('nfft')[()]
    
###### when do we NOT decode these values?! ######
    # scaling     = h5File['spec_parameters/'].get('scaling')[()]
    # mode        = h5File['spec_parameters/'].get('mode')[()]

    scaling     = h5File['spec_parameters/'].get('scaling')[()].decode('utf-8') #decoding needed all of a sudden? TS 12/7/2020
    mode        = h5File['spec_parameters/'].get('mode')[()].decode('utf-8')        


    fmin        = h5File['spec_parameters/'].get('fmin')[()]
    fmax        = h5File['spec_parameters/'].get('fmax')[()]


    winLen      = round(nperseg/fs,3)
    fracOL      = round(noverlap/nperseg,3)

    waveforms = h5File[f'waveforms/{station}/{channel}']

    n=0

    for i in range(len(evID_list)):

        n +=1

        if i%200==0:
            print(str(i)+' of '+str(len(evID_list)))

        evID = evID_list[i]
        
        if 'Event' in key:
            evID = evID_list[i][0:-2]
                                
        data = waveforms.get(evID)[:]


        fSTFT, tSTFT, STFT_0 = sp.signal.spectrogram(x=data,
                                                    fs=fs,
                                                    nperseg=nperseg,
                                                    noverlap=noverlap,
                                                    #nfft=Length of the FFT used, if a zero padded FFT is desired
                                                    nfft=nfft,
                                                    scaling=scaling,
                                                    axis=-1,
                                                    mode=mode)



        #trim before taking median ~Ts 11/17/2020

        if trim:
            freq_slice = np.where((fSTFT >= fmin) & (fSTFT <= fmax))
            #  keep only frequencies within range
            fSTFT   = fSTFT[freq_slice]
            STFT_0 = STFT_0[freq_slice,:][0]


        # =====  [BH added this, 10-31-2020]:
        # Quality control:
        anyNaNs = np.isnan(STFT_0).any()
        median_STFT0 = np.median(STFT_0)





        if anyNaNs==1 or median_STFT0==0 :
            if anyNaNs==1:
                print('OHHHH we got a NAN here!')
                #evID_list.remove(evID_list[i])
                evID_BADones.append(evID)
                pass
            if median_STFT0==0.:
                print('OHHHH we got a ZERO median here!!')
                #evID_list.remove(evID_list[i])
                evID_BADones.append(evID)
                pass

        if anyNaNs==0 and median_STFT0>0 :

            # try:
                
            if 'noProc' in key:
                STFT = STFT_0 ## no processing! TS 2020/02/16
                
            else:
                STFT_norm = STFT_0 / median_STFT0
                STFT = np.maximum(0, 20*np.log10(STFT_norm, where=STFT_norm != 0))
                # STFT = STFT + np.abs(STFT.min())
                

            # check for NaNs again
            anyNaNs2 = np.isnan(STFT).any()
            if anyNaNs2==1:
                print('OHHHH we got a NAN in the dB part!')
                evID_BADones.append(evID)


            # evID_list_QCd.append(evID)



            # =====================plot figure========================
            if figOutfile:

                if not os.path.isdir(figOutfile):
                    os.mkdir(figOutfile)

                plt.figure()

                plt.pcolormesh(tSTFT, fSTFT, STFT)
                cbar = plt.colorbar()
                plt.xlabel(f'Time (s)')
                plt.ylabel(f'Frequency (Hz)')
                
                
                if 'noProc' in key:
                    cbar.set_label('STFT [magnitude] ', rotation=270,labelpad=13)
                    plt.title(f"No processing \n fmin={fmin}Hz,fmax={fmax}Hz, fracO{fracOL}\n \
                    {winLen} s windows; padding={nfft}samples")
                    plt.savefig(f"{figOutfile}noProcessing_{evID}.png")
                else:
                    cbar.set_label('STFT/median(STFT) [dB] ', rotation=270,labelpad=13)
                    
                    plt.title(f"Normalized, in DB \n fmin={fmin}Hz,fmax={fmax}Hz, fracO{fracOL}\n \
                    {winLen} s windows; padding={nfft}samples")
                    plt.savefig(f"{figOutfile}normDB_{evID}.png")
                #cbar.set_label('abs(STFT)', rotation=270,labelpad=13)


                plt.close() # BH added 12/14/2020



            # =================save .mat file==========================
            if saveMat==True:
                if not os.path.isdir(sgramOutfile):
                    os.mkdir(sgramOutfile)


                spio.savemat(sgramOutfile + evID + '.mat',
                          {'STFT':STFT,
                            'fs':fs,
                            'nfft':nfft,
                            'nperseg':nperseg,
                            'noverlap':noverlap,
                            'fSTFT':fSTFT,
                            'tSTFT':tSTFT})
                #%%
            yield STFT, median_STFT0, evID,fSTFT,tSTFT,n, evID_BADones


            # except Exception as e:
            #        print(e)
