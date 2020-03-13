#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: maref
"""




def read_file(filename):
    import geopandas
    df = geopandas.read_file(filename)
    df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
    return df

def headerinfo(dataFrame):
   import pandas as pd
   hdinfo=dataFrame.columns.tolist()
   tinfo=hdinfo[18:]
   tinfo = [tinfo.replace('D_','') for tinfo in tinfo ]
   tstring=pd.DataFrame(tinfo)
   ts=pd.to_datetime(tstring[0], format='%Y%m%d').dt.strftime("%Y-%m-%d")
   ts=pd.to_datetime(ts)
   return hdinfo,tinfo,ts

def v2point(data,variable):
    import pandas as pd
    df2=Dataframe[['Lon','Lat',variable]]
    return df2   

def point2grd(data,output_filename):
    import gdal
    import pandas as pd
    import gdal
    pd.data.to_csv(output_filename+'.csv',index=False)
    str2=output_filename
    str1= '''<OGRVRTDataSource>
          <OGRVRTLayer name= '''
    str3='''  >
            <SrcDataSource> '''
    str4= ''' </SrcDataSource>
            <GeometryType>wkbPoint</GeometryType>
            <GeometryField encoding="PointFromColumns" x="Lon" y="Lat" z='''
    str5= ''' />
           </OGRVRTLayer>
    </OGRVRTDataSource> '''
    outstring =str1+'"'+str2+'"'+str3+str2+".csv"+str4+'"'+str(ds.columns[2])+'"'+str5
    text_file = open(output_filename+'.vrt', "wt")
    n = text_file.write(outstring)
    text_file.close()
    output=gdal.Grid(output_filename+'.tif',output_filename+'.vrt')




"""
shape2grid description:
Parameters:    
    dataFrame: geopandas dataframe
    gridSize : float grid size of the output grid
    values   : list of strings with the desired output fields 
    LonMin,LonMax: X bounderies
    LatMin,LatMax: Y bounderies
    method  : interpolation methode for griddata() {‘linear’, ‘nearest’, ‘cubic’}
Output:
    dictionary with NumPy array of the interpolated values + mask    
"""


def shape2grid(dataFrame,gridSize,values=None,LonMin=None,LonMax=None,LatMin=None,LatMax=None,method='linear'):
    from scipy.interpolate import griddata
    import numpy as np
    print("executing shape2grid:")

    #"Check for None inputs and Values"
    #PS: If max and min are choosen like this they might not fit together
    if LonMin==None:
        LonMin=min(dataFrame.Lon)
    if LonMax==None:
        LonMax=max(dataFrame.Lon)  
    if LatMin==None:
        LatMin=min(dataFrame.Lat)
    if LatMax==None:
        LatMax=max(dataFrame.Lat)          
    
    #"Check if no value, if yes: unpack all"
    if values==None:
        none,values_temp=dataFrame.axes # all list columns 
        values=values_temp.values.tolist()
    elif type(values)==str:
        values=[values]
    
    # generate info
        # geoTransform tuple
    '''
    tlx: The X coordinate of the upper-left corner of the raster
    W-E size: The size of each cell from west to east        
    tly: The Y coordinate of the upper-left corner of the raster        
    N-S size: The size of each cell from north to south. Generally speaking this should be negative.
    '''
    print("Generating info...")

    info=({'geoTransform':(LonMin, gridSize,0,LatMin,0, gridSize)})
    info.update({'init':dataFrame.crs})
    info.update({'projection':'+init='+dataFrame.crs.get('init')})
    
    
    grid_out=({'info':info})         
    
    # create grid for Interpolation
    x=np.arange(LonMin, LonMax, gridSize)
    y=np.arange(LatMin, LatMax, gridSize)
    
    grid = tuple(np.meshgrid(x,y))
    # points as array
    points=np.vstack((np.array(dataFrame.Lon),np.array(dataFrame.Lat))).T
    
    
    
    #Create mask to mask out to far interpolation results
    
    # Construct kd-tree, functionality copied from scipy.interpolate

    from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    from scipy.spatial import cKDTree

    tree = cKDTree(points)
    xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    dists, indexes = tree.query(xi)
    mask=dists > gridSize
    
    #  save mask to output
    grid_out.update({'mask':mask} )
    for value in values:
        if type(dataFrame[value][1])!=np.float64 :
            continue
        
        print("Spatial Interpolate: " + value)
        grid_z0 = griddata(points, dataFrame[value], tuple(grid), method)
        #  mask missing values with NaNs
        grid_z0[mask] = np.nan
        
        #"assign to final output"
        grid_out.update( {value: grid_z0} )
        
    # apply    getAcquisitionTime 
    grid_out=getAcquisitionTime(grid_out)

    return grid_out
    


"""
dispGrid description:
Parameters:    
    grid: output dict from shape2grid
    layer_name : string with Layer name in grid
    base_path   : path to basemap (geotif lat,lon, i.e. SAS output) 
  
