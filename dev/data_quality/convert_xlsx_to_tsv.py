import openpyxl
import csv
import os

print(os.getcwd())

xlsx_filename = 'dev/data_quality/mds-template.xlsx'
tsv_filename = 'dev/data_quality/mds-template-readonly.tsv'

# xlsx_filename = 'erms-template.xlsx'
# tsv_filename = 'erms-template-readonly.tsv'

wb = openpyxl.load_workbook(xlsx_filename)
sheet = wb.active

with open(tsv_filename, 'w', newline='') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')

    for row in sheet.iter_rows(values_only=True):
        tsv_writer.writerow(row)

print(f'Conversion from XLSX to TSV complete. TSV file saved as {tsv_filename}')
