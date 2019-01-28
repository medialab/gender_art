
# Gender Art Project

Add some description here...

# Configuration

```bash
$cp config.example.py  config.py
$vi config.py
```

# Requirements

- python 3
- node > 7
- [docker-compose](https://docs.docker.com/compose/install/) or MongoDB

```bash
$pip install -r requirements.txt
$npm i
```

# Instructions  

First download the data as json files:

```bash
$python download_all_files.py
```

Make sure you have a mongo database running on http://localhost:27017
You can use docker for that:

```bash
$docker-compose up
```

Or alternatively MongoDB with these two steps:
```bash
$mongod --dbpath "your\path\to\db"
$mongo
```

Then insert the data into a mongodb:
```bash
$node dataToMongo-splitfiles.js
```

# Scripts Descriptions

## download_all_files.py

A script to connect to API and download the files with pagination. Caches files already downloaded. Set clear to 'True' to empty cache. 
Requires config.py with login information. Performs initial cleaning of json documents.

## dataToMongo-splitfiles.js

Creates Mongo database with three collections: Author, Artwork and Media. Requires json data files.

## acquisition_modes.py

Generates csv files with all acquisition modes present in the database and their frequencies.

## Nationality_cleaning.ipynb

Cleans 'Nationality (Original)' column in authors dataset. Produces either one nationality or a sequence of nationalities. Does not distiguish between double nationality or a sequence.

## Missing_Data_Plots.ipynb

Distributions of missing data in time based on average dates for the artists.

## Filter_authors_birth_death_artwork_year.ipynb

Filters authors dataset to exclude artists who:
a) were born later than 1830;
b) died earlier than 1900;
c) whose latest artwork is created before 1900.

## Authors_VideoMuseum_Gender_Proportions.ipynb

Plots for gender proportions in authors dataset.

## gender_ratio_from_API.ipynb

Gender ratio plots from Video Museum API aggregations.

## Age_at_first_acquisition_plots.ipynb

Distributions of artists age when their first artwork was acquired by the museum by gender.







