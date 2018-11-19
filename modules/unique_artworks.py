import pymongo
import csvkit
import re
import cleaning

db = pymongo.MongoClient("localhost", 27017)["VideoMuseum"]

headers = {
'_id':'Id artwork',
'authors':'Id artists',
'title_notice':'Title',
'domain':'Domaine',
'acquisition_mode':'Mode acquisition (original)',
'new_acquisition_mode':'Mode acquisition (new categories)',
'acquisition':'Details acquisition (ex: name of leg)',
'acquisition_year':'Year acquisition',
'date_creation':'Date creation (original)',
'creation_year':'Year creation',
'acq_crea_diff':'Diff acquisition-creation in years'
}

project = {
    'authors':1,
    'title_notice':1,
    'domain':1,
    'acquisition_mode':1,
    'acquisition':1,
    'acquisition_year':1,
    'date_creation':1
}

# unique arworks
unique_artworks = db.Artwork.aggregate([
    {"$match": {"type":{'$in':['individual','nonseparable']}}},
    {"$project":project}
    ])
separable_artworks_groups = db.Artwork.aggregate([
    {"$match": {"type":'separable'}},
    {'$group': dict( [('_id','ensemble_id')] + [(k,{'$first':'$%s'%k}) for k,v in project.items()])},
    {"$project":project}
    ])


artworks = list(unique_artworks)+list(separable_artworks_groups)

for artwork in artworks:
    # cleaning acquisition mode
    artwork['new_acquisition_mode'] = cleaning.acquisition_mode_cleaning(artwork['acquisition_mode'])
    # creation date
    artwork['creation_year'] = cleaning.creation_date_cleaning(artwork['date_creation']) if 'date_creation' in artwork else ''
    try:
        artwork['acq_crea_diff'] = int(artwork['acquisition_year'])-int(artwork['creation_year'])
    except:
        artwork['acq_crea_diff'] = None
    artwork['authors'] = '|'.join(artwork['authors'])

#added 'utf-8' by Ruta Binkyte
with open("unique_artworks.csv", "w", encoding = 'utf-8' ) as f:
    artworks_csv = csvkit.DictWriter(f,fieldnames = headers.values())
    artworks_csv.writeheader()
    # setting human readable column names
    artworks_csv.writerows(( { headers[k]:v for k,v in artwork.items()} for artwork in artworks))