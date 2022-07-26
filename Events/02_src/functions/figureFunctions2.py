#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 19:20:53 2021

@author: theresasawi
"""





import h5py
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

import datetime as dtt

import datetime
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.metrics import classification_report

from obspy.signal.cross_correlation import correlate, xcorr_max


# sys.path.insert(0, '../01_DataPrep')
from scipy.io import loadmat

import seaborn as sns




from functions2 import getWF,makeHourlyDF, getSpectraMedian,resortByNMF
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo





##################################################################################################
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo
##################################################################################################


def plotWF(evID,dataH5_path,station,channel,fmin,fmax,fs,tSTFT,colorBy='cluster',k='',ax=None,**plt_kwargs):
    '''
    '''

    colors      =     plt_kwargs['colors']

    if ax is None:
        ax = plt.gca()


    wf_zeromean = getWF(evID,dataH5_path,station,channel,fmin,fmax,fs)


    if colorBy=='cluster':

        colorWF = colors[k-1]
    else:
        colorWF = 'k'

    ax.plot(wf_zeromean,color=colorWF,lw=1)

    plt.ylabel('Velocity')



# #### General
    ticks=[np.floor(c) for c in np.linspace(0,len(wf_zeromean),3)]
    ticklabels=[f'{c:.0f}' for c in np.linspace(0,np.ceil(max(tSTFT)),3)]
    plt.xticks(ticks=ticks,labels=ticklabels)

    plt.xlabel('t (s)')
    plt.xlim(0,len(wf_zeromean))
    return wf_zeromean




# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotSgram(specMat,evID,tSTFT, fSTFT,ax=None):
    #set x to datetime list or seconds in tSTFT
    # x=tSTFT
    if ax is None:
        ax = plt.gca()

    plt.pcolormesh(tSTFT, fSTFT, specMat,cmap=cm.magma, shading='auto')

    cbar = plt.colorbar(pad=.06)
    cbar.set_label('dB',labelpad=8)#,fontsize = 14)
#     plt.clim(0,45)
    date_title = str(pd.to_datetime('200' + evID))
    ax.set_title(date_title,pad=10)






    plt.ylabel('f (Hz)',labelpad=10)
    plt.xlabel('t (s)')

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotReconstructedStates(RMM,sel_state_single,fSTFT,lw=1,freq_list=None,colorBy='cluster',legend='inside',bb1=1,bb2=0,ax=None,normed='None',scale=1, **plt_kwargs):

    if ax is None:
        ax = plt.gca()

    colors      =     plt_kwargs['colors']


    for i, st in enumerate(sel_state_single):


        if colorBy=='all':
            cc = 'k'
        else:
            cc = colors[i]


        reconst_state = RMM[:,st]

        if normed=='max':
            reconst_state = reconst_state / np.max(reconst_state)

        if normed=='None':
            reconst_state = reconst_state ## because it's based on spectra that were normed by their medians .....


        reconst_state = reconst_state / scale

        ax.plot(fSTFT,reconst_state,
                lw=lw,
                ls='--',
                color=cc,
               label=f"S{sel_state_single[i]}")    #     /RMM[:,st].max()



    if legend=='inside':
        ax.legend()
    if legend=='outside':
        ax.legend(loc='right',bbox_to_anchor=(bb1,bb2))

    ax.set_xlabel('$f$ (Hz)',labelpad=4)
    ax.set_ylabel('Reconstructed dB')
    plt.grid('on')

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotMedianSpectra(path_proj,cat00,Kopt,fSTFT,station,leg,lw=1,normed='median',scale=1,ax=None,**plt_kwargs):

    if ax is None:
        ax = plt.gca()

    colors      =     plt_kwargs['colors']


    for k in range(1,Kopt+1):

        if normed=='median':
            specMatsum_med=getSpectraMedian(path_proj,cat00,k,station,normed=True)

            specMatsum_med = specMatsum_med / scale

            ylabell = 'dB/median(dB)'
        elif normed=='max':
            specMatsum_med=getSpectraMedian(path_proj,cat00,k,station,normed=False)
            specMatsum_med = specMatsum_med / np.max(specMatsum_med)
            ylabell = 'Normalized dB'
        else:
            specMatsum_med=getSpectraMedian(path_proj,cat00,k,station,normed=False)


        ax.plot(fSTFT,specMatsum_med,
                 lw=lw,
                 color=colors[k-1],
                 alpha=1,
                 label=leg[k-1]);

    ax.grid('on')
    ax.set_xlabel('$f$ (Hz)',labelpad=4)
    ax.set_ylabel(ylabell)


def plotFeaturesRolling(df,winSize,Kopt,width2,height2,dotSize=4,title='',xlabelfont=14,**plt_kwargs):
    import warnings

    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']
    numDays     =     plt_kwargs['numDays']


    fig, axes = plt.subplots(figsize=(width2,height2),nrows=3)
    ax1, ax2, ax3 = axes



    mss = 5
    lss = '-'


    for k in range(1,Kopt+1):


        plotFeaturesTimeline(df,Kopt,'SC',size=dotSize,ax=ax1,**plt_kwargs)
    #     df.SC.rolling(window=winSize,min_periods=1).mean().plot(ax=ax1,linestyle='None',lw=1,marker='o',ms=1,color='black',alpha=.8)

        ##depreciation warning for loffset of resampling
        warnings.filterwarnings("ignore")#, category=DeprecationWarning)

        df.SC.resample(winSize,closed='left',label='left', loffset='12H').mean().plot(ax=ax1,linestyle=lss,lw=1,marker='o',ms=mss,color='black',alpha=.8)
        ax1.set_title('Spectral centroid ($Hz$)',loc='left')
        ax1.set_ylabel('')


        plotFeaturesTimeline(df,Kopt,'log10RSAM',size=dotSize,ax=ax2,**plt_kwargs)
    #     df.log10RSAM.rolling(window=winSize,min_periods=1).mean().plot(ax=ax2,linestyle='None',lw=1,marker='o',ms=1,color='black',alpha=.8)
        df.log10RSAM.resample(winSize,closed='left',label='left', loffset='12H').mean().plot(ax=ax2,linestyle=lss,lw=1,marker='o',ms=mss,color='black',alpha=.8)

        ax2.set_title('log10RSAM ($m/s^2$)',loc='left')
        ax2.set_ylabel('')


        plotFeaturesTimeline(df,Kopt,'log10P2P',size=dotSize,ax=ax3,**plt_kwargs)
    #     df.log10P2P.rolling(window=winSize,min_periods=1).mean().plot(ax=ax3,linestyle='None',lw=1,marker='o',ms=1,color='black',alpha=.8)
        df.log10P2P.resample(winSize,closed='left',label='left', loffset='12H').mean().plot(ax=ax3,linestyle=lss,lw=1,marker='o',ms=mss,color='black',alpha=.8)

        ax3.set_title('log10P2P ($m/s^2$)',loc='left')
        ax3.set_ylabel('')


    for ax in axes:
        for tick in ax.get_xticklabels():
            tick.set_rotation(0)

        ax.set_xlim(tstart,tend)
        ax.set_xticks(day_ticks)
        ax.set_xticklabels(day_labels)
    #     plt.tight_layout()
    #     plt.ylim(-1e7,4e7)
        # plt.ylim(-1e7,train_set['log10abs_sum'].max())
        ax.yaxis.grid()


    ax1.set_xticklabels('')
    ax2.set_xticklabels('')

    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax3.set_xlabel('Date, 2007',fontsize=xlabelfont)

    plt.suptitle(title,fontsize=20)
    plt.subplots_adjust(wspace=0,hspace=.8)


# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotFeaturesTimeline(df,Kopt,feature,size=3,ax=None,**plt_kwargs):

    if ax is None:
        ax = plt.gca()

    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']
    hourMaxTemp =     plt_kwargs['hourMaxTemp']
    colors      =     plt_kwargs['colors']
    numDays     =     plt_kwargs['numDays']
    supraDraint =     plt_kwargs['supraDraint']
    subDraint      =     plt_kwargs['subDraint']
    drainEndt     =     plt_kwargs['drainEndt']

    for clus in range(1,Kopt+1):

        # print(i)
        cluscolor = colors[clus-1]
        dff = df[df.Cluster==clus]
        ax.plot(dff[feature],
              linestyle='none',
              marker='o',
              markeredgecolor=cluscolor,
              markerfacecolor='none',
              alpha=.4,
              ms=size)

    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    ax.set_xlim(tstart,tend)
    ax.set_xticks(day_ticks)
    ax.set_xticklabels(day_labels)
#     plt.tight_layout()
    # plt.ylim(-1e7,train_set['log10abs_sum'].max())
    ax.set_ylabel(feature)



    ax.yaxis.grid()

    lw2=2
    alphaT=.6
    lc='k'

    # axes.axvline(calvet,c='green',linestyle='--',linewidth=3, alpha=alphaT)
    ax.axvline(supraDraint,c=lc,linestyle='--',linewidth=lw2, alpha=alphaT)
    ax.axvline(subDraint,c=lc,linestyle='--',linewidth=lw2, alpha=alphaT)
    ax.axvline(drainEndt,c=lc,linestyle='--',linewidth=lw2, alpha=alphaT)
    ax.yaxis.grid()
    for i in range(numDays):
        ax.axvline(hourMaxTemp[i],c='gray',linestyle='--',linewidth=1,alpha=0.3)
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotFeatureBoxPlot(df,Kopt,feature,ax=None,**plt_kwargs):


    colors      =     plt_kwargs['colors']


    if ax is None:
        ax = plt.gca()


    my_pal = dict()

    for k in range(1,Kopt+1):
        my_pal.update({k: colors[k-1]})

    sns.boxplot(x='Cluster', y=f'{feature}', data=df, palette=my_pal,ax=ax)
    # ax.grid('off')
#     plt.tight_layout()

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotSpines(cat=None,k=None,axs=None,barWidth=10,alphaBar=.6,**plt_kwargs):

    if axs is None:
        axs = plt.gca()
    colors      =     plt_kwargs['colors']

    if cat is None:
        axs.spines['bottom'].set_color('limegreen')
        axs.spines['top'].set_color('limegreen')
        axs.spines['left'].set_color('limegreen')
        axs.spines['right'].set_color('limegreen')

    else:
        axs.spines['bottom'].set_color(colors[k-1])
        axs.spines['top'].set_color(colors[k-1])
        axs.spines['left'].set_color(colors[k-1])
        axs.spines['right'].set_color(colors[k-1])


    axs.spines['bottom'].set_linewidth(barWidth)
    axs.spines['top'].set_linewidth(barWidth)
    axs.spines['left'].set_linewidth(barWidth)
    axs.spines['right'].set_linewidth(barWidth)


    axs.spines['bottom'].set_alpha(alphaBar)
    axs.spines['top'].set_alpha(alphaBar)
    axs.spines['left'].set_alpha(alphaBar)
    axs.spines['right'].set_alpha(alphaBar)



## resampple not tested
# def plotFeatures(df,ax=None,**plt_kwargs):
#
#     if ax is None:
#         ax = plt.gca()
#
#     tstart      =     plt_kwargs['tstart']
#     tend        =     plt_kwargs['tend']
#     day_ticks   =     plt_kwargs['day_ticks']
#     day_labels  =     plt_kwargs['day_labels']
#     # hourMaxTemp =     plt_kwargs['hourMaxTemp']
#
#
#
#     ms = 9
#
#     RSAM_3HN = df.resample('3H').RSAM_norm.mean()
#     SC_3HN = df.resample('3H').SC_norm.mean()
#     P2P_3HN = df.resample('3H').P2P_norm.mean() + .2 #(for offsetting)
#     # VAR_3HN = df.resample('3H').VAR_norm.mean()
#
#     RSAM_3HN.plot(linestyle='-',marker='.',ms=ms,color='k',label='RSAM')
#     P2P_3HN.plot(linestyle='-',marker='.',ms=ms,color='r',label='Peak-to-peak amplitude')
#     SC_3HN.plot(linestyle='-',marker='.',ms=ms,color='b',label='Spectral centroid')
#
#     ax.set_xticks(day_ticks)
#     ax.set_xticklabels(day_labels,rotation=0)
#     ax.set_xlim(tstart,tend)
#     ax.set_xlabel('Date, 2007',labelpad=30)
#     ax.legend()
#     # ax.set_xticks([])
#     # ax.set_xticklabels('')
#     ax.set_ylabel('Normalized features\n (offset for clarity)',labelpad=10)




def plotMap(cat_map,colorBy='all',k=1,ax=None,size=10,alpha=.7, map_lim=None,buff=15,marker='o',edgecolor='cluster',lw=1,**plt_kwargs):
    """
    Plot lake boundaries from csv file

    Parameters
    ----------
    cat_map : pd.DataFrame
        Must have column names:  event_ID, X_m,Y_m,
    colorBy : str, optional
        Color markers by cluster assignment, or make all black.
        The default is 'all'.
        cluster : plots all data colored by cluster assignment
        oneCluster: data from one cluster, set k=cluster number
        all : plots all data, colored black
    k : int, optional
        Cluster number. The default is 1.
    ax : plt.ax(), optional
        current axis. The default is None.
    size : int, optional
        Size of marker. The default is 10.
    alpha : int, optional
        transperency of maarker. The default is .7.
    map_lim : np.array, optional
        limits of map boundaries. The default is None.
    buff : int, float, optional
        Budder around extrend of map lim. The default is 15.
    marker : matplotlib marker type, optional
        marker style. The default is 'o'.
    edgecolor : color str or RGB np.array
        marker edge color. The default is 'cluster', else is black.
    lw : int, flaot, optional
        line width. The default is 1.
    **plt_kwargs : dict
        see notebook for usage.

    Returns
    -------
    plt.axis()

    """

    colors      =     plt_kwargs['colors']

    if ax is None:
        ax = plt.gca()


    if plotLake:
        ### plot lake shore boundary
        lakexcsv = pd.read_csv('/Users/theresasawi/Documents/11_Manuscripts/SawiEtAl_2021/data/external/GarciaEtAl_2019/processed/lakeshore_x.csv',names=['x'])
        lakeycsv = pd.read_csv('/Users/theresasawi/Documents/11_Manuscripts/SawiEtAl_2021/data/external/GarciaEtAl_2019/processed/lakeshore_y.csv',names=['y'])

        ##adjusted manually
        lakexcsv['x'] = lakexcsv['x'] + 220980
        lakeycsv['y'] = lakeycsv['y'] + -5000410

        ax.plot(lakexcsv.x,lakeycsv.y,color='steelblue')
        ax.fill(lakexcsv['x'], lakeycsv['y'],color='steelblue',alpha=.2)
        ### END plot lake shore boundary




    ##some possible map settings
    try:
        x = cat_map.X_m
        y = cat_map.Y_m
    except:
        try:
            x = cat_map.lat
            y = cat_map.lon
        except:
            try:
                x = cat_map.lat
                y = cat_map.long
            except:
                pass



    if colorBy=='all':
        ax.scatter(x, y,
                     color='k',
                     s=size,
                     alpha=alpha,
                     marker=marker)


    if colorBy==None:
        print('no data plotted')

    if colorBy=='cluster':
        cat_rand = cat_map.sample(frac=1) #shuffle rows in catalog
        for i,k in enumerate(cat_rand.Cluster):
            x = cat_rand.X_m.iloc[i]
            y = cat_rand.Y_m.iloc[i]

            if edgecolor=='cluster':
                label = f'C{k}'
                ax.scatter(x, y,
                             color='none',
                             edgecolors=colors[k-1],
                             linewidths=lw,
                             s=size,
                             alpha=alpha,
                             label = label,
                             marker=marker);

            else: # borkder is black, facecolor is by cluster

                ax.scatter(x, y,
                             color=colors[k-1],
                             edgecolors='k',
                             linewidths=lw,
                             s=size,
                             alpha=alpha,
                             marker=marker);

    if colorBy=='oneCluster':
        clus_cat = cat_map[cat_map.Cluster==k]

        for i,k in enumerate(clus_cat.Cluster):
#         for k in range(1,Kopt+1):
#             k = int(k)
            x = clus_cat.X_m.iloc[i]
            y = clus_cat.Y_m.iloc[i]
            ax.scatter(x, y,
                         color=colors[k-1],
                         # edgecolors='k',
                           # linewidths=1,
                         s=size,
                         alpha=alpha,
                         marker='.');
    if colorBy=='datetime':

        sm = plt.cm.ScalarMappable(cmap='magma',
                                   norm=plt.Normalize(vmin=cat_map.index.min().value,
                                                      vmax=cat_map.index.max().value))

        x = cat_map.X_m
        y = cat_map.Y_m
        sc = ax.scatter(x,y,
                        s=size,
                        color=cat_map.datetime,
                        alpha=alpha,
                        marker='.');


#         cbar = plt.colorbar(sm,label='Date, 2007',orientation='horizontal',shrink=.8);
#         cbar.ax.set_xticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%b %d'))

#     if map_lim is None:
#         ax.set_xlim(cat_map.X_m.min()-buff,cat_map.X_m.max()+buff)
#         ax.set_ylim(cat_map.Y_m.min()-buff,cat_map.Y_m.max()+buff)
#     else:
#         ax.set_xlim(map_lim[0][0],map_lim[0][1])
#         ax.set_ylim(map_lim[1][0],map_lim[1][1])

    # ax.set_xticks([])







def plotMapGMT(cat_feat,stat_df,buff,colorBy='depth_km',maxColor=10):


    cat_star = cat_feat[colorBy]

    region = [
        cat_feat.long.min() - buff,
        cat_feat.long.max() + buff,
        cat_feat.lat.min() - buff,
        cat_feat.lat.max() + buff,
    ]

    print(region)


    fig = pygmt.Figure()
    fig.basemap(region=region, projection="M15c", frame=True)
    fig.coast(land="black", water="skyblue")

    if maxColor is not None:
        pygmt.makecpt(cmap="viridis", series=[cat_star.min(), maxColor])
    else:
        pygmt.makecpt(cmap="viridis", series=[cat_star.min(), cat_star.max()])

    fig.plot(
        x=cat_feat.long,
        y=cat_feat.lat,
        size=0.05 * 2 ** cat_feat.magnitude,
        color=cat_star,
        cmap=True,
        style="cc",
        pen="black",
    )

    if 'depth' in colorBy:
        fig.colorbar(frame='af+l"Depth (km)"')

    else:
        fig.colorbar(frame=f'af+l"{colorBy}"')

    fig.plot(x=stat_df.long, y=stat_df.lat,style="t.5c", color="pink", pen="black")




    fig.show()

    return fig




# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo
def plotStations(stn,station,size=80,ax=None):
    """
    plot gorner glacier stations 2007 array
    """
    if ax is None:
        ax = plt.gca()



    for i, stat in enumerate(stn.name):

        if station in stat:
            ### circle station
            # ax.scatter(stn.X.iloc[i],
            #             stn.Y.iloc[i],
            #              color='none',
            #              s=200,
            #              edgecolors='palegreen',
            #            linewidth=3,
            #            alpha=1,
            #              marker='o')


            ### fill station
            ax.scatter(stn.X.iloc[i],
                        stn.Y.iloc[i],
                          color='palegreen',
                          s=size,
                          edgecolors='palegreen',
                        linewidth=1,
                        alpha=1,
                          marker='^')

        ax.scatter(stn.X.iloc[i],
                stn.Y.iloc[i],
                 color='none',#,'palegreen',
                 s=size,
                 marker='^',
                  linewidth=1,
                 edgecolors='k',
                 alpha = .8)





def plotDepth(cat_map,stn,ax=None,byCluster=False,k=None,map_lim=None,buff=15,maxDepth=50,size=5,alpha=.7,stasize=80,**plt_kwargs):

    if ax is None:
        ax = plt.gca()

    colors      =     plt_kwargs['colors']

    if byCluster==True:
        clus_cat = cat_map[cat_map.Cluster==k]
        for i, k in enumerate(clus_cat.Cluster):

            ax.scatter(clus_cat.X_m.iloc[i],
                       clus_cat.Depth_m.iloc[i],
                        color=colors[k-1],
                        # edgecolors='k',
                        # linewidths=2,
                       s=size,
                       alpha=alpha);
    else:
        ax.scatter(cat_map.X_m,
                   cat_map.Depth_m,
                    color='k',
                   s=size,
                   alpha=alpha);

    ax.invert_yaxis()


    i=-1 #for J8

    # ax.scatter(stn.X.iloc[i],
    #             0,
    #              color='palegreen',
    #              s=200,
    #             alpha=1,
    #             marker='^',
    #             edgecolors='k',
    #            linewidth=1)


    ax.scatter(stn.X,np.zeros(len(stn.X)),c='None',marker='^',s=stasize,edgecolors='k',linewidth=1)

    ax.scatter(stn.X.iloc[i],0,c='palegreen',marker='^',s=stasize,edgecolors='k',linewidth=1)

    # # ax.set_xticks([])
    # ax.set_aspect('equal')
    ax.set_ylabel('Depth (m)',labelpad=4)
    ax.set_xlabel('Easting (m)',labelpad=4)
    if map_lim==None:
        ax.set_xlim(cat_map.X_m.min()-buff,cat_map.X_m.max()+buff)
    else:
        ax.set_xlim(map_lim[0][0],map_lim[0][1])
        ax.set_ylim(maxDepth,0)

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo
def plotDepthHist(cat_map,colorBy='all',k='',binWidth=10,ax=None,**plt_kwargs):
    colors      =     plt_kwargs['colors']

    if ax is None:
        ax = plt.gca()

    if colorBy == 'all':
        depth_bins = np.arange(0,cat_map.Depth_m.max(),binWidth)
        hist, bin_edges = np.histogram(cat_map.Depth_m, bins=depth_bins,density=True)
        ax.bar(bin_edges[:-1],hist,width=binWidth,color='k')
    if colorBy == 'cluster':
        cat_clus = cat_map[cat_map.Cluster==k]
        depth_bins = np.arange(0,cat_clus.Depth_m.max(),binWidth)
        hist, bin_edges = np.histogram(cat_clus.Depth_m, bins=depth_bins,density=True)
        ax.bar(bin_edges[:-1],hist,width=binWidth,color=colors[k-1],label=f'N={len(cat_clus)}')
        ax.legend(loc='upper right')

    ax.set_ylabel('Frequency')
    ax.set_xlabel('Depth (m)')

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotElev(cat_map,Kopt,stn,ax=None,colorBy='all', size=5,alpha=.7,**plt_kwargs):

    colors      =     plt_kwargs['colors']

    if ax is None:
        ax = plt.gca()

    elevStat = stn.Elevation.iloc[7]

    dElev = elevStat - 1.2*np.median(cat_map.Elevation_m)

    if colorBy=='all':
        ax.scatter(cat_map.X_m,cat_map.Elevation_m,color='k',s=size,alpha=alpha);


    elif colorBy=='cluster':
        for k in range(1,Kopt+1):
            clus_cat = cat_map[cat_map.Cluster==k]

            ax.scatter(clus_cat.X_m,clus_cat.Elevation_m,color=colors[k-1],s=size,alpha=alpha);


    elif colorBy=='datetime':

        sm = plt.cm.ScalarMappable(cmap='magma',
                                   norm=plt.Normalize(vmin=cat_map.index.min().value,
                                                      vmax=cat_map.index.max().value))

        x = cat_map.X_m
        y = cat_map.Elevation_m + dElev
        sc = ax.scatter(x,y,
                        s=size,
                        c=cat_map.datetime,
                        alpha=alpha,
                        marker='.');


        cbar = plt.colorbar(sm,label='Date, 2007',orientation='horizontal',shrink=.8,pad=.3);
        cbar.ax.set_xticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%b %d'))
#         plt.plot(lakexcsv.x,lakeycsv.y)

#     ax.text(628400,-1000,'VE=?')#,color='k',s=3,alpha=.7);
#     ax.set_aspect('equal')
    ax.scatter(stn.X,stn.Elevation,color='b',marker='^',s=50)
#     ax.set_xticks([])
    ax.set_ylabel('Elevation (m)',labelpad=30)
    ax.set_xlim(cat_map.X_m.min(),cat_map.X_m.max())
    ax.set_xlabel('Easting (m)',labelpad=30)
    # ax.set_ylim(cat_map.Y_m.min(),cat_map.Y_m.max())
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotHourBarStack(cat00,Kopt,dailyTempDiff,labelpad=10,label='right',ax=None,**plt_kwargs):

    hour24labels =     plt_kwargs['hour24labels']
    colors      =     plt_kwargs['colors']

    if ax is None:
        ax = plt.gca()

    cat000 = cat00.sort_values(by='Cluster')
    clus_ev_perhour0 = makeHourlyDF(cat000)

    d = []
    bottom = 0
    ss = clus_ev_perhour0.EvPerHour

    for k in range(1,Kopt+1):
        clus_ev_perhour1 = makeHourlyDF(cat000[cat000.Cluster==k])
        bar_heights = clus_ev_perhour1.EvPerHour/ss
        d.append(bar_heights)

        hour_labels = np.arange(0,len(clus_ev_perhour1.EvPerHour))
        collor = colors[k-1]

        if k ==1:
            ax.bar(hour_labels,clus_ev_perhour1.EvPerHour/ss, color=colors[0])

        else:
            bottom = bottom + d[k-2]
            ax.bar(hour_labels,bar_heights,bottom=bottom, color=collor)


##plotTempLine
    ax2 = ax.twinx()
    ax2.plot(dailyTempDiff,lw=2,color='k',ls='--')
    # [t.set_color('r') for t in ax2.yaxis.get_ticklabels()]
    
#     ax2.set_ylabel('')
    ax2.set_yticks([-2.5,0,2.5])
    ax2.set_yticklabels(['  -2.5','   0    $\Delta$T ($^\circ$C)','+2.5'])
    
#     if label == 'right':
#         ax2.set_ylabel('T ($^\circ$C)', color='k',labelpad=labelpad)
#     else:
#         ax2.set_ylabel('')
#         ax2.set_yticklabels([])

    ax.set_xticks(np.arange(0,24,6))

    ax.set_xticklabels(hour24labels[0:-1:6])
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Proportion per hour')

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotHourBar(cat00,Kopt,dailyTempDiff,ax=None,labelpad=10,label='right',colorBy='None',k=1,**plt_kwargs):

    hour24labels = plt_kwargs['hour24labels']
    colors      =     plt_kwargs['colors']


    if ax is None:
        ax = plt.gca()




    if colorBy == 'cluster':
        hour_df = cat00[cat00.Cluster==k]
        bar_color = colors[k-1]

    else:
        hour_df = cat00
        bar_color = 'black'


    clus_ev_perhour1 = makeHourlyDF(hour_df)

    hour_labels = np.arange(0,len(clus_ev_perhour1.EvPerHour))


    ax.bar(hour_labels,clus_ev_perhour1.EvPerHour, color=bar_color)


        ##plotTempLine
    ax2 = ax.twinx()
    ax2.plot(dailyTempDiff,lw=3,color='red',ls='--',alpha=.9)
    if label=='right':

        [t.set_color('red') for t in ax2.yaxis.get_ticklabels()]
        ax2.set_ylabel('')
        ax2.set_yticks([-2.5,0,2.5])
        ax2.set_yticklabels(['  -2.5','   0    T ($^\circ$C)','+2.5'])



    else:
        ax2.set_yticklabels([])
        ax2.set_ylabel('')
        ax2.set_yticks([])



    ax.set_xticks(np.arange(0,24,6))
    ax.set_xlim(-.5,23.5)



    ax.set_xticklabels(hour24labels[0:-1:6])


    ax.set_xlabel('Hour of Day')
    # ax.set_ylabel('Obersevations per hour')

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotBar(cat,Kopt,ax=None, byCluster=False, timeBin='D',barWidth=.5,**plt_kwargs):
    """


    Parameters
    ----------
    cat : index by pandas datetimte object, needs 'Cluster' and 'event_ID' columns
    Kopt : TYPE
        DESCRIPTION.
    ax : TYPE, optional
        DESCRIPTION. The default is None.
    byCluster : TYPE, optional
        DESCRIPTION. The default is False.
    timeBin : TYPE, optional
        DESCRIPTION. The default is 'D'.
    barWidth : TYPE, optional
        DESCRIPTION. The default is .5.
    **plt_kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    if ax is None:
        ax = plt.gca()


    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']
    numDays     =     plt_kwargs['numDays']
    hourMaxTemp =     plt_kwargs['hourMaxTemp']
    colors      =     plt_kwargs['colors']

    for i in range(numDays):
        ax.axvline(hourMaxTemp[i],c='gray',linestyle='-',linewidth=1,alpha=0.3)


    if byCluster == False:
        clus_events_perday = cat.resample(timeBin).event_ID.count()
        lenn = clus_events_perday.sum()
        ax.bar(clus_events_perday.index, clus_events_perday,
               width=barWidth,
               color='k',
               align='edge',
               label=f'N={lenn}',)

    if byCluster == True:

        for k in range(1,Kopt+1):
            clus_events = cat[cat.Cluster == k]

            clus_events_perday = clus_events.resample(timeBin).event_ID.count()
            lenn = clus_events_perday.sum()

            ax.bar(clus_events_perday.index, clus_events_perday, width=barWidth,color=colors[k-1],alpha=.7)

    ax.set_ylabel('Observations \n per hour',labelpad=4)
