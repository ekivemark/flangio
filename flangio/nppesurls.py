from django.conf.urls import patterns, include, url
from django.conf import settings
from apps.home.views import home_index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.mongodb.views import showdbs
from django.contrib.auth.decorators import login_required



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


    #Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    #to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    #url(r'^api/', include('flangio.versionsurls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^nppes/',      include('apps.nppes_write.urls')),
    url(r'^accounts/',   include('apps.accounts.urls')),
    url(r'^search/',     include('apps.search.urls')),
    url(r'^socialgraph/', include('apps.socialgraph.urls')),
    url(r'^mongodb/',   include('apps.mongodb.urls')),
    url(r'^import/',        include('apps.dataimport.urls')),
    url(r'^$', login_required(showdbs), name="home"),

    )
urlpatterns += staticfiles_urlpatterns()


