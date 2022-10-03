from pyavm import AVM
import os

path = "C:/Rprojects/eamena-arches-dev/data/photos/"
imagename = path + "APAAME_20211026_RHB-0705.DNG"
avm = AVM.from_image(imagename)
print(avm)
