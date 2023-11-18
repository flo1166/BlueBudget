# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 12:51:21 2023

@author: michi
"""

import os 
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

os.getcwd()
os.chdir('c:/users/michi/Desktop/HackaTUM/BlueBudget')

base_url = 'https://archive.sensor.community/'

# Lade die Hauptseite
main_page = requests.get(base_url)
main_soup = BeautifulSoup(main_page.content, 'html.parser')

# Finde alle Zeilen ('tr' Tags) mit Jahreslinks
year_rows = main_soup.find_all('tr')

# Filtere die Links für die Unterarchive der Jahre 2018 bis 2022
selected_year_archives = []

for row in year_rows:
    link = row.find('a', href=True)
    if link and link['href'].endswith('/') and link['href'][:-1].isdigit():
        year = link['href'][:-1]
        if 2018 <= int(year) <= 2022:
            selected_year_archives.append(base_url + link['href'])

print(selected_year_archives)

# Lade dataframe mit sensor_ids
sensor_ids = pd.read_excel('src/List_of_munich.xlsx')
sensor_ids = pd.DataFrame(data = sensor_ids)


sensor_ids['sensor_id'] = 'sensor_' + sensor_ids['sensor_id'].astype(str)

all_years_urls_df = pd.DataFrame(columns=['Year', 'URL'])

# Liste für die einzelnen DataFrames der Jahre
years_dataframes = []

# Iteriere über die URLs der ausgewählten Jahre
for year_url in selected_year_archives:
    year = year_url.split('/')[-2]  # Extrahiere das Jahr aus der URL
    
    year_page = requests.get(year_url)
    year_soup = BeautifulSoup(year_page.content, 'html.parser')
    
    # Finde alle Links zu den einzelnen Tagen für dieses Jahr
    day_links = year_soup.find_all('a', href=True)
    
    # Extrahiere die URLs der Tage und füge sie einem DataFrame hinzu
    year_urls = [{'Year': year, 'URL': base_url + day_link['href']} for day_link in day_links]
    years_dataframes.append(pd.DataFrame(year_urls))

# Verbinde alle DataFrames zu einem einzelnen DataFrame
all_years_urls_df = pd.concat(years_dataframes, ignore_index=True)

# Zeige den DataFrame mit allen URLs der Jahre
print(all_years_urls_df)

filtered_urls_df = all_years_urls_df[~all_years_urls_df['URL'].str.contains(r'https://archive.sensor.community/[^0-9]+$')]

# Zeige den neuen DataFrame ohne die URLs, die nicht mit einer Zahl enden
print(filtered_urls_df)

sensor_ids_series = sensor_ids['sensor_id']


def filter_sensor_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csv_links = soup.find_all('a', href=True)
    
    selected_csv_links = []
    for link in csv_links:
        for sensor_id in sensor_ids_series:
            if sensor_id in link['href']:
                selected_csv_links.append(link['href'])
    
    return {'Tag_URL': url, 'Sensor_URLs': selected_csv_links}

# Anwenden der Funktion auf jede URL im DataFrame
found_urls = filtered_urls_df['URL'].apply(filter_sensor_urls)


found_urls_df = pd.DataFrame(found_urls.tolist())


print(found_urls_df)



########################### 

temperature_munich = pd.read_excel('/src/temperature_data/meteostat_munich.xslx')
