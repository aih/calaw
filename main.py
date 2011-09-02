# Python
# Save Code sections to db using utils.loaddb.popCode, then
# Used to run this file with: find . -exec python ./main.py "{}" \;
# Now, instead, Run:
# commandline: python manage.py syncdb
# python manage.py shell
# from loaddb import *
# popCode()
# from main import main
# main()

import os, sys, re, subprocess
from subprocess import PIPE, Popen
from subdir import subfile
from loaddb import *

# Settings
regfile = os.path.abspath(os.path.dirname(__file__))+'/sectionlist.txt'

#Folder that holds the legislation files
path = os.getcwd() +"/calawcode/media/cacode2"
#TODO: do not include files that start with '.'
fileslist = os.listdir(path)

def makeRList(file):
    a = open(file,'rb')
    rlist = []
    for eachline in a:
        b = eachline.strip().split('@')
        c = tuple(b)
        rlist.append(c)
    a.close()
    return rlist

def rcompile(regfile):
    rlist = makeRList(regfile)
    findreplace = [(re.compile(pattrn,re.U|re.M), replacement) for pattrn, replacement in rlist]
    return findreplace

def main(path, fileslist):
    for file in fileslist.stdout.readlines():
        file = file.strip()
        #remove the path, leaving only the file name
        filename = file.rsplit('/',1)[1]
        if os.path.isfile(file):
            print "THE FILE IS:"+file 
            # Runs bash commands and channels output to the PIPE output
            parsedfile = Popen("ssed -R -e 's/^1. /ONE. /' " + file + " | txt2html --explicit_headings --indent_par_break --make_tables --make_anchors --xhtml | ssed -R -e 's/^<p>ONE. /<p>1. /' | ssed -R -n -f secparse.sed | ssed -R -f secparse2.sed", bufsize=-1, stdout=PIPE, shell=True)
    
            # Gets data from the stdout of the process above; this comes from the pipe, since stdout=PIPE was set
            # Popen.communicate()[0] is the stdout and Popen.communicate()[1] is the stderror
            parsedfile = parsedfile.communicate()
            parsedfile = parsedfile[0]
    
            # Further parses the output, with the Regex patterns in findreplace and saves the parsed data to a db
            parsedfile = subfile(parsedfile, findreplace)
            # Use loaddb functions to save the sections in parsedfile to the db  
            saveSectionData(codeinput, filename, parsedfile)
    
        elif len(filename)<5:
            codeinput = filename
    
