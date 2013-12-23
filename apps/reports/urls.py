#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.views.generic.simple import direct_to_template
from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns('',


    url(r'execute/xls/(?P<pk>[\w-]+)$', execute_report_xls, name='execute-report-xls'),
    url(r'execute/csv/(?P<pk>[\w-]+)$', execute_report_csv, name='execute-report-csv'),
    url(r'execute/json/(?P<pk>[\w-]+)$', execute_report_json, name='execute-report-json'),


    url(r'create/$', ReportCreate.as_view(), name='create-report'),
    
    url(r'delete/(?P<pk>\d+)$', delete_report,
       name='delete-custom-report'),
    
    url(r'update/(?P<pk>[\w-]+)$', ReportUpdate.as_view(),
       name='edit-report'),
    
    
    
    url(r'$', ReportList.as_view(), name='list-reports'),
    
)