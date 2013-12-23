#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',


    #API Calls (these return JSON). ------------------------------------------
    url(r'api/test-credentials',  api_test_credentials,
            name='api-test-credentials'),
    url(r'api/user/create', api_user_create,  name='api_user_create'),
    #TODO
    #url(r'api/user/read', api_read_user,  name='api_read_user'),
    #url(r'api/user/update', api_update_user,  name='api_update_user'),
    #url(r'api/user/delete', api_delete_user,  name='api_delete_user'),
    
    #Regular old views that require csrf token -------------------------------
    
    url(r'user/create',   user_create,    name='user_create'),
    url(r'user/update',   user_update,  name='user_update'),
    url(r'user/password', user_password,  name='user_password'),
    #url(r'user/delete',    delete_user,  name='delete_user'),

    
    #Login.Logout of the web interface
    url(r'login',  simple_email_login, name='login'),
    url(r'logout', simple_logout,  name='logout'),
    
    
    url(r'account-already-in-use/',
        TemplateView.as_view(template_name='accounts/already-in-use.html'),
        name='accounts_already_in_use'),
    
    
    
    #TODO
    
  
    
    #url(r'update',   update_user,  name='update_user'),
    #url(r'delete', delete_user,  name='delete_user'),
    
    )