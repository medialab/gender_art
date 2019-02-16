import pymongo, sys, re, datetime, csv, hashlib
sys.path.append('../modules')
from get_html_list import *

def get_deposit_number(ope_tail):
    regex_folder_number = re.compile(r'.*Dossier n° ?([0-9]+)', flags=re.S)
    m = regex_folder_number.match(ope_tail)
    return m if m is None else m.group(1)

def filter_operation_record(record):
    """Get some basic info about operation, as well as the un-parsed tail.
    Returns {'date': `string: YYYY/MM/DD`, 'opcode':`string`, 'oplabel':`string`, 'additional_date':`string`}"""
    rslt = {}
    regex_basic_fields = re.compile('([0-9]{4}\\/[0-9]{1,2}\\/[0-9]{1,2}) - (.+?) - (.+?)(?: - (.+))?$', flags=re.S)
    m = regex_basic_fields.match(record)
    if m is None:
        return None
    rslt['date'] = m.group(1)
    rslt['opcode'] = m.group(2)
    rslt['oplabel'] = m.group(3)
    rslt['additional_data'] = m.group(4)
    #if additional_data is not None:
    return rslt

def get_from_operation_expo_heuristic_range(field, opcode_start_list, opcode_end_list, opcode_trip_list, folder_category, year_limit = 0, complete_range = 0):
    """Get heuristic exhibition dates from the given field (aka list of operations) that is
    tagged as folder_category and newer than year_limit.
    If an exhibition is not closed when year_limit is reached (ie an exhibition ended after year_limit but started before),
    the start date search is done if complete_range is 1, else '' is returned for the start_date.
    Return is a dict in the form: {`Exhibition_title1`:[[start_date1, end_date1], [start_date2, end_date2]], `Exhibition title2`...}
    (a list of [start_date, end_date] is needed because several exhibitions can have the same title)"""
    #operation_list = get_list_from_html(field)
    operation_list = field
    #print(operation_list)
    # Order: last operation first
    #print('230E' in opcode_start_list, opcode_end_list)
    in_range = False
    in_end = False
    in_start = False
    range_dates = {}
    #today_date = datetime.date.today().isoformat().replace('-', '/')
    end_date = ''
    start_date = ''
    current_expo = ''
    current_offset = 0
    #missing_title = False
    for operation in operation_list:
        opdict = filter_operation_record(operation)
        #print(opdict)
        if opdict is not None and opdict['additional_data'] is not None and folder_category in opdict['additional_data']:
            if int(opdict['date'][0:4]) < year_limit:
                if not in_range:
                    return range_dates
                else:
                    if not complete_range:
                        return range_dates
                    #elif complete_range < 0:
                        #range_dates.append('...', end_date)
                        #for key, item in range_dates.items():
                        #    if item[0] == '':
                        #        item[0] = '...'
                    #    range_dates[current_expo][0] = '...'
                    #    return range_dates
            title = get_deposit_number(opdict['additional_data'])
            #title = None
            #print(range_dates)
            if title is None:
                title = ''
            if opdict['opcode'] not in opcode_trip_list and ((opdict['opcode'] in opcode_start_list and in_start) or (opdict['opcode'] in opcode_end_list and in_end)):
                if opdict['opcode'] in opcode_end_list and in_end and title == current_expo:#Narrow the range
                    range_dates[title][current_offset][0] = opdict['date']
                continue
            #elif opdict['opcode'] not in opcode_start_list and opdict['opcode'] not in opcode_end_list:
            #    in_end = in_start = False
            if (opdict['opcode'] in opcode_start_list and in_range) or (opdict['opcode'] in opcode_end_list and (not in_range or (in_range and not in_start and not in_end))):
                if opdict['opcode'] in opcode_start_list and in_range:
                    in_end = False
                    start_date = opdict['date']
                    #range_dates.append((start_date, end_date))
                    #if missing_title:
                    #    range_dates[title] = [[start_date, end_date]]
                    #else:
                    #    range_dates[title][current_offset][0] = start_date
                    # Tracking trip exhibitions, where title can be different
                    if title == current_expo:#No brain
                        range_dates[title][current_offset][0] = start_date
                    else:
                        range_dates[current_expo][current_offset][0] = start_date
                    #missing_title = True if opdict['opcode'] in opcode_trip_list else False
                    in_start = True if opdict['opcode'] not in opcode_trip_list else False
                    in_range = False
                    # ***DEBUG***
                    #print(range_dates)
                if opdict['opcode'] in opcode_end_list and (not in_range or (in_range and not(in_start or in_end))):
                # Not elif because trip opcodes must go there too
                # (not in_start and not in_end) because we want to catch trips with partial departure info
                    in_start = False
                    if in_range and not(in_start or in_end): #We must complete previous trip
                        #print(opdict)
                        range_dates[current_expo][current_offset][0] = opdict['date']
                    end_date = opdict['date']
                    if title not in range_dates:
                        range_dates[title] = [['', end_date]]
                        current_offset = 0
                    else:
                        range_dates[title].append(['', end_date])
                        current_offset = len(range_dates[title])-1
                    in_range = True
