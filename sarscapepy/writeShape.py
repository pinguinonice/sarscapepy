# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:34:51 2020

@author: Philipp
"""

def writeShape(grid_asc,grid_dsc,outpath,filename):
    """
    writeShape description:
    writes values to shapefile 
    Parameters: 
    input:
    grid_asc/dsc: orbit (output dict from shape2grid)
            after decomposeTwoOrbits
    
    outputpath: path to the gif. i.e. D:\\Philipp\\2-CodeProjects\\3-python\\sarscapepy\\output\\shapefiles\\test\\
    filename: output filename i.e. output.shp
   
    output: will save a gif as defined in outpath
        
    edit: 25.3.2020 Philipp Schneider, ifp
    """ 
    import numpy as np    
    import shapefile as shp
    
    # shape writer
    w = shp.Writer(outpath+filename, shp.POINT)
    w.autoBalance = 1 #ensures gemoetry and attributes match
    
    # define fields max length of name = 10 characters
    w.field('Vel_vert',"F",10,10)
    w.field('Vel_east',"F",10,10)
    w.field('Vel_asc',"F",10,10)
    w.field('Vel_dsc',"F",10,10)
    
    # for each pixel 
    for i in range(0,np.prod(grid_asc.get('velocity_vert').shape)-1):
        
        # check if masked value
        if grid_asc.get('mask').flatten()[i]:
            continue
        # create point based on lat lon fields
        lat=grid_asc.get('Lat').flatten()[i]
        lon=grid_asc.get('Lon').flatten()[i]
        w.point(lon,lat)
        
        
        # write all the records in each field created abve
        w.record(Vel_vert=grid_asc.get('velocity_vert').flatten()[i],
                 Vel_east=grid_asc.get('velocity_east').flatten()[i],
                 Vel_asc=grid_asc.get('velocity').flatten()[i], 
                 Vel_dsc=grid_dsc.get('velocity').flatten()[i] )
    
    
    # release file
    w.close()                               
    
    # for futer:
    # for key in grid_asc.keys():
#     if isinstance(grid_asc.get(key), (np.ndarray) ):
#         #print(key)
#         #print(type(grid_asc.get(key)))
#         if len(key)>10:
#             key=key[-11:-1]
            
#         w.field(key,"F",len(key),10)
# w.field(key,"F",len(key),10)
# w.point(49.32,32.22)
# for key in grid_asc.keys():
#      if isinstance(grid_asc.get(key), (np.ndarray) ):
#          if len(key)>10:
#             key=key[-11:-1]
#          w.record(**key=1)
#          print(key)
