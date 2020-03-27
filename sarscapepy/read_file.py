# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:48:46 2020

@author: Philipp
"""

def read_file(filename):
    """
    Created on Wed Mar 25 11:48:46 2020
    
    @author: Philipp
    """
    import geopandas
    df = geopandas.read_file(filename)
    df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
    return df