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

def helper_reader_river(directory, df_names, name):
    df = pd.DataFrame()
    for i in df_names:    
        temp_df = pd.read_csv(directory + i, sep = ';', header = 9, decimal = ',', parse_dates=['Datum'])
        df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
        df = df[['Datum', 'Mittelwert']]
    df = df.rename(columns = {'Mittelwert': name})
    return df

def reader_river(directory):
    df_names = os.listdir(directory)
    df_names_isar_abfluss = list(filter(re.compile(r"16005701_Abfluss*").match, df_names))
    df_names_isar_pegel = list(filter(re.compile(r"16005701_Pegel*").match, df_names))
    df_names_wuerm_abfluss = list(filter(re.compile(r"16665008_Abfluss*").match, df_names))
    df_names_wuerm_pegel = list(filter(re.compile(r"16665008_Pegel*").match, df_names))
    
    dfs = [df_names_isar_abfluss, df_names_isar_pegel, df_names_wuerm_abfluss, df_names_wuerm_pegel]
    df_columns = ['isar_abfluss', 'isar_pegel', 'wuerm_abfluss', 'wuerm_pegel']
    df = pd.DataFrame(columns = ['Datum'])
    for i,j in enumerate(dfs):
        temp_df = helper_reader_river(directory, j, df_columns[i])
        df = df.merge(temp_df, on = 'Datum', how = 'outer')
    return df
    
reader_river('src/river/')



        