#     ax.set_ylim(0,40)
#     ax.set_xlim(clus_events_perday.index.min(),clus_events_perday.index.max())
    ax.set_xticks(day_ticks)
    ax.set_xticklabels(day_labels)
#     ax.set_ylabel('Number of observations')
#     ax.set_xlabel('Date, 2007')
    ax.set_xlim(tstart,tend)

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotBarCluster(cat00,k,ax=None,barWidth=.1,timeBin='3H',**plt_kwargs):

    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']
    colors      =     plt_kwargs['colors']
    hourMaxTemp      =     plt_kwargs['hourMaxTemp']
    numDays      =     plt_kwargs['numDays']

    if ax is None:
        ax = plt.gca()

    for i in range(numDays):
        ax.axvline(hourMaxTemp[i],c='gray',linestyle='-',linewidth=1,alpha=0.3)


    k = int(k)
    clus_events = cat00[cat00.Cluster == k]

    clus_events_perday = clus_events.resample(timeBin).event_ID.count()
    lenn = clus_events_perday.sum()

    bar_heights = clus_events_perday

    ax.bar(clus_events_perday.index, bar_heights, width=barWidth,color=colors[k-1],alpha=1)
    # ax.grid()

#     ax.set_xlim(clus_events_perday.index.min(),clus_events_perday.index.max())

    ax.set_xlim(tstart,tend)
