#!/usr/bin/env python
# -*- coding: utf-8

import re
from pymongo import MongoClient

db = MongoClient("localhost", 27017)["mnam"]

def format_field(val):
    if type(val) == bool:
        return "1" if val else "0"
    if type(val) == list:
        return u"|".join([v for v in val])
    if val == None:
        return ''
    return val if type(val) == unicode else unicode(val)
format_csv = lambda val: ('"%s"' % val.replace('"', '""') if "," in val or '"' in val else val).encode('utf-8').replace("\n", "|")
csv_line = lambda dat,keys: ",".join([format_csv(format_field(dat[k])) for k in keys])

if __name__ == "__main__":

    fields = ["_id", "acquisition_year", "acquisition_mode", "date_creation", "type", "ensemble_id","domain", "domain_leaf", "domain_deno_for_grid", "domain_description_mst", "collection", "collection_department", "recap_authors", "authors_list", "authors_nationality", "authors_birth_death", "authors_name_complement", "title_notice", "title_list", "comments", "recap_description", "all_realized_operations_history", "hanging_history", "hanging_history_m34", "temporary_exhibitions_m30", "exposition_out_of_folder", "expositions", "expositions_without_current", "inscriptions", "authors"]
    med_fields = fields + ["url", "copyright", "legend", "max_width", "max_height"]
    array_fields = ["all_realized_operations_history", "hanging_history", "hanging_history_m34", "temporary_exhibitions_m30", "expositions", "authors"]

    artworks = open("artworks.csv", "w")
    print >> artworks, ",".join(fields)
    images = open("images_with_urls.csv", "w")
    print >> images, ",".join(med_fields)

    ensembles = {}
    inventory = {}
    uniq_doubles = {}
    #re_inv = re.compile(r"((?: (?:FH|AP|DOC))?|AM|DOC|GOB|JP|GMTT|LUX[.O ]*|MV|INV\.?|RF|N|LP|Fh|MI)[\s]*([A-Z]*[\d\-\.]+)")
    for a in db["Artwork"].find():
        dat = {}
        for key in fields:
            dat[key] = a.get(key, "")
        dat["description"] = dat["domain_description_mst"].replace(dat["domain"], "").replace(u"|", ", ")

        # skip = False
        # if a.get("ensemble_id", ""):
        #     if a["ensemble_id"] in ensembles:
        #         skip = True
        #     else:
        #         ensembles[a["ensemble_id"]] = True
        inventory_id = a.get("inventory", a.get("deposit_number", ""))
        skip = False
        if inventory_id != '':
            if inventory_id in inventory:    
                if inventory_id not in uniq_doubles:
                    print "skip duo inventory", inventory_id
                    uniq_doubles[inventory_id] = True
                skip = True
            else:
                inventory[inventory_id] = True

            dat["inventory_id"] = inventory_id
        else:
            print "missing inv", a.get("inventory")
        for field in array_fields:
            if field=="all_realized_operations_history":
                dat[field] = ';sep;'.join(dat[field])    
            else:
                dat[field] = '#'.join(dat[field])
        if not skip:
            print >> artworks, csv_line(dat, fields)
        for mid in a["medias"]:
            m = db["Media"].find_one({"_id": mid})
            if m["type"] != "image":
                continue
            med = dict(dat)
            med["url"] = m["url_template"].replace("{file_name}", m["file_name"]).replace("{size}", str(m["max_height"]))
            med["copyright"] = m.get("copyright", "")
            med["legend"] = m.get("legend", "")
            med["max_width"] = m.get("max_width", "")
            med["max_height"] = m.get("max_height", "")
            print >> images, csv_line(med, med_fields)

    artworks.close()
    images.close()

