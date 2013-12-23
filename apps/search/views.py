#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import os, uuid, json
from django.conf import settings
from django.shortcuts import render_to_response,  get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from ..accounts.decorators import access_required
from ..accounts.models import Permission
from forms import SavedSearchForm, ComplexSearchForm
from ..utils import *

from models import SavedSearch
from xls_utils import convert_to_xls, convert_to_csv, convert_labels_to_xls, convert_to_rows
from dict2xml import dict2xml
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
import shlex


def build_keys(request):
    """Perform the map/reduce to refresh the keys form. The display the custom report screen"""
    x = build_keys_with_mapreduce()
    messages.success(request, "Successfully completed MapReduce operation. Key rebuild for custom report complete.")
    return HttpResponseRedirect(reverse("home_index"))



def prepare_search_results(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), query={}):
    if not query:
        kwargs = {}
        for k,v in request.GET.items():
            kwargs[k]=v
            if kwargs.has_key('limit'):
                limit=int(kwargs['limit'])
                del kwargs['limit']
            if kwargs.has_key('skip'):
                skip=int(kwargs['skip'])
                del kwargs['skip']
    else:
        kwargs = query

    result = query_mongo(kwargs, database_name, collection_name,
                         skip=skip, limit=limit,return_keys=return_keys)
    
    return result
    

@csrf_exempt
def custom_report(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION):
    ckeys = get_collection_keys()

    if request.method == 'POST':
        form = KeysForm(ckeys, get_collection_labels(), request.POST)
        if form.is_valid():
            return_keys=[]
            data = form.cleaned_data
            for k,v in data.items():
                if v==True:
                    return_keys.append(k)

            q = massage_dates(json.loads(data['query']))

            if data['outputformat']=="xls":
                return search_xls(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))
            elif data['outputformat']=="csv":
                return search_csv(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))
            elif data['outputformat']=="xml":
                return search_xml(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))
            else:
                return search_json(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))

        else:

            return render_to_response('search/select-keys.html', {'form': form},
                RequestContext(request))

    #Get the distinct keys from the collection
    ckeys = get_collection_keys()

    #get the labels
    label_dict = get_collection_labels()

    return render_to_response('search/select-keys.html',
         {'form': KeysForm(ckeys, label_dict),}, RequestContext(request))























def search_json(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), query={}):
    
    print database_name, collection_name
    
    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    if int(result['code'])==200:
        listresults=result['results']

    else:
        response = json.dumps(result, indent =4)
        return HttpResponse(response, status=int(result['code']),
                            mimetype="application/json")

    if settings.RESPECT_SOCIAL_GRAPH:
        listresults=filter_social_graph(request, listresults)


        len_results=len(listresults)
        if len_results < result['num_results']:
            result['ommitted-results']= result['num_results'] - len_results
            result['results']=listresults

        jsonresults=to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            mimetype="application/json")
    else:
        jsonresults=to_json(normalize_results(result))
        return HttpResponse(jsonresults, status=int(result['code']),mimetype="application/json")



def search_xml(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), query={}):

    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    if int(result['code'])==200:
        listresults=result['results']

    else:
        response = dict2xml({"flangio":result})
        return HttpResponse(response, status=int(result['code']),
                            mimetype="application/xml")

    if settings.RESPECT_SOCIAL_GRAPH:
        listresults=filter_social_graph(request, listresults)


        len_results=len(listresults)
        if len_results < result['num_results']:
            result['ommitted-results']= result['num_results'] - len_results
            result['results']=listresults

        xmlresults=dict2xml({"flangio":result})
        return HttpResponse(xmlresults, status=int(result['code']),
                            mimetype="application/xml")
    else:
        xmlresults=dict2xml({"flangio":normalize_results(result)})
        return HttpResponse(xmlresults, status=int(result['code']),
                            mimetype="application/xml")





def search_xls(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), query={}):

    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    if int(result['code']) == 200:
        listresults=result['results']

        if settings.RESPECT_SOCIAL_GRAPH:
            listresults = filter_social_graph(request, listresults)
            len_results = len(listresults)
            if len_results < result['num_results']:
                result['ommitted-results']= result['num_results'] - len_results

        keylist = []

        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)


        return convert_to_xls(keylist, normalize_list(listresults))

    else:
        jsonresults=to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            mimetype="application/json")



