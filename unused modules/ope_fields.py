#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import pymongo
import re
import csv
import sys
import datetime

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

def get_operation_expo_title(operation):
    """Get exhibition title from operation tail ('additional_data' field from filter_operation_record).
    Returns the string or None."""
    regex_operation_title = re.compile('.+ - [MI][0-9]{2} - (.+)$')
    m = regex_operation_title.match(operation)
    if m is None:
        return None
    else:
        return m.group(1)

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
            title = get_operation_expo_title(operation)
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

def get_state_range(doc):
    """Unfinished attempt to track artwork location an status through operations."""
    start_date = ''
    end_date = ''
    ope_list = []
    location = '??'
    init_passed = False
    init_opcodes = ('220I', '220E', '299I', '299E')
    change_state = {'212I':'MNAM (accrochage)', '213I':'MNAM',\
    '221I':'MNAM', '241I':'MNAM (dépôt)', '242I':'MNAM', '260I':'MNAM (réserve)',\
    '261I':'MNAM', '262I':'MNAM (déménagement)', '210E':'Ext', '212E':'Ext (accrochage)',\
    '213E':'Ext', '240E':'Ext (itinérance)'}#...
    state_ranges = {}
    operation_list = reversed(doc["all_realized_operations_history"])
    for index, operation in enumerate(operation_list):
        op_dict = filter_operation_record(operation)
        if not index:
            start_date = op_dict['date']
        if not init_passed and op_dict['opcode'] in init_opcodes:
            if ope_list != []:
                end_date = op_dict['date']
                state_ranges[(start_date, end_date)] = (location, ope_list)
                ope_list = []
                start_date = op_dict['date']
                end_date = ''
            else:
                start_date = op_dict['date']
            if op_dict['opcode'][-1] == 'E':
                location = 'Ext (init)'
            elif op_dict['opcode'][-1] == 'I':
                location = 'MNAM (init)'
            init_passed = True
        if op_dict['opcode'] in change_state:
            end_date = op_dict['date']
            state_ranges[(start_date, end_date)] = (location, ope_list)
            location = change_state[op_dict['opcode']]
            ope_list = []
            start_date = op_dict['date']
            end_date = ''
        ope_list.append(op_dict)
    return state_ranges

#if len(sys.argv) < 2:
#    sys.exit('Usage: '+sys.argv[0]+' [destinationCSVfile]')

#if __name__ == "main":
#field_dict = {"all_realized_operations_history":1, "expositions_without_current":1}#, "hanging_history":1, "expositions_without_current":1, "expositions":1}
#c = pymongo.MongoClient()
#cursor = c.myproject.Artwork.find({'_id':'150000000030904'},field_dict)#'_id':'150000000030904', 150000000461389
#opc = 0
#dc = 0
#folder_list = {'M20':('230E', '221I'), 'M22':('230E', '221I'), 'M25':('230E', '221I'), 'M29':('230E', '221I'), 'M30':('230E', '221I'), 'M32':('230E', '221I'), 'M36':('230E', '221I'), 'M99':('230E', '221I')}#, 'M34':('212I', '213I')
#for doc in cursor:
#    if "all_realized_operations_history" in doc and "expositions_without_current" in doc:
#        print(tag_expo_with_folder(doc, folder_list))
    #print(get_state_range(doc))
#print(tu)
#    opc += tu[0]
#    dc += tu[1]
#print(opc, dc)
    #filter_field(doc, "all_realized_operations_history")
        #print(doc)
    #expos_operation = get_from_operation_expo_heuristic_range(doc['all_realized_operations_history'], '230E', '221I', 'M20', 0, 0)
