import os
import pandas as pd

# print(os.getcwd())
local = "C:/Rprojects/eamena-arches-dev/"

# Load the XLSX file into a DataFrame
xlsx_file = local + 'data/layouts/symbology.xlsx'
df = pd.read_excel(xlsx_file)

# Convert the DataFrame to a Markdown table
markdown_table = df.to_markdown(index=False)

# Specify the output Markdown file
markdown_file = local + 'data/layouts/koppen.md'

# Save the Markdown table to the specified file
with open(markdown_file, 'w') as f:
    f.write(markdown_table)

print(f"Markdown table saved to {markdown_file}")
