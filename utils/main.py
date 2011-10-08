# Python
# run popCode() then main()

import os, sys, re, subprocess, fnmatch
import pickle
from subprocess import PIPE, Popen
from lxml import html, etree
from lxml.cssselect import CSSSelector as cs
from laws import models

# Settings
regfile = './utils/sectionlist.txt'

# Folder that holds the legislation files
pathin = "./media/cacodegit/"
divisions = cs('div')

def unix_find(pathin):
    """Return results similar to the Unix find command run without options
    i.e. traverse a directory tree and return all the file paths
    """
    for root, dirs, files in os.walk(pathin):
        for filename in [filename for filename in files if not fnmatch.fnmatch(filename, '.*')]:
                yield os.path.join(root, filename) 


# Populate the Code table
codedictpath = './utils/codedict'
codedict = pickle.load(open(codedictpath,'rb'))
def popCode(codedict):
    for codeabbr in codedict:
        code_current = models.Code(
            name = codeabbr,
            fullname = codedict[codeabbr],
            url = '/laws/target/'+codeabbr+'/'
        )   
        code_current.save()


def subfile(parsedfile, findreplace):
    """ replaces all strings by a regex substitution, 
    using the list of pattrn/replacement tuples provided in frlist (a list of tuples)
    """
    numRep= []
    for couple in findreplace:
        outtext = re.subn(couple[0],couple[1], parsedfile)
        parsedfile=outtext[0]
        numRep.append(outtext[1])
        # print 'substituted:', numRep[-1]
    return parsedfile
    

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

def parsefile(filepath, findreplace):
    # Runs bash commands and channels output to the PIPE output
    parsedfile = Popen("ssed -R -e 's/^1\. /ONE. /' " + filepath + " | txt2html --explicit_headings --indent_par_break --make_tables --make_anchors --xhtml | ssed -R -e 's/^<p>ONE. /<p>1. /' | ssed -R -n -f ./utils/secparse.sed | ssed -R -f ./utils/secparse2.sed", bufsize=-1, stdout=PIPE, shell=True)
    # Gets data from the stdout of the process above; this comes from the pipe, since stdout=PIPE was set
    # Popen.communicate()[0] is the stdout and Popen.communicate()[1] is the stderror
    parsedfile = parsedfile.communicate()
    parsedfile = parsedfile[0]
    
    # Further parses the output, with the Regex patterns in findreplace and saves the parsed data to a db
    parsedfile = subfile(parsedfile, findreplace)
    return parsedfile

def getSectionsHTML(inputfiletext):
    """ Save each section of the codes to the db
    """

    tree = html.document_fromstring(inputfiletext) 
    # creates a list of the div elements of the document
    sections = divisions(tree)
    #creates a list of tuples for each section: section number and html content
    sections_html = [(section.get("id"), etree.tostring(section)) for section in sections]         
    return  sections_html

def saveSectionFile(codeinput, filename, inputfiletext):
    code_instance = models.Code.objects.get(name = codeinput)
    sectionfile_current = models.SectionFile(
        code= code_instance,
        sectionfile = filename,
        url = code_instance.url + filename + '/',
        text = inputfiletext
    )
    sectionfile_current.save() 
    return sectionfile_current

def saveSections(codeinput, sections, sectionfile_current):
    code_instance = models.Code.objects.get(name = codeinput)
    for section in sections:
        if section[0] is not None:
            secnm = section[0].split("-")[1]
        else:
            #Set section number to -1 for non-section text (e.g. headings)
            secnm = -1

        section_current = models.Section(
            code = code_instance,
            secnumber = secnm,
            sectionfile = sectionfile_current,
            text = section[1]
        )
        section_current.save()

def saveSectionData(codename, filename, inputfiletext):
    sections_html = getSectionsHTML(inputfiletext)
    sectionfile_current = saveSectionFile(codename, filename, inputfiletext)
    saveSections(codename, sections_html, sectionfile_current)   

def main(pathin = pathin, regfile = regfile):
    #popCode(codedict)
    findreplace = rcompile(regfile)
    codes = [dir for dir in os.listdir(pathin) if dir[0] is not '.']
    for codename in codes:
        print 'Parsing: ' + codename
        with open(pathin+codename+'-combined', 'wb') as codefile:
            fileslist = unix_find(pathin+codename+'/')
            for filepath in fileslist:
                codeandfile = filepath.split(pathin)[1]

                try:
                    # print "PARSING: " + codeandfile 
                    parsedfile = parsefile(filepath, findreplace)
                except:
                    print "Trouble parsing the file: " + codeandfile
                
                try:
                    codefile.write('<!-- '+ codeandfile+'-->\n'+parsedfile)
                except:
                    print "Trouble writing to the file object."

        # Use loaddb functions to save the sections in parsedfile to the db  
        # saveSectionData(codename, filename, parsedfile)

if __name__ == '__main__':
    main()
