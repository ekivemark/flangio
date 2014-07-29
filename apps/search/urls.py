#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..accounts.decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    #return JSON
    url(r'^search.json$', login_required(search_json), name="search_json"),
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/search.json$',
         login_required(search_json), name="search_json_w_params"),
    
    
    
    #return CSV
    url(r'^search.csv$',  login_required(search_csv), name="search_csv"),
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/search.csv$',
         login_required(search_csv), name="search_csv_w_params"),
    

    
    #return HTML Table
    url(r'^search.html$',  login_required(search_html), name="search_html"),
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/search.html$',
         login_required(search_html), name="search_html_w_params"),


    
    url(r'^run-saved-search/(?P<slug>\S+)/(?P<skip>[^/]+)/(?P<limit>[^/]+)$',
                    login_required(run_saved_search_by_slug),
                    name="run_saved_search_by_slug"),


    #url(r'^run-saved-search/(?P<slug>[^.]+).(?P<output_format>\S+)$',
    #                login_required(run_saved_search_by_slug),
    #                name="run_saved_search_by_slug"),
    
    
    #url(r'^run-saved-search/(?P<slug>\w+).(?P<output_format>\S+)$',
    #                login_required(run_saved_search_by_slug),
    #                name="run_saved_search_by_slug"),
    
    
    url(r'^run-saved-search/(?P<slug>\S+)$',
                    login_required(run_saved_search_by_slug),
                    name="run_saved_search_by_slug"),
    
   
    url(r'^edit-saved-search/(?P<slug>\S+)$',
                    login_required(edit_saved_search_by_slug),
                    name="edit_saved_search_by_slug"),
    
    url(r'^delete-saved-search/(?P<slug>\S+)$',
                    login_required(delete_saved_search_by_slug),
                    name="delete_saved_search_by_slug"),
    
    url(r'^create-saved-search$', login_required(create_saved_search),
                    name="create_saved_search"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/create-saved-search$',
         login_required(create_saved_search), name="create_saved_search_w_params"),
    
    
    url(r'^complex-search$',
        login_required(complex_search), name="complex_search"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/complex-search$',
         login_required(complex_search), name="complex-search"),
    
    url(r'^saved-searches$', login_required(display_saved_searches),
                    name="saved_searches"),
    
    url(r'^build-keys', login_required(build_keys),
                    name="search_build_keys"),
    
    url(r'^custom-report', login_required(custom_report),
                   name="custom_report"),
    
    url(r'^data-dictionary', login_required(data_dictionary),
                    name="data_dictionary"),
    
    url(r'^load-labels-from-data-dictonary', login_required(load_labels),
                    name="load_labels"),
    
    
    #API CALLS -------------------------------------------------------------    


    # search for all get all features that match the search dict
    #return JSON
    url(r'^api/search.json$', json_login_required(search_json),
        name="api_search_json"),
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/search.json$',
         json_login_required(search_json), name="api_search_json_w_params"),
    
    #return CSV
    url(r'^api/search.csv$',  json_login_required(search_csv),
        name="api_search_csv"),
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/search.csv$',
         json_login_required(search_csv), name="api_search_csv_w_params"),

 
    #return HTML Table
    url(r'^api/search.html$',  json_login_required(search_html),
        name="api_search_html"),
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/search.html$',
         json_login_required(search_html), name="api_search_html_w_params"),
    
    url(r'^api/run-saved-search/(?P<slug>\S+)$',
        json_login_required(run_saved_search_by_slug),
        name="run_saved_search_by_slug"),
    
    url(r'^api/complex-search$',
        json_login_required(csrf_exempt(complex_search)),
        name="api_complex_search"),
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/complex-search$',
         json_login_required(csrf_exempt(complex_search)), name="api_complex_search"),

    )