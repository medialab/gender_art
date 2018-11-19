import pymongo, csv, sys, re

def get_list_from_html(field):
    regex_item = re.compile('<li>(.*?)<\/li>', flags=re.S)
    tab = regex_item.split(field)
    new_tab = []
    for item in tab:
        if len(item) > 0 and 'ul>' not in item and item != '\n':
            new_tab.append(item)
    return new_tab

if len(sys.argv) < 3:
    sys.exit('USAGE : '+sys.arg[0]+' [srcCSV] [networkCSV]')

#id, ens id, authors_list, title_notice, ch brut, 2xmd5, end, start
exhib_dict = {}
with open(sys.argv[1], 'r') as f:
    sc = csv.reader(f)
    for record in sc:
        if record[2] not in exhib_dict:
            exhib_dict[record[2]] = []
        exhib_dict[record[2]].append([record[0], record[1], record[7], record[11]])
print(exhib_dict)
c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({'expositions':{'$exists':True}},{'expositions':1, 'ensemble_id':1, 'title_list':1, 'authors_list':1})
g = open(sys.argv[2], 'w')
dc = csv.writer(g)
dc.writerow(['Artwork id', 'Ensemble id', 'Author', 'Title', 'Exhibition (champs brut)', 'raw_md5', 'uniq_md5', 'start date', 'end date'])
for doc in cursor:
    for art_exhibition in get_list_from_html(doc['expositions']):
        if art_exhibition not in exhib_dict:
            print('Pb:    ', art_exhibition)
        else:
            for record in exhib_dict[art_exhibition]:
                dc.writerow([doc['_id'], doc['ensemble_id'] if 'ensemble_id' in doc else '', doc['authors_list'], doc['title_list'], art_exhibition]+record)