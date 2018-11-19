import sys, csv
sys.path.append('../modules')
import pymongo
from ope_fields import *
from melt_ope_expo import *
from get_html_list import *

def comp_dates(datestring1, datestring2):
	if datestring1 == '' or datestring1 == '...':
		return -2
	if datestring2 == '' or datestring2 == '...':
		return 2
	#print(datestring1)
	[year1, month1, day1] = datestring1.split('/')
	[year2, month2, day2] = datestring2.split('/')
	if int(year1) < int(year2):
		return -1
	if int(year2) > int(year2):
		return 1
	if month1 == '00' or month2 == '00' or month1 == month2:
		return 0
	if int(month1) < int(month2):
		return -1
	if int(month1) > int(month2):
		return 1
	if day1 == '00' or day2 == '00' or day1 == day2:
		return 0
	return -1 if int(day1) < int(day2) else 1

if len(sys.argv) < 3:
	sys.exit('USAGE : '+sys.argv[0]+' [destI20file] [destNetworkfile]')

start_tuple = ('212I',)
end_tuple = ('213I',)
category = 'I20'

i20_info = {}
i20_network = {}

find_dict = {"all_realized_operations_history":{"$exists":True}}
field_dict = {"all_realized_operations_history":1}#, "hanging_history":1, "expositions_without_current":1, "expositions":1}
c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({},field_dict)
for doc in cursor:
	if "all_realized_operations_history" in doc:
		ranges = get_from_operation_expo_heuristic_range(get_list_from_html(doc["all_realized_operations_history"]), start_tuple, end_tuple, [], 'I20', 1995, 1)
		for key, value in ranges.items():
			#print(key)
			if key in i20_info:
				for single_heuristic_date in value:
			#		print(single_heuristic_date)
					for i in range(2):
						comp = comp_dates(single_heuristic_date[i], i20_info[key][i])
						if i20_info[key][i] == '' or i20_info[key][i] == '...' or comp == 2*i-1:
							i20_info[key][i] = single_heuristic_date[i]
						elif comp == 0:
							if i20_info[key][i].split('/')[1] == '00':
								i20_info[key][i] = single_heuristic_date[i]
							elif i20_info[key][i].split('/')[2] == '00':
								i20_info[key][i] = single_heuristic_date[i]
			else:
				i20_info[key] = value[0]
				i20_network[key] = []
			i20_network[key].append(doc['_id'])
print(i20_network)
with open(sys.argv[1], 'w') as f, open(sys.argv[2], 'w') as g:
	i20CSV = csv.writer(f)
	networkCSV = csv.writer(g)
	for key, artList in i20_network.items():
		for art in artList:
			networkCSV.writerow([art, key] + i20_info[key])
		i20CSV.writerow([key] + i20_info[key])