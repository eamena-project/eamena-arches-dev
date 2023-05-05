import os
import json

rootDir = "C:\\Users\\Thomas Huet\\Desktop\\EAMENA\\IT\\dbs\\24test\\"

json_document = rootDir + "Grid_Square_2023-05-04_10-46-43.json"
print(json_document)

python_obj = json.loads(json_document)


