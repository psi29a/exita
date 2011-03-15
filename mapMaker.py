#!/usr/bin/python
# Export from an image map information based on system characters such cp437.

import os, errno, sys, getopt
from PIL import Image
from hashlib import md5
from progressbar import ProgressBar, Percentage, ETA

def mkdir_p(path):
    """ python version of mkdir -p """
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

def usage():
    print """Usage: mapMaker.py options file
 Takes any character based image, such as a map, and covert it into 
 human/machine parsable parts.
  
Options:
    -c  int     : Code page to use for decoding image, default is "cp437"
    -s  string  : Size of character set, default is "8,12"
    -g  int     : Number of glyps in code page, default is "256"
    -o  string  : Output method: txt, html, htmimg, csv and all, default is "all"
    -f  string  : "/location/to/file" to be processed
    -h  --help  : Prints this help message
 
Examples:
./mapMaker.py -f /opt/df/worldMap.bmp
./mapMaker.py -c cp437 -g 256 -o all -f /opt/df/worldMap.bmp

"""

# default parameters 
inputFile = ""
codePage = "cp437"
glyphSize = [8,12]
glyphs = 256
outputType = "all"

# parse our options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hc:s:g:o:f:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts: 
    if opt in ("-c"):
        codePage = arg
    elif opt in ("-s"):
        glyphSize = eval("["+arg+"]")
    elif opt in ("-g"):
        glyphs = arg
    elif opt in ("-o"):
        outputType = arg
    elif opt in ("-f"):
        inputFile = arg
    elif opt in ("-h", "--help"):
        usage()
        sys.exit()
    else:
        usage()
        sys.exit(2)        
        
# some sanity checking
if os.path.exists(inputFile):
    workingDir = os.path.dirname(arg)+os.sep
    workingFile = os.path.basename(arg)
    legendSave = workingDir+"legend"+os.sep
else:
    usage()
    sys.exit("The file: "+inputFile+" does not exist.")

if len(glyphSize) == 2:
    glyphMap = os.getcwd()+os.sep+"fonts"+os.sep+codePage+"-"+"x".join(map(str,glyphSize))+".pbm"
else:
    usage()
    sys.exit("Your code page (glypsh) size is incorrect.")
    
if not os.path.exists(glyphMap):
    usage()
    sys.exit("The file: "+glyphMap+" does not exist. Please check your fonts directory.")


# setup environment
mkdir_p(legendSave)

# import map image
mapObject = Image.open(workingDir+workingFile)
mapSize = mapObject.size

# import font image
glyphObject = Image.open(glyphMap)
glyphObjectSize = glyphObject.size
glyphElements = []
for y in range(0,glyphObjectSize[1],glyphSize[1]):
    for x in range(0,glyphObjectSize[0],glyphSize[0]):
        if len(glyphElements) < glyphs:
            glyphElements.append(glyphObject.crop([x,y,x+glyphSize[0],y+glyphSize[1]]))

# parse elements from image map
elements = elementsGlyph = {}
internalMap = []
outputUTF = ""
outputHTMLplain = "<body style='background-color:#000000'><pre>\n"
outputHTMLimg = "<p style='width:2056px;'>"

# setup progressbar
widgets = ['Processing: ', Percentage(), ' ', ETA() ]
pbar = ProgressBar(widgets=widgets, maxval=(mapSize[1]/glyphSize[1]+1)*(mapSize[0]/glyphSize[0])+1)

x = y = 0
for offsetY in range(0,mapSize[1],glyphSize[1]):
    for offsetX in range(0,mapSize[0],glyphSize[0]):
        # get offsetX,offsetY
        element = mapObject.crop([offsetX,offsetY,offsetX+glyphSize[0],offsetY+glyphSize[1]])
        md5sum = md5(str(list(element.getdata()))).hexdigest()
        # if map element is unique, export
        if not elements.has_key(md5sum):
            element.save(legendSave+md5sum+".bmp")
            # if map element matches supplied font file, export extra details
            foundFont = False
            glyphCode = 0;
            colour = (0,0,0)
            for glyphElement in glyphElements:
                # since our font glyphs are in black and white (1bit), we need
                # convert the map glyph from 24-bit colour to grayscale, then
                # from grayscale to (1bit) using point function to take anything
                # not black and set to white.
                if list(glyphElement.getdata()) == list(element.convert("L").point(lambda i: i * 20,"1").getdata()):
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
    
fileObject = open(workingDir+workingFile+".txt","w")
fileObject.write(outputUTF)
fileObject.close()

fileObject = open(workingDir+workingFile+".html","w")
fileObject.write(outputHTMLplain)
fileObject.close()

fileObject = open(workingDir+workingFile+".htm","w")
fileObject.write(outputHTMLimg)
fileObject.close()

pbar.finish()
sys.stdout.write('Finished\n')
