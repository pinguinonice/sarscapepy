# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:02:53 2020

@author: philipp
"""


from sarscapepy import shape2grid, read_file,interpolateTemporal,animateGrid,decomposeTwoOrbits,writeShape

# read file
#path_asc= input('Enter Shape file name please : ')
# PSI
path_asc= 'D:/Philipp/5-Projects/STINGS/Idrija/Idrija II/PS_S44A_II/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'
path_dsc= 'D:/Philipp/5-Projects/STINGS/Idrija/Idrija II/PS_S22D_II/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

# SBAS
path_asc= r'D:\Philipp\5-Projects\STINGS\Idrija\Idrija II\SB_S44A_III\SBAS_SBAS_processing\inversion\vector\SI_v50d0_h50d0_c0d6_VD_0.shp'
path_dsc= r'D:\Philipp\5-Projects\STINGS\Idrija\Idrija II\SB_S22D_II\SBAS_SBAS_processing\inversion\vector\SI_v50d0_h50d0_c0d6_VD_0.shp'

#read header and drop last coloumn!
asc=read_file(path_asc)
dsc=read_file(path_dsc)

# rename xpos and ypos field


#interpolate to grid
LonMin=14.0
LonMax=14.06
LatMin=45.98
LatMax=46.03

grid_asc=shape2grid(dataFrame=asc, values=None, gridSize=1/3600, LonMin=LonMin,LonMax=LonMax,LatMin=LatMin,LatMax=LatMax, method='linear')
grid_dsc=shape2grid(dataFrame=dsc, values=None, gridSize=1/3600, LonMin=LonMin,LonMax=LonMax,LatMin=LatMin,LatMax=LatMax, method='linear')


grid_asc, grid_dsc=decomposeTwoOrbits(grid_asc, grid_dsc, layer_name='velocity')


outpath='D:\\Philipp\\2-CodeProjects\\3-python\\sarscapepy\\output\\shapefiles\\test\\'
filename='outputSBAS.shp'
writeShape(grid_asc,grid_dsc,outpath,filename)    



