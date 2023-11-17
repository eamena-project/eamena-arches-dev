

#%%

import os
import pandas as pd

# print(os.getcwd())
local = "C:/Rprojects/eamena-arches-dev/"

# Load the XLSX file into a DataFrame
xlsx_file = local + 'data/layouts/symbology.xlsx'
xls = pd.read_excel(xlsx_file, sheet_name=None)

for sheet_name, df in xls.items():
    # Process each sheet as needed
    print(f"Sheet Name: {sheet_name}")
    # Convert the DataFrame to a Markdown table
    markdown_table = df.to_markdown(index=False)
    # Specify the output Markdown file
    markdown_file = local + f'data/layouts/{sheet_name}.md'
    # Save the Markdown table to the specified file
    with open(markdown_file, 'w') as f:
        f.write(markdown_table)
    print(f"Markdown table saved to {markdown_file}")

# %%
