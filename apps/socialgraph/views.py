# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, sys
from ..accounts.models import Permission
from ..accounts.decorators import json_login_required, access_required
from models import SocialGraph


@json_login_required
@csrf_exempt
def social_graph_delete(request):
    """If the request is not POST then return bad request"""
    if request.method == 'GET':
        jsonstr={"status": "405",
                 "message": "This method is not implemented or not allowed. Try a POST"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=405)

    attrs={}
    for attr in request.POST:
        """load our attrs dict with request.POST attrs"""
        attrs[attr]=request.POST[attr]

    if attrs.has_key('grantor')==False or attrs.has_key('grantee')==False:
        jsonstr={"status": "400", "message": "You must supply a grantor and a grantee"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=400)
    
    #check that the grantor exists
    try:
        grantor = User.objects.get(username=attrs['grantor'])
    except(User.DoesNotExist):
        jsonstr={"status": "404", "message": "Grantor user does not Exist.",
                 "exists": "false"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=404)
    
    #check that the grantee exists	
    try:
        grantee = User.objects.get(username=attrs['grantee'])
    except(User.DoesNotExist):
        jsonstr={"status": "404",
                 "message": "Grantee user does not Exist.",
                 "exists": "false"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=404)
   
    if grantor!=request.user:
        # message was wrong

        jsonstr={"status": "401",
                 "message": "Unauthorized - You do not have the right to delete this social graph."}

        jsonstr=json.dumps( jsonstr, indent=4)
        return HttpResponse( jsonstr, status=401)

    sg=SocialGraph.objects.filter(grantor=grantor, grantee=grantee)
    how_many = sg.count()
    # Test for nothing to delete when a socialgraph does not exist?
    sg.delete()
    if how_many == 0:
        jsonstr={"status": "200", "message": "Nothing to delete"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
    else:
        jsonstr={"status": "200", "message": "Social graph deleted","result": how_many}
        jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse( jsonstr, status=200)




    
@json_login_required
@csrf_exempt
def social_graph_create(request):
    """If the request is not POST then return bad request"""
    if request.method == 'GET':
        jsonstr={"status": "405",
                 "message": "This method is Not implemented or not allowed. Try a POST"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=405)
    
    attrs={}	
    for attr in request.POST:
        #print "%s=%s" % (attr,request.POST[attr])
	"""load our attrs dict with request.POST attrs"""

        attrs[attr]=request.POST[attr]
	
	
    if attrs.has_key('grantor')==False or attrs.has_key('grantee')==False:
        jsonstr={"status": "400", "message": "You must supply a grantor and a grantee"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=400)

    try:
        grantor = User.objects.get(username=attrs['grantor'])
    except(User.DoesNotExist):
        jsonstr={"status": "404",
                 "message": "Grantor user does not Exist.",
                 "exists": "false"}
        jsonstr=json.dumps( jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=404)
	
    try:
        grantee = User.objects.get(username=attrs['grantee'])
    except(User.DoesNotExist):
        jsonstr={"status": "404",
                 "message": "Grantee user does not Exist.",
                 "exists": "false"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=404)
	
    try:
        p=Permission.objects.get(user=request.user,
                                 permission_name="create-any-socialgraph")
    except:
        if grantor!=request.user:
            jsonstr={"status": "401",
                     "message": "Unauthorized - You do not have the right to create this socialgraph."}
            jsonstr=json.dumps(jsonstr, indent=4)
            return HttpResponse( jsonstr, status=401)

    try:
        sg=SocialGraph.objects.create(grantor=grantor, grantee=grantee)
        sg.save()
        jsonstr={"status": "200", "message": "Social graph created"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=200)
    except:
        print sys.exc_info()
        jsonstr={"status": "409", "message": "Conflict. The social graph already exists"}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        return HttpResponse( jsonstr, status=409)
