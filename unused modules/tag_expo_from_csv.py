import sys
import pymongo
import csv
from merge_quantiquali_csv import *
from ope_fields import *

if len(sys.argv) < 3:
    print('USAGE : '+sys.argv[0]+' [expositionsCSV] [destCSV]')

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
    folder_list = {'M20':(('230E','241E', '240E', '210E', '302'), ('221I', '221E','242E','240E'), ('240E',)), 'M32':(('230E','241E', '240E', '210E', '302'), ('221I','242E','240E'), ('240E',))}#, 'M22':('230E', '221I'), 'M25':('230E', '221I'), 'M29':('230E', '221I'), 'M30':('230E', '221I'), 'M32':('230E', '221I'), 'M36':('230E', '221I'), 'M99':('230E', '221I')}#, 'M34':('212I', '213I')
    expo_dict = {}
    srcCSV = csv.reader(f)
    destCSV = csv.writer(g)
    c = pymongo.MongoClient()
    ope_info = {}
    for num_line, record in enumerate(srcCSV):
        if not num_line:
            destCSV.writerow(record+['Categorie'])
        else:
            if record[0] not in expo_dict:# or expo_dict[record[0]] == '???': in case we have higher precision after
                doc = c.myproject.Artwork.find_one({"$text":{"$search":'"'+record[0]+'"'}, "all_realized_operations_history":{"$exists":"true"}, "title_notice":{"$exists":"true"}},{"all_realized_operations_history":1, "title_notice":1})
                if doc is None:
                    expo_dict[record[0]] = 'None'
                else:
                    print(doc["title_notice"], record[0])
                    #cursor = c.myproject.Artwork.find_one()
                    #for doc in cursor:
                    #    if "all_realized_operations_history" in doc:
                    #print(doc["all_realized_operations_history"])
                    folder_gotcha = False
                    for folder, anchor_ope in folder_list.items():
                        try:
                            ope_info[folder] = get_from_operation_expo_heuristic_range(doc["all_realized_operations_history"], anchor_ope[0], anchor_ope[1], anchor_ope[2], folder, 1989, 1)
                        except:
                            print(doc['_id'], doc['title_notice'], folder)
                            raise                
                        #print(ope_info[folder], folder)
                        rslt = tag_one_expo_with_folder(record[0], ope_info, expo_title = record[1], start_date_expo = record[6], end_date_expo = record[7])
                        if rslt != []:
                        #print(rslt)
                            expo_dict[record[0]] = rslt[0][0]
                            folder_gotcha = True
                    if not folder_gotcha:
                        expo_dict[record[0]] = '???'
            destCSV.writerow(record+[expo_dict[record[0]]])
#cursor = c.myproject.Artwork.find