# Modules overview

## authors.py

Type: runable script

Outputs a .csv file with all authors from MongoDB.

## clean_authors_nationalities.py

Type: runable script

From a .csv file listing authors, adds a column with their "clean" nationality.

## expo_fields.py

Type: reusable module

Some functions to extract structured data (title, place, start & end dates) from an exhibition record.

## get_all_artworks.py

Type: runable script

Outputs the list of all artworks, from the MongoDB, to a .csv file (in ../data)

## get_html_list.py

Type: reusable module

Convert html list to json list. As this is done when inserting data to the database,
it isn't needed when grabing data from the mongodb.

## queryToCSV.py

Type: runable script

Get directly a CSV from a mongo query.

Command-line arguments:

1. Mongo restriction dict (first argument of the find method)
2. Mongo projection dict (second argument of the find method)
3. Destination CSV file
