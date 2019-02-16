# Modules overview

## clean_results-splitted_correct_lists.py

Type: runable script

Basically the same as `clean_results-splitted.py` using the modular `get_html_list.py`.

## cleaning.py

Type: reusable module

An unused module to clean artworks fields when exporting to .csv.

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

## melt_ope_expo.py

Type: reusable module

Tag exhibition (taken from exhibition fields) by the operations in `all_realized_operation_history`.

## merge_quantiquali_csv.py

Merge two CSV files (one categorized as quali, the other as quanti with this approach:

1. Copy quali CSV
2. Copy records from quanti CSV which are not already present in the quali CSV

Command-line arguments:

1. Quanti CSV file
2. Quali CSV file
3. Destination CSV file

## ope_fields.py

Type: reusable module

Some functions to extract basic data (date, operation code, and the description tail)
from the operation field `all_realized_operation_history`,
as well as trying to guess exhibition start & end date.

## tag_expo_from_csv.py

Type: runable script

Use `melt_ope_expo.py` to tag exhibitions from a CSV file.

Command-line arguments:

1. Source CSV
2. Destination CSV

## unique_artworks

Type: runable script

Unused script to export MongoDB artworks database to .csv file.