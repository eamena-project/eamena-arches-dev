import openpyxl
import csv

# Replace 'input.xlsx' with the actual name of your XLSX file
# Replace 'output.tsv' with the desired name of your TSV file
xlsx_filename = 'template.xlsx'
tsv_filename = 'template.tsv'

# Load the XLSX file
wb = openpyxl.load_workbook(xlsx_filename)
sheet = wb.active

# Open the TSV file for writing
with open(tsv_filename, 'w', newline='') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')

    # Iterate through rows in the XLSX sheet and write them as TSV rows
    for row in sheet.iter_rows(values_only=True):
        tsv_writer.writerow(row)

print(f'Conversion from XLSX to TSV complete. TSV file saved as {tsv_filename}')
