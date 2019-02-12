import pymongo
import sys
import csv
import json

db = pymongo.MongoClient("localhost", 27017)["VideoMuseum"]
cursor = db.Artwork.find(no_cursor_timeout = True)
n = cursor.count()
print("Number of artworks in query:", n)

header = {
    '_id' : 1,
    'ensemble_id' : 1,
    'nb_elements' : 1,
    'related' : 1,
    'type' : 1,
    'recap_inventory' : 1,
    'recap_title' : 1,
    'recap_nature' : 1,
    'title_notice' : 1,
    'title_list' : 1,
    'title_ensemble' : 1,
    'collection_department' : 1,
    'dimensions_additional' : 1,
    'inscriptions' : 1,
    'expositions_without_current' : 1,
    'expositions' : 1,
    'bibliography' : 1,
    'copyright' : 1,
    'author_in_common' : 1,
    'is_dissoc' : 1,
    'collection' : 1,
    'acquisition_mode' : 1,
    'recap_copyright' : 1,
    'date_creation' : 1,
    'acquisition_year' : 1,
    'domain' : 1,
    'domain_leaf' : 1,
    'domain_deno_for_grid' : 1,
    'domain_description_mst' : 1,
    'comments' : 1,
    'recap_description' : 1,
    'recap_authors' : 1,
    'authors_notice' : 1,
    'authors_list' : 1,
    'dimensions' : 1,
    'recap_dimensions' : 1,
    'acquisition' : 1,
    'inventory' : 1,
    'inventory_for_grid' : 1,
    'key_words_thema' : 1,
    'rights_management_leaf' : 1,
    'default_tooltip_ua_description' : 1,
    'authors_name_complement' : 1,
    'authors_site' : 1,
    'authors_documents' : 1,
    'authors_video' : 1,
    'authors_nationality' : 1,
    'authors_birth_death' : 1,
    'live_and_work' : 1,
    'author_bibliography' : 1,
    'recap_nationality' : 1,
    'recap_name_complement' : 1,
    'recap_birth_death' : 1,
    'recap_live_and_work' : 1,
    'recap_author_bibliography' : 1,
    'recap_live_work' : 1,
    'nb_images' : 1,
    'medias' : 1,
    'recap_image_unavailable' : 1,
    'authors' : 1,
    'localisation_if_deposit' : 1,
    'number_provisory' : 1,
    'key_words_icono' : 1,
    'image_unavailable' : 1,
    'title_serial' : 1,
    'key_words_movement' : 1,
    'title_attributed' : 1,
    'creation_stage' : 1,
    'domain_deno' : 1,
    'deposit_number' : 1,
    'deposit_number_for_grid' : 1,
    'tirage_design' : 1,
    'number_exhibition' : 1,
    'realisation_location' : 1,
    'recap_multi' : 1,
    'dimensions_without_margin' : 1,
    'tirage' : 1,
    'collaborators_design' : 1,
    'authors_live_work' : 1,
    'collaborators' : 1,
    'tirage_photo' : 1,
    'title_old' : 1,
    'number_entry' : 1,
    'production_circumstances' : 1,
    'subtitle' : 1,
    'number_identification' : 1,
    'number_artist_studio' : 1,
    'title_other' : 1,
    'text_notes' : 1,
    'title_old_by_artist' : 1,
    'number_document' : 1,
    'title_collection' : 1,
    'number_depositary_or_loaner' : 1,
    'recap_bibliography' : 1,
    'ensemble' : 1,
    'old_owners' : 1,
    'recap_title_trad' : 1,
    'number_artist' : 1,
    'trans_title_attributed' : 1,
    'number_isbn' : 1,
    'number_succession' : 1,
    'trans_subtitle' : 1,
    'number_issn' : 1,
    'mnam_mnr' : 1,
    'trans_title_serial' : 1,
    'number_catalogue' : 1,
    'number_frame' : 1,
    'trans_title_ensemble' : 1,
    'trans_title_other' : 1,
    'trans_title_old' : 1,
    'old_attributions' : 1
}

clean_modalities = {}
with open( '../data/acquisition_mode_clean.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for r in reader:
        clean_modalities[r[1]] = r[2]

with open("../data/ALL_ARTWORKS.csv", 'w', newline='', encoding='utf-8') as f:
    destCSV = csv.writer(f)
    destCSV.writerow(list(header) + ["acquisition_mode_clean"])
    i = 0
    for doc in cursor:
        if i % 10000 == 0:
            print("Getting artwork", i+1,"to", min([i + 10000, n]))
        i += 1
        doc_line = []
        for field in header:
            if field in doc:
                if not isinstance(doc[field], list):
                    if isinstance(doc[field], str):
                        doc[field] = doc[field].replace('\n', '').replace('\t', '')
                    doc_line.append(doc[field])
                else:
                    composite = '|'.join(doc[field])
                    composite = composite.replace('\n', '').replace('\t', '')
                    doc_line.append(composite)
            else:
                doc_line.append('')
        if "acquisition_mode" in doc:
            if doc["acquisition_mode"] in clean_modalities:
                clean_acquisition = clean_modalities[doc["acquisition_mode"]]
                doc_line.append(clean_acquisition)
            else:
                print("Warning: artwork", doc["_id"], "has unknown acquisition mode:", doc["acquisition_mode"])
                doc_line.append(doc["acquisition_mode"])
        destCSV.writerow(doc_line)
print('Done')
