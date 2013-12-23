#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json, string, random
from django.contrib.auth import login, authenticate
from httpauth import HttpBasicAuthentication
from django.http import HttpResponse
from models import Permission
from datetime import date

def random_string(length=6, alphabet=string.letters+string.digits):
    """
    Return a random string of given length and alphabet.

    Default alphabet is url-friendly (base62).
    This method lifted from @shazow - thanx man.
    """
    return ''.join([random.choice(alphabet) for i in xrange(length)])


def user_permissions(request):
    try:
        p=Permission.objects.filter(user=request.user)
        pl=[]
        for i in p:
            pl.append(i.permission_name)
        return tuple(pl)
    except(Permission.DoesNotExist):
        return ()



def authorize(request):
    a=HttpBasicAuthentication()
    if a.is_authenticated(request):
        login(request,request.user)
        auth=True
    else:
        if request.user.is_authenticated():
            auth=True
        else:
            auth=False
    return auth

def unauthorized_json_response(additional_info=None):
    body={"code": "401",
          "message": "Unauthorized - Your account credentials were invalid."}
    if additional_info:
        body['message']="%s %s" % (body['message'], additional_info)
    body=json.dumps(body, indent=4, )
    return body




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
                receiver=User.objects.get(anonymous_patient_id=data['receiver'])
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
                sender=User.objects.get(anonymous_patient_id=data['sender'])
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
                up = User.objects.get(anonymous_patient_id=data['subject'])
                subject = up.user
            except User.DoesNotExist:
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







#def validate_user_data(attrs):
#    
#    #valid gender values
#    gc=('female', 'male','transgender_male_to_female', 'transgender_female_to_male',
#    'sexual_reassignment_male_to_female', 'sexual_reassignment_female_to_male')
#    
#        
#    error=""
#    if attrs.has_key('first_name')==False:
#        error+="You must supply first_name. "
#    
#    if attrs.has_key('last_name')==False:
#        error+="You must supply last_name. "
#        
#    if attrs.has_key('email')==False:
#        error+="You must supply email. "
#        
#    if attrs.has_key('username')==False:
#        error+="You must supply username. "
#        
#    if attrs.has_key('height_in')==False:
#        error+="You must supply height_in. "
#        
#    if attrs.has_key('gender')==False:
#        error+="You must supply gender. "
#    elif gc.__contains__(attrs['gender'])==False:
#        error+="You must supply a valid gender value. %s" % (str(gc))
#
#
#    
#    if attrs.has_key('pin')==False:
#        error+="You must supply a 4 digit pin. "
#    else:
#        if len(attrs['pin'])!=4:
#            error+="Your pin must 4 numbers long. "
#        try:
#            x=int(attrs['pin'])
#        except:    
#            error+="Your 4 digit pin must be a number. "
#    
#    if attrs.has_key('birthdate')==False:
#        error+="You must supply birthdate. "
#    elif len(attrs['birthdate'])!=10:
#        error+="Birthdate must be formatted YYYY-MM-DD"
#    else:
#        try:
#            year=str(attrs['birthdate'][0:4])
#            if year.isdigit():
#                year=int(year)
#            else:
#                error+="birthdate year is not a number. "
#        
#            month=str(attrs['birthdate'][5:7])
#            if month.isdigit():
#                month=int(month)
#            else:
#                error+="birthdate month is not a number. "
#            
#            day=attrs['birthdate'][8:10]
#            
#            if day.isdigit():
#                day=int(day)
#            else:
#                error+= "birthdate day is not a number. "
#                
#            d=date(year, month, day)
#        except:
#            error+="Birthdate must be formatted YYYY-MM-DD"        
#    
#    if attrs.has_key('complaint_title')==False:
#        attrs['complaint_title']=""
#        
#    if attrs.has_key('complaint_detail')==False:
#        attrs['complaint_detail']=""
#
#    if attrs.has_key('complaint_title')==False:
#        attrs['complaint_title']=""
#        
#    if attrs.has_key('allergies')==False:
#        attrs['allergies']=""
#        
#    if attrs.has_key('medications')==False:
#        attrs['medications']=""
#        
#    if attrs.has_key('procedures')==False:
#        attrs['procedures']=""
#        
#    if attrs.has_key('conditions')==False:
#        attrs['conditions']=""
#        
#    if attrs.has_key('primary_insurance_or_payer')==False:
#        attrs['primary_insurance_or_payer']=""
#        
#    if attrs.has_key('secondary_insurance_or_payer')==False:
#        attrs['secondary_insurance_or_payer']=""
#        
#    if attrs.has_key('organization')==False:
#        attrs['organization']=""
#        
#    if attrs.has_key('twitter')==False:
#        attrs['twitter']=""
#        """Add a check to see if this user exists."""
#    
#        
#    if attrs.has_key('steps_per_day_goal')==False:
#        attrs['steps_per_day_goal']="10000"
#        
#    if attrs.has_key('weight_goal')==False:
#        error+="You must supply weight_goal. "
#    else:
#        try:
#            x=float(attrs['weight_goal'])
#        except:
#            error+="weight_goal must be a number. "
#
#            
#    if attrs.has_key('mobile_phone_number')==False or attrs.has_key('mobile_phone_number')=="":
#        attrs['mobile_phone_number']=""
#    else:
#        if len(attrs['mobile_phone_number'])!=10 and len(attrs['mobile_phone_number'])!=11:
#            
#            error+="mobile_phone number %s must be 10 or 11 digits.  US Only. " % (attrs['mobile_phone_number'])
#        try:
#            x=int(attrs['mobile_phone_number'])
#        except:
#            error+="mobile_phone_number must be all numbers and length 10 or 11. US Only (For now.). "
#        if len(attrs['mobile_phone_number'])==10:
#            attrs['mobile_phone_number']="+1%s" % (attrs['mobile_phone_number'])
#        if len(attrs['mobile_phone_number'])==11:
#            attrs['mobile_phone_number']="+%s" % (attrs['mobile_phone_number'])
#        
#    if attrs.has_key('fax_number')==False:
#        attrs['fax_number']=""
#    else:
#        if len(attrs['fax_number'])!=10 and len(attrs['fax_number'])!=11:
#            error+="fax_number must be 10 or 11 digits.  US Only "
#        try:
#            x=int(attrs['fax_number'])
#        except:
#            error+="fax_number must be all numbers and length 10 or 11. US Only. "
#     
#    
#    if error:
#        attrs['error']=error
#    
#    return attrs

def normalize_phone_number(pn):
    try:
        pn=str(pn)
    except:
        return None
    if len(pn)!=10 and len(pn)!=11:
        return None    
    try:
        x=int(pn)
    except:
        return None
    
    if len(pn)==10:
        pn="+1%s" % (pn)
    if len(pn)==11:
        pn="+%s" % (pn)
    return pn