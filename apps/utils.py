#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from accounts.models import flangioUser as User
from django.utils.datastructures import SortedDict
import os, json, sys, uuid, csv, pickle
from pymongo import Connection
from socialgraph.models import SocialGraph
from datetime import datetime, date, time
from bson.code import Code
from pymongo import Connection, DESCENDING
from bson.objectid import ObjectId

from pymongo import MongoClient


def to_json(results_dict):
    return json.dumps(results_dict, indent = 4)
    
def massage_dates(qdict):

    for k,v in qdict.items():
        if k.__contains__("date"):
            print "i am a date!"
            v=datetime()
        if type(v)==type({}):
            if k.__contains__("datetime"):
                print "i am a datetime!"
    return qdict

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
                    gp=User.objects.get(anonymous_patient_id=grantr)
                    grantor = gp.user
                except(User.DoesNotExist):
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

def query_mongo(query={}, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=()):
    """return a response_dict  with a list of search results"""
    

    l=[]
    response_dict={}
    
    try:
        mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        
        db          =   mc[str(database_name)]
        collection   = db[str(collection_name)]
        
        
        if return_keys:
            return_dict={}
            for k in return_keys:
                return_dict[k]=1
            #print "returndict=",return_dict
            mysearchresult=collection.find(query, return_dict).skip(skip).limit(limit)
        else:
            mysearchresult=collection.find(query).skip(skip).limit(limit)
        
        response_dict['num_results']=int(mysearchresult.count(with_limit_and_skip=False))
        response_dict['code']=200
        response_dict['type']="search-results"
        for d in mysearchresult:
            d['id'] = d['_id'].__str__()
            del d['_id']
            l.append(d)
        response_dict['results']=l
            
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=500
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict


def query_mongo_sort_decend(query={}, database_name=settings.MONGO_DB_NAME,
                collection_name=settings.MONGO_MASTER_COLLECTION,
                skip=0, limit=settings.MONGO_LIMIT, return_keys=(), sortkey=None):
    """return a response_dict  with a list of search results in decending
    order based on a sort key
    """
    
    l=[]
    response_dict={}
    
    try:
        mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        
        db          =   mc[str(database_name)]
        collection   = db[str(collection_name)]
        
        if return_keys:
            return_dict={}
            for k in return_keys:
                return_dict[k]=1
            print "returndict=",return_dict
            mysearchresult=collection.find(query, return_dict).skip(skip).limit(limit).sort(sortkey,DESCENDING)
        else:
            mysearchresult=collection.find(query).skip(skip).limit(limit).sort(sortkey,DESCENDING)
        
        response_dict['num_results']=int(mysearchresult.count(with_limit_and_skip=False))
        response_dict['code']=200
        response_dict['type']="search-results"
        for d in mysearchresult:
            d['id'] = d['_id'].__str__()
            del d['_id']
            l.append(d)
        response_dict['results']=l
            
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=500
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict



def delete_mongo(query={}, database_name=settings.MONGO_DB_NAME,
                 collection_name=settings.MONGO_MASTER_COLLECTION,
                 just_one=False):
    """delete from mongo helper"""
    
    l=[]
    response_dict={}
    
    try:
        mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        db          =   mc[str(database_name)]
        collection   = db[str(collection_name)]
        
        
        mysearchresult=collection.remove(query, just_one)
        
        
        #response_dict['num_results']=int(mysearchresult.count())
        response_dict['code']=200
        response_dict['type']="remove-confirmation"
 
            
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=500
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict



def write_mongo(document, database_name=settings.MONGO_DB_NAME,
                 collection_name=settings.MONGO_MASTER_COLLECTION,
                 update = False):
    

    """Write a document to the collection. Return a response_dict containing
    the written record. Method functions as both insert or update based on update
    parameter"""
    
    l=[]
    response_dict={}
    try:
        mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        db          =   mc[str(database_name)]
        collection   = db[str(collection_name)]
        
        potential_key_found = False
        existing_transaction_id = None
        existing_mongo_id  = None
        
        
        #enforce non-repudiation constraint on create
        #if document.has_key("transaction_id"):
        #    existing_transaction_id = collection.find_one({'transaction_id':document['transaction_id']})  
        #    if existing_transaction_id: 
        #        potential_key_found = True
        
        if document.has_key("id"):
            document["_id"] = ObjectId(document["id"])
            del document["id"]   
            
        if document.has_key("_id"):
            existing_mongo_id = collection.find_one({'_id':document['_id']})
            if existing_mongo_id:
                potential_key_found = True
        
        if update==False and potential_key_found==True:
                """409 conflict"""
                response_dict['num_results']=0
                response_dict['code']=409
                response_dict['type']="Error"
                response_dict['results']=[]
                response_dict['message']="Perhaps you meant to perform an update instead?"
                response_dict['errors']=["Conflict. This transaction_id has already been created.",]
                return response_dict
            
    
        elif update and potential_key_found: #this is an update
            #set kwargs _id to the existing_id to force to overwrite existing document
            
    
            #if existing_transaction_id:
            #     
            #    document['_id'] = ObjectId(existing_transaction_id['_id'])
            #    document['history']=True
            #    history_collection_name = "%s_history" % str(collection_name)
            #    history_collection   = db[str(history_collection_name)]
            #    
            #    history_object = existing_transaction_id
            #    history_object['historical_id'] = existing_transaction_id['_id']
            #    del history_object['_id']
            #    #now write the record to the historical collection
            #    written_object = history_collection.insert(history_object)
                
                
                
            if existing_mongo_id:
                document['_id'] =  ObjectId(existing_mongo_id['_id'])
                document['history']=True
                document['verified']=False
                history_collection_name = "%s_history" % str(collection_name)
                history_collection   = db[str(history_collection_name)]
                
                print history_collection
                print existing_mongo_id
                
                history_object = existing_mongo_id
                
                
                history_object['historical_id'] = existing_mongo_id['_id']
                del history_object['_id']
                print history_object
                
                #now write the record to the historical collection
                written_object = history_collection.insert(history_object)
                
            
            
            
            #update the record
            myobjectid=collection.save(document)
            
        else:
            # this is new so perform an insert.
            myobjectid=collection.insert(document)
        
        #now fetch the record we just wrote so that we write it back to the DB.
        myobject=collection.find_one({'_id':myobjectid})
        response_dict['code']=200
        response_dict['type']="write-results"
        myobject['id'] = myobject['_id'].__str__()
        del myobject['_id']
        l.append(myobject)
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