#     ax.set_ylim(0,40)
#     ax.set_xlim(clus_events_perday.index.min(),clus_events_perday.index.max())
    ax.set_xticks(day_ticks)
    ax.set_xticklabels(day_labels)
    # ax.legend(loc='upper right')
#     ax.set_ylabel('Number of observations')
#     ax.set_xlabel('Date, 2007')
    ax.set_xlim(tstart,tend)

def plotBarStacked(cat00,Kopt,barWidth=.9,timeSpan='D',ax=None,**plt_kwargs):

    if ax is None:
        ax = plt.gca()

    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']
    colors      =     plt_kwargs['colors']
    hourMaxTemp      =     plt_kwargs['hourMaxTemp']
    numDays      =     plt_kwargs['numDays']

    for i in range(numDays):
        ax.axvline(hourMaxTemp[i],c='gray',linestyle='-',linewidth=1,alpha=0.3)


    cat000 = cat00.sort_values(by='Cluster')
    clus_ev_perday0 = cat000.resample(timeSpan).event_ID.count()
    bar_labels = np.array(clus_ev_perday0.index)

    d = []
    bottom = 0

    for k in range(1,Kopt+1):

        ax = plt.gca()
        clusCat = cat000[cat000.Cluster==k]
    #         print(len(clusCat),k)
        clus_ev_perday1 = clusCat.resample(timeSpan).event_ID.count()
        bar_height = np.array(clus_ev_perday1/ clus_ev_perday0 )

        bar_height[np.isnan(bar_height)]=0

    #     day_labels = clus_ev_perday0.

        d.append(bar_height)

        collor = colors[k-1]

        if k ==1:
            ax.bar(bar_labels,bar_height,barWidth,bottom=bottom, color=collor,align='edge')

        else:
            bottom = bottom + d[k-2] #+ d[k-2]
            ax.bar(bar_labels,bar_height,barWidth,bottom=bottom, align='edge')#,bottom=bottom)#, color=collor)

        ax.set_xlim(tstart,tend)
        ax.set_xticks(day_ticks)
        ax.set_xticklabels(day_labels)
    ax.set_xlabel('Date, 2007')
    ax.set_ylabel('Proportion of observations')
    ax.set_xlim(tstart,tend)



