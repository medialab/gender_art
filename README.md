
# Gender art project

Add some description here...

# Configuration

```bash
$cp config.example.py  config.py
$vi config.py
```

# requirements

- python 3
- node > 7
- [docker-compose](https://docs.docker.com/compose/install/)

```bash
$pip install -r requirements.txt
$npm i
```

# Instructions  

First we download the data to json files :

```bash
$python download_all_files.py
```

Make sure you have a mongo database running on http://localhost:27017
You can use docker for that :

```bash
$docker-compose up
```

Or alternatively MongoDB with these two steps:
```bash
$mongod --dbpath "your\path\to\db"
$mongo
```

Then we insert the data into a mongodb

```bash
$node dataToMongo-splitfiles.js
```
