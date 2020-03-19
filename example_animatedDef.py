# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:53:17 2020

@author: philipp
"""

from sarscapepy import shape2grid, dispGrid, read_file,interpolateTemporal,animateGrid

# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Idrija II/PS_S22D_II\PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

df = read_file(filename)


#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')

# temporal resample
timeStart = '20170101'
timeEnd ='20200101'
timeStepDays=30 #days
kind= 'cubic' #‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’
grid =interpolateTemporal(grid, timeStart, timeEnd, timeStepDays, kind =kind)


base_path="basemap/Idrija_14.tif"
out_path="output/animation2.gif"
clim=(-30,30)

animateGrid(grid,clim,out_path,base_path=base_path)




