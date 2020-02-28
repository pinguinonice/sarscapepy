# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:16:35 2020

@author: philipp
"""

from sarscapepy import shape2grid,showDeformationHistory,read_file,interpolateTemporal

# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

df = read_file(filename)

#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')



timeStart = '20170101'
timeEnd ='20200101'
timeStepDays=1 #days
kind= 'cubic' #‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’
grid_inter =interpolateTemporal(grid, timeStart, timeEnd, timeStepDays, kind =kind)


base_path="basemap/Idrija_14.tif"


# show map, click point show interpolated and original def history
showDeformationHistory(grid_inter,base_path)