"""
    
# display on basemap
    
def dispGrid(grid,layer_name=None,base_path=None,fig=None, ax=None,clim=(-40,40)):
    

    import numpy as np
    import georaster
    import matplotlib.pyplot as plt


    
    # load grid as georeferenced georaster
    layer = georaster.SingleBandRaster.from_array(grid.get(layer_name), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))
    
    
    
    # new plot if no plot is provided plot
    if fig==None or ax==None:
        fig, ax = plt.subplots()
        newplot=True
        
        
    ax.set_title(layer_name)
    # if basemap path is set
    if type(base_path) == str:
        # load basemap
        base = georaster.MultiBandRaster(base_path)
        ax.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)
    
    plot_grid=ax.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
    

    #check if there is more than one axes
    plot_grid.set_clim(clim[0],clim[1])  

    if len(plt.gcf().axes) < 2:
        cbar = fig.colorbar(plot_grid)


    # label axis
    plt.xlabel('Lon')
    plt.ylabel('Lat')
    
    # flip Lat axis
    if plt.ylim()[0]>plt.ylim()[1]:
        plt.ylim(plt.ylim()[::-1])
    
    plt.show()
    #fig.canvas.manager.window.raise_()
    return fig, ax
           
"""
decomposeTwoOrbits description:
    following:  https://www.sciencedirect.com/science/article/pii/S0377027305003070?via%3Dihub
Parameters: 
    input:
    grid_asc: orbit1 (output dict from shape2grid)
    grid_dsc: orbit2 (output dict from shape2grid)

    output
    grid_vert: vertical grid (up down) horizonata
    grid_horz: horizontal grid (east west)
"""    
  
def decomposeTwoOrbits(grid_asc, grid_dsc, layer_name):
    import numpy as np
    
    # check input
    # assert len(grid_asc)==len(grid_dsc), 'dicts (grids) have different length' # error for wrong input
    
    # check if A_LOS and I_ALOS exists
    
    # check if layer_name exists in both grids
    
    # check if layer_name is np layer

    
    # get both layers 
    layer_asc= grid_asc.get(layer_name).flatten()
    layer_dsc= grid_dsc.get(layer_name).flatten()
    
    # assign empyte outpu
    layer_east=np.full_like(layer_asc,np.nan)
    layer_vert=np.full_like(layer_asc,np.nan)

    
    AZ_asc=grid_asc.get('LOS_Az').flatten()/180*np.pi
    IN_asc=grid_asc.get('LOS_In').flatten()/180*np.pi
    AZ_dsc=grid_dsc.get('LOS_Az').flatten()/180*np.pi
    IN_dsc=grid_dsc.get('LOS_In').flatten()/180*np.pi   
    
        #for each pixel   
    for i in range(0, len(AZ_asc)-1):   
        # check for nan
        if np.isnan( AZ_asc[i]) or np.isnan( AZ_dsc[i]):
            continue
        ''' this needs to be rethought since I only implemented a approximation 
            as in https://www.sciencedirect.com/science/article/pii/S0377027305003070?via%3Dihub
        '''
        # build A matrix
        # A=np.array([[-np.cos( IN_asc[i]), np.sin( IN_asc[i])*np.cos( AZ_asc[i]) ],
        #             [-np.cos( IN_dsc[i]), np.sin( IN_dsc[i])*np.cos( AZ_dsc[i]) ]] )
        # # build observations
        # b=np.array([layer_asc[i],layer_dsc[i]])
        # x = np.matmul(A, b)
        
        # layer_vert[i]= x[0]      
        # layer_east[i]= x[1]
        
        layer_vert[i]= (layer_dsc[i]+layer_asc[i])/(2*np.sin( IN_asc[i]))    
        layer_east[i]= (layer_dsc[i]-layer_asc[i])/(2*np.cos( IN_asc[i]))
        
        # print('-------------')        
        # print('AZ_dsc=',AZ_dsc[i])
        # print('AZ_asc=',AZ_asc[i])
        # print('IN_dsc=',IN_dsc[i])
        # print('IN_asc=',IN_asc[i])
        # print('A=',A)

        # print('x=',x)
        # print('b=',b)
        # print('layer_east[i]=',layer_east[i])
        # print('layer_vert[i]=',layer_vert[i])
        
         
        
        # to vert and horzreshape  
         #"assign to final output"
        grid_asc.update( {layer_name+'_vert': layer_vert.reshape(grid_asc.get(layer_name).shape)} )
        grid_asc.update( {layer_name+'_east': layer_east.reshape(grid_asc.get(layer_name).shape)} )
        
        grid_dsc.update( {layer_name+'_vert': layer_vert.reshape(grid_dsc.get(layer_name).shape)} )
        grid_dsc.update( {layer_name+'_east': layer_east.reshape(grid_dsc.get(layer_name).shape)} )

        

    
    
    return grid_asc, grid_dsc

"""
getAcquisitionTime description:
   
