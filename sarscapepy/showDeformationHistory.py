# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:32:43 2020

@author: Philipp
"""

def showDeformationHistory(grid,base_path):
    """
    showDeformationHistory description:
       draws def history
    Parameters: 
     input:
        grid: orbit (output dict from shape2grid)
                WITH AcquisitionTime from  getAcquisitionTime
       
        
        
        edit: 27.2.2020 Philipp Schneider, ifp
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.widgets import Cursor
    from sarscapepy import dispGrid
    
    # display on basemap
    
    fig, ax=dispGrid(grid,layer_name='velocity',base_path=base_path,fig=None, ax=None,clim=(-20,20))
    
    # wait for click
    cursor = Cursor(ax, useblit=True, color='black', linewidth=1)
    X=np.array(plt.ginput(1)).flatten() 
    plt.plot(X[0],X[1],'r+')
    plt.show()

    
    
    # get pixel coordinates from lat lon
    fig2, ax2 = plt.subplots()
    col= int(np.round((X[0] - grid.get('info').get('geoTransform')[0])/grid.get('info').get('geoTransform')[1]))
    row= int(np.round((X[1] - grid.get('info').get('geoTransform')[3])/grid.get('info').get('geoTransform')[5]))
    
    # get all values for all D_ maps
    D=[grid.get(dateString)[row][col] for dateString in grid.get('AcquisitionTime').get('DateStrigns')]   
     
    # get times
    grid.get('AcquisitionTime').get('JulianDays')
    dates=grid.get('AcquisitionTime').get('DatesDateTimes');
    
    # plot
    plt.plot_date(dates,D)
    plt.show()
    
    plt.plot_date(dates,D,'r-o')
    plt.ylabel('Deformation [mm]')
    plt.title('Deformation History')
    plt.grid(True)
    plt.show()
	
    # in case of interpolated data
    # check if original existst 
    if "orgAcquisitionTime" in grid:
        # get pixel coordinates from lat lon
        fig3, ax3 = plt.subplots()
        col= int(np.round((X[0] - grid.get('info').get('geoTransform')[0])/grid.get('info').get('geoTransform')[1]))
        row= int(np.round((X[1] - grid.get('info').get('geoTransform')[3])/grid.get('info').get('geoTransform')[5]))
        
        # get all values for all D_ maps
        D=[grid.get('org'+dateString)[row][col] for dateString in grid.get('orgAcquisitionTime').get('DateStrigns')]   
         
        # get times
        grid.get('orgAcquisitionTime').get('JulianDays')
        dates=grid.get('orgAcquisitionTime').get('DatesDateTimes');
        
        # plot
        plt.plot_date(dates,D)
        plt.show()
        
        plt.plot_date(dates,D,'r-o')
        plt.ylabel('Deformation [mm]')
        plt.title('Original Deformation History')
        plt.grid(True)
        plt.show()  
