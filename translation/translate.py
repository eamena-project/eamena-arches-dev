import os

# print (os.getcwd())

with open(os.getcwd()+'/translation/for_translation_arches-70_djangopo_fr_samp.po') as f:
    lines = f.readlines()
    print(lines, end='\n')