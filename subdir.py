# -*- coding: utf-8 -*-
# Python

# find and replace in a dir by multiple pairs of regex

import os, sys,shutil,re

# replaces all strings by a regex substitution, using the list of pattrn/replacement tuples provided in frlist (a list of tuples)
def subfile(parsedfile, findreplace):

    numRep= []
    for couple in findreplace:
        outtext = re.subn(couple[0],couple[1], parsedfile)
        parsedfile=outtext[0]
        # TODO: Here is a place and save sections of outtext to db--using loaddb.py

        numRep.append(outtext[1])
        print 'substituted:', numRep[-1]
    return parsedfile
