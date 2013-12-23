#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 

from django.conf import settings
from ..accounts.models import flangioUser as User
from django.utils.datastructures import SortedDict
import os, json, sys, uuid
from omhe.core.parseomhe import parseomhe
from pymongo import Connection
from ..socialgraph.models import SocialGraph
#from ..accounts.models import UserProfile
import pickle
from datetime import datetime, date, time
from bson.code import Code


def massage_dates(qdict):
    
    for k,v in qdict.items():
        if k.__contains__("date"):
            print "i am a date!"
            v=datetime()
        if type(v)==type({}):
            if k.__contains__("datetime"):
                print "i am a datetime!"
    return qdict
    


def build_keys_with_mapreduce(collection_name=None):
    map= Code("function() { "
              "    for (var key in this)"
              "        { emit(key, null); } }"
              )
    reduce = Code("function(key, stuff)"
                  "{ return null; }"
                  )
    

    mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
    db = 	    mconnection[settings.MONGO_DB_NAME]

    if collection_name:
        collection = db[collection_name]
        result_collection_name = "%s_keys" % (collection_name)
    else:
        collection = db[settings.MONGO_MASTER_COLLECTION]
        result_collection_name = "%s_keys" % (settings.MONGO_MASTER_COLLECTION)
    
    print "mr: %s %s %s" % (settings.MONGO_DB_NAME, collection, result_collection_name)

    result = collection.map_reduce(map, reduce, result_collection_name)
    
    print result
    
    return None
    
    
def raw_query_mongo_db(kwargs, collection_name=None):
    #for key in kwargs:
    #    print "arg: %s: %s" % (key, kwargs[key])

    """return a result list or an empty list"""
    l=[]
    response_dict={}
    
    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	        mconnection[settings.MONGO_DB_NAME]
        if not collection_name:
            transactions = db[settings.MONGO_MASTER_COLLECTION]
        elif (collection_name=="history"):
            transactions = db[settings.MONGO_HISTORYDB_NAME]
        
        mysearchresult=transactions.find(kwargs)
        mysearchcount=mysearchresult.count()
        if mysearchcount>0:
            response_dict['code']=200
            for d in mysearchresult:
                l.append(d)
            response_dict['results']=l
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['code']=400

        response_dict['type']="Error"
        response_dict['message']=str(sys.exc_info())
    return response_dict

def prepare_idTransaction_dict(model_instance):
    fields = SortedDict()
    
    for field in model_instance._meta.fields:
        try:
            if getattr(model_instance, field.name) not in (None, ''):
                newfieldname ="%s" % (field.name)
                   
                value = getattr(model_instance, field.name)
                #if a datetime sting, then turn into a datetime
                try:
                    value = time.strptime(value, "%Y-%m-%d %H:%M:%S")
                except:
                    pass
                try:
                    value = time.strptime(value, "%Y-%m-%d")
                except:
                    pass
                try:
                    value = time.strptime(value, "%H:%M:%S")
                except:
                    pass
                
            fields[newfieldname] = str(value)
        except:
            pass
    
    fields.insert(0,'_id', model_instance.transaction_id)
    if fields.has_key('extra_fields'):
        ef =json.loads(fields['extra_fields'])
        fields.update(ef)
        del fields['extra_fields']
 
    if fields.has_key('tags'):
        fields['tags'] = json.loads(fields['tags'])

    
    #print "The tx type is ", fields['transaction_type']
    if fields['transaction_type']=="omhe":
        if fields['text'] != "":
            p = parseomhe()
            d = p.parse(fields['text'])
            del d['transaction_id'], d['transaction_datetime']
            fields.update(d)
            

    #for k in fields.keys():
    #    print k,"= ",fields[k]
    
    return fields


def update_filename(instance, filename):
    path = "transaction-files/"
    format = instance.patient.patient_id + "-" + filename
    return os.path.join(path, format)

