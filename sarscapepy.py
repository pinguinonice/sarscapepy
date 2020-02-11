#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: maref
"""
import gdal
import numpy as np
import geopandas
filename= input('Enter Shape file name please : ')
df = geopandas.read_file(filename)


def shape2grid(df,value,gridSize,Xmin,Xmanx,Ymin,Ymax,methode,fillValue):
    grid_x, grid_y = np.mgrid[Xmin:Xmanx:gridSize, Ymin:Ymax:gridSize]
    grid_z0 = griddata(df.X,df.Y, df[value], (grid_x, grid_y), method)
    
    
dg=shape2grid(df,,gridSize,Xmin,Xmanx,Ymin,Ymax,methode,fillValue)
        
    
ds = gdal.Grid(test, arry, format='GTiff',
               outputBounds=[0.0, 0.0, 100.0, 100.0],
               width=10, height=10, outputType=gdal.GDT_Float32,
               algorithm='invdist:power=2.0:smoothing=1.0',
               zfield='height')    