def search_csv(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), query={}):
    
    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    #print result.keys()

    if int(result['code']) == 200:
        listresults=result['results']
        if settings.RESPECT_SOCIAL_GRAPH:
            listresults = filter_social_graph(request, listresults)
            len_results = len(listresults)
            if len_results < result['num_results']:
                result['ommitted-results']= result['num_results'] - len_results

        keylist = []
        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)


        return convert_to_csv(keylist, listresults)

    else:
        jsonresults=to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            mimetype="application/json")



def search_html(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), query={}):
    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S UTC')    
    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    #print result.keys()

    if int(result['code']) == 200:
        listresults=result['results']
        if settings.RESPECT_SOCIAL_GRAPH:
            listresults = filter_social_graph(request, listresults)
            len_results = len(listresults)
            if len_results < result['num_results']:
                result['ommitted-results']= result['num_results'] - len_results

        keylist = []
        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)
        context ={"rows": convert_to_rows(keylist, listresults),
                  "timestamp": timestamp}
        
        return render_to_response('search/html-table.html',
                              RequestContext(request, context,))   


    else:
        jsonresults=to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            mimetype="application/json")








@csrf_exempt
def data_dictionary(request):

    if request.method == 'POST':
        form = DataDictionaryForm(request.POST)
        if form.is_valid():
            data = form.save()

            if data['outputformat']=="xls":
                return convert_labels_to_xls(data)

            else:
                response = json.dumps(data['labels'], indent =4)
                return HttpResponse(response, status=200,
                                    mimetype="application/json")
        else:
            #The form contained errors.
            return render_to_response('search/data-dictionary.html',
                                 {'form': form}, RequestContext(request))

    #A GET
    return render_to_response('search/data-dictionary.html',
         {'form': DataDictionaryForm()}, RequestContext(request))






@csrf_exempt
def load_labels(request):

    labels = get_labels_tuple()

    for i in labels:
        variable = strip_occurences(i[0])
        try:
            DataLabelMeta.objects.create(variable_name=variable,
                                          verbose_name=i[1],
                                          label=i[1],)
        except(IntegrityError):
            l =  DataLabelMeta.objects.get(variable_name=variable)
            l.verbose_name = i[1]
            l.label=i[1]
            l.question_text=i[1]
            l.save()
    return HttpResponse("OK")

    if request.method == 'POST':
        form = DataDictionaryForm(request.POST)
        if form.is_valid():
            data = form.save()

            if data['outputformat']=="xls":
                return convert_labels_to_xls(data)

            else:
                response = json.dumps(data['labels'], indent =4)
                return HttpResponse(response, status=200,
                                    mimetype="application/json")
        else:
            #The form contained errors.
            return render_to_response('search/data-dictionary.html',
                                 {'form': form}, RequestContext(request))

    #A GET
    return render_to_response('search/data-dictionary.html',
         {'form': DataDictionaryForm()}, RequestContext(request))





    




