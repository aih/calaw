#Python
# To remove all newlines that break up a title:
# May need to repeat this, if a title is broken up over more than two lines
#find ./toc_raw2/* | xargs ssed -R -i -e :a -e '$!N; s_\n_@_;ta' 
#find ./toc_raw2/* | xargs ssed -R -i -e :a -e '$!N; s_@(\s*\w+\s((\d+[a-z]?\.)+))_\n\1_;ta'
#find ./toc_raw2/* | xargs ssed -R -i -e 's_@\s+_ _'
#find ./toc_raw2/* | xargs ssed -R -i -e 's_@+_\n_g'

#To separate the fields
#ssed -R -e "s_^(\s*\w+)\s((?:\d+\w?\.)+)\s+([A-Z][A-Za-z\-\;\:\,\' ]+(?:[12][019]\d{2})?)\s?(?:\.{2,})?\s*((?:\d+\.?)+)?_@\1@\2@\3@\4@_"

import re
filepath = '/Users/tabulaw/Documents/workspace/calaw/templates/toc_parsed_a/bpc_table_of_contents'
# Want to save:
# [code, parents, depth, level_name (e.g. 'Article'), level_number, startpage]
 
items = []
def main():
    parents = maybe_parents = last_parents = ''
    # Open file
    with open(filepath, 'rb') as file:
        file_all = file.read()        
        for each_line in file_all:
            items = each_line.split('@')
            try:
                depth = len(items[0])
                level_name = items[1].strip()
                level_number = items[2].strip()
                title = items[3].strip()
                if Depth < lastDepth:
                    last_depth = Depth
                    last_parents = maybe_parents
                    parents = parents + '>>' + last_parents
                maybe_parents = parents
                startpage = items[4].strip()
            except:
                pass
           # Check items to make sure they make sense 
main()
#Wherever there is a CODE-this-###:
# Title name, CODE-this-###

