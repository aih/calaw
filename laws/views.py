# -*- coding: utf-8 -*-
# CALaws 

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from laws import models 
from laws.models import SectionFile, SearchForm
from utils.searchtext import searchtext_sphinx, searchtext_FTS4
from utils.utils import *
from operator import itemgetter
from lxml import html, etree
from lxml.cssselect import CSSSelector as cs
import settings
            
bodysel = cs('body')

def target_remove(request):
        current_url = request.get_full_path()
        new_url = current_url.replace('target/','')
        return HttpResponseRedirect(new_url)

@render_to("code_display.html")
def target_to_section(request, codename, target_section):
        if codename == 'this':
            current_url = request.META['HTTP_REFERER']            
            codename = current_url.split('-')[1]
            #For Table of Contents, there is a trailing / that needs to be removed
            codename = codename.strip('/')
            print request.get_full_path()
            #Hack to ensure there is one, and only one './' at the end of the url
            new_url = request.get_full_path().rstrip('/').rstrip('.')+'./' 
            new_url = new_url.replace('this',codename) 
            return HttpResponseRedirect(new_url)
        else:
            code_current = models.Code.objects.get(name = codename)
            code_fn = code_current.fullname
            target_section = target_section.rsplit('.',1)[0]+'.'
            section_current = models.Section.objects.get(code = code_current, secnumber = target_section)
            #print section_current
            sectionfile = models.SectionFile.objects.get(section = section_current)
            tree_section = html.document_fromstring(sectionfile.text)
            body = etree.tostring(bodysel(tree_section)[0], pretty_print=False, method='html') # selects the body element of the document
            return locals()

def codes_index(request):
    searchform = SearchForm(request.POST)
    response = render_to_response('codelist.html', locals(), context_instance=RequestContext(request))
    return response

@render_to("code_display.html")
def code_toc(request, codename):
    searchform = SearchForm(request.POST)
    code_current = models.Code.objects.get(name = codename)
    code_fn = code_current.fullname
    code_toc = open(settings.PROJECT_PATH +'/templates/'+ 'tocs/' + codename + '_toc.html')
    tree_toc = html.document_fromstring(code_toc.read())
    code_toc.close()
    body = etree.tostring(bodysel(tree_toc)[0], pretty_print=False, method='html') # selects the body element of the document
    #response = render_to_response(codename+'_toc.html', locals(), context_instance=RequestContext(request))
    return locals() 

def my404(request):
    """
    We need this handler to populate some variables for flatpages
    """
    #user = get_user_object(request)
    #profile = get_profile_object(user)
    response = render_to_response('404.html', locals(), context_instance=RequestContext(request))
    response.status_code = 404
    return response

@render_to("search.html")
def search(request): 
    if request.method == u'POST':
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            query = searchform.cleaned_data['query']
            page_id = searchform.cleaned_data['page']
            #Sphinx search query; returns a list of dictionaries; options set for snippet excerpts
            #Limited by djangosphinx to 20 results, unless defaults are changed
            resultslist = searchtext_sphinx(query)
            total = len(resultslist)
            #queryids = searchtext_FTS4(query)
            resultsids = map(itemgetter('id'), resultslist)
            if len(resultsids)>0:
                try:
                    #Can also use .in_bulk(resultsids), but it seems a bit slower
                    # p_main = Paginator(all_results, 5)
                    # main_result = p_main.page(1) #page_id)
                    rpassages =[ (SectionFile.objects.get(id=r), resultslist._get_passages(
                                            instance=SectionFile.objects.get(id=r),
                                            fields=['text'],
                                            words=query)['text'])  for r in resultsids]
                except SectionFile.objects.in_bulk(resultsids)==None:
                    pass
            else:
                emptyquery = True 
    else:
        searchform = SearchForm(initial={"page":"1"})
    return locals()
