# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 10:28:05 2023

@author: Florian Korn
"""

import os
import re
import pandas as pd

os.chdir('C:/Eigene Dateien/HackaTumProjekt')

def reader_groundwater(directory):
    '''
    This reader adds all groundwater files togheter

    Parameters
    ----------
    directory : string
        Where to search for the groundwater files.

    Returns
    -------
    df : pd.DataFrame()
        with all groundwater data.

    '''
    df_names = os.listdir(directory)
    df_names = list(filter(re.compile(r"16*").match, df_names))
    df = pd.DataFrame()
    
    for i in df_names:    
        temp_df = pd.read_csv(directory + i, sep = ';', header = 6, decimal = ',', parse_dates=['Datum'])
        temp_df['messstation'] = i[:5]
        df = pd.concat([df, temp_df])
    return df

df_groundwater = reader_groundwater('src/groundwater/')

        