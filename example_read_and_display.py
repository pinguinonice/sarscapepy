#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: pippo
"""

from sarscapepy import shape2grid, dispGrid, read_file

# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

df = read_file(filename)


#interpolate to grid
grid=shape2grid(dataFrame=df, values='Velocity', gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')


# display on basemap
base_path="basemap/Idrija_14.tif"

dispGrid(grid,layer_name='Velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))


