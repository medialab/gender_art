import pymongo
import csv, re

def get_list_from_html(field):
    regex_item = re.compile('<li>(.*?)<\/li>', flags=re.S)
    tab = regex_item.split(field)
    new_tab = []
    for item in tab:
        if len(item) > 0 and 'ul>' not in item and item != '\n':
            new_tab.append(item)
    return new_tab

c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({'deposit_history':{'$exists':True}},{'deposit_history':1})

regex_place_time = re.compile(r'([0-9]{4}/[0-9]{2}/[0-9]{2}|\?//00) - (.*)', flags=re.S)

with open('deposit_list.csv', 'w') as f:
    df = csv.writer(f)
    for doc in cursor:
        for deposit in get_list_from_html(doc['deposit_history']):
            m = regex_place_time.match(deposit)
            #print(m)
            #if m is None:
            #    print(deposit)
            #
            df.writerow([deposit, m.group(1), m.group(2)])