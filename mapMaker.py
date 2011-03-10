#!/usr/bin/python

import os, errno
import ImageFont, ImageDraw
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
locationFonts = os.getcwd()+"/fonts/"
font = "cp437-8x12.pbm"

# setup environment
mkdir_p(locationSave)

# import map image
mapObject = Image.open(locationDir+locationFile)
mapSize = mapObject.size

# import font image
fontObject = Image.open(locationFonts+font)
fontSize = fontObject.size
fontElements = []
for x in range(0,fontSize[0],elementSize[0]):
    for y in range(0,fontSize[1],elementSize[1]):
        fontElements.append(fontObject.crop([x,y,x+elementSize[0],y+elementSize[1]]))

# parse elements from image map
elements = {}
elementsGlyph = {}
elementsString = ""
for x in range(0,mapSize[0],elementSize[0]):
    for y in range(0,mapSize[1],elementSize[1]):
        #print x,y
        element = mapObject.crop([x,y,x+elementSize[0],y+elementSize[1]])
        md5sum = md5(str(list(element.getdata()))).hexdigest()
        # if map element is unique, export
        if not elements.has_key(md5sum):
            elements[md5sum]=1
            element.save(locationSave+md5sum+".bmp")
            # if map element matches supplied font file, export extra details
            foundFont = False
            glyphCode = 0;
            for fontElement in fontElements:
                if list(fontElement.getdata()) == list(element.convert("L").point(lambda i: i * 100,"1").getdata()):
                    print "Found a match for map element: "+md5sum
                    foundFont = True
                    break
                glyphCode+=1
                    
            if not foundFont:
                print "Could not find glyph for map element: "+md5sum
    
    
    
    