##################################################################################################
# ##################################################################################################
#         _   _                     _       _
#        | | | |                   | |     | |
#    ___ | |_| |__   ___ _ __    __| | __ _| |_ __ _
#   / _ \| __| '_ \ / _ \ '__|  / _` |/ _` | __/ _` |
#  | (_) | |_| | | |  __/ |    | (_| | (_| | || (_| |
#   \___/ \__|_| |_|\___|_|     \__,_|\__,_|\__\__,_|


##################################################################################################

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotGPS(gps_data,ax=None,size=.5,ylabel='right',**plt_kwargs):


    if ax is None:
        ax = plt.gca()

    ax2 = ax.twinx()


    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']


    ax2.plot(gps_data,c='darkgreen',linestyle='None',marker='.',ms=size,alpha=1)

    [t.set_color('darkgreen') for t in ax2.yaxis.get_ticklabels()]


    if ylabel=='right':
        ax2.set_ylabel('GPS displacement (m)',color='darkgreen')#  \n ($cm/day$)
        # ax3.set_yticks([0,5,15,25,35])
        # ax3.set_yticklabels(['0','5','15','25','35'])
    else:
        ax2.set_ylabel('')#,color='darkgreen')
        ax2.set_yticklabels('')
        ax2.set_yticks([])


    ax2.set_xticks(day_ticks)
    ax2.set_xticklabels(day_labels)
    ax2.set_xlim(tstart,tend)
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotLake(lake_df,rain_df,ax=None,ylabel=None,legend=False,bb1=0,bb2=2,**plt_kwargs):


    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']
    numDays      =     plt_kwargs['numDays']



    if ax is None:
        ax = plt.gca()

    ax3 = ax.twinx()
    label= labelR = None

    if ylabel=='left':
        ax3.set_yticks([])
        ax3.set_yticklabels('')
        ax.set_ylabel('Lake height (m) \n Rain (mm) ',color='b')
        ax.set_yticks(np.arange(0,61,10))
        ax.set_yticklabels([f'{a:.0f}' for a in np.arange(0,61,10)])
        [t.set_color('b') for t in ax.yaxis.get_ticklabels()]
