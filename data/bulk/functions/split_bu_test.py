import os
import argparse
import pandas as pd
import requests as rq
import tempfile

def split_and_save_tables(df, sheet_name, output_dir):
    # Identify start of new tables based on hashtag in the first column
    starts = df[df[df.columns[0]].astype(str).str.startswith('#')].index
    # Include the end of the sheet as the end point for the last table
    ends = df.index[df[df.columns[0]].isna() & df.index.to_series().shift(-1).isna()][1:].tolist() + [df.index[-1] + 1]
    
    for start, end in zip(starts, ends):
        if start < end:
            table_df = df.loc[start:end-1]
            table_name = table_df.iloc[0,0].lstrip('#').strip().replace(' ', '_')
            tsv_file_path = os.path.join(output_dir, f"{sheet_name}_{table_name}.tsv")
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

    os.remove(tmp_file_path)  # Clean up temporary file

if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('FileIn', type=str, help='The BU template that will be exported in as many TSV files it has spreadsheets')
    argp.add_argument('DirOut', type=str, help='The folder path where to write the many TSV')
    args = argp.parse_args()
    
    main(args.FileIn, args.DirOut)