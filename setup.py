from cx_Freeze import setup, Executable

includes = ['encodings.cp437','encodings.utf_8','encodings.ascii']
excludes = []
packages = []
path = []

mapMaker = Executable(
    # what to build
    script = "mapMaker.py",
    initScript = None,
    #base = 'Win32GUI',
    #targetDir = r"dist",
    #targetName = "simplewx.exe",
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = None,
)

setup(
        name = "mapMaker",
        version = "0.1",
        description = "Exports character based image maps to text",
        options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path
                             }
               },

        executables = [mapMaker]
)

