# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 12:13:51 2018

@author: ruta binkyte
"""

import pymongo
import pandas as pd
import csv

db = pymongo.MongoClient("localhost", 27017)["VideoMuseum"]

project = {

    'ensemble_id':1,
    'acquisition_mode':1,
}

# unique arworks
unique_artworks = db.Artwork.aggregate([
    {"$match": {"type":{'$in':['individual','nonseparable']}}},
    {"$project":project}
    ])
separable_artworks_groups = db.Artwork.aggregate([
    {"$match": {"type":{'$in':['separable']}}}, 
    {"$project":project}
    ])

u_art = list(unique_artworks)
s_art = list(separable_artworks_groups)     

#get acquisition modes from unique artworks list
u_acquisition_modes = []
for i in range(len(u_art)):
    
   mode = u_art[i]['acquisition_mode']
   u_acquisition_modes.append(mode)    

#get acquisition modes from series list, one for each series object
s_acquisition_modes = []
ensemble_id = []
for i in range(len(s_art)):
   id = s_art[i]['ensemble_id']
   #take only one object of series
   if id not in ensemble_id:
       ensemble_id.append(id)
       mode = s_art[i]['acquisition_mode']
       s_acquisition_modes.append(mode)   


acquisition_modes = s_acquisition_modes + u_acquisition_modes
acquisition_series = pd.Series(acquisition_modes)
value_counts = acquisition_series.value_counts()

df = value_counts.rename_axis('acquisition_mode').reset_index(name='frequency')

df.to_csv('acquisition_modes.csv', sep=',', encoding = 'utf-8-sig')
        