def run_saved_search_by_slug(request, slug, skip=0, limit = settings.MONGO_LIMIT):
    ss = get_object_or_404(SavedSearch,  slug=slug, user=request.user)
    
    not_int = False
    response_dict = {}
    try:
        skip = int(skip)
    except ValueError:
        response_dict['message']="Skip must be an integer."
        not_int = True
    try:
        limit = int(limit)
        
    except ValueError:
        response_dict['message']="Limit must be an integer."
        not_int = True
    if not_int:
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response = json.dumps(response_dict, indent =4)
        return HttpResponse(response, status=int(response_dict['code']),
                mimetype="application/json")
    
    
    
    try:
        query = json.loads(ss.query)
        print ss.query
    
    except ValueError:
        response_dict = {}
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']="Your query was not valid JSON."
        response = json.dumps(response_dict, indent =4)
        return HttpResponse(response, status=int(response_dict['code']),
                mimetype="application/json")
    
    
    #setup the list of keys for return if specified.
    key_list=()
    if ss.return_keys:  
        key_list = shlex.split(ss.return_keys)
    print ss.query, ss.database_name, ss.collection_name
    if ss.output_format=="json":
        
        return search_json(request, database_name=ss.database_name,
                           collection_name =ss.collection_name,
                           query = query, skip=int(skip), limit=int(limit),
                           return_keys= key_list)
    
    if ss.output_format=="xml":
        return search_xml(request,
                          database_name=ss.database_name,
                           collection_name =ss.collection_name,
                          query = query,
                           return_keys= key_list) 
    
    if ss.output_format=="html":
        return search_html(request,
                          database_name=ss.database_name,
                          collection_name =ss.collection_name,
                          query = query,
                          return_keys= key_list) 
    

    if ss.output_format=="csv":
        return search_csv(request,
                          database_name=ss.database_name,
                           collection_name =ss.collection_name,
                          query = query,
                           return_keys= key_list)
    
    if ss.output_format=="xls":
        return search_xls(request,
                          database_name=ss.database_name,
                          collection_name =ss.collection_name,
                          query = query,
                          return_keys= key_list)
    
    #these next line "should" never execute.
    response_dict = {}
    response_dict['num_results']=0
    response_dict['code']=500
    response_dict['type']="Error"
    response_dict['results']=[]
    response_dict['message']="Oops something has gone wrong.  Please contact a systems administrator."
    response = json.dumps(response_dict, indent =4)
    return HttpResponse(response, status=int(response_dict['code']),
                            mimetype="application/json")



def create_saved_search(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                        skip=0, limit=200, return_keys=()):
    name = _("Create a Saved Search")
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            ss = form.save(commit = False)
            ss.user = request.user
            ss.save()
                
            return HttpResponseRedirect(reverse('saved_searches'))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
            
   #this is a GET
    

    idata ={'database_name': database_name,
            'collection_name': collection_name}
    
    
    context= {'name':name,
              'form': SavedSearchForm(initial=idata)
              }
    return render_to_response('generic/bootstrapform.html',
                             RequestContext(request, context,))
    
    
    
def complex_search(request, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                        skip=0, limit=200, return_keys=()):
    name = _("Run a Complex Search")
    if request.method == 'POST':
        form = ComplexSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                query = json.loads(query)
            except ValueError:
                #Quert was not valid JSON ------------------
                response_dict = {}
                response_dict['num_results']=0
                response_dict['code']=400
                response_dict['type']="Error"
                response_dict['results']=[]
                response_dict['message']="Your query was not valid JSON."
                response = json.dumps(response_dict, indent =4)
                return HttpResponse(response, status=int(response_dict['code']),
                                    mimetype="application/json")
            #Query was valid JSON    
            if form.cleaned_data['output_format']=="json":
                return search_json(request, query = query)
            if form.cleaned_data['output_format']=="xml":
                return search_xml(request, query = query) 
            if form.cleaned_data['output_format']=="csv":
                return search_csv(request, query = query)
            if form.cleaned_data['output_format']=="xls":
                return search_xls(request, query = query)
            
            #these next line "should" never execute, but here just in case.
            response_dict = {}
            response_dict['num_results']=0
            response_dict['code']=500
            response_dict['type']="Error"
            response_dict['results']=[]
            response_dict['message']="Oops somthing has gone wrong.  Please contact a systems administrator"
            response = json.dumps(response_dict, indent =4)
            return HttpResponse(response, status=int(response_dict['code']),
                                    mimetype="application/json")
            

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
            
   #this is a GET
    
    #if the database and collection are not identified, use the main one
    # defined in settings.
    if not database_name or collection_name:
        idata ={'database_name': settings.MONGO_DB_NAME,
           'collection_name': settings.MONGO_MASTER_COLLECTION,
           }
    else:
        idata ={'database_name': database_name,
             'collection_name': collection_name,
             }
    idata['output_format'] = 'json'
    idata['query']="{}"
    
    context= {'name':name,
              'form': ComplexSearchForm(initial=idata)
              }
    return render_to_response('generic/bootstrapform.html',
                             RequestContext(request, context,))

def saved_searches(request):
     
    savedsearches = SavedSearch.objects.all()
    context = {"savedsearches": savedsearches }
    return render_to_response('search/previous.html',
                              RequestContext(request, context,))
