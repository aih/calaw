#!/usr/bin/env python

import os, sys, re, subprocess
from subprocess import PIPE, Popen

#def changename():
a=b=2
if a == b:    
#TODO: Remember to replace filespath with the folder that holds the legislation files
    filespath = "/Users/tabulaw/Documents/workspace/calawscode/media/cacode2"
    #Seed codeinput with first Code name.  This should not be strictly necessary.
    codeinput = "bpc"
    #Find makes a list of all files in the directory; ignoring files that start with '.'
    cmd = "find "+filespath+" ! -iname '.*' -print"
    fileslist = Popen(cmd, shell=True, stdout=PIPE)
    for file in fileslist.stdout.readlines():
        file = file.strip()
        #remove the path, leaving only the file name
        filename = file.rsplit('/',1)[1]
        if os.path.isfile(file):
            fullfilenamenew = file + "-" + codeinput
            filenamenew = filename + "-" + codeinput
            print filename + " to " + filenamenew
            Popen("mv "+file+" "+fullfilenamenew, shell=True,)
            # Runs bash commands and channels output to the PIPE output
        elif len(filename)<5:
            codeinput = filename
