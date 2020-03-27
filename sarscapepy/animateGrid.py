# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:34:14 2020

@author: Philipp
"""

def animateGrid(grid,clim,out_path,base_path=None,suffix=''):
    """
    animateGrid description:
       animateGrid (all D_XXXXXX) 
       Parameters: 
     input:
        grid: orbit (output dict from shape2grid)
                WITH AcquisitionTime from  getAcquisitionTime
        clim: min an max of colorbar. tuple like clim=(-50,50)
        output_path: path to the gif. i.e. output/animation.gif
        base_path: path to basemap
       
     output: will save a gif as defined in out_path
            
        edit: 17.3.2020 Philipp Schneider, ifp
    """
    import numpy as np
    import georaster
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.animation import PillowWriter
    
    DateStrigns=[key for key in grid.keys() if ('D_' in key) and (suffix in key) and ('org' not in key)]
        
    # new plot 
    fig, ax = plt.subplots()
            
    
    title = ax.text(0.5,1.05,DateStrigns[0], 
                        size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
    # if basemap path is set
    if type(base_path) == str:
        # load basemap
        base = georaster.MultiBandRaster(base_path)
        plot_base=plt.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)
    
    layer = georaster.SingleBandRaster.from_array(grid.get(DateStrigns[0]), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))   
    plot_grid=plt.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
    plot_grid.set_clim(clim[0],clim[1])  
    
    
    # Create colorbar
    cbar = plt.colorbar(plot_grid)
    cbar_ticks = np.linspace(clim[0],clim[1], num=6, endpoint=True)
    cbar.ax.set_autoscale_on(True)
    cbar.set_ticks(cbar_ticks)
    cbar.set_label('[mm]', labelpad=-40, y=1.05, rotation=0)
    
    # label axis
    plt.xlabel('Lon')
    plt.ylabel('Lat')
    
    # flip Lat axis
    if plt.ylim()[0]>plt.ylim()[1]:
       plt.ylim(plt.ylim()[::-1])
    
    
    #fig.canvas.manager.window.raise_()
    
    # frame grabbing  initialysed
    ims=[]
    ims.append([plot_grid,title])
    
    for DateString in DateStrigns[1:]:
        layer = georaster.SingleBandRaster.from_array(grid.get(DateString), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))   
        plot_grid=plt.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
        plot_grid.set_clim(clim[0],clim[1]) 
        
        cbar.set_clim(vmin=clim[0],vmax=clim[1])
        cbar.set_ticks(cbar_ticks)
        cbar.set_label('[mm]', labelpad=-40, y=1.05, rotation=0)

        cbar.draw_all() 
    
        
      
        
        title = ax.text(0.5,1.05,DateString, 
                        size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
        
        
        # grab frame
        ims.append([plot_grid,title])
    
    
    ani = animation.ArtistAnimation(fig, ims, interval=20, repeat_delay=0)
    
    writer = PillowWriter(fps=2)
    ani.save(out_path, writer=writer)
    print("Created animation in:"+out_path)