#         ax.legend(loc='upper left',bbox_to_anchor=(bb1,bb2))


    if ylabel=='right':
#         ax3.set_yticks([])
#         ax3.set_yticklabels('')
#         ax3 = ax
        label='Lake height (m)'
        labelR = 'Rain (mm)'
        ax3.set_ylabel('Lake height (m)\n Rain (mm) ',color='b')#
        # ax3.set_yticks([0,5,15,25,35])
        # ax3.set_yticklabels(['0','5','15','25','35'])
    else:
        ax3.set_ylabel('',color='b')
        ax3.set_yticks([])
        ax3.set_yticklabels('')

    [t.set_color('b') for t in ax3.yaxis.get_ticklabels()]


    ax3.plot(lake_df.lake,c='b',lw=3,ls='--',label=label)

    rain10 = rain_df * 10 #convert cm to mm
    ax3.plot(rain10,c='b',label=labelR,lw=1)

    ax3.set_xticks(day_ticks)
    ax3.set_xticklabels(day_labels)

    ax3.set_xlabel('')
    ax3.set_xlim(tstart,tend)
#     ax3.set_ylim(0,44)
#     ax.set_ylim(0,38)

    # for i in range(numDays):
    #     ax.axvline(hourMaxTemp[i],c='gray',linestyle='--',linewidth=1,alpha=.5)

#     if legend is True:
#         if ylabel == 'right':
#             ax3.legend(loc='upper left',bbox_to_anchor=(bb1,bb2))
#             ax.legend(loc='upper left',bbox_to_anchor=(bb1,bb2))

#         if ylabel == 'left':
#             ax.legend(loc='upper left',bbox_to_anchor=(bb1,bb2))
#             ax3.legend(loc='upper left',bbox_to_anchor=(bb1,bb2))

    ax3.set_xlim(tstart,tend)
    ax.set_xlim(tstart,tend)
    ax3.set_ylim(bottom=0)
    ax.set_ylim(bottom=0)
    
    
