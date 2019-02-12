from expo_fields import *
from ope_fields import *

def fuzzy_lower_dates(d1, d2):
    if d1 < d2:
        return 1.0
    if d1.year == d2.year:
        if d1.month == d2.month:
            return 0.7
        else:
            return 0.3
    else:
        return 0.0

def tag_one_expo_with_folder(exposition, ope_info):
    expo_list = []
    basic_expo = get_expo_title_other(exposition)
    if basic_expo is not None:
        #print('Coucou')
        #dico_count += 1
        #print(basic_expo['title'])
        for folder, heuristics in ope_info.items():
            if basic_expo['title'] in heuristics:# and folder_dict[dico['title']][1] in dico['other']:#2nd condition: maybe, maybe not
                place_time_list = get_expo_place_time(basic_expo['other'])
                for place_time in place_time_list:
                    if place_time is not None and place_time['time'] is not None:
                        tab = extract_date(place_time['time'])
                        for item in tab:# TODO Work on that !
                            item[1] = '12' if item[1] == '00' else item[1]
                            item[2] = '28' if item[2] == '00' else item[2]#28 because February
                        start_date_expo = datetime.date(int(tab[0][0]), int(tab[0][1]), int(tab[0][2]))
                        end_date_expo = datetime.date(int(tab[1][0]), int(tab[1][1]), int(tab[1][2]))
                        #date alignment
                        max_score = 0.0
                        max_ope = None
                        #print('Dah')
                        for ope_date in heuristics[basic_expo['title']]:
                            if ope_date[0] != '...' and ope_date[0] != '':
                                start_date_raw = ope_date[0].split('/')
                                start_date_ope = datetime.date(int(start_date_raw[0]), int(start_date_raw[1]), int(start_date_raw[2]))
#                                if start_date_raw != '' else datetime.date(1,1,1) # typically: didn't catch last expo before it goes to 211I
                            else:
                                start_date_ope = datetime.date(1, 1, 1)
                            if ope_date[1] != '...':
                                end_date_raw = ope_date[1].split('/')
                                end_date_ope = datetime.date(int(end_date_raw[0]), int(end_date_raw[1]), int(end_date_raw[2]))
                            else:
                                end_date_ope = datetime.date.today()
                            #print(basic_expo['title'], start_date_ope.isoformat(), end_date_ope.isoformat())
                            #if start_date_ope < start_date_expo and end_date_expo < end_date_ope:
                            #    print('M20', basic_expo['title'], start_date_ope.isoformat(), start_date_expo.isoformat(), end_date_expo.isoformat(), end_date_ope.isoformat())
                            cur_score = fuzzy_lower_dates(start_date_ope, start_date_expo) * fuzzy_lower_dates(end_date_expo, end_date_ope)
                            if cur_score > max_score:
                                max_score = cur_score
                                max_ope = ope_date
                        if max_score > 0.0:
                            #print('M20', basic_expo['title'], max_ope[0].replace('/', '-'), start_date_expo.isoformat(), end_date_expo.isoformat(), max_ope[1].replace('/', '-'))
                            expo_list.append((folder, basic_expo, start_date_expo, end_date_expo, max_score))
    return expo_list

def tag_expo_with_folder(json, folder_list):
    #folder_dict = {}
    #opcount = 0
    #dico_count = 0
    #for operation in get_list_from_html(json["all_realized_operations_history"]):
    #    basic_fields = filter_operation_record(operation)
    #    if basic_fields is not None and basic_fields['additional_data'] is not None:
    #        if basic_fields['opcode'] == '302' and 'M20' in basic_fields['additional_data']:
    #            m = re.match('.+ - M20 - (.+)$', basic_fields['additional_data'])
    #            if m is not None:
    #                folder_dict[m.group(1)] = ('M20', basic_fields['date'][0:4])
    #                opcount += 1
    ope_info = {}
    expo_list = []
    for folder, anchor_ope in folder_list.items():
        #print(folder)
        ope_info[folder] = get_from_operation_expo_heuristic_range(get_list_from_html(json['all_realized_operations_history']), anchor_ope[0], anchor_ope[1], folder, 0, 0)
    #print(ope_info)
    #print(ope_info)
    #print(ope_dates)
    for exposition in get_list_from_html(json['expositions_without_current']):
        #print('Yah')
        expo_list += tag_one_expo_with_folder(exposition, ope_info)
    return expo_list
                #print(basic_expo['title'], 'M20', ope_info[basic_expo['title']])#folder_dict[basic_expo['title']][0])
    #        else:
    #            print(dico['title'],'$',sep='')
    #print(folder_dict)
    #return (opcount, dico_count)