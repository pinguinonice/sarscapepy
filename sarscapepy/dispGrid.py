# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:28:21 2020

@author: Philipp
"""

def dispGrid(grid,layer_name=None,base_path=None,fig=None, ax=None,clim=(-40,40)):
    """
    dispGrid description:
    Parameters:    
        grid: output dict from shape2grid
        layer_name : string with Layer name in grid
        base_path   : path to basemap (geotif lat,lon, i.e. SAS output) 
      
    """

    import numpy as np
    import georaster
    import matplotlib.pyplot as plt


    
    # load grid as georeferenced georaster
    layer = georaster.SingleBandRaster.from_array(grid.get(layer_name), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))
    
    
    
    # new plot if no plot is provided plot
    if fig==None or ax==None:
        fig, ax = plt.subplots()
        newplot=True
        
        
    ax.set_title(layer_name)
    # if basemap path is set
    if type(base_path) == str:
        # load basemap
        base = georaster.MultiBandRaster(base_path)
        ax.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)
    
    plot_grid=ax.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
    

    #check if there is more than one axes
    plot_grid.set_clim(clim[0],clim[1])  

    if len(plt.gcf().axes) < 2:
        cbar = fig.colorbar(plot_grid)


    # label axis
    plt.xlabel('Lon')
    plt.ylabel('Lat')
    
    # flip Lat axis
    if plt.ylim()[0]>plt.ylim()[1]:
        plt.ylim(plt.ylim()[::-1])
    
    plt.show()
    #fig.canvas.manager.window.raise_()
    return fig, ax
           
  