def plotTemp(temp_series,ax=None,labels='on',alpha=1,**plt_kwargs):

    if ax is None:
        ax = plt.gca()
    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']


    ax2 = ax.twinx()
    ax2.set_yticklabels('')
    ax2.set_yticks([])

#     [t.set_color('r') for t in ax2.yaxis.get_ticklabels()]
    ax2.plot(temp_series,label='T ($C^\circ$)',c='red',lw=1,alpha=alpha)

    #zero line
    ax2.axhline(y=0,c='red',linestyle='--',alpha=.5,label='0($^\circ$C)')




    if labels == 'on':
        ##scale line
        tx = dtt.datetime(2007, 7, 16)
        tx2 = dtt.datetime(2007, 7, 16,7,0,0)
        txZero = dtt.datetime(2007, 7, 16)
        yZero = -18
        yMax = 30
        yMin = 20
        yTen = yMin+2
        ax2.text(txZero,yZero,'0$^\circ$C',color='r',alpha=.8)#,rotation=90)
        ax2.vlines(tx, ymin=yMin, ymax=yMax,color='r',lw=1,alpha=.8) #scale line
        ax2.text(tx2,yTen,'10$^\circ$C',color='r',alpha=.8)




    ax2.set_xlim(tstart,tend)
    ax2.set_ylim(-70,70)
    ax2.set_xticks(day_ticks)
    ax2.set_xticklabels(day_labels)
    ax2.set_xlim(tstart,tend)
    ax.set_xlim(tstart,tend)

def plotStrainRate(garciaDF_D,garciaDF_3H,ax=None,ylabel='right',**plt_kwargs):


    if ax is None:
        ax = plt.gca()


    tstart      =     plt_kwargs['tstart']
    tend        =     plt_kwargs['tend']
    day_ticks   =     plt_kwargs['day_ticks']
    day_labels  =     plt_kwargs['day_labels']


    ax2 = ax.twinx()


    ax2.plot(garciaDF_3H.st_3H,label='Strain rate \n ($\mu m/day$)$',c='darkgreen',lw=1,alpha=1)
    ax2.plot(garciaDF_D.st_D,label=None,c='darkgreen',ls='--',lw=1,alpha=1)

    [t.set_color('darkgreen') for t in ax2.yaxis.get_ticklabels()]


#     if ylabel=='left':
#         ax2.set_yticks([])
#         ax2.set_yticklabels('')
#         ax2 = ax
#         ax.set_ylabel('Strain $\mu m/day$',color='darkgreen')
#         # ax.set_yticks([0,5,15,25,35])
#         # ax.set_yticklabels(['0','5','15','25','35'])

    if ylabel=='right':
        ax2.set_ylabel('Strain rate \n ($\mu m/day$)',color='darkgreen')#
        # ax3.set_yticks([0,5,15,25,35])
        # ax3.set_yticklabels(['0','5','15','25','35'])
    else:
        ax2.set_ylabel('')#,color='darkgreen')
        ax2.set_yticks([])
        ax2.set_yticklabels('')

    ax2.set_xlim(tstart,tend)
    # ax2.set_ylim(-70,70)
    ax2.set_xticks(day_ticks)
    ax2.set_xticklabels(day_labels)
    ax2.set_xlim(tstart,tend)
    ax.set_xlim(tstart,tend)


def plotLakeOutline(cat_map):
    lakexcsv = pd.read_csv('/Users/theresasawi/Documents/SpecUFEx_v1/GARCIA_BundledData2007/lakeshore_x.csv',names=['x'])
    lakeycsv = pd.read_csv('/Users/theresasawi/Documents/SpecUFEx_v1/GARCIA_BundledData2007/lakeshore_y.csv',names=['y'])

    lakexcsv['x'] = lakexcsv['x'] + 220980
    lakeycsv['y'] = lakeycsv['y'] + -5000410
    plt.plot(lakexcsv.x,lakeycsv.y,color='steelblue')
    plt.fill(lakexcsv['x'], lakeycsv['y'],color='steelblue',alpha=.2)
    plt.xlim(cat_map.X_m.min(),cat_map.X_m.max())
    plt.ylim(cat_map.Y_m.min(),cat_map.Y_m.max())




##################################################################################################
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo
##################################################################################################

##################################################################################################
# ##################################################################################################
#        _           _            _
#       | |         | |          (_)
#    ___| |_   _ ___| |_ ___ _ __ _ _ __   __ _
#   / __| | | | / __| __/ _ \ '__| | '_ \ / _` |
#  | (__| | |_| \__ \ ||  __/ |  | | | | | (_| |
#   \___|_|\__,_|___/\__\___|_|  |_|_| |_|\__, |
#                                          __/ |
#                                         |___/
##################################################################################################

# ##################################################################################################
# # .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo
# ##################################################################################################


def plotPCA(cat00,catall,Kopt, size=5,size2=15, alpha=.5,labelpad = 5,fontsize=8,ax=None, fig=None, **plt_kwargs):


    colors      =     plt_kwargs['colors']


    if fig is None:
        fig = plt.gcf()

    if ax is None:
        ax = plt.gca()



    for k in range(1,Kopt+1):

        catk = cat00[cat00.Cluster == k]
        ax.scatter(catk.PC1,catk.PC3,catk.PC2,
                      s=size,
                      marker='x',
                      color=colors[k-1],
                      alpha=alpha)


