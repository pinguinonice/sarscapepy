#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:48:20 2020

@author: maref
"""
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles
from cartopy.io.srtm import srtm_composite

from osgeo import gdal
from osgeo import gdal_array
import sys
import pandas
import argparse
def cmd(cmdi):
        import subprocess
        import shlex
        ps = subprocess.Popen(cmdi,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
#print(output)
        return output 
def read_file(filename):
    import geopandas
    df = geopandas.read_file(filename)
    return df
def dropl(gdata):
    dg=gdata.iloc[:,:-1]
    return dg
def headerinfo(dataFrame):
   import pandas as pd
   hdinfo=dataFrame.columns.tolist()
   tinfo=hdinfo[5:]
   tinfo = [tinfo.replace('D_','') for tinfo in tinfo ]
   tstring=pd.DataFrame(tinfo)
   ts=pd.to_datetime(tstring[0], format='%Y%m%d').dt.strftime("%Y-%m-%d")
   ts=pd.to_datetime(ts)
   return hdinfo,tinfo,ts

def v2point(dataFrame,variable):
    df2=dataFrame[['Lon','Lat',variable]]
    return df2 

def crtcrd(dataFrame,outProj):
    import pyproj
    import pandas as pd
    inProj=dataFrame.crs
    #dataFrame.to_crs({'init': 'epsg:4326'})
    dataFrame.to_crs(outProj)
    x2,y2 = pyproj.transform(inProj,outProj,dataFrame.X.to_list(),dataFrame.Y.to_list())
    X2=pd.DataFrame(x2,columns = ['X'])
    Y2=pd.DataFrame(y2,columns = ['Y'])
    dfc=dataFrame
    dfc['X']=X2
    dfc['Y']=Y2
    return dfc,X2,Y2
def dt2gd(dataFrame):
    import pandas as pd
    import geopandas
    import matplotlib.pyplot as plt
    gdf = geopandas.GeoDataFrame(dataFrame, geometry=geopandas.points_from_xy(dataFrame.X, dataFrame.Y))
    gdf.crs=dataFrame.crs
    gdf.plot(color='red')
    plt.show()
    return gdf
def save_gdb(dataFrame,file):
    import geopandas
    dataFrame.to_file(file)
    return

###########################################################################################################
def sbas_dformat(dataFrame):
    import pandas as pd
    import geopandas
    dfv=dataFrame[['xpos','ypos','velocity','ILOS','ALOS']].copy()
    f1=dfv.rename(columns={'xpos':'X','ypos':'Y','velocity':'Velocity','ILOS':'LOS_In','ALOS':'LOS_Az'})
    f2=dataFrame.iloc[:,:-9]
    f2=f2.iloc[:,10:]
    result =pd.concat([f1, f2], axis=1)
    result.crs=dataFrame.crs
    result=dt2gd(result)
    return result
def ps_dformat(dataFrame):
    import pandas as pd
    import geopandas
    f1=dataFrame[['X','Y','Velocity','LOS_In','LOS_Az']]
    f2=dataFrame.iloc[:,18:]
    result =pd.concat([f1, f2], axis=1)
    result.crs=dataFrame.crs
    return result
################################################################################################################
def s2grid(dataFrame,gridSize,LonMin=None,LonMax=None,LatMin=None,LatMax=None,method='linear'):
    from scipy.interpolate import griddata
    import numpy as np
    print("executing shape2grid:")
    #"Check for None inputs and Values"
    #PS: If max and min are choosen like this they might not fit together
    if LonMin==None:
       LonMin=min(dataFrame.X)
    if LonMax==None:
       LonMax=max(dataFrame.X)  
    if LatMin==None:
       LatMin=min(dataFrame.Y)
    if LatMax==None:
     LatMax=max(dataFrame.Y)   


    dataFrame=dropl(dataFrame)       
    x=np.arange(LonMin, LonMax, gridSize)
    y=np.arange(LatMin, LatMax, gridSize)
    grid = tuple(np.meshgrid(x,y))
    ind=grid[0].flatten().size
    shape=pandas.DataFrame(columns=dataFrame.columns,index=range(0,ind))
    shape.crs=dataFrame.crs
    shape.X=grid[0].flatten()
    shape.Y=grid[1].flatten()
    # create grid for Interpolation
    grid = tuple(np.meshgrid(x,y))
    # points as array
    points=np.vstack((np.array(dataFrame.X),np.array(dataFrame.Y))).T
    #Create mask to mask out to far interpolation results
    # Construct kd-tree, functionality copied from scipy.interpolate
    from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    from scipy.spatial import cKDTree
    tree = cKDTree(points)
    xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    dists, indexes = tree.query(xi)
    mask=dists > gridSize
    
    
    for i in  range(2,len(dataFrame.columns)):
        value=dataFrame.iloc[:,i]
        grid_z0 = griddata(points, value, tuple(grid), 'linear')
        #  mask missing values with NaNs
        grid_z0[mask] = np.nan
        shape.iloc[:,i]=grid_z0.flatten()
       
    print("Finished!")
    
    shape=shape.dropna()
    shape.crs=dataFrame.crs
    shape=dt2gd(shape)
    shape.index=pandas.RangeIndex(len(shape.index))
    return shape
def pmask(dataFrame,gridSize,grid):
    #Create mask to mask out to far interpolation results
    # Construct kd-tree, functionality copied from scipy.interpolate\
    from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    from scipy.spatial import cKDTree
    points=np.vstack((np.array(dataFrame.X),np.array(dataFrame.Y))).T
    tree = cKDTree(points)
    xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    dists, indexes = tree.query(xi)
    mask=dists > gridSize
    return points,mask
#####################################################################
def cshape(DataFrame,X,Y,Radius=0.001):
    import panda as pd
    da=DataFrame
    dl=dropl(da)
    df=da[(da.X<=X-Radius) &(da.X<=X+Radius) &(da.Y>=Y-Radius)&(da.Y>=Y+Radius)]
    dm=-1*df.mean(axis=0)
    dm.X=0
    dm.Y=0
    dm.LOS_In=0
    dm.LOS_Az=0
    od= pd.DataFrame([[1]*len(da.columns)],index=da.index,colums=da.columns)
    od=dropl(od)
    u2=od.mul(dm,axis=1)
    s1=dl.add(u2)
    return s1
#######################################################################################
def shapetr(DataFrame1,DataFrame2):
    import pandas as pd
    psc1=dropl(DataFrame1)
    psc2=dropl(DataFrame2)
    
    hdinfo1,tinfo1,ts1=headerinfo(dataFrame=psc1)
    hdinfo2,tinfo2,ts2=headerinfo(dataFrame=psc2)
    ###################################################################################
    psc1t=psc1.iloc[:,5:]
    psc1v=psc1.iloc[:,:5]
    psc1t=psc1t.transpose()
    p1t=psc1t.set_index(ts1)
    #p1t=psc1t.set_index(pd.DatetimeIndex(ts1))
    p1t.index.name='t'
    ###################################################################################
    psc2t=psc2.iloc[:,5:]
    psc2v=psc2.iloc[:,:5]
    psc2t=psc2t.transpose()
    p2t=psc2t.set_index(ts2)
    ####################################################################################
    # p2t=psc2t.set_index(pd.DatetimeIndex(ts2))
    p2t.index.name='t'
    p2tr=p2t.resample('D').mean().interpolate('linear')
    #####################################################################################
    p2tc=p2tr.iloc[p2tr.index.isin(p1t.index)]
    ######################################################################################
    p1tc=p1tc=p1t.loc[p1t.index.isin(p2tc.index)]
    
    #####################################################################################
    #Calibrate both of them and set deformation zero time zero!
    #Create 
    onedf1= pd.DataFrame([[1]*len(p1tc.columns)],index=p1tc.index)
    v1=-1*p1tc.iloc[:1,:]
    u1=onedf1*v1.values
    p1tr=p1tc+u1
    p1tr.index=p1tr.index.strftime('D_%Y%m%d')
    p1trt=p1tr.transpose()
    p1sh=pd.concat([psc1v, p1trt], axis=1)
    onedf2= pd.DataFrame([[1]*len(p2tc.columns)],index=p2tc.index)
    v2=-1*p2tc.iloc[:1,:]
    u2=onedf2*v2.values
    p2tr=p2tc+u2
    p2tr.index=p2tr.index.strftime('D_%Y%m%d')
    p2trt=p2tr.transpose()
    p2sh=pd.concat([psc2v, p2trt], axis=1)
    ########################################################################################
    p1sh=dt2gd(p1sh)
    p2sh=dt2gd(p2sh)
    
    return p1sh,p2sh
####################################################################################################################
def d2grid(dataFrame1,dataFrame2,gridSize,LonMin=None,LonMax=None,LatMin=None,LatMax=None,method='linear'):
    from scipy.interpolate import griddata
    import numpy as np
    import pandas
    print("executing shape2grid:")
    #"Check for None inputs and Values"
    #PS: If max and min are choosen like this they might not fit together
    if LonMin==None:
       LonMin=min(min(dataFrame1.X),min(dataFrame2.X))
    if LonMax==None:
       LonMax=max(max(dataFrame1.X),max(dataFrame2.X))  
    if LatMin==None:
       LatMin=min(min(dataFrame1.Y),min(dataFrame2.Y)) 
    if LatMax==None:
     LatMax=max(max(dataFrame1.Y),max(dataFrame2.Y))    
#0.000833333/3  is 0.000277777
    dataFrame1=dropl(dataFrame1)       
    x=np.arange(LonMin, LonMax, gridSize)
    y=np.arange(LatMin, LatMax, gridSize)
    grid = tuple(np.meshgrid(x,y))
    ind=grid[0].flatten().size
    shape=pandas.DataFrame(columns=dataFrame1.columns,index=range(0,ind))
    shape.crs=dataFrame1.crs
    shape.X=grid[0].flatten()
    shape.Y=grid[1].flatten()
    shapee=shape.copy()
    shapev=shape.copy()
    # create grid for Interpolation
    grid = tuple(np.meshgrid(x,y))
    # points as array
    # points=np.vstack((np.array(dataFrame.X),np.array(dataFrame.Y))).T
    # #Create mask to mask out to far interpolation results
    # # Construct kd-tree, functionality copied from scipy.interpolate
    # from scipy.interpolate.interpnd import _ndim_coords_from_arrays
    # from scipy.spatial import cKDTree
    # tree = cKDTree(points)
    # xi = _ndim_coords_from_arrays(tuple(grid), ndim=points.shape[1])
    # dists, indexes = tree.query(xi)
    # mask=dists > gridSize
    (points1,mask1)=pmask(dataFrame1,gridSize,grid)
    (points2,mask2)=pmask(dataFrame2,gridSize,grid)    
    mask=mask1&mask2
    inc1=(dataFrame1.iloc[:,3]).mean()
    az1=(dataFrame1.iloc[:,4]).mean()
    inc2=(dataFrame2.iloc[:,3]).mean()
    az2=(dataFrame2.iloc[:,4]).mean()
    inc1=np.deg2rad(inc1)
    az1=np.deg2rad(az1)
    inc2=np.deg2rad(inc2)
    az2=np.deg2rad(az2)
    inc2r=np.deg2rad(inc2)
    
    #  mask missing values with NaNs

    for i in  range(2,len(dataFrame1.columns)):
        if i==3 or i==4 :
           continue
        value1=dataFrame1.iloc[:,i]
        value2=dataFrame2.iloc[:,i]
        v1g = griddata(points1, value1, tuple(grid), 'linear')
        v2g = griddata(points2, value2, tuple(grid), 'linear')
        #  mask missing values with NaNs
        v1g[mask] = np.nan
        v2g[mask] = np.nan
        v1=v1g.flatten()
        v2=v2g.flatten()
        a=np.cos(inc1)
        b=np.cos((inc2))
        c=np.cos((np.pi/2)-inc1)
        d=np.cos((3*np.pi/2)-az1)
        e=np.cos((np.pi/2)-inc2)
        f=np.cos((3*np.pi/2)-az2)
        # g=np.cos(inc2)
        # h=
        # shapev.iloc[:,i]=(v1f+v2f)/2*np.sin(inc2r)
        # shapee.iloc[:,i]=(v1f-v2f)/2*np.np.cos(inc2r)
        shapee.iloc[:,i]=((v1/a)-(v2/b))/(((c*d)/a)-((e*f)/b))
        shapev.iloc[:,i]=((v1/c*d)-(v2/e*f))/((a/(c*d))-(b/(e*f)))
        # (((v1f/np.cos((np.pi/2)-inc1)*np.cos((3*np.pi/2)-az1))-(v2f/np.cos((np.pi/2)-inc2)*np.cos((3*np.pi/2)-az2)))/(((np.cos((inc1)/np.cos((np.pi/2)-inc1)*np.cos((3*np.pi/2)-az1))-(np.cos(inc2)))/(np.cos((np.pi/2)-inc2)*np.cos((3*np.pi/2)-az2)))) 
                                                                                                                                        
    #print("Finished!")
    shapee.drop(shapee.iloc[:,3:5], inplace = True, axis = 1)
    shapev.drop(shapev.iloc[:,3:5], inplace = True, axis = 1)
####################################################################    
    shapev=shapev.dropna()
    shapev.crs=dataFrame1.crs
    shapev=dt2gd(shapev)
    shapev.index=pandas.RangeIndex(len(shapev.index))
####################################################################
    shapee=shapee.dropna()
    shapee.crs=dataFrame2.crs
    shapee=dt2gd(shapee)
    shapee.index=pandas.RangeIndex(len(shapee.index))
    return shapev,shapee
