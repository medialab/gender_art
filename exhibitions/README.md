# Scripts overview

## dedup_exhib.py

*Type: runable script*

Deduplicate exhibitions.

## del_noncat_exhib.py

*Type: runable script*

Delete untagged exhibitions from an exhibition CSV.
**It uses the mongodb database to list the untagged exhibitions.**

## deposit_list.py

*Type: runable script*

Get from the mongodb a CSV of deposits by querying the deposit_history field.

## *[important] get_all_exhibitions.py*

*Type: runable script*

From the Mongo database, returns a .csv file with 2 columns: raw description and list of artworkds id in them (sep by " | ").

## *[important] get_all_exhibitions_parsed.py*

*Type: runable script*

From the Mongo database, returns a .csv file with parsed description of each exhibition, and the list of artworks.
Based on: https://github.com/medialab/MNAM/blob/master/modules/expo_fields.py

## get_deposit_history_ope.py

*Type: runable script*

This is crappy.

Get through the operations field all the deposits, print the absent from
deposit_history field ones.
**It uses the mongodb database to get the operations field.**

## get_exhibition_artwork_network.py

*Type: runable script*

Compute a CSV of the artwork-to-exhibitions network.
**It uses the mongodb database to iterate through each artwork.**

## hanging_list.py

*Type: runable script*

Get a list of MNAM hangings through operations field, filtering by
I20 tag (aka 1995 to 2010 hangings).
**It uses the mongodb database to get the operations field.**

## parse_exhibitions.py

*Type: runable script*

Crappy. Draft for parsing of the exhibitions.
