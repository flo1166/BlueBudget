# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:45:25 2023

@author: Florian Korn
"""
# imports
import os
os.chdir('C:/Eigene Dateien/HackaTumProjekt')
from file_reader import reader_groundwater, reader_river
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate, GridSearchCV
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
import datetime
from sklearn.metrics import r2_score
from mlxtend.feature_selection import SequentialFeatureSelector as sfs

# build data set
def load_data():
    df_groundwater = reader_groundwater('src/groundwater/')
    df_wheater = pd.read_excel("src/temperature_data/meteostat_export.xlsx", parse_dates=['date'])
    df_river = reader_river('src/river/')
    return df_groundwater, df_wheater, df_river

df_groundwater, df_wheater, df_river = load_data()

def plz_to_messstation(PLZ):
    mapping_plz_municipality = pd.read_excel('src/mapping/munich_postal_code.xlsx', index_col = 0, header = None)
    mapping_plz_municipality['combined'] = mapping_plz_municipality.values.tolist()
    municipality = mapping_plz_municipality[mapping_plz_municipality['combined'].map(lambda x:PLZ in x)].index.values[0]
    municipality_to_groundwater = pd.read_csv('src/mapping/municipality_to_groundwater.csv', sep = ',', index_col = 0)
    return str(int(municipality_to_groundwater[municipality_to_groundwater['name'] == municipality]['groundwater_ID'].values[0]))



def train_model(PLZ):
    messstation_filter = plz_to_messstation(PLZ)
    df_groundwater, df_wheater, df_river = load_data()
    df_ml = df_river.merge(df_wheater, left_on = 'Datum', right_on = 'date', how = 'outer').merge(df_groundwater[df_groundwater['messstation'].isin([messstation_filter])][['Datum', 'Grundwasserstand [m ü. NN]']], on = 'Datum', how = 'outer')
    df_ml = df_ml.drop(columns = 'date')
    df_ml = df_ml.set_index('Datum')
    df_ml = df_ml[df_ml.index >= datetime.datetime(2018, 1, 1, 0, 0)]
    df_ml['season'] = df_ml.index.month
    df_ml.dropna(subset=['Grundwasserstand [m ü. NN]'], inplace=True)
    num_attribs = df_ml.columns
    num_attribs = num_attribs.to_list()
    num_attribs = df_ml.columns.to_list()[:-1]
    
    imputer = make_column_transformer((SimpleImputer(strategy = 'constant', fill_value = 0, copy = False), ['prcp', 'snow', 'wdir']),
                                      remainder = 'passthrough',
                                      verbose_feature_names_out = False)
    
    imputer2 = make_column_transformer((SimpleImputer(strategy = 'mean', copy = False), ['tsun']),
                                      remainder = 'passthrough',
                                      verbose_feature_names_out = False)
    
    scaling = make_column_transformer((StandardScaler(), num_attribs),
                                      remainder = 'passthrough',
                                      verbose_feature_names_out = False)
    
    preprocessing = make_pipeline(imputer, imputer2, scaling).set_output(transform="pandas")
    
    # Train and Test set
    X_train, X_test, y_train, y_test = train_test_split(df_ml.iloc[:, :-1], 
                                                        df_ml.iloc[:, [-1]],
                                                        train_size = 0.7, 
                                                        random_state = 190,
                                                        shuffle=False)
    
    sequential_features = SequentialFeatureSelector(estimator = LinearRegression(),
                                                    n_features_to_select = 'auto',
                                                    direction  = 'forward',
                                                    scoring = 'r2',
                                                    n_jobs = -1)
    
    pipe_LR = make_pipeline(preprocessing,
                            sequential_features,
                            LinearRegression(n_jobs = -1)) # standardization needed because of lasso ridge regression (big coefficients -> strong punishment)
    
    pipe_LR = pipe_LR.fit(X_train, y_train)
    
    pipe_LR.score(X_test, y_test)
    
    #print(pipe_LR.steps[1][-1].get_feature_names_out(df_ml.iloc[:,:-1].columns))
    return make_pipeline(preprocessing,
                         sequential_features,
                         LinearRegression(n_jobs = -1)).fit(df_ml.iloc[:, :-1], df_ml.iloc[:, [-1]]), df_ml, preprocessing

def visualisation_groundwater(LR_model, df_ml, preprocessing, date):
    date = pd.to_datetime(date)
    df_ml = df_ml[df_ml.index < date]
    df_ml = df_ml.sort_index().iloc[-6:-1, :-2]
    pred = LR_model.predict(preprocessing.fit_transform(df_ml))

    data = [
        {'date': str(date), 'level': pred[4], 'type': 'Predicted'},
        {'date': str(date), 'level': pred[3], 'type': 'Predicted'},
        {'date': str(date), 'level': pred[2], 'type': 'Predicted'},
        {'date': str(date), 'level': pred[1], 'type': 'Predicted'},
        {'date': str(date), 'level': pred[0], 'type': 'Predicted'}
    ]

    return data


    


