__author__ = 'mark'

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import unittest
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.core.urlresolvers import reverse
from datetime import date, datetime

from apps.accounts.models import User,UserProfile,Permission

import inspect
import ast

from settings_test import *



"""
Tests Utilities Framework for the flangio app.
Used by testing modules.

Generate the test data
python manage.py dumpdata {app_name} --indent=4 --settings=test.settings.dev >./apps/{app}/fixtures/{App}_testdata.json
"""

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def disable(self):
    self.HEADER = ''
    self.OKBLUE = ''
    self.OKGREEN = ''
    self.WARNING = ''
    self.FAIL = ''
    self.ENDC = ''



def Test_Start(message=""):
    print "_______________________________________________"
    caller = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    print "Test Harness:" + inspect.getframeinfo(inspect.currentframe().f_back)[0]
    print term_color.OKGREEN + "Entering:" + caller + term_color.ENDC
    if message != "":
        print "Notes:"+message
    print "------------------------------------------------"
    return


def Test_Msg(message="",success=True):
    if message=="":
        return
    else:
        print "     Note:____________________"
        if success:
            print "     "+message
        else:
            print "     "+term_color.FAIL+message+term_color.ENDC
        print "     -------------------------"
        return
    return

def Test_End(message="",success=True):
    print "------------------------------------------------"
    caller = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    print "Leaving:" + caller
    if message != "":
        if success:
            print "Notes:"+message
        else:
            print "Notes:"+term_color.FAIL+message+term_color.ENDC
    print "________________________________________________"
    return


def create_user_account(self, user_name="", email_address="", pwd="", showprint=False):
    """ Attempt to create a user
    """

    showprint = True
    try:
        u = User.objects.get(username=user_name)
    except:
        u = []

    if showprint != False:
        print "User Account Info (Pre-create):", u

        u = User.objects.create_user(username=MASTER_USER_NAME, email=MASTER_EMAIL, password=MASTER_PASSWORD)
        now_allowed = give_permission_set(MASTER_USER_NAME,MASTER_PERMISSIONS)

        if showprint != False:
            print "User Created:", u
            print "with permissions:", now_allowed



    post_url = "/accounts/create/"
    post_parameters = {"first_name": USER_FIRST_NAME,
                       "last_name" : USER_LAST_NAME,
                       "username"  : user_name,
                       "password1" : pwd,
                       "password2" : pwd,
                       "pin"       : USER_PIN,
                       "email"     : email_address,
                       "mobile_phone_number" : USER_PHONE
    }
    code_return = 200

    output = []
    called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    looked_for = USER_CREATED_SUCCESS
    result = test_for_post(self, code_return, MASTER_USER_NAME, MASTER_PASSWORD, output, post_url,post_parameters, looked_for, called_by, showprint)

    if showprint != False:
        print "Result returned:"
        print result
        print "Output:"
        print output
        print ""

    give_permission(user_name,"create-any-socialgraph")
    give_permission(user_name,"create-other-users")
    check_permission(user_name,True)

    if result == None:
        Test_Msg("Account Created "+str(code_return)+" - "+user_name)
    else:
        Test_Msg("Account Problem "+str(code_return)+" - "+user_name, success=False)



    return u


def test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint=False, post_mode="POST" ):
    """
    Do a POST by default

    Set post_mode to "GET" to do a GET
    """
    response = output

    # Test_Start(called_by)

    access = self.client.login(username=usrname,password=passwd)
    if showprint != False:
        print "Access:", access


    # Do a POST (default) or a GET
    if post_mode == "GET":
        response = self.client.get(post_url,post_parameters,follow=True)
    else:
        response = self.client.post(post_url,post_parameters,follow=True)


    if showprint == True:
        print "Expecting code: "+ str(code_return) + " Got this: " + str(response.status_code)
        # print response.content

    # Check that the response is = code_return.

    got_code = self.assertEqual(str(response.status_code), str(code_return))
    if showprint == True:
        print "AssertEqual Result (Got_code): [" + str(got_code) +"]"
        print response.content
        # check response details
        # print "%s = %s" % (response.status_code, code_return)

    result = got_code

    # Pass reference to output so this can be tested in calling function
    output.append(response.content)

    if (str(code_return) == str(response.status_code)) and looked_for != "":
        # We got the return code we expected
        # Now we Test to see if we got the String we expected
        # and we have a value to test for in the output

        if showprint != False:
            print "response:====================="
            print response.content
            print "end of response==============="
            print "looked_for===================="
            print looked_for
            print "end of looked_for============="

        Look_For_What = looked_for
        result = None

        try:
            # result = self.assertContains(response,Look_For_What)

            result = self.assertContains(response, Look_For_What, status_code=code_return )
            # outcome = self.assertContains(response, looked_for, status_code=code_return )
            # outcome = self.assertContains(response.content, looked_for )
            # outcome = self.assertContains(response, looked_for )

            # result = "skipped"
            Test_Msg( "Successful Test:\n     Outcome = " + str(result))
        # except result != None:
        except AssertionError:
            Test_Msg("No match in Page "+post_url)
            result = False
            if showprint==True:
                print "Looking for:"+Look_For_What
                print "in this output:"
                print response.content
                # Test_End(called_by)

        if showprint != False:
            print "Outcome of Text comparison:"
            print result



    return result