#                    if opdict['opcode'] not in opcode_trip_list:
#                        in_end = True
                    in_end = True if opdict['opcode'] not in opcode_trip_list else False
                    current_expo = title
            elif opdict['opcode'] in opcode_start_list and not in_range:
                if range_dates == {}:#still in the expo now
                    range_dates[title] = [[opdict['date'], '...']]
                elif title != current_expo: #didn't trace the older return, but we have the departure
                    if title not in range_dates:
                        range_dates[title] = [[opdict['date'], range_dates[current_expo][current_offset][0]]] # heuristic
                    else:
                        range_dates[title].append([opdict['date'], range_dates[current_expo][current_offset][0]])
                else:
                    print(opdict)
                    raise RuntimeWarning
                current_expo = title
                current_offset = 0
                in_start = True if opdict['opcode'] not in opcode_trip_list else False
                in_range = not in_start
            elif opdict['opcode'] in opcode_end_list and in_range:
                print(opdict)
                raise RuntimeWarning
    return range_dates

missing_deposit = set()
if len(sys.argv) < 2:
    sys.exit('USAGE : '+sys.argv[0]+' [networkCSV]')
today = datetime.date.today().isoformat().replace('-', '/')
#print(today)
c = pymongo.MongoClient()
cursor = c.myproject.Artwork.find({'$and':[{'deposit_history':{'$exists':True}}, {'all_realized_operations_history':{'$exists':True}}]},{'deposit_history':1, 'all_realized_operations_history':1, 'ensemble_id':1, 'title_list':1, 'authors_list':1})
folder = ['M10', 'M11', 'M19']
f = open(sys.argv[1], 'w')
dc = csv.writer(f)
dc.writerow(['Artwork id','Ensemble id','Author','Title','Deposit (champs brut)','folder_number','start date','end date'])
for doc in cursor:
    number2bscanned = set()
    target_deposit = {}
    prob = 0
    for target in get_list_from_html(doc['deposit_history']):
        #print(target)
        folder_number = get_deposit_number(target)
        if folder_number in target_deposit:
            prob += 1
        if '(en cours)' in target:
            target_deposit[folder_number] = [target[:11], today, target]
        else:
            target_deposit[folder_number] = [target[:11], '...', target]
            number2bscanned.add(folder_number)
    ope_deposit = {}
#    print(target_deposit)
#doc = cursor
    if number2bscanned:
#        print('Bleh')
        for f in folder:
            cur_deposit = get_from_operation_expo_heuristic_range(get_list_from_html(doc['all_realized_operations_history']), ('230E', '220E', '244E'), ('221I', '221E'), [], f)
            if cur_deposit != {}:
                ope_deposit.update(cur_deposit)
    for key in number2bscanned:
        if key in ope_deposit:
            target_deposit[key][1] = ope_deposit[key][0][1]
        else:
            missing_deposit.add(key)
    for key, item in target_deposit.items():
        dc.writerow([doc['_id'], doc['ensemble_id'] if 'ensemble_id' in doc else '', doc['authors_list'], doc['title_list'], target_deposit[key][2], key, target_deposit[key][0], target_deposit[key][1], prob])
    #print(doc['_id'], target_deposit)
        #print(doc['_id'], f, )
    #if doc_deposit == {}:
    #    print(doc['_id'])
    #print(doc_deposit)
for key in missing_deposit:
    print(key)

    
    