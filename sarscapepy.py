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
    
def dispGrid(grid,layer_name=None,base_path=None):
    

    import numpy as np
    import georaster
    import matplotlib.pyplot as plt


    
    # load grid as georeferenced georaster
    layer = georaster.SingleBandRaster.from_array(grid.get(layer_name), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))
    
    
    
    # plot
    fig, ax = plt.subplots()
    t = plt.title(layer_name)
    # if basemap path is set
    if type(base_path) == str:
        # load basemap
        base = georaster.MultiBandRaster(base_path)
        plt.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)
    
    plot_grid=plt.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
    
    # set coloraxis
    plt.clim(-20,20) 
    cbar = fig.colorbar(plot_grid)
    
    # label axis
    plt.xlabel('Lon')
    plt.ylabel('Lat')
    
    # flip Lat axis
    plt.ylim(plt.ylim()[::-1])
    plt.show()
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
    DateStrigns=[key for key in grid.keys() if 'D_' in key]
    
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
plotAcquisitionTimeline description:
   
Parameters: 
 input:
    grid: orbit (output dict from shape2grid)
            WITH AcquisitionTime from  getAcquisitionTime
    ylabel: i.e name of the orbit
    title : i.e. place
    
    
    edit: 27.2.2020 Philipp Schneider, ifp
""" 
def showDeformationHistory(grid):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.widgets import Cursor
    
    # display on basemap
    base_path="basemap/Idrija_14.tif"
    fig, ax=dispGrid(grid,layer_name='Velocity',base_path=base_path)
    
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
    
#Function to convert Data Frame to GeoDataFrame,It is really handy!
def dt2gd(dataFrame):
    import pandas as pd
    import geopandas
    import matplotlib.pyplot as plt
    gdf = geopandas.GeoDataFrame(dataFrame, geometry=geopandas.points_from_xy(dataFrame.X, dataFrame.Y))
    gdf.crs=dataFrame.crs
 #  gdf.plot(color='red')
 #   plt.show()
    return gdf

