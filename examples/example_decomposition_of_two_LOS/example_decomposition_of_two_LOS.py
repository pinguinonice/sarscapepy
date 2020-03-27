# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:18:27 2020

@author: philipp
"""

from sarscapepy import shape2grid, dispGrid,read_file, decomposeTwoOrbits

# read file
#path_asc= input('Enter Shape file name please : ')
# PSI
path_asc= '../example_data/PSI/asc/PSI_PS_60_0_VD.shp'
path_dsc= '../example_data/PSI/dsc/PSI_PS_60_0_VD.shp'

# SBAS
# path_asc= '../example_data/SBAS/asc/SI_v50d0_h50d0_c0d6_VD_0.shp'
# path_dsc= '../example_data/SBAS/dsc/SI_v50d0_h50d0_c0d6_VD_0.shp'

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


grid_asc, grid_dsc=decomposeTwoOrbits(grid_asc, grid_dsc, layer_name='velocity')

# display on basemap
base_path="../example_data/basemap/Idrija_14.tif"

dispGrid(grid_asc,layer_name='velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))
dispGrid(grid_dsc,layer_name='velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))
dispGrid(grid_asc,layer_name='velocity_vert',base_path=base_path,fig=None, ax=None,clim=(-20,20))
dispGrid(grid_asc,layer_name='velocity_east',base_path=base_path,fig=None, ax=None,clim=(-20,20))