def delete_tx(attrs, collection=None):
    #Connect to the db or fail.
    try:
        mconnection     = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db              = mconnection[settings.MONGO_DB_NAME]
        transactions    = db[settings.MONGO_MASTER_COLLECTION_NAME]
        history         = db[settings.MONGO_HISTORYDB_NAME]
    except:
        error=str(sys.exc_value)
        d={"code":'500',
           "message": "MongoDB Connection Error. Mongo may not be running.",
           "errors":(error,)}
        return d
    
    
    #Check to be sure this transaction_id exists
    mysearchresult=transactions.find_one({'transaction_id':attrs['transaction_id']})
     
    if mysearchresult:
        # This tx already exists (this uuid has been submitted before)
        if settings.ALLOW_DELETE_TX==True:
            attrs['history']=True
            responsedict=mysearchresult
            responsedict['_id'] = str(uuid.uuid4()) 
            hist_id=history.insert(responsedict)
            #print "saved to history!!!"
            r= transactions.remove({'_id': attrs['transaction_id']})
        #print "removed origional from main collection"
            return {"code": "200", "message": "Transaction deleted.",}	    
        else:
            #if settings.ALLOW_DELETE_TX==False, then we fail the delete attempt.
            error="%s could not be deleted because the server is not configured to allow deletes." % (attrs['transaction_id'])
            d={"code": '403',
               "message": "Fobidden.  Deletes are not allowed.",
               "errors": (error,)}
            return d
    else:
        error="%s does not exist." % (attrs['transaction_id'])
        d={"code": '404',
            "message": "Not found.  The transaction you are trying to delete does not exist.",
            "errors": (error,)}
        return d
   




def create_mongo_transaction(attrs):       
    #Connect to the db or fail.
    try:
        mconnection     = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db              = mconnection[settings.MONGO_DB_NAME]
        transactions    = db[settings.MONGO_MASTER_COLLECTION_NAME]
        history         = db[settings.MONGO_HISTORYDB_NAME]
    except:
        error=str(sys.exc_value)
        d={"code":'500',
           "message": "MongoDB Connection Error. Mongo may not be running.",
           "errors":(error,)}
        return d
    
    #Check to make sure we haven't used this txid already.
    mysearchresult=transactions.find_one({'transaction_id':attrs['transaction_id']})
    
    if mysearchresult:
        # This tx already exists (this uuid has been submitted before)
        if settings.ALLOW_UPDATE_TX==True:
            attrs['history']=True
            responsedict=transactions.find_one(
                                {'transaction_id': attrs['transaction_id']})
            responsedict['_id'] = str(uuid.uuid4()) 
            hist_id=history.insert(responsedict)
            print "saved to history!!!"
            r= transactions.remove({'_id': attrs['transaction_id']})
            print "removed original from main collection"
        else:
            #if settings.ALLOW_UPDATE_TX==False, we fail the create attempt.
            error="%s already submitted" % (attrs['transaction_id'])
            d={"code": '409',
               "message": "Duplicate/Conflict",
               "errors": (error,)}
            return d
        
    my_id=transactions.insert(attrs)

    mysearchresult=transactions.find({'_id':attrs['_id']})
    
    result_list=[]
    for r in mysearchresult:
        result_list.append(r)
        

    d={"code": "200",
        "message": "OK",
        "results": result_list}
    return d



def filter_social_graph(request, serial_result):
    result_list=[]
    try:
        grantee=User.objects.get(username=request.user)
    except(User.DoesNotExist):
        error = "The grantee could not be found."

        print error
        grantee=None

    for r in serial_result:
        try:
            grantr=r['subject']
            grantor=User.objects.get(username=grantr)
        except(User.DoesNotExist):
            try:
                grantor=User.objects.get(email=grantr)
            except(User.DoesNotExist):
                try:
                    gp=UserProfile.objects.get(anonymous_patient_id=grantr)
                    grantor = gp.user
                except(UserProfile.DoesNotExist):
                    error = "The grantor could not be found."

        try:
            sg=SocialGraph.objects.get(grantor=grantor, grantee=grantee)
            result_list.append(r)
        except(SocialGraph.DoesNotExist):
            """"Keep going"""
            pass
        except(User.DoesNotExist):
            print """The user does not exist.  Fatal Server Error!"""
            return ()

    return result_list
    
    