Parameters: 
    :
    grid: orbit (output dict from shape2grid)
    

    output
    grid: with dict field AcquisitionTime
    AcquisitionTime:  DateStrigns, JulianDays, DatesDateTimes
    
    edit: 27.2.2020 Philipp Schneider ifp
"""    
  
def getAcquisitionTime(grid):
    from datetime import datetime
    from  jdcal import gcal2jd
    # get all D_*values
    DateStrigns=[key for key in grid.keys() if 'D_' in key[0:2]]
    
    # convert all D_*values to datetime
    DatesDateTimes=[datetime.strptime(DateStr[2:],'%Y%m%d') for DateStr in DateStrigns]
    
    # convert all datetime to julian day 
    JulianDays=[gcal2jd(DatesDateTime.year,DatesDateTime.month,DatesDateTime.day)[1] for DatesDateTime in DatesDateTimes]
    
    AcquisitionTime={'DateStrigns': DateStrigns,
                     'JulianDays' : JulianDays,
                     'DatesDateTimes': DatesDateTimes
                     }
    grid.update({'AcquisitionTime': AcquisitionTime})
    
    return grid
    
"""
plotAcquisitionTimeline description:
   
Parameters: 
 input:
    grid: orbit (output dict from shape2grid)
            WITH AcquisitionTime from  getAcquisitionTime
    ylabel: i.e name of the orbit
    title : i.e. place
    
    
    edit: 27.2.2020 Philipp Schneider, ifp
"""     


def plotAcquisitionTimeline(grid,title='AcquisitionTime',ylabel='Data'):
    import matplotlib.pyplot as plt
    import numpy as np
    
    grid.get('AcquisitionTime').get('JulianDays')
    dates=grid.get('AcquisitionTime').get('DatesDateTimes');
    
    plt.plot_date(dates,np.full_like(grid.get('AcquisitionTime').get('JulianDays'),1),'ro')
    plt.yticks([], [])
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

"""
showDeformationHistory description:
   draws def history
Parameters: 
 input:
    grid: orbit (output dict from shape2grid)
            WITH AcquisitionTime from  getAcquisitionTime
   
    
    
    edit: 27.2.2020 Philipp Schneider, ifp
