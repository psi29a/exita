#!/usr/bin/python
# Export from an image map information based on system characters such cp437.

import os, errno
import sys
from PIL import Image
from hashlib import md5
from progressbar import ProgressBar, Percentage, ETA

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor
        

# parameters 
locationDir = "/opt/df/"
legendSave = locationDir+"legend"+os.sep
locationFile = "worldMap.bmp"
elementSize = [8,12]
locationFonts = os.getcwd()+os.sep+"fonts"+os.sep
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
outputHTMLplain = "<body style='background-color:#000000'><pre>\n"
outputHTMLimg = "<p style='width:2056px;'>"

# setup progressbar
widgets = ['Processing: ', Percentage(), ' ', ETA() ]
pbar = ProgressBar(widgets=widgets, maxval=(mapSize[1]/elementSize[1]+1)*(mapSize[0]/elementSize[0])+1)

x = y = 0
for offsetY in range(0,mapSize[1],elementSize[1]):
    for offsetX in range(0,mapSize[0],elementSize[0]):
        # get offsetX,offsetY
        element = mapObject.crop([offsetX,offsetY,offsetX+elementSize[0],offsetY+elementSize[1]])
        md5sum = md5(str(list(element.getdata()))).hexdigest()
        # if map element is unique, export
        if not elements.has_key(md5sum):
            element.save(legendSave+md5sum+".bmp")
            # if map element matches supplied font file, export extra details
            foundFont = False
            glyphCode = 0;
            colour = (0,0,0)
            for fontElement in fontElements:
                # since our font glyphs are in black and white (1bit), we need
                # convert the map glyph from 24-bit colour to grayscale, then
                # from grayscale to (1bit) using point function to take anything
                # not black and set to white.
                if list(fontElement.getdata()) == list(element.convert("L").point(lambda i: i * 20,"1").getdata()):
                    #print "Found a match for map element: "+chr(glyphCode).decode('cp437')
                    foundFont = True
                    break
                glyphCode+=1
            if not foundFont:
                glyphCode=-1
                print "Could not find glyph for map element: "+md5sum
                
            # find the colour of the glyph, as it could have additional meaning.
            for pixelColour in list(element.getdata()):
                if not pixelColour == colour: # pure black
                    colour = pixelColour
                    break
                
            elements[md5sum]=glyphCode,colour  
        
        internalMap.append((x,y,md5sum,glyphCode))
        outputUTF+=chr(elements[md5sum][0]).decode('cp437').encode('utf-8')
        outputHTMLplain+="<font color='"+RGBToHTMLColor(elements[md5sum][1])+"'>"+chr(elements[md5sum][0]).decode('cp437').encode('ascii', 'xmlcharrefreplace')+"</font>"
        outputHTMLimg+="<img src='"+legendSave+md5sum+".bmp"+"' style='border:none; margin:0px; padding:0px;'/>"
        x+=1
    outputUTF+="\n"
    outputHTMLplain += "\n"
    outputHTMLimg += "<br/>"    
    y+=1
    #print x+y
    pbar.update(x+y)

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

pbar.finish()
sys.stdout.write('Finished\n')
