#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: maref
"""



"""
shape2grid description:
    
"""
from scipy.interpolate import griddata
import numpy as np

def shape2grid(dataFrame,value,gridSize,Xmin=None,Xmax=None,Ymin=None,Ymax=None,method='linear',fillValue=np.nan):
    "Check for None inputs and Values"
    if Xmin==None:
        Xmin=min(dataFrame.X)
    if Xmax==None:
        Xmax=max(dataFrame.X)  
    if Ymin==None:
        Ymin=min(dataFrame.Y)
    if Ymax==None:
        Ymax=max(dataFrame.Y)          
    
    "Interpolate"
    x=np.arange(Xmin, Xmax, gridSize)
    y=np.arange(Ymin, Ymax, gridSize)
    
    grid = np.meshgrid(x,y)
    points=np.vstack((np.array(dataFrame.X),np.array(dataFrame.Y))).T
    
    grid_z0 = griddata(points, dataFrame[value], tuple(grid), method)
    
    "remove to far values"
    
    # Construct kd-tree, functionality copied from scipy.interpolate

    from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    from scipy.spatial import cKDTree

    tree = cKDTree(points)
    xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    dists, indexes = tree.query(xi)

    #  mask missing values with NaNs

    grid_z0[dists > gridSize] = np.nan
    
    
    return grid_z0
    
    
    
        
    
  