def bulk_csv_import_mongo(csvfile, delete_collection_before_import=False,
                          database_name=settings.MONGO_DB_NAME,
                          collection_name=None):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""
    #print "writing ", csvfile._get_path(), "to the collection" , settings.MONGO_DB_NAME, settings.MONGO_MASTER_COLLECTION
    l=[]
    response_dict={}
    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	        mconnection[database_name]
        if not collection_name:
            collection = db[settings.MONGO_MASTER_COLLECTION]
        else:
            collection = db[collection_name]

        
        if delete_collection_before_import:
            myobjectid=collection.remove({})
            
        #open the csv file.
        csvhandle = csv.reader(open(csvfile._get_path(), 'rb'), delimiter=',')
        

    
        rowindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :
            
            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")
                    cleaned_headers.append(c)
            else:
          
                record = dict(zip(cleaned_headers, row))
                #if there is no values, skip the key value pair
                kwargs ={}
        
                #Only populate fields that are not blank.
                for k,v in record.items():
                    if v:
                        kwargs[k]=v
                        
                try:
                    
                    myobjectid=collection.insert(kwargs)
                    success+=1
                except:
                    error_message = "Error on row " + rowindex +  ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))
                
  
            rowindex+=1
            
        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:
            
            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict  
        
    
            
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
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
    readfile            = open(filename, 'r')
    buffer              = readfile.read()
    readfile.close()
    last_since_id       = int(buffer)
    new_since_id        = int(last_since_id) + 1
    openfile            = open(filename, 'w')
    openfile.writelines(str(new_since_id))
    openfile.close()
    return new_since_id




def get_user_profile_info(identifier):
    """Get the user profile based on username, email, vid, or anon ID, else
       return None
    """
    up = None
    try:
        up = User.objects.get(username=identifier)
    except User.DoesNotExist:
        try:
           up = User.objects.get(email=identifier) 
        except User.DoesNotExist:
            try:
                up = User.objects.get(vid=identifier) 
            except User.DoesNotExist:
                try:
                    up = User.objects.get(anonymous_patient_id=identifier) 
                except UserProfile.DoesNotExist:
                    up=None
    return up          

def build_non_observational_key(k):
    
    if str(k).__contains__("__"):
        model_field_split = str(k).split("__")
        newlabel = "%s_" % (model_field_split[0])

        field_occurence_split =  str(model_field_split[1]).split("_")

        for i in  field_occurence_split[:-1]:
            newlabel = "%s_%s" % (newlabel,i)
        return newlabel   
    return k

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
           "message": "MongoDB Connection Error. MongoDB may not be running or flangio cannot access it.",
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







def raw_query_mongo_db(kwargs, collection_name=None):
    #for key in kwargs:
    #    print "arg: %s: %s" % (key, kwargs[key])

    """return a result list or an empty list"""
    l=[]
    response_dict={}

    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db =            mconnection[settings.MONGO_DB_NAME]
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



def get_collection_keys(collection_name=None):
    l=[]
    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db =            mconnection[settings.MONGO_DB_NAME]
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
        mconnection     = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db              = mconnection[settings.MONGO_DB_NAME]
        collection      = db[settings.MONGO_MASTER_LABELS_COLLECTION]

        result = collection.find_one({})

        label_dict = dict((x, y) for x, y in result['labels'])

        return label_dict
    except:
        print "Error reading from Mongo!", str(sys.exc_info())
        return {}

def get_labels_tuple():
    l=[]
    try:
        mconnection     = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db              = mconnection[settings.MONGO_DB_NAME]
        collection      = db[settings.MONGO_MASTER_LABELS_COLLECTION]

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



def build_keys_with_mapreduce(collection_name=None):
    map= Code("function() { "
              "    for (var key in this)"
              "        { emit(key, null); } }"
              )
    reduce = Code("function(key, stuff)"
                  "{ return null; }"
                  )


    mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
    db =            mconnection[settings.MONGO_DB_NAME]

    if collection_name:
        collection = db[collection_name]
        result_collection_name = "%s_keys" % (collection_name)
    else:
        collection = db[settings.MONGO_MASTER_COLLECTION]
        result_collection_name = "%s_keys" % (settings.MONGO_MASTER_COLLECTION)

    #print "mr: %s %s %s" % (settings.MONGO_DB_NAME, collection, result_collection_name)

    result = collection.map_reduce(map, reduce, result_collection_name)
    return None


def raw_query_mongo_db(kwargs, collection_name=None):
    #for key in kwargs:
    #    print "arg: %s: %s" % (key, kwargs[key])

    """return a result list or an empty list"""
    l=[]
    response_dict={}

    try:
        mconnection =   Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db =            mconnection[settings.MONGO_DB_NAME]
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


def massage_dates(qdict):

    for k,v in qdict.items():
        if k.__contains__("date"):
            print "i am a date!"
            v=datetime()
        if type(v)==type({}):
            if k.__contains__("datetime"):
                print "i am a datetime!"
    return qdict




    