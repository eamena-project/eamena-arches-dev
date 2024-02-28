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
	
	for start, end in zip(starts, ends):
		table_df = df.iloc[start:end-1].copy()  # Extract table without the dummy end
		table_title = table_df.iloc[0, 0].lstrip('#').strip().replace(' ', '_')
		sheet_name = sheet_name.strip().replace(' ', '_')
		# Adjust to handle empty or generic titles
		table_name = f"{table_title}" if table_title else f"{sheet_name}_Table_{start}"
		# tsv_file_path = os.path.join(output_dir, f"{table_name}.tsv")
		os.makedirs(os.path.join(output_dir, sheet_name), exist_ok=True)
		tsv_file_path = os.path.join(output_dir, sheet_name, f"{table_name}.tsv") 

		table_df = table_df.iloc[1:] # rm the first row
		# print(table_df.iloc[0, 0])
		table_df.columns = [table_df.columns[0].lstrip('#')] + table_df.columns[1:].tolist()
		# table_df.iloc[0, 0] = table_df_.iloc[0, 0].replace('#', '') # rm the leading '#'
		# Save table to TSV, omitting initial hashtag row if necessary
		table_df.to_csv(tsv_file_path, sep='\t', index=False)
		print(f"Saved {tsv_file_path}")

def main(file_in, dir_out):
	bu_url = "https://github.com/eamena-project/eamena-arches-dev/raw/main/data/bulk/templates/" + file_in
	response = rq.get(bu_url)

	with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
		tmp_file.write(response.content)
		tmp_file_path = tmp_file.name

	xl = pd.ExcelFile(tmp_file_path)

	for sheet_name in xl.sheet_names:
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