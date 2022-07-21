#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def getSpecParams(key):

    """
    set for each project
    """
    print( ' key : ', key)
    
    if key == "BB_Gorner_Event_Redo":
        fmin            = 15
        fmax            = 80
        winLen_Sec      = .08#seconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding
        
    if key == "BB_Gorner_Event_Redo_v2":
        fmin            = 15
        fmax            = 80
        winLen_Sec      = .08#seconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding
                
        
    if key == "AA_Gorner_00":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .05#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding
        
         
    elif key == "BB_Gorner_Cont_Final":  ## TS 2/19/2021
        fmin            = 10
        fmax            = 400
        winLen_Sec      = .09#seconds
        fracOverlap     = 1/2
        nfft            = 2**11 #padding  
        
        
        
    elif key == "BB_Gorner_Event_Final":  ## TS 2/19/2021
        fmin            = 10
        fmax            = 400
        winLen_Sec      = .09#seconds
        fracOverlap     = 1/2
        nfft            = 2**11 #padding  
        
        
        
        
        
    elif key == "CC_Gorner_Cont_J5_noProc_01":  ## TS 2/16/2021
        fmin            = 8
        fmax            = 450
        winLen_Sec      = .13#seconds
        fracOverlap     = 1/2
        nfft            = 2**11 #padding  
        
    elif key == "BB_Gorner_Cont_05_b":  ## TS 2/15/2021
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .09#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding   

        
    elif key == "BB_Gorner_Event_J5":  ## TS2/7/2021
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .09#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding   
        
    elif key == "BB_Gorner_Event_J5_02":  ## TS2/7/2021
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .03#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding           
        
        
    elif key == "ErtaAle_07":  ## 2/5/2021
        fmin            = .5
        fmax            = 15
        winLen_Sec      = 3#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding               
        
    elif key == "ErtaAle_06":  ## 2/5/2021
        fmin            = .5
        fmax            = 15
        winLen_Sec      = 3#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding           
        

    elif key == "Erta_Ale_05":
        fmin            = .1
        fmax            = 15
        winLen_Sec      = .5#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding  

        
    elif key == "BB_Gorner_Cont_01":
        fmin            = 8
        fmax            = 100
        winLen_Sec      = 0.15#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding  
        
    elif key == "BB_Gorner_Cont_02":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.15#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding          

    elif key == "BB_Gorner_Cont_03":
        fmin            = 8
        fmax            = 200
        winLen_Sec      = 0.15#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding      
        
        
    elif key == "BB_Gorner_Cont_04": ##closest to orig settings
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.09#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding            

    elif key == "ErtaAle_00":  ## 12/09/2020
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.1#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding        
        
        
       

    # elif key == "AA_Gorner_Cont_00":  ## 12/09/2020
    #     fmin            = 8
    #     fmax            = 300
    #     winLen_Sec      = 0.09#seconds
    #     fracOverlap     = 1/2
    #     nfft            = 2**10 #padding

    elif key == "AA_Gorner_Cont_00":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.05#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding
        
    elif key == "AA_Gorner_Cont_J458":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.1#seconds
        fracOverlap     = 1/2
        nfft            = 2**10 #padding        

    elif key == "AA_Gorner_Cont_01":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.01#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding

    elif key == "AA_Gorner_Cont_02":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.05#seconds
        fracOverlap     = 1/4
        nfft            = 2**13 #padding

    elif key == "AA_Gorner_Cont_03":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.1#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding

    elif key == "AA_Gorner_Cont_04":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.03#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding

    elif key == "AA_Gorner_Cont_05":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.03#seconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding

    elif key == "AA_Gorner_Cont_06":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = 0.01#seconds
        fracOverlap     = 1/2
        nfft            = 2**12 #padding


    elif key == "AA_Gorner_01":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .01#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding
    elif key == "AA_Gorner_02":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .05#sefmin, fmax, winLen_Sec, fracOverlap, nfftconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding
    elif key == "AA_Gorner_03":
        fmin            = 8
        fmax            = 300
        winLen_Sec      = .01#seconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding
    elif key == "GeysersNW_TS_mac2":
        fmin            = .5
        fmax            = 100
        winLen_Sec      = .5#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding
    elif key == "GeysersNW_TS_mac3_medRes":
        fmin            = .5
        fmax            = 75
        winLen_Sec      = .2#seconds
        fracOverlap     = 1/4
        nfft            = 2**10 #padding

    elif key == "GeysersNW_BH_ub_dbox":
        fmin            = 1
        fmax            = 150
        winLen_Sec      = 0.05 #.1#seconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding
    elif key == 'MIT_NER_BHdisk' or 'MIT_NER_TSdisk':
        expt = 'Water'
        #expt = 'Dry'
        if expt=='Water':
            #fmin            = 2e5
            fmax            = 1.01e6 #800000
            winLen_Sec      = 0.0006553/100 #0.15 #.1#seconds
            fmin            = 1/(2*winLen_Sec)
            fracOverlap     = 1/4
            nfft            = 2**14 #padding

    else: #defaut
        print("\n ### ### NO KEY SPECIFIED, USING DEFAULT SGRAM PARAMETERS ### ### ")
        fmin            = .5
        fmax            = 100
        winLen_Sec      = .1#seconds
        fracOverlap     = 1/4
        nfft            = 2**12 #padding

    return fmin, fmax, winLen_Sec, fracOverlap, nfft
