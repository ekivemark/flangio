#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import datetime
import io
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, CreateView
from django.core.urlresolvers import reverse
from models import Report
from django.http import HttpResponse
from utils import query_mongo_for_report
from ..transaction.views import search_xls, search_csv, search_json


@login_required
def execute_report_xls(request, pk):
    r =get_object_or_404(Report, pk=pk)
    #search mongo using a supplied JSON file
    request.GET = query_mongo_for_report(r.query)
    return search_xls(request)

@login_required
def execute_report_csv(request, pk):
    r =get_object_or_404(Report, pk=pk)
    #search mongo using a supplied JSON file
    request.GET = query_mongo_for_report(r.query)
    return search_csv(request)
    
    
@login_required
def execute_report_json(request, pk):
    r =get_object_or_404(Report, pk=pk)
    #search mongo using a supplied JSON file
    request.GET = query_mongo_for_report(r.query)
    return search_json(request)



@login_required
def delete_report(request, pk):

    get_object_or_404(Report, pk=pk).delete()
    messages.success(request, 'The report has been deleted successfully')
    return redirect('list-reports')

class ReportList(ListView):
    model = Report
    template_name = 'reports/list.html'
    context_object_name = 'reports'
    
class ReportUpdate(UpdateView):
    model               = Report
    template_name       = 'reports/edit.html'
    context_object_name = 'reports'
    success_url         = '/reports/'


class ReportCreate(CreateView):
    model               = Report
    template_name       = 'reports/edit.html'
    context_object_name = 'reports'
    success_url         = '/reports/'
