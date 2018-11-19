# Modules overview

## get_html_list.py

Type: reusable module

Convert html list to json list. As this is done when inserting data to the database,
it isn't needed when grabing data from the mongodb.

## get_geoloc.py

Type: runable script

Get geonames geolocation from given csv column.

Command-line arguments:

1. Source CSV path
2. Destination CSV path
3. Source CSV column number for querying geonames

## groupEnsemblesAndExport_mod.py

Type: runable script

Produce the uniq_artworks CSV file:
- When we face an individual artwork, insert it
- When we face a non-separable set, insert it
- When we face an artwork which is part of a separable set, insert juste one record for the entire set

Command-line arguments: None (destination CSV path is hardcoded)

## expo_fields.py

Type: reusable module

Some functions to extract structured data (title, place, start & end dates) from an exhibition record.

## ope_fields.py

Type: reusable module

Some functions to extract basic data (date, operation code, and the description tail)
from the operation field `all_realized_operation_history`,
as well as trying to guess exhibition start & end date.

## melt_ope_expo.py

Type: reusable module

Tag exhibition (taken from exhibition fields) by the operations in `all_realized_operation_history`.

## tag_expo_from_csv.py

Type: runable script

Use `melt_ope_expo.py` to tag exhibitions from a CSV file.

Command-line arguments:

1. Source CSV
2. Destination CSV

## queryToCSV.py

Type: runable script

Get directly a CSV from a mongo query.

Command-line arguments:

1. Mongo restriction dict (first argument of the find method)
2. Mongo projection dict (second argument of the find method)
3. Destination CSV file

## clean_results-splitted_correct_lists.py

Type: runable script

Basically the same as `clean_results-splitted.py` using the modular `get_html_list.py`.

## merge_quantiquali_csv.py

Merge two CSV files (one categorized as quali, the other as quanti with this approach:

1. Copy quali CSV
2. Copy records from quanti CSV which are not already present in the quali CSV

Command-line arguments:

1. Quanti CSV file
2. Quali CSV file
3. Destination CSV file