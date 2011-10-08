#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
from os import environ
import lxml.html
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.contrib.sessions.models import *
from django.db import connection, transaction

from laws.models import *

cursor = connection.cursor()

j = SectionFile.objects.all()
iterr = 1
print 'starting loop'
for i in j:
    if iterr%100==0 :
        print iterr
    # strips sections of HTML; consider also stripping stop words 
    t = lxml.html.fromstring(i.text)
    txt = t.text_content()
    cursor.execute("INSERT INTO sectionsearch (slug, body) VALUES (%s, %s)", (i.id, txt))
    iterr += 1

transaction.commit_unless_managed()
