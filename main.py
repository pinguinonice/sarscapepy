#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: pippo
"""

import geopandas



from sarscapepy import shape2grid, dispGrid,read_file,headerinfo,v2point

# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'
#filename='D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'

#read header and drop last coloumn!
df=read_file(filename)
#extract header information and time series
hdinfo,tinfo,ts=headerinfo(dataFrame=df)
#interpolate to grid
grid=shape2grid(dataFrame=df, values='Velocity', gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')
#extract a variable with lat and Lon!
ds=v2point(df,'Velocity')
#save GeoTiff and interpolation!
point2grd(ds,"tr")


# display on basemap
base_path="basemap/Idrija_14.tif"

dispGrid(grid,layer_name='Velocity',base_path=base_path)
