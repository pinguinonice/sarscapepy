#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:53:42 2020

@author: maref


Decomposition and Temporal resampling for data set
"""


import geopandas
import pandas as pd
import gdal
#import sarscapepy
from sarscapepy.others.sardef import read_file,headerinfo,v2point,cmd,dropl,crtcrd,sbas_dformat,dt2gd,save_gdb,ps_dformat,s2grid,d2grid,s2grid,d2grid,shapetr
import subprocess
import shlex

# read file
#filename= input('Enter Shape file name please : ')
# PSI
fileps1= '../example_data/PSI/asc/PSI_PS_60_0_VD.shp'
fileps2= '../example_data/PSI/dsc/PSI_PS_60_0_VD.shp'

# SBAS
filesbas1= '../example_data/SBAS/asc/SI_v50d0_h50d0_c0d6_VD_0.shp'
filesbas2= '../example_data/SBAS/dsc/SI_v50d0_h50d0_c0d6_VD_0.shp'

############################################################################################
#Reading file
sb1=read_file(filesbas1)
sb2=read_file(filesbas2)
#convert them into standard format
sb1a=sbas_dformat(sb1)
sb2a=sbas_dformat(sb2)
#Change coordinate system to Geographic WGS84
(sb1c,X2,Y2)=crtcrd(sb1a,'epsg:4326')
(sb2c,X2,Y2)=crtcrd(sb2a,'epsg:4326')
#Convert panda data frame to geopandaframe
sb1c=dt2gd(sb1c)
sb2c=dt2gd(sb2c)
save_gdb(sb1c,'sbas-descending.shp')
save_gdb(sb2c,'sbas-ascending.shp')
###############################################################################################
#Temporal and spatial Resampling 
(sb1sh,sb2sh)=shapetr(sb1c,sb2c)
save_gdb(sb1sh,'sbas-descending-temporalresampled.shp')
save_gdb(sb2sh,'sbas-ascending-temporalresampled.shp')
######################################################################################
#Decomposition Descending and Ascending 
(sbshapev,sbshapee)=d2grid(sb1sh,sb2sh,gridSize=0.00013888888,method='linear')
save_gdb(sbshapee,'sb-shapee.shp')
save_gdb(sbshapev,'sb-shapev.shp')
