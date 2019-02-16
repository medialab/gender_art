import sys, csv
sys.path.append('../modules')
import pymongo
from ope_fields import *
from melt_ope_expo import *
from get_html_list import *

#if len(sys.argv) < 3:
if len(sys.argv) < 2:
    sys.exit('Nope')

start_tuple = ('212I',)
end_tuple = ('213I',)
category = 'I20'
m34_dict = {} 
g = open(sys.argv[1], 'w')
#f = open(sys.argv[1], 'r')
#sc = csv.reader(f)
dc = csv.writer(g)
#for record in sc:
#    if record[-1] == '1':
#        m34_dict[record[1]] = [record[-3], record[-2]]
#        dc.writerow([record[1], record[-3], record[-2], 'M34'])
find_dict = {"all_realized_operations_history":{"$exists":True}}
field_dict = {"all_realized_operations_history":1, "hanging_history_m34":1, 'exposition_out_of_folder':1}#, "hanging_history":1, "expositions_without_current":1, "expositions":1}
c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({},field_dict)
for doc in cursor:
    if "all_realized_operations_history" in doc:
        ranges = get_from_operation_expo_heuristic_range(get_list_from_html(doc["all_realized_operations_history"]), start_tuple, end_tuple, [], 'I20', 1995, 1)
        for key, value in ranges.items():
            for single_heuristic_date in value:
                dc.writerow([key, single_heuristic_date[0].replace('/', '-'), single_heuristic_date[1].replace('/', '-'),'I20'])
        #for key, value in ranges.items():
        #    for single_heuristic_date in value:
        #        if single_heuristic_date[0] == '' or single_heuristic_date[1] == '...':
        #            print(doc['_id'])
        #        else:
        #            if key in m34_dict:
        #                if int(single_heuristic_date[0].split('/')[0]) > int(m34_dict[key][1].split('-')[0]) or int(single_heuristic_date[1].split('/')[0]) < int(m34_dict[key][0].split('-')[0]):
        #                #if single_heuristic_date[0].split('/')[0] != m34_dict[key][0].split('-')[0] and (int(single_heuristic_date[1].split('/')[0]) <= int(m34_dict[key][1].split('-')[0]) and):
        #                    dc.writerow([key] + single_heuristic_date + ['I20'])
        #                    m34_dict[key].append(single_heuristic_date)
        #            else:
        #                dc.writerow([key, single_heuristic_date[0].replace('/', '-'), single_heuristic_date[1].replace('/', '-'),'I20'])
        #                m34_dict[key] = [single_heuristic_date]