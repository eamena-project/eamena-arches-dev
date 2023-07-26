#!/usr/bin/python3
# Split an XLSX template into separate sheets and convert each sheet into a TSV (Tab-Separated Values) 
# By Thomas Huet, EAMENA project, University of Oxford

import os
import argparse
import pandas as pd
import requests as rq
import tempfile

argp = argparse.ArgumentParser()
argp.add_argument('DirOut', metavar='dir_out', type=str, help='The folder path where to write the many TSV', default='')
args = argp.parse_args()


bu_url = "https://github.com/eamena-project/eamena-arches-dev/raw/main/data/bulk/templates/Bulk_Upload_template_221025.xlsx"
bu_name = os.path.basename(bu_url)

response = rq.get(bu_url)

temp_dir = tempfile.mkdtemp()
temp_file_path = os.path.join(temp_dir, bu_name)

with open(temp_file_path, "wb") as f:
    f.write(response.content)

xl = pd.ExcelFile(temp_file_path)

output_dir = args.DirOut

for sheet_name in xl.sheet_names:
    df = xl.parse(sheet_name)
    tsv_file = f"bu_{sheet_name}.tsv"
    df.to_csv(os.path.join(output_dir, tsv_file), sep="\t", index=False)
