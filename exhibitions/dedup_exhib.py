import csv, sys

if len(sys.argv) < 3:
    sys.exit('USAGE: Srccsv1 Destcsv2')

dedup_set = set({})
f = open(sys.argv[1])
g = open(sys.argv[2], 'w')
dc  = csv.writer(g)
for record in csv.reader(f):
    if (record[0], record[1]) not in dedup_set:
        dedup_set.add((record[0], record[1]))
        dc.writerow(record)
f.close()
g.close()