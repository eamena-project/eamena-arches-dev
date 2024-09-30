#!/usr/bin/python3
# Split an XLSX template into separate sheets, and tables from each separated sheet into into a TSV (Tab-Separated Values) 
# By Thomas Huet, EAMENA project, University of Oxford

import os
import argparse
import pandas as pd
import requests as rq
import tempfile

def split_and_save_tables(df, sheet_name, output_dir, markdown_table, root_values = "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data/rm/hp/values"):
	"""
	Read a BU template XLSX file and identify start of new tables based on hashtag (#) in the first column
	"""

	starts = df[df[df.columns[0]].astype(str).str.startswith('#')].index
	# Add the end of the dataframe as a dummy end point for the last table
	ends = starts[1:].tolist() + [len(df) + 1]
	sheet_name = sheet_name.strip().replace(' ', '_')
	os.makedirs(os.path.join(output_dir, sheet_name), exist_ok=True)
	
	for start, end in zip(starts, ends):
		table_df = df.iloc[start:end-1].copy()  # Extract table without the dummy end
		table_title = table_df.iloc[0, 0].lstrip('#').strip().replace(' ', '_')
		# sheet_name = sheet_name.strip().replace(' ', '_')
		# Adjust to handle empty or generic titles
		table_name = f"{table_title}" if table_title else f"{sheet_name}_Table_{start}"
		table_name = table_name.replace('/', '_') # to manage values like `Condition Assessment\Damage`

		# tsv_file_path = os.path.join(output_dir, f"{table_name}.tsv")
		tsv_file_path = os.path.join(output_dir, sheet_name, f"{table_name}.tsv") 
		# table_df = table_df.iloc[1:] # rm the first row
		# table_df.columns = [table_df.columns[0].lstrip('#')] + table_df.columns[1:].tolist()
		table_df.iloc[0, 0] = table_df.iloc[0, 0].lstrip('#')
		table_df.columns = table_df.iloc[0]
		table_df = table_df.drop(table_df.index[0])
		table_df = table_df.reset_index(drop=True)
		# Save table to TSV
		table_df.to_csv(tsv_file_path, sep='\t', index=False)

		table_name_tsv = table_name + ".tsv"
		# print(f"  - saved {tsv_file_path}")
		# print("\n")
		level1_txt = sheet_name.replace('_', ' ')
		# level1_url = os.path.join(root_values, sheet_name)
		level1_url = root_values + "/" + sheet_name
		level3_txt = table_name.replace('_', ' ')
		# level3_url = os.path.join(root_values, sheet_name, table_name_tsv)
		level3_url = root_values + "/" + sheet_name + "/" + table_name_tsv
		# print(level1_url)
		level1_link = f"[{level1_txt}]({level1_url})"
		level3_link = f"[{level3_txt}]({level3_url})"
		markdown_table += f"| {level1_link} | {level3_link} |\n"
	return(markdown_table)
		# print(level1_txt + " : " + level1_url)
		# print(level3_txt + " : " + level3_url)
		# print("\n")

def main(file_in, dir_out):
	# reads a BU template
	bu_url = "https://github.com/eamena-project/eamena-arches-dev/raw/main/dbs/database.eamena/data/bulk_data/templates/" + file_in
	response = rq.get(bu_url)

	with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
		tmp_file.write(response.content)
		tmp_file_path = tmp_file.name

	markdown_table = ''

	xl = pd.ExcelFile(tmp_file_path)

	# # will not read these worksheets
	# excluded_ws = ["Heritage Place", "Heritage Place example", "Minimum Enhanced Data Standards", "Info Resource", "InfoRes - Imagery", "InfoRes - Cartography", "Person-Organization", "Grid Square", "Relationships", "Colour Coding", "Sheet1"]
	included_ws =['Archaeological Assessment', 'Cultural Periods', 'Condition Assessment']

	for sheet_name in xl.sheet_names:
		if sheet_name in included_ws:
			print("* read: " + sheet_name)
			df = xl.parse(sheet_name)
			markdown_table = markdown_table + split_and_save_tables(df, sheet_name, dir_out, markdown_table)

	# add header and empty line
	markdown_table = "| level1 | level3 |\n|--------|--------|\n" + markdown_table + "| | |\n"
	# print(markdown_table)
	outmd = os.path.join(dir_out, "README.md")
	with open(outmd, "w") as file:
		file.write(markdown_table)
	print("README file exported")
	xl.close()
	os.remove(tmp_file_path)  # Clean up temporary file
	# Md table
	# markdown_table = create_markdown_table(data)

if __name__ == "__main__":
	# for example: py split_bu_template.py "Bulk_Upload_template_231017.xlsx" "C:/Rprojects/eamena-arches-dev/data/bulk/templates/doc"
	argp = argparse.ArgumentParser()
	argp.add_argument('FileIn', type=str, help='The BU template that will be exported in as many TSV files it has spreadsheets')
	argp.add_argument('DirOut', type=str, help='The folder path where to write the many TSV')
	args = argp.parse_args()
	
	main(args.FileIn, args.DirOut)