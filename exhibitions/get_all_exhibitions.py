import csv, sys, pymongo
import pandas as pd
sys.path.append('../modules')
from get_html_list import *

field_dict = {'expositions':1}
db = pymongo.MongoClient("localhost", 27017)["VideoMuseum"]
cursor = db.myproject.Artwork.find({}, field_dict)
all_artworks = db.Artwork.find({}, no_cursor_timeout = True)
n = all_artworks.count()
print("Number of artworks in database:", n)

res = pd.DataFrame(columns = ['Exhibitions', 'Artworks'])
i = 0

for doc in all_artworks:
    # print("ID:", doc["_id"])
    if i % 1000 == 0:
        print("Finding exhibitions in artworks", i,"to", min([i + 1000, n]))

    if "expositions" in doc:
        # print(doc["expositions"])
        for exhibition in doc["expositions"]:

            if exhibition in res['Exhibitions'].unique():
                plus = ' | ' + doc["_id"]
                res.ix[(res['Exhibitions'].isin([exhibition])), 'Artworks'] += plus

            else:
                tmp = pd.DataFrame({'Exhibitions':exhibition, 'Artworks':doc["_id"]}, index = [0])
                res = res.append(tmp, ignore_index = True)
    i += 1

all_artworks.close()
print("Done. Number of exhibitions found:", res.shape[0])
res.to_csv("all_exhibitions.csv", sep = ";")
