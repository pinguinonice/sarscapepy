# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:22:45 2020

@author: philipp
"""

from sarscapepy import shape2grid,read_file,getAcquisitionTime

filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

df = read_file(filename)


#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')

# create datetime field

grid=getAcquisitionTime(grid)