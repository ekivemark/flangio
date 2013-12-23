#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..accounts.decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',

    url(r'^$', showdbs, name="show_dbs"),
    
    url(r'^new-database$', create_new_database, name="create_new_database"),

    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/clear$',
         login_required(clear_collection), name="clear_collection"), 
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/drop$',
         login_required(delete_collection), name="delete_collection"), 

    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/ensure-index$',
         login_required(simple_ensure_index), name="simple_index_create"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/delete$',
         login_required(remove_data_from_collection), name="remove_data_from_collection_w_params"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/create$',
         login_required(create_document_in_collection), name="create_document_in_collection_w_params"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/update$',
        login_required(update_document_in_collection), name="update_document_in_collection_w_params"),
    
    url(r'^database/(?P<database_name>[^/]+)/drop$',
         login_required(drop_database), name="drop_database"),

    url(r'^database/(?P<database_name>[^/]+)/create-collection$',
         login_required(create_collection), name="create_collection"),
    
    #API calls ----------------------------------------------------------------
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/clear$',
         json_login_required(clear_collection), name="api_clear_collection"), 
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/drop$',
         json_login_required(delete_collection), name="api_delete_collection"), 
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>\[^/]+)/ensure-index$',
         json_login_required(csrf_exempt(simple_ensure_index)), name="api_simple_index_create"),

    url(r'^api/database/(?P<database_name>[^/]+)/drop$',
         json_login_required(drop_database), name="api_drop_database"),

    url(r'^api/database/(?P<database_name>[^/]+)/create-collection$',
         json_login_required(create_collection), name="api_create_collection"),    

    )