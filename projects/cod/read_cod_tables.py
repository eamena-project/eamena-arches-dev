# %%

import pandas as pd
import os


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
