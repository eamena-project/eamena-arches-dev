# %%
# convert DNG to JPG using the magick library (Windows)
# see: https://technologytales.com/2016/06/08/batch-conversion-of-dng-files-to-other-file-types-with-the-linux-command-line/
# see: C:\Rprojects\Rdev\gmm\marmotta\extract\extract_lithics_4.py

import os
import subprocess

loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/"

img_name = 'APAAME_20141020_RHB-0143'
imgin = img_name + '.dng'
imgout = img_name + '.jpg'
os.chdir(loc_path)
# os.system() nor subprocess.call() aren't working... while this works from PS or CMD
cmd_to_jpg = "magick convert '%s' '%s'" % (imgin, imgout)
# os.system(cmd_to_jpg)
subprocess.call(cmd_to_jpg)
print("      ... DNG converted to JPG")