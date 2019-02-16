import pymongo, csv, sys
sys.path.append('../modules')
from get_html_list import *

if len(sys.argv) < 4:
    sys.exit(sys.argv[0]+' [srcCSV] [column number] [destCSV]')

#exhib_dict_info = {}
#exhib_dict_arwork
garbage_set = set()

c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({'exposition_out_of_folder':{'$exists':True}}, {'exposition_out_of_folder':1})
for doc in cursor:
    for garbage in get_list_from_html(doc['exposition_out_of_folder']):
        #if garbage not in garbage_set:
            garbage_set.add(garbage)
print(len(garbage_set))
with open(sys.argv[1], 'r') as f, open(sys.argv[3], 'w') as g:
    srcCSV = csv.reader(f)
    destCSV = csv.writer(g)
    for record in srcCSV:
        anchor_field = record[int(sys.argv[2])-1]
        if anchor_field not in garbage_set:
            destCSV.writerow(record)