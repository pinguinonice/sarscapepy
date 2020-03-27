#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: pippo
"""
        
from sarscapepy import read_file,shape2grid
from sarscapepy import dispGrid

# read file
#filename= input('Enter Shape file name please : ')
filename= '../example_data/PSI/asc/PSI_PS_60_0_VD.shp'

df = read_file(filename)


#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')


# display on basemap
base_path="../example_data/basemap/Idrija_14.tif"

dispGrid(grid,layer_name='velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))


