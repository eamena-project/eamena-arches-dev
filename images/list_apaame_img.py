# list all files (images) for a given folder
# create a txt file

import os

name_img_set = 'Qasr-el-Hallabat'
fold = "C:/Rprojects/_coll/220808 CAA22/3dapaame/images"
list_img = os.listdir(fold)
# list_img = list_img.replace(".tif", "")
list_img = [w.replace('.tif', '') for w in list_img]
out_file = os.getcwd()+'/images/'+name_img_set+'.txt'
with open(out_file, 'w') as f:
    for item in list_img:
        f.write("%s\n" % item)
print(out_file)
