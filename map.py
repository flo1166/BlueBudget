# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 11:57:48 2023

@author: Florian Korn
"""
import os
os.chdir('C:/Eigene Dateien/HackaTumProjekt')
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

plt.rcParams['figure.figsize'] = (20, 10)
df_municipalities = gpd.read_file('src/cityborders/municipalities.json')
mapping_groundwater = pd.read_csv('src/mapping/groundwater_mapping.csv', sep = ';')

def map_groundwater_to_municipalities(df_municipalities, mapping_groundwater):
    for l, i in enumerate(df_municipalities['geometry']):
        for j in range(len(mapping_groundwater['east'])):
            if i.contains(Point(mapping_groundwater.loc[j, 'east'], mapping_groundwater.loc[j, 'north'])):
                mapping_groundwater.loc[j, 'municipality'] = df_municipalities.loc[l, 'name']
    mapping_groundwater.to_csv('src/mapping/mapping_groundwater_complete.csv')
    return mapping_groundwater

mapping_groundwater = map_groundwater_to_municipalities(df_municipalities, mapping_groundwater)