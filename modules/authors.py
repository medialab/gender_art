import pymongo
import csvkit
import re
import cleaning
import pandas as pd

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
'artworks':'ID artworks',
'average_year': 'average_year',
'creation_years': 'artworks_creation_years'
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
authors = list(db.Author.aggregate([{"$project":project}]))

artwork_creation_date = {str(a['_id']):a['date_creation'] for a in db.Artwork.aggregate([{"$match":{'date_creation':{'$exists':'true'}}},
{"$project":{"date_creation":1}}])}

for author in authors:
    # cleaning acquisition mode
    if 'authors_birth_death' in author:
       author.update(cleaning.artist_birthdeath_parsing(author['authors_birth_death']))
       del author['authors_birth_death']
    try:
        years = [int(y) for id in author['artworks'] for y in cleaning.years_re.findall(artwork_creation_date[str(id)])]
    except KeyError as e :
        # no creation date could be retrieved
        years = []
    author['creation_years'] = '|'.join([str(y) for y in years])
    if 'birthYear' in author and author['birthYear']:
        years.append(int(author['birthYear']))
    if 'deathYear' in author and author['deathYear']:
        years.append(int(author['deathYear']))
    author['average_year'] = int(sum(years)/len(years)) if len(years)>0 else None

    author['artworks'] = '|'.join(author['artworks'])
    author['name.notice']= author["name"]["notice"]
    del author["name"]

df = pd.DataFrame(authors)
print(list(df.columns.values))
df.columns = [headers[c] for c in df.columns.values]
# print(list(headers.values()))
df = df[list(headers.values())]
df.to_csv("authors.csv", encoding = "utf-8", sep = ";", index = False)


# # Added encoding='utf-8' by ruta
# with open("authors.csv", "w", encoding='utf-8') as f:
#     authors_csv = csvkit.DictWriter(f,fieldnames = headers.values())
#     authors_csv.writeheader()
#     # setting human readable column names
#     authors_csv.writerows(( { headers[k]:v for k,v in author.items()} for author in authors))
