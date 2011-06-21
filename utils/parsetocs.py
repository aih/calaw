#Python
# To Parse Tables of Content:
# 1. Remove all newlines that break up a title:
#    May need to repeat this, if a title is broken up over more than two lines
#find ./toc_raw2/* | xargs ssed -R -i -e :a -e '$!N; s_\n_@_;ta' 
#find ./toc_raw2/* | xargs ssed -R -i -e :a -e '$!N; s_@(\s*\w+\s((\d+[a-z]?\.)+))_\n\1_;ta'
#find ./toc_raw2/* | xargs ssed -R -i -e 's_@\s+_ _'
#find ./toc_raw2/* | xargs ssed -R -i -e 's_@+_\n_g'

# 2. Separate the fields
#ssed -R -e "s_^(\s*\w+)\s((?:\d+\w?\.)+)\s+([A-Z][A-Za-z\-\;\:\,\' ]+(?:[12][019]\d{2})?)\s?(?:\.{2,})?\s*((?:\d+\.?)+)?_@\1@\2@\3@\4@_"

# Save titles and parents (Division, Part, Chapter, etc.) to db

filespath = '/Users/tabulaw/Documents/workspace/calaw/tocs/toc_parsed_fields'
import os, sys, re, subprocess
from subprocess import PIPE, Popen
from laws.models import *
 
def parsetocs(filepath):
    items = []
    last_depth = 0
    level_number = 0
    title = ''
    code_title = filepath.rsplit('/',1)[-1].split('_',1)[0] 
    current_levels = [ code_title + ' >> ']
    # Open file
    with open(filepath, 'r') as file:
        for each_line in file:
            items = each_line.split('@')
            print items
            if len(items)>1:
                    depth = len(items[1]) - len(items[1].lstrip())
                    level_name = items[1].strip()
                    level_number = items[2].strip()
                    title = items[3].strip()
                    try:
                        startpage = items[4].strip()
                    except:
                        pass
                    current_level = level_name+' '+level_number+' '+title+' >> '
                    # Adjust for any change in hierarchy depth
                    if (depth < last_depth) | (depth == last_depth):
                        current_levels= current_levels[:(depth-last_depth-1)]
                    current_levels.append(current_level)
                    last_depth = depth
                    print current_levels
                    sfname = SectionFileName(
                                                name = current_level,
                                                parents = current_levels,
                                                sectionfile = SectionFile.objects.get(
                                                                                        section=Section.objects.get(
                                                                                                                    secnumber = startpage,
                                                                                                                    code = Code.objects.get(name = code_title)
                                                                                                                    )
                                                                                    )
                                            )
                    print sfname
                    #sfname.save()                     
def main():
    #Find makes a list of all files in the directory; ignoring files that start with '.'
    cmd = "find "+filespath+" ! -iname '.*' -print"
    print cmd
    fileslist = Popen(cmd, shell=True, stdout=PIPE)
    for filepath in fileslist.stdout.readlines():
        filepath = filepath.strip()
        if os.path.isfile(filepath):
            parsetocs(filepath)
        else:
            print filepath + ' is not a file!'
            pass
                    # print depth, level_name, level_number, title, startpage, current_levels 
