# Python

from lxml import html, etree
from lxml.cssselect import CSSSelector as cs
from laws import models
import pickle

# Populate the Code table
codedictpath = '/Users/tabulaw/Documents/workspace/calaw/codedict'
codedict = pickle.load(open(codedictpath,'rb'))
def popCode():
    for codeabbr in codedict:
        saveCode(codeabbr)

def saveCode(codeabbr):
    code_current = models.Code(
        name = codeabbr,
        fullname = codedict[codeabbr],
        url = '/laws/target/'+codeabbr+'/'
    )   
    code_current.save()

# Parse sections and save each to the db
divsel = cs('div')
def getSectionsHTML(inputfiletext):
    #a = open(inputfile)
    # Grabs the whole page 
    #inputfiletext = read(a)
    #a.close()
    #tree = html.parse(inputfiletext) 
    tree = html.document_fromstring(inputfiletext) 
    sections = divsel(tree) # creates a list of the div elements of the document
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

    # Save each section to the db
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

def saveSectionData(codeinput, filename, inputfiletext):
    sections_html = getSectionsHTML(inputfiletext)
    sectionfile_current = saveSectionFile(codeinput, filename, inputfiletext)
    saveSections(codeinput, sections_html, sectionfile_current)   
