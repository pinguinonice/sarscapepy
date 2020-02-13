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
    Xmin,Xmax: X bounderies
    Ymin,Ymax: Y bounderies
    method  : interpolation methode for griddata() {‘linear’, ‘nearest’, ‘cubic’}
Output:
    dictionary with NumPy array of the interpolated values + mask    
"""
from scipy.interpolate import griddata
import numpy as np

def shape2grid(dataFrame,gridSize,values=None,Xmin=None,Xmax=None,Ymin=None,Ymax=None,method='linear'):
    print("executing shape2grid:")

    #"Check for None inputs and Values"
    #PS: If max and min are choosen like this they might not fit together
    if Xmin==None:
        Xmin=min(dataFrame.X)
    if Xmax==None:
        Xmax=max(dataFrame.X)  
    if Ymin==None:
        Ymin=min(dataFrame.Y)
    if Ymax==None:
        Ymax=max(dataFrame.Y)          
    
    #"Check if no value, if yes: unpack all"
    if values==None:
        none,values_temp=dataFrame.axes
        values=values_temp.values.tolist()
    elif type(values)==str:
        values=[values]
        
            
    
    # create grid for Interpolation
    x=np.arange(Xmin, Xmax, gridSize)
    y=np.arange(Ymin, Ymax, gridSize)
    
    grid = tuple(np.meshgrid(x,y))
    # points as array
    points=np.vstack((np.array(dataFrame.X),np.array(dataFrame.Y))).T
    
    
    
    #Create mask
    
    # Construct kd-tree, functionality copied from scipy.interpolate

    from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    from scipy.spatial import cKDTree

    tree = cKDTree(points)
    xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    dists, indexes = tree.query(xi)
    mask=dists > gridSize
    
    #  save mask to output
    grid_out={'Mask':mask}
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
    
    
    
        
    
  