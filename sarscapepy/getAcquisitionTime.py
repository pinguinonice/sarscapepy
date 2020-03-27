# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:31:36 2020

@author: Philipp
"""

def getAcquisitionTime(grid):
    """
    getAcquisitionTime description:
       
    Parameters: 
        :
        grid: orbit (output dict from shape2grid)
        
    
        output
        grid: with dict field AcquisitionTime
        AcquisitionTime:  DateStrigns, JulianDays, DatesDateTimes
        
        edit: 27.2.2020 Philipp Schneider ifp
    """ 
    from datetime import datetime
    from  jdcal import gcal2jd
    # get all D_*values
    DateStrigns=[key for key in grid.keys() if 'D_' in key[0:2]]
    
    # convert all D_*values to datetime
    DatesDateTimes=[datetime.strptime(DateStr[2:],'%Y%m%d') for DateStr in DateStrigns]
    
    # convert all datetime to julian day 
    JulianDays=[gcal2jd(DatesDateTime.year,DatesDateTime.month,DatesDateTime.day)[1] for DatesDateTime in DatesDateTimes]
    
    AcquisitionTime={'DateStrigns': DateStrigns,
                     'JulianDays' : JulianDays,
                     'DatesDateTimes': DatesDateTimes
                     }
    grid.update({'AcquisitionTime': AcquisitionTime})
    
    return grid