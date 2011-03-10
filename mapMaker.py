#!/usr/bin/python

import os, errno
from PIL import Image
from hashlib import md5

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
        

# parameters 
locationDir = "/opt/df/"
locationSave = locationDir+"legend/"
locationFile = "worldMap.bmp"
elementSize = [8,12]

# setup environment
mkdir_p(locationSave)

# import image map
mapObject = Image.open(locationDir+locationFile)
mapSize = mapObject.size
elements = {}

# parse elements from image map
for x in range(0,mapSize[0],elementSize[0]):
    for y in range(0,mapSize[1],elementSize[1]):
        #print x,y
        element = mapObject.crop([x,y,x+elementSize[0],y+elementSize[1]])
        md5sum = md5(str(list(element.getdata()))).hexdigest()
        if not elements.has_key(md5sum):
            elements[md5sum]=1
            element.save(locationSave+md5sum+".bmp")
#        element.show()
#        break
#    break
    
    
    
    
    