# plot top FPs
    ax.scatter(catall.PC1,catall.PC3,catall.PC2,
                      s=size2,
                      marker='x',
                      color='k',
                      alpha=1)

    # sm = plt.cm.ScalarMappable(cmap=colors,
    #                            norm=plt.Normalize(vmin=df_stat.Cluster(),vmax=df_stat.Cluster()))
    axLabel = 'PC'#'Principal component '#label for plotting
    # cbar = plt.colorbar(sm,label=stat_name,shrink=.6,pad=.3);

    ax.set_xlabel(f'{axLabel} 1',labelpad=labelpad, fontsize = fontsize);
    ax.set_ylabel(f'{axLabel} 3',labelpad=labelpad, fontsize = fontsize);
    ax.set_zlabel(f'{axLabel} 2',labelpad=labelpad, fontsize = fontsize);

    ax.set_xlim(-.6,.6)
    ax.set_ylim(-.6,.6)
    ax.set_zlim(-.6,.6)

    ticks =  np.linspace(-.6,.6,5)
    tick_labels = [f'{t:.1f}' for t in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(ticks)
    ax.set_yticklabels(tick_labels)
    ax.set_zticks(ticks)
    ax.set_zticklabels(tick_labels)



def plotPCA_Stat(cat00, catall, df_stat, stat_name, Kopt, cmap,cbar=True,size=5,size2=100,alpha = .8,labelpad=10, fontsize=12,ax=None, fig=None):



    if fig is None:
        fig = plt.gcf()

    if ax is None:
        ax = plt.gca()


    if stat_name == 'Date, 2007':

        sm = plt.cm.ScalarMappable(cmap=cmap,
                                   norm=plt.Normalize(vmin=cat00.index.min().value,vmax=cat00.index.max().value))

    else:
        sm = plt.cm.ScalarMappable(cmap=cmap,
                                   norm=plt.Normalize(vmin=df_stat.min(),vmax=df_stat.max()))


    if cbar:
        cbar = plt.colorbar(sm,label=stat_name,shrink=.3,pad=.2);

        if stat_name == 'Date, 2007':
            cbar.ax.set_yticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%b %d'))



    ax.scatter(cat00.PC1, cat00.PC3,cat00.PC2,
                    s=size,
                    c=df_stat,
                    marker='x',
                    alpha=alpha,
                    cmap=cmap);



    ax.scatter(catall.PC1,catall.PC3,catall.PC2,
                      s=size2,
                      marker='x',
                      color='k',
                      alpha=1)




    axLabel = 'PC'#'Principal component '#label for plotting

    ax.set_xlabel(f'{axLabel} 1',labelpad=labelpad, fontsize = fontsize);
    ax.set_ylabel(f'{axLabel} 3',labelpad=labelpad, fontsize = fontsize);
    ax.set_zlabel(f'{axLabel} 2',labelpad=labelpad, fontsize = fontsize);
    ax.set_title(stat_name,fontsize=14)
    ax.set_xlim(-.6,.6)
    ax.set_ylim(-.6,.6)
    ax.set_zlim(-.6,.6)

    ticks =  np.linspace(-.6,.6,5)
    tick_labels = [f'{t:.1f}' for t in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(ticks)
    ax.set_yticklabels(tick_labels)
    ax.set_zticks(ticks)
    ax.set_zticklabels(tick_labels)


    

def plotPCA2D(cat00,catall,Kopt, size=5,size2=15, alpha=.5,labelpad = 5,fontsize=8,ax=None, fig=None, **plt_kwargs):


    colors      =     plt_kwargs['colors']


    if fig is None:
        fig = plt.gcf()

    if ax is None:
        ax = plt.gca()



    for k in range(1,Kopt+1):

        catk = cat00[cat00.Cluster == k]
        ax.scatter(catk.PC1,catk.PC2,
                      s=size,
                      marker='x',
                      color=colors[k-1],
                      alpha=alpha)


# plot top FPs
    ax.scatter(catall.PC1,catall.PC2,
                      s=size2,
                      marker='x',
                      color='k',
                      alpha=1)

    # sm = plt.cm.ScalarMappable(cmap=colors,
    #                            norm=plt.Normalize(vmin=df_stat.Cluster(),vmax=df_stat.Cluster()))
    axLabel = 'Principal component'#'Principal component '#label for plotting
    # cbar = plt.colorbar(sm,label=stat_name,shrink=.6,pad=.3);

    ax.set_xlabel(f'{axLabel} 1',labelpad=labelpad, fontsize = fontsize);
    ax.set_ylabel(f'{axLabel} 2',labelpad=labelpad, fontsize = fontsize);


    ax.set_xlim(-.6,.6)
    ax.set_ylim(-.6,.6)


    ticks =  np.linspace(-.6,.6,5)
    tick_labels = [f'{t:.1f}' for t in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(ticks)
    ax.set_yticklabels(tick_labels)





def plot_pca_components(x, coefficients=None, mean=0, components=None,
                        imshape=(15, 15), n_components=8, fontsize=12,
                        show_mean=True):
    if coefficients is None:
        coefficients = x

    if components is None:
        components = np.eye(len(coefficients), len(x))

    mean = np.zeros_like(x) + mean


    fig = plt.figure(figsize=(1.2 * (5 + n_components), 1.2 * 2))
    g = plt.GridSpec(2, 4 + bool(show_mean) + n_components, hspace=0.3)

    def show(i, j, x, title=None):
        ax = fig.add_subplot(g[i, j], xticks=[], yticks=[])
        ax.imshow(x.reshape(imshape), interpolation='nearest')
        if title:
            ax.set_title(title, fontsize=fontsize)

    show(slice(2), slice(2), x, "True")

    approx = mean.copy()

    counter = 2
    if show_mean:
        show(0, 2, np.zeros_like(x) + mean, r'$\mu$')
        show(1, 2, approx, r'$1 \cdot \mu$')
        counter += 1

    for i in range(n_components):
        approx = approx + coefficients[i] * components[i]
        show(0, i + counter, components[i], r'$c_{0}$'.format(i + 1))
        show(1, i + counter, approx,
             r"${0:.2f} \cdot c_{1}$".format(coefficients[i], i + 1))
        if show_mean or i > 0:
            plt.gca().text(0, 1.05, '$+$', ha='right', va='bottom',
                           transform=plt.gca().transAxes, fontsize=fontsize)

    show(slice(2), slice(-2, None), approx, "Approx")
    return fig

def plotPVE(sklearn_pca,ax=None):

    if ax is None:
        ax = plt.gca()


    ax.bar([1,2,3], sklearn_pca.explained_variance_ratio_[0:3],alpha=.4)
    ax.set_xticks([1,2,3])
    ax.set_xticklabels(['1','2','3'])
    ax.plot([1,2,3], np.cumsum(sklearn_pca.explained_variance_ratio_[0:3]),'o-k',label='cumulative')
    ax.legend(fontsize=8)
    plt.title('Proportion of variance explained')
    plt.ylabel('')
    plt.xlabel('Principal component (PC)');




def plotSSE(Kopt2, sse,range_n_clusters,starSize=1.5,ax=None):

    if ax is None:
        ax = plt.gca()

    ax.plot(range_n_clusters, sse,color='k')
    ax.plot(Kopt2, sse[Kopt2-2],color='orange',marker='*',ms=starSize,alpha=.5)
    
    ax.set_xticks([int(r) for r in range_n_clusters])
    ax.set_xticklabels([str(r) for r in range_n_clusters])
    
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Sum of squared error')
    
    ax.grid()


def plotSilhScore(Kopt2, avgSils, range_n_clusters,starSize=1.5,ax=None):

    if ax is None:
        ax = plt.gca()

    ax.plot(range_n_clusters,avgSils,color='k')
    ax.plot(Kopt2, avgSils[Kopt2-2],color='orange',marker='*',ms=starSize,alpha=.5)

    ax.set_xticks([int(r) for r in range_n_clusters])
    ax.set_xticklabels([str(r) for r in range_n_clusters])

    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Mean silhouette score')

    ax.grid()


def plotConfusionMatrix(cat00,sgram_df_clustered,norm_by='true',ax=None):
#     norm_by: 'true', 'pred', or None
    if ax is None:
        ax = plt.gca()

    y_true = np.array(cat00.Cluster)
    y_pred = np.array(sgram_df_clustered.Cluster)

    cm = confusion_matrix(y_true,y_pred,normalize=norm_by)
    sns.heatmap(cm)
    plt.xlabel('Clustered on spectra')
    plt.ylabel('Clustered on PC of FP')

    print(cm)
    print(classification_report(y_true, y_pred))

# sgram_df['datetime_index'] = [pd.to_datetime(d) for d in catall.datetime];
# sgram_df.sort_values(by='datetime_index');





def plotCCMatrix(catCC,shift_cc,dataH5_path,station,channel,fmin,fmax,fs,ax=None):
###    shift_cc : #Number of samples to shift for cross correlation. The cross-correlation will consist of 2*shift+1 or 2*shift samples. The sample with zero shift will be in the middle.

    if ax is None:
        ax = plt.gca()

    cc_mat = np.zeros([len(catCC),len(catCC)])
    lag_mat = np.zeros([len(catCC),len(catCC)])

    for i in range(len(catCC)):
        for j in range(len(catCC)):

            evIDA = catCC.event_ID.iloc[i]
            evIDB = catCC.event_ID.iloc[j]


            wf_A = getWF(evIDA,dataH5_path,station,channel,fmin=fmin,fmax=fmax,fs=fs)
            wf_B = getWF(evIDB,dataH5_path,station,channel,fmin=fmin,fmax=fmax,fs=fs)



            cc = correlate(wf_A, wf_B, shift_cc)
            lag, max_cc = xcorr_max(cc)

            cc_mat[i,j] = max_cc
            lag_mat[i,j] = lag


    plt.imshow(cc_mat)
    cbar = plt.colorbar(pad=.06)
    cbar.set_label('Correlation coefficient',labelpad=8)#,fontsize = 14)

    plt.clim(-1,1)

    return cc_mat,lag_mat


def plotCCMatrix_Synth(wf_list,shift_cc):
###    shift_cc : #Number of samples to shift for cross correlation. The cross-correlation will consist of 2*shift+1 or 2*shift samples. The sample with zero shift will be in the middle.

    cc_mat = np.zeros([len(wf_list),len(wf_list)])
    lag_mat = np.zeros([len(wf_list),len(wf_list)])

    for i in range(len(wf_list)):
        for j in range(len(wf_list)):

            wf_A = wf_list[i]
            wf_B = wf_list[j]


            cc = correlate(wf_A, wf_B, shift_cc)
            lag, max_cc = xcorr_max(cc)

            cc_mat[i,j] = max_cc
            lag_mat[i,j] = lag

    plt.figure()
    plt.imshow(cc_mat)
    cbar = plt.colorbar(pad=.06)
    cbar.set_label('Correlation coefficient',labelpad=8)#,fontsize = 14)
    plt.clim(-1,1)

    return cc_mat



# ##################################################################################################
# ##################################################################################################
#    _____                 _    _ ______ ______                    _               _
#   / ____|               | |  | |  ____|  ____|                  | |             | |
#  | (___  _ __   ___  ___| |  | | |__  | |__  __  __   ___  _   _| |_ _ __  _   _| |_
#   \___ \| '_ \ / _ \/ __| |  | |  __| |  __| \ \/ /  / _ \| | | | __| '_ \| | | | __|
#   ____) | |_) |  __/ (__| |__| | |    | |____ >  <  | (_) | |_| | |_| |_) | |_| | |_
#  |_____/| .__/ \___|\___|\____/|_|    |______/_/\_\  \___/ \__,_|\__| .__/ \__,_|\__|
#         | |                                                         | |
#         |_|                                                         |_|
##################################################################################################




##################################################################################################
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo
##################################################################################################


## plot NMF dictionary, sorted
def plotW(W_new, numPatterns, fSTFT, aspect=.3,ax=None):

    if ax is None:
        ax = plt.gca()

    ax.set_aspect(aspect)

    im = plt.pcolormesh(np.arange(numPatterns),fSTFT, W_new,cmap=cm.magma,shading='auto')

#     freqLabels = [str(i) for i in [20,40,60,80]]


#     plt.yticks(ticks=[20,40,60,80],
#                labels=freqLabels)


    plt.xlabel('$P$')
#     plt.yticks(ticks=np.arange(int(fSTFT.min()),int(fSTFT.max()),40),labels=freqLabels)
    plt.ylabel('f (Hz)')

    # cbar = plt.colorbar(im,fraction=0.1, pad=0.1)
    # cbar.set_label('Power',labelpad=10)
    # cbar.set_ticks([])
    # plt.title('W; NMF Dictionary')

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotWACM(evID,pathACM,order_swap,W_new,tSTFT, fSTFT,ax=None):

    if ax is None:
        ax = plt.gca()


    fi = 'out.' + str(evID) + '.mat'



    mat = loadmat(pathACM  + fi)

    ACMMat = mat.get('H')
    gain = mat.get('gain')
    Xpwr = mat.get('Xpwr')

    gain_new = resortByNMF(gain,order_swap)

    a = resortByNMF(ACMMat.T,order_swap)

    Wa = W_new@ (gain_new * a).T

    plt.pcolormesh(tSTFT, fSTFT, Wa,cmap=cm.magma,shading='auto')
    plt.xlabel('t (s)')
    plt.ylabel('f (Hz)')

#     cbar = plt.colorbar(pad=.06)
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotACM(evID,pathACM,order_swap,tSTFT, numPatterns, ax=None):

    if ax is None:
        ax = plt.gca()


    fi = 'out.' + str(evID) + '.mat'



    mat = loadmat(pathACM  + fi)

    ACMMat = mat.get('H')
    gain = mat.get('gain')
    Xpwr = mat.get('Xpwr')

    gain_new = resortByNMF(gain,order_swap)

    a = resortByNMF(ACMMat.T,order_swap)

    ACM = (gain_new * a).T

    plt.pcolormesh(tSTFT, np.arange(numPatterns), ACM,cmap=cm.magma,shading='auto')
    plt.xlabel('t (s)')
    plt.ylabel('$P$')

#     cbar = plt.colorbar(pad=.06)
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotSTM(evID,pathSTM,tSTFT,ax=None):

    if ax is None:
        ax = plt.gca()

    fi = 'out.' + str(evID) + '.mat'


    mat = loadmat(pathSTM  + fi)

    STMMat = mat.get('gam')



    plt.pcolormesh(tSTFT, np.arange(STMMat.shape[0]), STMMat ,cmap=cm.magma,shading='auto')


    plt.xlabel('t (s)')
    plt.ylabel('$S$')
#     ax.set_ylim(0,9)

#     cbar = plt.colorbar(pad=.06)
#     plt.yticks(ticks = list(range(0,numStates,5)),labels=list(range(0,numStates,5)))

#     cbar.set_label('',labelpad=18,fontsize = smallfont)
    # plt.gca().invert_yaxis()

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo


def plotFP(path_proj, outfile_name,evID,ax=None):

    if ax is None:
        ax = plt.gca()
    # ax.set_aspect('equal')
    with h5py.File(path_proj + outfile_name,'r') as MLout:

        fp = MLout['SpecUFEX_output/fprints'].get(str(evID))[:]


    plt.pcolormesh(fp,cmap=cm.magma)#, aspect='auto')
    # plt.yticks(ticks = [0,5,10],labels=['0','5','10'])
    # plt.xticks(ticks = [0,5,10],labels=['0','5','10'])
    plt.yticks(ticks = [0,10],labels=['0','10'])
    plt.xticks(ticks = [0,10],labels=['0','10'])


    ax.set_xlabel('$S(t+1)$')
    ax.set_ylabel('$S(t)$')
#     ax.set_xlim(0,9)
#     ax.set_ylim(0,9)
#     cbar = plt.colorbar(pad=.06)

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

def plotEB(EB_new,aspect=1,ax=None):

    if ax is None:
        ax = plt.gca()


    ax.set_aspect(aspect)
    im = plt.pcolormesh(EB_new.T,cmap=cm.magma,shading='auto')



    ax.set_xlabel('$S$')
    ax.set_ylabel('$P$')
    # plt.gca().invert_yaxis()
#     ax.set_xticks(np.arange(0,numStates,5))#,ha='left')#,alignment='center')#, fontsize=10)
#     ax.set_xticklabels(np.arange(0,numStates,5),horizontalalignment='left')
#     ax.set_yticks(ticks = np.arange(0,numPatterns,5))#,alignment='center')#, fontsize=10)

# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo..oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo

## plot reverse mapping matrix RMM

def plotRMM(RMM,fSTFT,numStates,aspect=.5,ax=None):

    if ax is None:
        ax = plt.gca()

    ax.set_aspect(aspect)
#     ax.set_aspect('equal')
    ax.pcolormesh(np.arange(0,numStates+1),fSTFT,RMM,cmap=cm.magma,shading='auto')

    # freqLabels = [str(i) for i in [20,40,60,80]]


    # plt.yticks(ticks=[20,40,60,80],
    #            labels=freqLabels)

    ax.set_xlabel('$S$')
    ax.set_ylabel('f (Hz)')