def normalize_results(results_dict):
    #Define some dummy/default values
    mydt=datetime.now()
    myd=date.today()
    myt=time(0,0)
    
    for r in results_dict['results']:
        for k,v in r.items():
            if type(r[k]) == type(mydt):
                r[k]= v.__str__()
                #print r[k]
    return results_dict

def normalize_list(results_list):
    #Define some dummy/default values
    mydt=datetime.now()
    myd=date.today()
    myt=time(0,0)
    
    for r in results_list:
        for k,v in r.items():
            if type(r[k]) == type(mydt):
                r[k]= v.__str__()
    
    return results_list


def to_json(results_dict):
    
    return json.dumps(results_dict, indent = 4)







def query_mongo(kwargs, collection_name=None, skip=0, limit=settings.MONGO_LIMIT, return_keys=()):
    """return a response_dict  with a list of search results"""
    print "collection_name =", collection_name , settings.MONGO_DB_NAME, settings.MONGO_MASTER_COLLECTION
    #print "skip and limit", skip, limit
    l=[]
    response_dict={}
    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	        mconnection[settings.MONGO_DB_NAME]
        if not collection_name:
            collection = db[settings.MONGO_MASTER_COLLECTION]
        else:
            collection = db[collection_name]
           
        if return_keys:
            return_dict={}
            for k in return_keys:
                return_dict[k]=1
            #print "returndict=",return_dict
            mysearchresult=collection.find(kwargs, return_dict).skip(skip).limit(limit)
        else:
            mysearchresult=collection.find(kwargs).skip(skip).limit(limit)
        
        print "response",  mysearchresult.count()

    
        response_dict['num_results']=int(mysearchresult.count(with_limit_and_skip=False))
        response_dict['code']=200
        response_dict['type']="search-results"
        for d in mysearchresult:
            d['id'] = d['_id'].__str__()
            del d['_id']
            l.append(d)
        response_dict['results']=l
            
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict



def get_collection_keys(collection_name=None):
    l=[]
    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	        mconnection[settings.MONGO_DB_NAME]
        if not collection_name:
            ckey_collection = "%s_keys" % (settings.MONGO_MASTER_COLLECTION)
            print settings.MONGO_DB_NAME, ckey_collection
            collection = db[ckey_collection]
        else:
            ckey_collection = "%s_keys" % (collection_name)
            collection = db[ckey_collection]
        result = collection.find({}).distinct("_id")
        for r in result:
            l.append(r)
        
        if settings.SORTCOLUMNS:
            nl=[] #new list list
            #sort the list according to our list

            for i in settings.SORTCOLUMNS:
                for j in l:
                    if j.__contains__(i):
                        nl.append(j)
            difflist = list(set(l) - set(nl))

            for i in difflist:
                nl.append(i)
            return nl

        else:
            return sorted(l)
    except:
        print "Error.", str(sys.exc_info())
        return []



def get_collection_labels():
    l=[]
    try:
        mconnection 	= Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db 	     	= mconnection[settings.MONGO_DB_NAME]
        collection	= db[settings.MONGO_MASTER_LABELS_COLLECTION]
        
        result = collection.find_one({})

	label_dict = dict((x, y) for x, y in result['labels'])

        return label_dict
    except:
        print "Error reading from Mongo!", str(sys.exc_info())
        return {}

def get_labels_tuple():
    l=[]
    try:
        mconnection 	= Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db 	     	= mconnection[settings.MONGO_DB_NAME]
        collection	= db[settings.MONGO_MASTER_LABELS_COLLECTION]
        
        dbresult = collection.find_one({})
        
	labels = dbresult['labels']
	
	result=[]
        result.append(("Name", "Label"))

	for i in labels:
	    result.append(tuple(i))
	
        return result
    except:
        print "Error reading from Mongo!", str(sys.exc_info())
        return {}

