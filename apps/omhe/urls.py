#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'create', create_transaction,  name='create_transaction'),
    url(r'^update/$', update_transaction, name="update_transaction"),
    
    
    # search for all get all features that match the search dict
    #return JSON
    url(r'^search.json$', search_json, name="search_json"),
    
    #return CSV
    url(r'^search.csv$', search_csv, name="search_csv"),
    
    #return Excel
    url(r'^search.xls$', search_xls, name="search_xls"),
    
    #return XML
    url(r'^search.xml$', search_xml, name="search_xml"),
    
    #get a transaction by txid (returns a json object)
    url(r'^read/(?P<txid>[^.]+).json$', get_by_transaction_id,
        name="get_by_transaction_id"),
    
  
     
    
    #url(r'^build-keys', build_keys, name="search_build_keys"),
    
    #url(r'^custom-report', custom_report, name="custom_report"),
    
    #url(r'^data-dictionary', data_dictionary, name="data_dictionary"),
    
    #url(r'^load-labels-from-data-dictonary', load_labels,
    #    name="load_labels"),
    
    

    #get a transaction by txid (returns a json object)


    #Added a delete.
    url(r'^delete/$', delete_transaction,
        name="delete_transaction_id"),

    url(r'^since/(?P<sinceid>[^.]+).json$', get_since_id,
        name="get_since_id"),

    url(r'^my/(?P<txtype>.*)$', get_my_transactions_by_type,
        name="get_my_transactions"),


    )