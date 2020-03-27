# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:32:06 2020

@author: Philipp
"""

def plotAcquisitionTimeline(grid,title='AcquisitionTime',ylabel='Data'):
    """
    plotAcquisitionTimeline description:
       
    Parameters: 
     input:
        grid: orbit (output dict from shape2grid)
                WITH AcquisitionTime from  getAcquisitionTime
        ylabel: i.e name of the orbit
        title : i.e. place
        
        
        edit: 27.2.2020 Philipp Schneider, ifp
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    grid.get('AcquisitionTime').get('JulianDays')
    dates=grid.get('AcquisitionTime').get('DatesDateTimes');
    
    plt.plot_date(dates,np.full_like(grid.get('AcquisitionTime').get('JulianDays'),1),'ro')
    plt.yticks([], [])
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()
