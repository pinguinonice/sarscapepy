# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:59:10 2020

@author: philipp
"""

from sarscapepy import shape2grid,showDeformationHistory,read_file

# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

df = read_file(filename)

#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')

# show map, click point show def history
base_path="basemap/Idrija_14.tif"

# show map, click point show def history
showDeformationHistory(grid,base_path)

