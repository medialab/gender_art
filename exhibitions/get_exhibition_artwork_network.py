import csv, sys, pymongo
sys.path.append('../modules')
from get_html_list import *

if len(sys.argv) < 3:
    sys.exit(sys.argv[0]+' [destNetworkCSV] [srcExhibitionCSV list] ')

field_dict = {'exposition_out_of_folder':1, 'expositions':1, "hanging_history_m34":1, "temporary_exhibitions_m30":1}
c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({}, field_dict)
exhib_info_dict = {}
exhib_artwork_network = {}
for i in range(len(sys.argv)-2):
    filename = sys.argv[i+2]
    print(filename)
    with open(filename) as f:
        srcCSV = csv.reader(f)
        focus_index = 2
        for record in srcCSV:
            exhib_info_dict[record[focus_index]] = [record[0], record[focus_index+6], record[-1]]
            exhib_artwork_network[record[focus_index]] = []
#print(exhib_info_dict)
for doc in cursor:
    for field in set(field_dict.keys()) - set(('exposition_out_of_folder',)):
        if field in doc:
            for exhibition in get_list_from_html(doc[field]):
                #print(exhibition)
                if 'exposition_out_of_folder' not in doc or exhibition not in doc['exposition_out_of_folder']:
                    if exhibition in exhib_artwork_network:
                        exhib_artwork_network[exhibition].append((doc['_id'], field))
#print(exhib_artwork_network)
with open(sys.argv[1], 'w') as g:
    destCSV = csv.writer(g)
    destCSV.writerow(['Artwork_id', 'Exhibition_hash', 'Exhibition_type', 'Start_date', 'End_date'])
    for exhibition, artwork_list in exhib_artwork_network.items():
        for artwork_info in artwork_list:
            destCSV.writerow([artwork_info[0], exhib_info_dict[exhibition][0], artwork_info[1], exhib_info_dict[exhibition][1], exhib_info_dict[exhibition][2]])
