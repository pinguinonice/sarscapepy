# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:30:34 2020

@author: Philipp
"""

def decomposeTwoOrbits(grid_asc, grid_dsc, layer_name):
    """
    decomposeTwoOrbits description:
        following:  https://www.sciencedirect.com/science/article/pii/S0377027305003070?via%3Dihub
    Parameters: 
        input:
        grid_asc: orbit1 (output dict from shape2grid)
        grid_dsc: orbit2 (output dict from shape2grid)
    
        output
        grid_vert: vertical grid (up down) horizonata
        grid_horz: horizontal grid (east west)
    """
    import numpy as np
    
    # check input
    # assert len(grid_asc)==len(grid_dsc), 'dicts (grids) have different length' # error for wrong input
    
    # check if A_LOS and I_ALOS exists
    
    # check if layer_name exists in both grids
    
    # check if layer_name is np layer

    
    # get both layers 
    layer_asc= grid_asc.get(layer_name).flatten()
    layer_dsc= grid_dsc.get(layer_name).flatten()
    
    # assign empyte outpu
    layer_east=np.full_like(layer_asc,np.nan)
    layer_vert=np.full_like(layer_asc,np.nan)

    try:
        AZ_asc=grid_asc.get('LOS_Az').flatten()/180*np.pi
        IN_asc=grid_asc.get('LOS_In').flatten()/180*np.pi
        AZ_dsc=grid_dsc.get('LOS_Az').flatten()/180*np.pi
        IN_dsc=grid_dsc.get('LOS_In').flatten()/180*np.pi 
    except:    
        AZ_asc=grid_asc.get('ALOS').flatten()/180*np.pi
        IN_asc=grid_asc.get('ILOS').flatten()/180*np.pi
        AZ_dsc=grid_dsc.get('ALOS').flatten()/180*np.pi
        IN_dsc=grid_dsc.get('ILOS').flatten()/180*np.pi 
        
        
        
        #for each pixel   
    for i in range(0, len(AZ_asc)-1):   
        # check for nan
        if np.isnan( AZ_asc[i]) or np.isnan( AZ_dsc[i]):
            continue
        ''' this needs to be rethought since I only implemented a approximation 
            as in https://www.sciencedirect.com/science/article/pii/S0377027305003070?via%3Dihub
        '''
        # build A matrix
        # A=np.array([[-np.cos( IN_asc[i]), np.sin( IN_asc[i])*np.cos( AZ_asc[i]) ],
        #             [-np.cos( IN_dsc[i]), np.sin( IN_dsc[i])*np.cos( AZ_dsc[i]) ]] )
        # # build observations
        # b=np.array([layer_asc[i],layer_dsc[i]])
        # x = np.matmul(A, b)
        
        # layer_vert[i]= x[0]      
        # layer_east[i]= x[1]
        
        layer_vert[i]= (layer_dsc[i]+layer_asc[i])/(2*np.sin( IN_asc[i]))    
        layer_east[i]= (layer_dsc[i]-layer_asc[i])/(2*np.cos( IN_asc[i]))
        
        # print('-------------')        
        # print('AZ_dsc=',AZ_dsc[i])
        # print('AZ_asc=',AZ_asc[i])
        # print('IN_dsc=',IN_dsc[i])
        # print('IN_asc=',IN_asc[i])
        # print('A=',A)

        # print('x=',x)
        # print('b=',b)
        # print('layer_east[i]=',layer_east[i])
        # print('layer_vert[i]=',layer_vert[i])
        
         
        
        # to vert and horzreshape  
         #"assign to final output"
        grid_asc.update( {layer_name+'_vert': layer_vert.reshape(grid_asc.get(layer_name).shape)} )
        grid_asc.update( {layer_name+'_east': layer_east.reshape(grid_asc.get(layer_name).shape)} )
        
        grid_dsc.update( {layer_name+'_vert': layer_vert.reshape(grid_dsc.get(layer_name).shape)} )
        grid_dsc.update( {layer_name+'_east': layer_east.reshape(grid_dsc.get(layer_name).shape)} )

        

    
    
    return grid_asc, grid_dsc

 