#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime

def gorner_dt(evID,key):

    """
    returns datetime from gorner event ID
    evID: event ID (ex. 71719235959)
    """



    if "Event"  in key or 'Cont' in key: #TS 2021/02/07 for J5 events
        datt = str(evID)
        timestamp = datetime.datetime(
                         int('200' + datt[0]),
                         int( datt[1:3]),
                         int( datt[3:5]),
                         int( datt[5:7]),
                         int( datt[7:9]),
                         int( datt[9:11])
                          )
        
    # if "Cont"  in key: #TS 2021/02/15 for J5 cont
    #     if len(evID) == 12:
    #         datt = str(evID)[1:]
    #     else:
    #         datt = str(evID)
    #     timestamp = datetime.datetime(
    #                      int('200' + datt[0]),
    #                      int( datt[1:3]),
    #                      int( datt[3:5]),
    #                      int( datt[5:7]),
    #                      int( datt[7:9]),
    #                      int( datt[9:11])
    #                       )



    # elif "05" not in key: ##what is this? TS 2021/02/07
    #     datt = evID
    #     timestamp = datetime.datetime(
    #                      int('200' + datt[0]),
    #                      int( datt[1:3]),
    #                      int( datt[3:5]),
    #                      int( datt[5:7]),
    #                      int( datt[7:9]),
    #                      int( datt[9:11])
    #                       )



    else:
        datt = evID[1:]
        timestamp = datetime.datetime(
                         int('200' + datt[0]),
                         int( datt[1:3]),
                         int( datt[3:5]),
                         int( datt[5:7]),
                         int( datt[7:9]),
                         int( datt[9:11])
                          )


    # else:
    #     datt = evID
    #     timestamp = datetime.datetime(
    #                      int('200' + datt[0]),
    #                      int( datt[1:3]),
    #                      int( datt[3:5]),
    #                      int( datt[5:7]),
    #                      int( datt[7:9]),
    #                      int( datt[9:11])
    #                       )
        # return np.array(d,dtype='S') ## return in H5-friendly format
    return timestamp
