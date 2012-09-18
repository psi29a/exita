"""
Part of the Exita project.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
02110-1301 USA
"""

from cx_Freeze import setup, Executable

includes = ['encodings.cp437', 'encodings.utf_8', 'encodings.ascii']
excludes = []
packages = []
path = []

mapMaker = Executable( 
    # what to build
    script = "exita.py",
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
        name = "Exita",
        version = "0.2",
        description = "Exports character based images to ascii",
        options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path
                             }
               },

        executables = [exita]
 )