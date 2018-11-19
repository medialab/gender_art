import csv
import sys

if len(sys.argv) < 4:
    sys.exit('USAGE : '+sys.argv[0]+' [quantiCSVsourcefile] [qualiCSVsourcefile] [quantiWithQualiCSVdestfile]')

expo_set = set()

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'r') as g, open(sys.argv[3], 'w') as h:
    quantiCSV = csv.reader(f)
    qualiCSV = csv.reader(g)
    destCSV = csv.writer(h)
    for line in qualiCSV:
        destCSV.writerow(line)
        expo_set.add(line[0])
    for line_num, line in enumerate(quantiCSV):
        if not line_num or line[0] in expo_set:
            continue
        else:
            destCSV.writerow(line)
print('Done')