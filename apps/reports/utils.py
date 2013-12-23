import json, sys


def query_mongo_for_report(report_query):
    """ Takes in a report definition in JSON"""
    
    #create a blank dict to hold the params we will pass to mongo.
    qd={}
    
    try:
      #build our query dict object,  
      jd =  json.loads(report_query)
      
    
      #Copy the items and make sure date ranges get coppied over.
      for k,v in jd.items():
        
        
        if type(v)==type({}) and v.has_key("start") and v.has_key("end"):
            qd[k]={"$gte": v['start'], "$lte": v['end']}
        elif k=="data_model_name":
            qd[k]={"$in": v}            
        else:
            qd[k]=v 
      
      # remove aggregate key=
      if jd.has_key('aggregate_by'):
        print "aggregate results"
        aggregate_by = jd['aggregate_by']
        del jd['aggregate_by']
        print "remove agrregate from dict"
    
      return qd
    except:
        print "ERROR : ", sys.exc_value