""" 
def showDeformationHistory(grid,base_path):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.widgets import Cursor
    
    # display on basemap
    
    fig, ax=dispGrid(grid,layer_name='Velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))
    
    # wait for click
    cursor = Cursor(ax, useblit=True, color='black', linewidth=1)
    X=np.array(plt.ginput(1)).flatten() 
    plt.plot(X[0],X[1],'r+')
    plt.show()

    
    
    # get pixel coordinates from lat lon
    fig2, ax2 = plt.subplots()
    col= int(np.round((X[0] - grid.get('info').get('geoTransform')[0])/grid.get('info').get('geoTransform')[1]))
    row= int(np.round((X[1] - grid.get('info').get('geoTransform')[3])/grid.get('info').get('geoTransform')[5]))
    
    # get all values for all D_ maps
    D=[grid.get(dateString)[row][col] for dateString in grid.get('AcquisitionTime').get('DateStrigns')]   
     
    # get times
    grid.get('AcquisitionTime').get('JulianDays')
    dates=grid.get('AcquisitionTime').get('DatesDateTimes');
    
    # plot
    plt.plot_date(dates,D)
    plt.show()
    
    plt.plot_date(dates,D,'r-o')
    plt.ylabel('Deformation [mm]')
    plt.title('Deformation History')
    plt.grid(True)
    plt.show()
	
    # in case of interpolated data
    # check if original existst 
    if "orgAcquisitionTime" in grid:
        # get pixel coordinates from lat lon
        fig3, ax3 = plt.subplots()
        col= int(np.round((X[0] - grid.get('info').get('geoTransform')[0])/grid.get('info').get('geoTransform')[1]))
        row= int(np.round((X[1] - grid.get('info').get('geoTransform')[3])/grid.get('info').get('geoTransform')[5]))
        
        # get all values for all D_ maps
        D=[grid.get('org'+dateString)[row][col] for dateString in grid.get('orgAcquisitionTime').get('DateStrigns')]   
         
        # get times
        grid.get('orgAcquisitionTime').get('JulianDays')
        dates=grid.get('orgAcquisitionTime').get('DatesDateTimes');
        
        # plot
        plt.plot_date(dates,D)
        plt.show()
        
        plt.plot_date(dates,D,'r-o')
        plt.ylabel('Deformation [mm]')
        plt.title('Original Deformation History')
        plt.grid(True)
        plt.show()  

    
#Function to convert Data Frame to GeoDataFrame,It is really handy! @Mohseniaref 2020.3.5 
def dt2gd(dataFrame):
    import pandas as pd
    import geopandas
    import matplotlib.pyplot as plt
    gdf = geopandas.GeoDataFrame(dataFrame, geometry=geopandas.points_from_xy(dataFrame.X, dataFrame.Y))
    gdf.crs=dataFrame.crs
 #  gdf.plot(color='red')
 #   plt.show()
    return gdf
#Function to create standard PS geodataframe from original PS data from SARSCAPE,same done with SBAS  
def ps_dformat(dataFrame):
    import pandas as pd
    import geopandas
    f1=dataFrame[['X','Y','Velocity','LOS_In','LOS_Az']]
    f2=dataFrame.iloc[:,18:]
    result =pd.concat([f1, f2], axis=1)
    result.crs=dataFrame.crs
    return result
 
  
        
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

def interpolateTemporal(grid,  timeStart ,  timeEnd ,  timeStepDays , kind ='linear'):
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
    grid=getAcquisitionTime(grid)
    
        
    return grid    

#Function to create standard SBAS geodataframe from original SBAS data from SARSCAPE

def sbas_dformat(dataFrame):
    import pandas as pd
    import geopandas
    dfv=dataFrame[['xpos','ypos','velocity','ILOS','ALOS']].copy()
    f1=dfv.rename(columns={'xpos':'X','ypos':'Y','velocity':'Velocity','ILOS':'LOS_In','ALOS':'LOS_Az'})
    f2=dataFrame.iloc[:,:-9]
    f2=f2.iloc[:,10:]
    result =pd.concat([f1, f2], axis=1)
    result.crs=dataFrame.crs
    result=dt2gd(result)
    return result
	
	
#Griding all data and save them in single shape file
def s2grid(dataFrame,gridSize,LonMin=None,LonMax=None,LatMin=None,LatMax=None,method='linear'):
    from scipy.interpolate import griddata
    import numpy as np
    print("executing shape2grid:")
    #"Check for None inputs and Values"
    #PS: If max and min are choosen like this they might not fit together
    if LonMin==None:
       LonMin=min(dataFrame.X)
    if LonMax==None:
       LonMax=max(dataFrame.X)  
    if LatMin==None:
       LatMin=min(dataFrame.Y)
    if LatMax==None:
     LatMax=max(dataFrame.Y)  
    dataFrame=dropl(dataFrame)       
    x=np.arange(LonMin, LonMax, gridSize)
    y=np.arange(LatMin, LatMax, gridSize)
    grid = tuple(np.meshgrid(x,y))
    ind=grid[0].flatten().size
    shape=pandas.DataFrame(columns=dataFrame.columns,index=range(0,ind))
    shape.crs=dataFrame.crs
    shape.X=grid[0].flatten()
    shape.Y=grid[1].flatten()
    # create grid for Interpolation
    grid = tuple(np.meshgrid(x,y))
    # points as array
    points=np.vstack((np.array(dataFrame.X),np.array(dataFrame.Y))).T
    #Create mask to mask out to far interpolation results
    # Construct kd-tree, functionality copied from scipy.interpolate
    from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    from scipy.spatial import cKDTree
    tree = cKDTree(points)
    xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    dists, indexes = tree.query(xi)
    mask=dists > gridSize
    
    for i in  range(2,len(dataFrame.columns)):
        value=dataFrame.iloc[:,i]
        grid_z0 = griddata(points, value, tuple(grid), 'linear')
        #  mask missing values with NaNs
        grid_z0[mask] = np.nan
        shape.iloc[:,i]=grid_z0.flatten()
       
    print("Finished!")
    
    shape=shape.dropna()
    shape.crs=dataFrame.crs
    shape=dt2gd(shape)
    shape.index=pandas.RangeIndex(len(shape.index))
    return shape
