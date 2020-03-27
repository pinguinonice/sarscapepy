# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:27:20 2020

@author: Philipp
"""

def shape2grid(dataFrame,gridSize,values=None,LonMin=None,LonMax=None,LatMin=None,LatMax=None,method='linear'):
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
    from scipy.interpolate import griddata
    import numpy as np
    import utm
    print("executing shape2grid:")
    # check if Lat and lon field exist
    
    try:
        dataFrame.Lon
    except AttributeError:
        print('No Lat,Lon field, assuming UTM33T')
    
        lat,lon=utm.to_latlon(dataFrame.xpos,dataFrame.ypos, 33, 'T')
        dataFrame['Lat']=lat
        dataFrame['Lon']=lon
    

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
    info.update({'init':'epsg:4326'})
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
    from sarscapepy import getAcquisitionTime 
    grid_out=getAcquisitionTime(grid_out)

    return grid_out
    

