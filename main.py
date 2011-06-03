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
from MakeRList import makeRList
from loaddb import *

def main():
    # Compiles regex substitutions
    regfile = './sectionlist.txt'
    rlist = makeRList(regfile)
    findreplace = [(re.compile(pattrn,re.U|re.M), replacement) for pattrn, replacement in rlist]
    
    
    #TODO: Remember to replace filespath with the folder that holds the legislation files
    filespath = "/Users/tabulaw/Documents/workspace/calawcode/media/cacode2"
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
            print "THE FILE IS:"+file 
            # Runs bash commands and channels output to the PIPE output
            parsedfile = Popen("ssed -R -e 's/^1. /ONE. /' " + file + " | txt2html --explicit_headings --indent_par_break --make_tables --make_anchors --xhtml | ssed -R -e 's/^<p>ONE. /<p>1. /' | ssed -R -n -f secparse.sed | ssed -R -f secparse2.sed", bufsize=-1, stdout=PIPE, shell=True)
    
            # Gets data from the stdout of the process above; this comes from the pipe, since stdout=PIPE was set
            # Popen.communicate()[0] is the stdout and Popen.communicate()[1] is the stderror
            parsedfile = parsedfile.communicate()
            parsedfile = parsedfile[0]
    
            # Further parses the output, with the Regex patterns in findreplace and writes the parsed data to a file
            parsedfile = subfile(parsedfile, findreplace)
            # Use loaddb functions to save the sections in parsedfile to the db  
            saveSectionData(codeinput, filename, parsedfile)
    
        # Save the parsed file to file.html
        #    file = filename + ".html"
            print ' saving to db:', file
        #    print ' writing:', file
        #    with open("./"+file,'w') as f:
        #        f.write(parsedfile)
        elif len(filename)<5:
            codeinput = filename
    
