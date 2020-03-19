# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:02:53 2020

@author: philipp
"""


from sarscapepy import shape2grid, read_file,interpolateTemporal,animateGrid,decomposeTwoOrbits

# read file
#path_asc= input('Enter Shape file name please : ')
path_asc= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'
path_dsc= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

#path_asc='D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'

#read header and drop last coloumn!
asc=read_file(path_asc)
dsc=read_file(path_dsc)

#interpolate to grid
LonMin=14.01
LonMax=14.05
LatMin=45.99
LatMax=46.02

grid_asc=shape2grid(dataFrame=asc, values=None, gridSize=1/3600, LonMin=LonMin,LonMax=LonMax,LatMin=LatMin,LatMax=LatMax, method='linear')
grid_dsc=shape2grid(dataFrame=dsc, values=None, gridSize=1/3600, LonMin=LonMin,LonMax=LonMax,LatMin=LatMin,LatMax=LatMax, method='linear')

# temporal resample
timeStart = '20180103'
timeEnd ='20190823'
timeStepDays=10 #days
kind= 'cubic' #‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’
grid_asc =interpolateTemporal(grid_asc, timeStart, timeEnd, timeStepDays, kind =kind)
grid_dsc =interpolateTemporal(grid_dsc, timeStart, timeEnd, timeStepDays, kind =kind)

# decompose all D_XXXXXX
suffix='_vert'
DateStrigns=[key for key in grid_asc.keys() if (('D_' in key) and (suffix not in key) and ('org' not in key)) ]

for DateStrign in DateStrigns:
    grid_asc, grid_dsc=decomposeTwoOrbits(grid_asc, grid_dsc, layer_name=DateStrign)

# animate and save vertical
base_path="basemap/Idrija_14.tif"
out_path="output/animation_vert.gif"
clim=(-30,30)

animateGrid(grid_asc,clim,out_path,base_path=base_path,suffix='_vert')


# animate and save horizontal
base_path="basemap/Idrija_14.tif"
out_path="output/animation_east.gif"
clim=(-30,30)

animateGrid(grid_asc,clim,out_path,base_path=base_path,suffix='_east')



