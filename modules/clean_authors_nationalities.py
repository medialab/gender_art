import pymongo
import sys
import csv
import json
import pandas as pd

authors = pd.read_csv("../authors_all2.csv", encoding='utf-8')

clean_nat = {}
with open( '../data/nationalities_mod_clean.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for r in reader:
        clean_nat[r[0]] = r[-1]

nat_clean = []
for x in authors['Nationality (original)']:
    if pd.isnull(x):
        nat_clean.append('')
    else:
        nat_clean.append(clean_nat[x])

authors["nationality_clean"] = pd.Series(nat_clean, index=authors.index)
authors.to_csv("../authors_all3.csv", encoding='utf-8')

print('Done')