def query_mongo_db(kwargs, collection_name=None):
    """return a result list or an empty list"""
    l=[]
    response_dict={}
    
    try:        
        mconnection = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = mconnection[settings.MONGO_DB_NAME]
        if not collection_name:
            transactions = db[settings.MONGO_MASTER_COLLECTION]
        elif (collection_name=="history"):
            transactions = db[settings.MONGO_HISTORYDB_NAME]
        
        mysearchresult=transactions.find(kwargs)
        mysearchcount=mysearchresult.count()
        if mysearchcount>0:
            for d in mysearchresult:
                print "-----------------------------------------------"
                #print d
                #if d.has_key('data_model_name'):
                #    del d['data_model_name']
                l.append(d)
            
            response_dict['code']=200
            response_dict['message']="Search complete."
            response_dict['type']="flangioResponse"
            response_dict['results']=l
            response_dict['num_results']=len(l)
        else:
            response_dict['code']=404
            response_dict['type']="Error"
            response_dict['message']="Not Found"
            response_dict['results']=l
            response_dict['num_results']=len(l)
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['code']=500
        response_dict['type']="Error"
        response_dict['message']="Error reading from Mongo: " + str(sys.exc_value)
        response_dict['results']=[]
    return response_dict


def verify_users_exist_and_sg(data):
    """
    Scan supplied user id's for exist valitity. All must exists.
    Compare ids against username, email, and anonymous_patient_id
    in that order.
    """
    
    data['errors']=[]
    try:
        receiver=User.objects.get(username=data['receiver'])
    except User.DoesNotExist:
        try:
            receiver=User.objects.get(email=data['receiver'])
        except User.DoesNotExist:
            try:
                receiver=UserProfile.objects.get(anonymous_patient_id=data['receiver'])
            except UserProfile.DoesNotExist:
                msg ="Receiver %s not found." %(data['receiver'])
                data['errors'].append({'field':'receiver','description':msg})

    try:
        sender=User.objects.get(username=data['sender'])
    except User.DoesNotExist:
        try:
            sender=User.objects.get(email=data['sender'])
        except User.DoesNotExist:
            try:
                sender=UserProfile.objects.get(anonymous_patient_id=data['sender'])
            except UserProfile.DoesNotExist:
                msg ="Sender %s not found." %(data['sender'])
                data['errors'].append({'field':'sender','description': msg})

    try:
        subject=User.objects.get(username=data['subject'])
    except User.DoesNotExist:
        try:
            subject=User.objects.get(email=data['subject'])
        except User.DoesNotExist:
            try:
                up = UserProfile.objects.get(anonymous_patient_id=data['subject'])
		subject = up.user
            except UserProfile.DoesNotExist:
                msg ="Subject %s not found." %(data['subject'])
                data['errors'].append({'field':'subject', 'description': msg })
    
    social_graph_errors = verify_social_graph(sender, receiver, subject)
        
    if social_graph_errors:
	data['errors'].append(social_graph_errors)

    #If all is good then this should be an empty list.
    if not data['errors']:
        del data['errors']
    return data


def verify_social_graph(sender, receiver, subject):
    """You must pass in 3 user objects"""  
    errors = []
    if settings.RESPECT_SOCIAL_GRAPH==False:
        return errors
    #otherwise verify that a Social graph G exists between sender and subject.
    try:
        sg=SocialGraph.objects.get(grantor=subject, grantee=sender)
    except(SocialGraph.DoesNotExist):
        error = "A social graph does not exist between the grantor %s and the grantee %s." % (subject, sender)
        errors.append(error)

    return errors

def get_since_id(filename=settings.SINCE_ID_FILE):
    readfile 		= open(filename, 'r')
    buffer 		= readfile.read()
    readfile.close()
    last_since_id 	= int(buffer)
    new_since_id 	= int(last_since_id) + 1
    openfile 		= open(filename, 'w')
    openfile.writelines(str(new_since_id))
    openfile.close()
    return new_since_id
    
    
def strip_occurences(s):
    
    o =("_0","_1","_2","_3","_4","_5","_6","_7","_8","_9","_10","_11","_12",)
    for l in o:
        if s.endswith(l):
            ns = s.strip(l)
            return ns
    return s


def build_non_observational_key(k):
    
    if str(k).__contains__("__"):
        model_field_split = str(k).split("__")
        newlabel = "%s_" % (model_field_split[0])

        field_occurence_split =  str(model_field_split[1]).split("_")

        for i in  field_occurence_split[:-1]:
            newlabel = "%s_%s" % (newlabel,i)
        return newlabel   
    return k
    