def check_error(error_output={}, fields_to_check={}, expected_error="", showprint=False ):

    result = False
    if showprint != False:
        print "Errors to Evaluate:"
        print error_output

        print "Fields to check:"
        print fields_to_check

        print "Expected Error:[" + expected_error +"]"

        print ast.literal_eval(error_output)

    error_evaluation = ast.literal_eval(error_output)
    # print "errors:"
    # print error_evaluation['errors']



    for key in fields_to_check:
        # print "Evaluating:"+ key
        for dict in error_evaluation['errors']:
            # print dict['field']
            # print "dictionary:"
            # print dict['field'] + " - " + str(dict['description'])
            if (key == dict['field']):
                #print "Got match on key"
                # print dict['description']
                desc = dict['description']
                #print desc[0] +" / " + expected_error
                if desc[0] == expected_error:
                    if showprint != False:
                        print "Match on " + key + " and [" +expected_error + "]"
                    fields_to_check[key] = "True"
                # we had a match so set result to True
                result = True



    return result

def check_permission(usr_name="",showprint=False):
    """
    View permissions for a user profile
    """
    if usr_name=="":
        usr_key = 1
    else:
        try:
            usr_key = User.objects.get(username=usr_name)
        except:
            usr_key = 1

    usr_permission = Permission.objects.filter(user=usr_key)

    if showprint!=False:
        print "User:", usr_name
        print "key:", str(usr_key)
        print "Permissions:",usr_permission


    return usr_permission

def give_permission(usr_name="",permit_this="",showprint=False):
    """
    Add a permission to a user
    """

    if usr_name=="":
        if showprint!=False:
            print "No permission added"
        result = ""
    else:
        usr_key = User.objects.get(username=usr_name)
        if showprint!=False:
            print "got usr_key"
            print usr_key
            print "Now adding permission:["+permit_this+"]"

        new_permission = Permission(user=usr_key, permission_name=permit_this)
        new_permission.save()
        result = new_permission

    return result

def give_permission_set(usr_name="",permission_set={}, showprint=False):
    """
    receive a Dict and assign each permission in the dict to the usr_name
    """
    if usr_name=="":
        if showprint!=False:
            print "No permission added"
        result = ""
    else:
        usr_key = User.objects.get(username=usr_name)
        if showprint!=False:
            print "got usr_key: ",usr_name,"=",usr_key

        for permission in permission_set:
            if showprint!=False:
                print "Now adding permission:[",permission,"]"

            new_permission = Permission(user=usr_key, permission_name=permission)
            new_permission.save()

        result = check_permission(usr_name)
    return result


def remove_permission(usr_name="",not_permitted="",showprint=False):
    """
    remove a permission from a user
    """

    if usr_name=="":
        if showprint!=False:
            print not_permitted+" permission not revoked"
        result = ""
    else:
        usr_key = User.objects.get(username=usr_name)
        if showprint!=False:
            print "revoking ["+not_permitted+"] for ", usr_key

        kill_permission = Permission.objects.filter(user=usr_key, permission_name=not_permitted)
        if showprint!=False:
            print kill_permission

        kill_permission.delete()
        result = "revoked ["+not_permitted+"] for "+str(usr_key)

    return result

def required_fields(model_source='apps.accounts.UserProfile'):

    model = import_object(model_source)

    # print model

    model_object= model._meta
    # print model_object

    model_fields = model_object._fields()

    reqd_fields = {}

    for o in model_fields:
        if o.blank!=True:
            add_param = '"'+str(o.name)+'": '+str(o.default)+','
            # print add_param
            reqd_fields[o.name] = o.default

    return reqd_fields

class term_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def display_function_info():

    caller = inspect.getframeinfo(inspect.currentframe().f_back)[2]

    print ""
    print term_color.OKGREEN+"{0}:{1}".format(inspect.getframeinfo(inspect.currentframe().f_back)[0], caller) +term_color.ENDC

    return

def display_data_set(message="Command Set",display_set=('Nothing to evaluate')):

    print message
    print "========= START OF SET ========="
    print display_set
    print "========== END OF SET =========="
    print " "

    return

def display_test_result(value_tested="Empty",outcome="No Result"):

    print "Testing Value: [" + str(value_tested) +"]"
    print "======= start of result ======="
    print outcome
    print "======== end of Result ========"
    print " "

    return