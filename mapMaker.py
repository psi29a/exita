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
legendSave = locationDir+"legend/"
locationFile = "worldMap.bmp"
elementSize = [8,12]
locationFonts = os.getcwd()+"/fonts/"
font = "cp437-8x12.pbm"
fontGlyphs = 256

# setup environment
mkdir_p(legendSave)

# import map image
mapObject = Image.open(locationDir+locationFile)
mapSize = mapObject.size

# import font image
fontObject = Image.open(locationFonts+font)
fontSize = fontObject.size
fontElements = []
for y in range(0,fontSize[1],elementSize[1]):
    for x in range(0,fontSize[0],elementSize[0]):
        if len(fontElements) < fontGlyphs:
            fontElements.append(fontObject.crop([x,y,x+elementSize[0],y+elementSize[1]]))

# parse elements from image map
elements = elementsGlyph = {}
internalMap = []
outputUTF = ""
outputHTMLplain = "<pre>\n"
outputHTMLimg = "<p style='width:2056px;'>"

x = y = 0
for offsetY in range(0,mapSize[1],elementSize[1]):
    for offsetX in range(0,mapSize[0],elementSize[0]):
        #print offsetX,offsetY
        element = mapObject.crop([offsetX,offsetY,offsetX+elementSize[0],offsetY+elementSize[1]])
        md5sum = md5(str(list(element.getdata()))).hexdigest()
        # if map element is unique, export
        if not elements.has_key(md5sum):
            element.save(legendSave+md5sum+".bmp")
            # if map element matches supplied font file, export extra details
            foundFont = False
            glyphCode = 0;
            for fontElement in fontElements:
                # since our font glyphs are in black and white (1bit), we need
                # convert the map glyph from 24-bit colour to grayscale, then
                # from grayscale to (1bit) using point function to take anything
                # not black and set to white.
                if list(fontElement.getdata()) == list(element.convert("L").point(lambda i: i * 20,"1").getdata()):
                    print "Found a match for map element: "+chr(glyphCode).decode('cp437')
                    foundFont = True
                    break
                glyphCode+=1
                    
            if not foundFont:
                glyphCode=-1
                elements[md5sum]=glyphCode
                print "Could not find glyph for map element: "+md5sum
            elements[md5sum]=glyphCode
        else:
            glyphCode = elements[md5sum]        
        
        internalMap.append((x,y,md5sum,glyphCode))
        outputUTF+=chr(glyphCode).decode('cp437').encode('utf-8')
        outputHTMLplain+=chr(glyphCode).decode('cp437').encode('ascii', 'xmlcharrefreplace')
        outputHTMLimg+="<img src='"+legendSave+md5sum+".bmp"+"' style='border:none; margin:0px; padding:0px;'/>"
        x+=1
    outputUTF+="\n"
    outputHTMLplain += "\n"
    outputHTMLimg += "<br/>"    
    y+=1
outputHTMLplain += "</pre>\n"
outputHTMLimg += "</p>\n"
    
fileObject = open(locationDir+locationFile+".txt","w")
fileObject.write(outputUTF)
fileObject.close()

fileObject = open(locationDir+locationFile+".html","w")
fileObject.write(outputHTMLplain)
fileObject.close()

fileObject = open(locationDir+locationFile+".htm","w")
fileObject.write(outputHTMLimg)
fileObject.close()
