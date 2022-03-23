# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 21:37:59 2022

@description: collect resourceid from a CSV export
"""

import csv

data_rm_path = 'C:/Users/Thomas Huet/Desktop/EAMENA/IT/dbs/masdar-palestine/'
data_rm_csv='Heritage Place.csv'
data_rm_id='Heritage_Place_ID.csv'
csv_file_in=data_rm_path+data_rm_csv
csv_file_out=data_rm_path+data_rm_id

resource_ids =[]
with open (csv_file_in, newline="") as csv_file:
    csv_reder = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reder:
        resource_ids.append(row['resourceid'])

ofile=open(csv_file_out,"w", newline='')
wr = csv.writer(ofile, delimiter=',')
for elem in resource_ids:
   wr.writerow([elem])
ofile.close()

print("file: "+data_rm_id+" has been exported")
        
