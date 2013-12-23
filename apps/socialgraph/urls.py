#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'create', social_graph_create,  name='social_graph_create'),
    url(r'delete', social_graph_delete,  name='social_graph_delete'),
    
    )