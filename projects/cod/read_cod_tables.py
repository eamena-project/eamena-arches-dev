# %%

import pandas as pd
import os

# %%
# convert all XLSX tables into CSV

def xlsx2csv(data_in, path_out):
	"""
	Read an XLSX, or a folder of XLSX, and convert it/them into a CSV. The filenames would be the same.

	:param data_in: A folder path or a file path
	:param path_out: A folder path

	"""
	import os

	if os.path.isdir(data_in):
		print(f"Read the directory {data_in}")
		all_files = os.listdir(data_in)
		xlsx_files = [file for file in all_files if file.endswith('.xlsx')]
		for xlsx_file in xlsx_files:
			data_in_filename = os.path.splitext(xlsx_file)[0]
			print(f"Read the XLSX file {data_in_filename}")
			df = pd.read_excel(f"{data_in}/{xlsx_file}")
			path_out_data = f"{path_out}/{data_in_filename}.csv"
			df.to_csv(path_out_data, index=False)
			print(f"The file {data_in_filename}.csv has been exported into {path_out}")
	elif os.path.isfile(data_in):
		if data_in.endswith('.xlsx'):
			data_in_filename = os.path.basename(data_in)
			data_in_filename = os.path.splitext(data_in_filename)[0]
			# data_in_filename = os.path.splitext(data_in)[0]
			print(f"Read the XLSX file {data_in_filename}")
			df = pd.read_excel(data_in)
			path_out_data = f"{path_out}/{data_in_filename}.csv"
			df.to_csv(path_out_data, index=False)
			print(f"The file {data_in_filename}.csv has been exported into {path_out}")
	else:
		print("It is neither a file nor a directory.")


data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/221224PhotosBCKP.xlsx"
data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/csv/"
xlsx2csv(data_in, path_out)


# base_path = os.path.dirname(__file__)
# tables_path = os.path.join(base_path, "db_data", "tables")
# tables = os.listdir(tables_path)
# ltables = [os.path.join(tables_path, table) for table in tables]



# %%

base_path = os.path.dirname(__file__)
tables_path = os.path.join(base_path, "db_data", "tables")
tables = os.listdir(tables_path)
ltables = [os.path.join(tables_path, table) for table in tables]

# Read the Excel tables
condition = pd.read_excel(ltables[0])
dating = pd.read_excel(ltables[1])
features = pd.read_excel(ltables[2])
featuresnumbers = pd.read_excel(ltables[3])
photos = pd.read_excel(ltables[4])
records = pd.read_excel(ltables[5])
# records1 = pd.read_excel(ltables[6])
smallpics = pd.read_excel(ltables[7])

# Save the 'condition' dataframe to CSV
condition.to_csv("C:/Rprojects/eamena-arches-dev/projects/cairo/reference_data/condition.csv", index=False)

# Merge tables and perform data selection in HP
records = records.merge(photos, on="ID", how="left")
df = records.merge(condition, on="conditionID", how="left")
df = df.dropna(how='all', axis=1)
df = df.merge(smallpics, left_on="ID", right_on="UnitNumber", how="left")
df = df.dropna(how='all', axis=1)
df = df.merge(dating, left_on="datetypenumber", right_on="TypeNumber", how="left")
df = df.dropna(how='all', axis=1)

df.loc[len(df)] = pd.NA
df.to_csv("C:/Rprojects/eamena-arches-dev/projects/cairo/business_data/hp.csv", index=False)

# Merge features for BC (Built Components)
df = features.merge(featuresnumbers, left_on="featureID1", right_on="featureID", how="left")
df = df.dropna(how='all', axis=1)
df.loc[len(df)] = pd.NA
df.to_csv("C:/Rprojects/eamena-arches-dev/projects/cairo/business_data/bc.csv", index=False)


# %%

import os

# Example file path
file_path = '/path/to/your/file/example.xlsx'

# Extract the base name (filename with extension)
file_name_with_extension = os.path.basename(file_path)

# Remove the extension
file_name_without_extension = os.path.splitext(file_name_with_extension)[0]

print("File name with extension:", file_name_with_extension)
print("File name without extension:", file_name_without_extension)

# %%
