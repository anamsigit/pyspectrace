# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 16:25:46 2019

@author: Ocean Insight Inc.
"""

import os
import getpass
import platform
import os.path

user=getpass.getuser()
user_home=os.path.expanduser("~"+user)
program_data = os.path.normpath("./oceandirect")
os_platform = platform.system()

## Change the path name here
if os_platform == 'Darwin':
    #For OSX, make sure that OCEANDIRECT_HOME points to the ./lib folder.
    oceandirect_libname=("liboceandirect.dylib")
elif os.name == 'nt':
    #For windows, make sure that OCEANDIRECT_HOME points to the ./lib folder.
    oceandirect_libname=("OceanDirect.dll")
else:
    #For linux, make sure that LD_LIBRARY_PATH and OCEANDIRECT_HOME points to the ./lib folder.
    oceandirect_libname=("liboceandirect.so")

module_path=os.path.dirname(__file__)
oceandirect_dll = module_path + os.path.normpath("/lib/"+oceandirect_libname)

#oceandirect_dll = os.path.normpath(program_data+"/lib/"+oceandirect_libname)
#print("oceandirect_dll: ", oceandirect_dll)
