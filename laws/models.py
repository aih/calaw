from django.db import models
from django import forms 
from djangosphinx.models import SphinxQuerySet

# Create your models here.
class Code(models.Model):
    name = models.CharField(max_length=4)
    fullname = models.CharField(max_length=255) 
    url = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name #self.title

class Section(models.Model):
    secnumber= models.CharField(max_length=10)
    text = models.TextField(null=True, blank=True)
    code = models.ForeignKey('Code')
    sectionfile = models.ForeignKey('SectionFile')
    def __unicode__(self):
        return self.secnumber #self.secnumber

class SectionFile(models.Model):
    sectionfile = models.CharField(max_length=20)
    code = models.ForeignKey('Code')
    text = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=255)
    sectionfilename = models.ForeignKey('SectionFileName', blank=True, null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return self.sectionfile #self.sectionfile

class SectionFileIndex(models.Model):
    sectionfile = models.CharField(max_length=20)
    code = models.ForeignKey('Code')
    text = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.sectionfile #self.sectionfile
    
    search = SphinxQuerySet(
        index = 'calaw1',
        weights = { # individual field weighting
            'sectionfile': 0,
            'code': 0,
            'text': 100,
            'url': 0,
        },
        mode = 'SPH_MATCH_EXTENDED2',
        rankmode = 'SPH_RANK_SPH04',
        #"Only_Sphinx" mode makes search independent from the db; necessary when using a db that is not supported by Sphinx (e.g. sqlite)
        #Found in a git branch of the djangosphinx code
        only_sphinx = True
    )
       
    class Meta:
        db_table = 'calaw1'

class SectionFileName(models.Model):
    name = models.CharField(max_length=255)
    parents = models.CharField(max_length=255)

    def __unicode__(self):
        return self.parents #self.name

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"right_btn", "onfocus":"$('#id_query').css('background','none'); var q=$('#id_query').val(); if (q=='Search...') {$('#id_query').val(''); $('#id_query').css('font-weight','bolder');}","onblur":"var q=$('#id_query').val(); \r\n if (q=='') {$('#id_query').val('Search...'); $('#id_query').css('font-weight','normal'); $('#id_query').css('background', 'transparent url(/site_media/img/icons/magnifier.png) no-repeat scroll right center'); } "}), initial="Search...", label="Search...")
    page = forms.IntegerField(widget=forms.HiddenInput())

