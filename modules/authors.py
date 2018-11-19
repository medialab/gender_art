import pymongo
import csvkit
import re
import cleaning

db = pymongo.MongoClient("localhost", 27017)["VideoMuseum"]# changed to VideoMuseum by Ruta Binkyte

headers = {
'_id':'Id artist',
'name.notice':'name',
'name_complement':'name extended',
'type':'type',
'birthYear':'Birth year',
'deathYear':'Death year',
'birthCity':'Birth city',
'birthState':'Birth state',
'birthCountry':'Birth country',
'deathCity':'Death city',
'deathState':'Death state',
'deathCountry':'Death country',
'gender':'Gender',
'nationality':'Nationality (original)',
'artworks':'ID artworks'
}

project = {
    'type':1,
    'authors_birth_death':1,
    'name.notice':1,
    'name_complement':1,
    'gender':1,
    'nationality':1,
    'artworks':1
}

# unique arworks
authors = list(db.Author.aggregate([
    {"$project":project}
    ]))
for author in authors:
    # cleaning acquisition mode
    if 'authors_birth_death' in author:
        author.update(cleaning.artist_birthdeath_parsing(author['authors_birth_death']))
        del author['authors_birth_death']
    author['artworks'] = '|'.join(author['artworks'])
    author['name.notice']= author["name"]["notice"]
    del author["name"]

    # added encoding='utf-8' by ruta
with open("authors.csv", "w", encoding='utf-8') as f:
    authors_csv = csvkit.DictWriter(f,fieldnames = headers.values())
    authors_csv.writeheader()
    # setting human readable column names
    authors_csv.writerows(( { headers[k]:v for k,v in author.items()} for author in authors))