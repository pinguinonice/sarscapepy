# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:18:27 2020

@author: philipp
"""

from sarscapepy import shape2grid, dispGrid,read_file,headerinfo,v2point,point2grd, decomposeTwoOrbits

# read file
#path_asc= input('Enter Shape file name please : ')
path_asc= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'
path_dsc= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

#path_asc='D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'

#read header and drop last coloumn!
asc=read_file(path_asc)
dsc=read_file(path_dsc)

#interpolate to grid
LonMin=14.00
LonMax=14.06
LatMin=45.98
LatMax=46.04

grid_asc=shape2grid(dataFrame=asc, values=None, gridSize=1/3600, LonMin=LonMin,LonMax=LonMax,LatMin=LatMin,LatMax=LatMax, method='linear')
grid_dsc=shape2grid(dataFrame=dsc, values=None, gridSize=1/3600, LonMin=LonMin,LonMax=LonMax,LatMin=LatMin,LatMax=LatMax, method='linear')


grid_asc, grid_dsc=decomposeTwoOrbits(grid_asc, grid_dsc, layer_name='Velocity')

# display on basemap
base_path="basemap/Idrija_14.tif"

dispGrid(grid_asc,layer_name='Velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))
dispGrid(grid_dsc,layer_name='Velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))
dispGrid(grid_asc,layer_name='Velocity_vert',base_path=base_path,fig=None, ax=None,clim=(-20,20))
dispGrid(grid_asc,layer_name='Velocity_east',base_path=base_path,fig=None, ax=None,clim=(-20,20))