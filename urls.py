from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from laws.views import * 
from django.contrib import admin
import os

admin.autodiscover()

# Set up the databrowse application
from django.contrib import databrowse
from laws.models import Code, SectionFile, Section

#databrowse.site.register(Code)
#databrowse.site.register(SectionFile)
#databrowse.site.register(Section)

admin.site.register(Code)
admin.site.register(SectionFile)
admin.site.register(Section)


handler404 = 'calaw.laws.views.my404'

urlpatterns = patterns('',
    # Example:
    # (r'^calaw/', include('calaw.foo.urls')),
    
    # Target urls:
      (r'^laws/target/.*?', 'laws.views.target_remove'),

    # Statutes:
      (r'^laws/CODE-(?P<codename>[a-z]{3,4})-(?P<target_section>[0-9.]*)/?', 'laws.views.target_to_section'),

    # Code tables of contents:
      (r'^laws/C(?:ODE|ode)-(?P<codename>[a-z]{3,4})/?', 'laws.views.code_toc'),

    # Enamble admin documentation:
      (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Enable the admin:
      (r'^admin/', include(admin.site.urls)),
    
    # Allow browsing of the data
    #  (r'^databrowse/(.*)', 'databrowse.site.root'),

    # Search page and results
       (r'^search/?$', 'laws.views.search'),

    # Search page and results
       (r'^searchtest/?$', 'laws.views.search2'),
    
    # Robots directive
    url(r'^robots.txt$', 'direct_to_template', {'template': 'robots.txt'}, name='robots.txt'),
    
    # Default to the index
       (r'^', 'laws.views.codes_index'),
)
