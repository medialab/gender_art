
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
