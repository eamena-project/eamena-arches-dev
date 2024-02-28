import os
import argparse
import pandas as pd
import requests as rq
import tempfile

def split_and_save_tables(df, sheet_name, output_dir):
	# Identify start of new tables based on hashtag in the first column
	starts = df[df[df.columns[0]].astype(str).str.startswith('#')].index
	# Add the end of the dataframe as a dummy end point for the last table
	ends = starts[1:].tolist() + [len(df) + 1]
	sheet_name = sheet_name.strip().replace(' ', '_')
	os.makedirs(os.path.join(output_dir, sheet_name), exist_ok=True)
	root_values = "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data/rm/hp/values"


	for start, end in zip(starts, ends):
		table_df = df.iloc[start:end-1].copy()  # Extract table without the dummy end
		table_title = table_df.iloc[0, 0].lstrip('#').strip().replace(' ', '_')
		# sheet_name = sheet_name.strip().replace(' ', '_')
		# Adjust to handle empty or generic titles
		table_name = f"{table_title}" if table_title else f"{sheet_name}_Table_{start}"
		table_name = table_name.replace('/', '_') # to manage values like `Condition Assessment\Damage`

		# tsv_file_path = os.path.join(output_dir, f"{table_name}.tsv")
		tsv_file_path = os.path.join(output_dir, sheet_name, f"{table_name}.tsv") 
		table_df = table_df.iloc[1:] # rm the first row
		table_df.columns = [table_df.columns[0].lstrip('#')] + table_df.columns[1:].tolist()
		# Save table to TSV
		table_df.to_csv(tsv_file_path, sep='\t', index=False)

		table_name_tsv = table_name + ".tsv"
		print(f"  - saved {tsv_file_path}")
		print("\n")
		level1_txt = sheet_name.replace('_', ' ')
		level1_url = os.path.join(root_values, sheet_name)
		level3_txt = table_name.replace('_', ' ')
		level3_url = os.path.join(root_values, sheet_name, table_name_tsv)
		print(level1_txt + " : " + level1_url)
		print(level3_txt + " : " + level3_url)
		print("\n")

def main(file_in, dir_out):
	# reads a BU template
	bu_url = "https://github.com/eamena-project/eamena-arches-dev/raw/main/dbs/database.eamena/data/bulk_data/templates/" + file_in
	response = rq.get(bu_url)

	with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
		tmp_file.write(response.content)
		tmp_file_path = tmp_file.name

	xl = pd.ExcelFile(tmp_file_path)

	for sheet_name in xl.sheet_names:
		print("* read: " + sheet_name)
		df = xl.parse(sheet_name)
		split_and_save_tables(df, sheet_name, dir_out)
	xl.close()
	os.remove(tmp_file_path)  # Clean up temporary file

if __name__ == "__main__":
	argp = argparse.ArgumentParser()
	argp.add_argument('FileIn', type=str, help='The BU template that will be exported in as many TSV files it has spreadsheets')
	argp.add_argument('DirOut', type=str, help='The folder path where to write the many TSV')
	args = argp.parse_args()
	
	main(args.FileIn, args.DirOut)