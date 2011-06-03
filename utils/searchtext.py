#-*-coding: utf-8 -*-
from django.db import connection
from laws import models

#Takes a search string as an argument (e.g. 'motor vehicles') and returns a list of the SectionList.id that match that query

def searchtext_FTS4(query):
    cursor = connection.cursor()
    cursor.execute("SELECT slug FROM sectionsearch WHERE body MATCH %s", (query,))
    results = cursor.fetchall()
    return results

def searchtext_sphinx(query):
    results = models.SectionFileIndex.search.query(query).set_options(
                passages=True, passages_opts={'before_match':"<font style='font-weight: bold'>",'after_match':'</font>','around':6,},
                weights = { # individual field weighting
                    'sectionfile': 0,
                    'code': 0,
                    'text': 100,
                    'url': 0,
                },
                mode = 'SPH_MATCH_EXTENDED2',
                rankmode = 'SPH_RANK_SPH04',
)
    return results
