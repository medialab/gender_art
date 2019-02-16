import csv, sys, pymongo, re
import pandas as pd
from itertools import compress

def contains_numbers(mystring):
    return any(char.isdigit() for char in mystring)

def remove_after_numbers(mystring):
    if len(mystring) == 0: return mystring
    while(len(mystring) > 0 and not (mystring[-1].isdigit() or mystring[-1] == ')')):
        mystring = mystring[:-1]
    return mystring

def remove_space_before(mystring):
    if len(mystring) == 0: return mystring
    while(len(mystring) > 0 and mystring[0] == ' '):
        mystring = mystring[1:]
    return mystring

def clean_string(mystring):
    return remove_after_numbers(remove_space_before(mystring))

################################################################################

res = pd.read_csv("all_exhibitions.csv", sep = ";", encoding = "utf-8")
i = 0

for index, element in res.iterrows():

    if i % 1000 == 0: print(i)
    i += 1

    exhibition = element["Exhibitions"]

    # GET THE DATE
    if not '//' in exhibition:
        exh = exhibition.replace('\r', '').replace('\n', ' ')
        all_elements = re.split(',|\.|:', exh)
        # print(all_elements)
        ind = [re.search(r'(1[89][0-9][0-9]|20[01][0-9])', i) != None for i in all_elements]
        remainder = list(compress([clean_string(i) for i in all_elements], ind))
        date = ' | '.join(remainder)
        # print(date)
    else:
        exh = exhibition.split('//', 1)[-1].replace('\r', '').replace('\n', ' ')
        all_elements = re.split(',|\.|:|//', exh)
        # print(all_elements)
        ind = [re.search(r'(1[89][0-9][0-9]|20[01][0-9])', i) != None for i in all_elements]
        remainder = list(compress([clean_string(i) for i in all_elements], ind))
        date = ' | '.join(remainder)
        # print(date)
    res.loc[index, "Date"] = date

    # First char is linebreak
    if exhibition[0] in ["\r", "\n"]:
        exh = exhibition.replace('\r', '').replace('\n', ' ')
        if "n°" in exh[0:3] or "cat." in exh[0:6] or "rep." in exh[0:6]: pass
        else: pass #print(remove_space_before(exh))

    # First char is not linebreak (less crappy)
    else:
        exh = exhibition.replace('\r', '').replace('\n', ' ')
        # Exhibition with various locations: harder case
        if "//" in exh:
            pass
            # print(len(exh.split(", ")))
        # Only one location
        else:
            # The text has a nice form: "name : placestuff, timestuff"
            if len(exh.split(" : ")) == 2:
                name = exh.split(" : ")[0]
                place = ''.join(exh.split(" : ")[1].split(",")[:-1])
                time = exh.split(" : ")[1].split(",")[-1]
                # print(place, "|||", time)
                res.loc[index, "Name"] = name
                res.loc[index, "Place"] = place
            # Not enough elements in split
            elif len(exh.split(" : ")) < 2:

                if contains_numbers(exh.split(",")[-1]):
                    split_dot = exh.split(",")[-1].split('.')
                    ind = [re.search(r'[12]\d{3}', i) != None for i in split_dot]
                    remainder = list(compress([clean_string(i) for i in split_dot], ind))
                    if len(remainder) > 1:
                        pass # print(' | '.join(remainder))


            elif len(exh.split(" : ")) > 2:
                pass #print(exh)

tokeep = [re.search(r'(19[89][0-9]|20[01][0-9])', i) != None for i in res['Date']]
res = res[tokeep]

res.to_csv("all_exhibitions_parsed.csv", sep = ";")
