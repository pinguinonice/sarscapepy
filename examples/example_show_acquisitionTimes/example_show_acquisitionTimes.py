# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:22:45 2020

@author: philipp
"""

from sarscapepy import shape2grid,read_file,plotAcquisitionTimeline

filename= '../example_data/PSI/asc/PSI_PS_60_0_VD.shp'

df = read_file(filename)

#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')


# plot AcquisitionTime
plotAcquisitionTimeline(grid,title='AcquisitionTime',ylabel='Data')
