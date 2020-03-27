# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:33:31 2020

@author: Philipp
"""

def interpolateTemporal(grid,  timeStart ,  timeEnd ,  timeStepDays , kind ='linear'):
    """
    interpolateTemporal description:
       interpolate temporal
       Parameters: 
     input:
        grid: orbit (output dict from shape2grid)
                WITH AcquisitionTime from  getAcquisitionTime
       timeEnd: string i.e. 20200228 (if not in Acquisition intervall will set on last days)
       timeStart :  string i.e. 19910119 (if not in Acquisition intervall will set on first days)
       timeStepDays: int steps in days i.e. 12 
       kind   : string ‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’
       
    output: grid with original values orgD_*
                    and new values D_*
            
        edit: 28.2.2020 Philipp Schneider, ifp
    """ 
    from datetime import datetime
    from  jdcal import gcal2jd,jd2gcal
    from scipy import interpolate
    import numpy as np
    import copy
    grid=copy.deepcopy(grid)
    
    # convert start end to julian day
    timeStart=gcal2jd(datetime.strptime(timeStart,'%Y%m%d').year ,datetime.strptime(timeStart,'%Y%m%d').month,datetime.strptime(timeStart,'%Y%m%d').day)[1]
    timeEnd=gcal2jd(datetime.strptime(timeEnd,'%Y%m%d').year ,datetime.strptime(timeEnd,'%Y%m%d').month,datetime.strptime(timeEnd,'%Y%m%d').day)[1]
    
    
    # get all acq dates
    t=grid.get('AcquisitionTime').get('JulianDays')
    
    
    # check if start and end are in the time interval
    if timeStart<t[0]:
        print('Cannot interpolate')
        print('timeStart < first Acquisition day!')
        print('timeStart is set to first day', t[0])
        timeStart=t[0]
    if timeEnd>t[-1]:
        print('Cannot interpolate')
        print('timeEnd > last Acquisition day!')
        print('timeEnd is set to last day', t[-1])
        timeEnd=t[-1]
        
        
    # get dates for resample
    tnew=np.arange(timeStart,timeEnd,timeStepDays)
    
    
    # create empyt cube 
    datCube=np.full(np.array([grid.get('mask').shape[0],grid.get('mask').shape[1],tnew.shape[0]]).flatten(),np.nan)
    
    # itter over all full cells
    print('Temporal Interpolate between ',timeStart,' and ',timeEnd)
    for row in np.arange(0,grid.get('mask').shape[0]-1):
        for col in  np.arange(0,grid.get('mask').shape[1]-1):
            # check if cell is empty
            if grid.get('mask')[row][col]:
                continue
            
            # print(row)
            # print(col)
            # get all values in a Cell
    
            Data=[grid.get(dateString)[row][col] for dateString in grid.get('AcquisitionTime').get('DateStrigns')]   
            
            # interpolate
            f = interpolate.interp1d(t, Data,kind)
            Datanew=f(tnew)
            # assign new values to datacube
            datCube[row,col,:]=Datanew;
        print(".", end ="")         
    
    # rename old fields D_* -> orgD_         
    DateStrigns=[key for key in grid.keys() if 'D_' in key[0:2]]   
      
    for oldkey in DateStrigns:
        newkey='org'+oldkey
        grid.update({newkey: grid[oldkey]})  
        del grid[oldkey]
        # crete new date string julianday -> D_*
    for i in np.arange(0,datCube.shape[2]-1,1):        
        datetimetn=jd2gcal(2400000.5,tnew[i]) 
        stringDateTime= datetime(datetimetn[0], datetimetn[1], datetimetn[2]).strftime('%Y%m%d')        
        grid.update({'D_'+stringDateTime: datCube[:,:,i]})  
        
    # rename org AcquisitionTime   ->   orgAcquisiTiontime 
    oldkey='AcquisitionTime'
    newkey='org'+oldkey
    grid.update({newkey: grid[oldkey]})
    #delete AcquisitionTime
    del grid[oldkey]
    #create new AcquisitionTime
    from sarscapepy import getAcquisitionTime
    grid=getAcquisitionTime(grid)
    
        
    return grid    
