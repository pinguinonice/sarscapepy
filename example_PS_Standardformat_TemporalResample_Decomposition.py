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
from sardef import read_file,headerinfo,v2point,cmd,dropl,crtcrd,sbas_dformat,dt2gd,save_gdb,ps_dformat,s2grid,d2grid,s2grid,d2grid,shapetr
import subprocess
import shlex

# read file
#filename= input('Enter Shape file name please : ')
fileps1= '/mnt/simorgh/Project_01/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'
fileps2='/mnt/simorgh/Project_01/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'
filesbas1='/mnt/simorgh/Project_01/Idrija/SB_S22D/SBAS_SBAS_processing/inversion/vector/SI_v50d0_h50d0_c0d6_0.shp'
filesbas2='/mnt/simorgh/Project_01/Idrija/SB_S44A_II/SBAS_SBAS_processing/inversion/vector/SI_v50d0_h50d0_c0d6_0.shp'

############################################################################################
#Reading file
ps1=read_file(fileps1)
ps2=read_file(fileps2)
#convert them into standard format
ps1a=ps_dformat(ps1)
ps2a=ps_dformat(ps2)
#Change coordinate system to Geographic WGS84
(ps1c,X2,Y2)=crtcrd(ps1a,'epsg:4326')
(ps2c,X2,Y2)=crtcrd(ps2a,'epsg:4326')
#Convert panda data frame to geopandaframe
save_gdb(ps1c,'ps-descending.shp')
save_gdb(ps2c,'ps-ascending.shp')
###############################################################################################
#Temporal and spatial Resampling 
(ps1sh,ps2sh)=shapetr(ps1c,ps2c)
######################################################################################
#Decomposition Descending and Ascending 
(ps_shapev,ps_shapee)=d2grid(ps1sh,ps2sh,gridSize=0.00013888888,method='linear')
save_gdb(ps_shapee,'ps-shapee.shp')
save_gdb(ps_shapev,'ps-shapev.shp')
