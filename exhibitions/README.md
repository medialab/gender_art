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

## i20.py

*Type: runable script*

Compute a CSV of the artwork-to-I20 exhibitions network.
**It uses the mongodb database to iterate through each artwork.**

## m20_get_network.py

*Type: runable script*

Compute a CSV of the artwork-to-M20 exhibitions network.
**It uses the mongodb database to iterate through each artwork.**

## m30_get_network.py

*Type: runable script*

Compute a CSV of the artwork-to-M30 exhibitions network.
**It uses the mongodb database to iterate through each artwork.**
