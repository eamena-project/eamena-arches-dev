# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 21:37:59 2022

@description: collect EAMENA ID from a CSV export
"""

import csv

csv_path = 'C:/Rprojects/eamena-arches-dev/data/to_rm/Heritage Place.csv'

resource_ids =[]
with open (csv_path, newline="") as csv_file:
    csv_reder = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reder:
        resource_ids.append(row['EAMENA ID'])

path="C:/Rprojects/eamena-arches-dev/data/to_rm/Heritage Place_ID.csv"
ofile=open(path,"w")
wr = csv.writer(ofile)
for elem in resource_ids:
   wr.writerow([elem])
ofile.close()

        
