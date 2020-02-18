#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: maref
"""



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
        
        print("Interpolate: " + value)
        grid_z0 = griddata(points, dataFrame[value], tuple(grid), method)
        #  mask missing values with NaNs
        grid_z0[mask] = np.nan
        
        #"assign to final output"
        grid_out.update( {value: grid_z0} )
    
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
           
    
  
