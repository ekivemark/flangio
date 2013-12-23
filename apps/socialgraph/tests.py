"""
run "python manage.py test socialgraph>test_results/socialgraph_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""

__author__ = 'mark @ekivemark'

from django.test import TestCase
from ..accounts.models import User, UserProfile
from ..tests.test_utils import *
from ..tests.settings_test import *

import inspect
import uuid

"""
Tests for the flangio.socialgraph app.

Run from root of flangio app.
Run with "python manage.py test {app name}"
Example: python manage.py test socialgraph >./test_results/socialgraph_testresult.txt

Remember: every test definition must begin with "test_"

Generate the test data properly indented for readability
python manage.py dumpdata socialgraph --indent=4 >./apps/socialgraph/fixtures/testdata.json

"""

# Add module specific test variables here

PERMISSION_NAME="create-any-socialgraph"

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class Socialgraph_Simple_TestCase(TestCase):
    """Background to this test harness
       and prove the test harness works
    """

    # Add your fixtures here
    # fixtures = ['testdata.json']

    def test_basic_addition_Socialgraph(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("flangio.apps.socialgraph.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("flangio.apps.socialgraph.tests.py")

        return

    def test_load_home_page(self):
        """
        Test that we are loading the home page
        """

        Test_Start()

        showprint = False

        Test_Msg("Go to Home Page for flangio")

        # Transaction create should test for an existing account
        usrname = ""
        passwd  = ""
        # reset output
        output = []
        post_url = "/"
        post_parameters = {}
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Congratulations. You've successfully setup flangio."

        # set page code expected to be returned
        code_return = 200
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_End()

        return

class Create_Socialgraph_TestCase(TestCase):
    """
    /socialgraph/create
    /socialgraph/delete

    receive POST
    Login is required

    Sequence:
    - create:
    - attempt with no user account or bad password. Expect fail.
    - attempt a get
    	jsonstr={"status": "405",
                 "message": "This method is Not implemented or not allowed. Try a POST"}
    - post with missing grantor
    - post with missing grantee
        jsonstr={"status": "400", "message": "You must supply a grantor and a grantee"}
    - post with bad grantor
        jsonstr={"status": "404",
                 "message": "Grantor user does not Exist.",
                 "exists": "false"}
	- post with bad grantee
	    jsonstr={"status": "404",
                 "message": "Grantee user does not Exist.",
                 "exists": "false"}
	- remove create any socialgraph permission. expect fail
		jsonstr={"status": "401",
                 "message": "Unauthorized - You do not have the right to create this socialgraph."}
    - add in socialgraph permission. expect pass
    	jsonstr={"status": "200", "message": "Social graph created"}
    - create identical socialgraph
    	jsonstr={"status": "409", "message": "Conflict. The social graph already exists"}


    - delete:
    - attempt with no user account or bad password. Expect fail.
    - attempt a get
    	jsonstr={"status": "405",
                 "message": "This method is not implemented or not allowed. Try a POST"}
    - post with missing grantor
    - post with missing grantee
        jsonstr={"status": "400", "message": "You must supply a grantor and a grantee"}
    - post with a bad grantor
    	jsonstr={"status": "404", "message": "Grantor user does not Exist.",
                 "exists": "false"}
    - post with a bad grantee
    	jsonstr={"status": "404",
                 "message": "Grantee user does not Exist.",
                 "exists": "false"}
    - attempt delete with a different user account (grantor and user should match)
    	jsonstr={"status": "401",
                  "message": "Unauthorized - You do not have the right to delete this social graph."}
    - delete the social graph
        jsonstr={"status": "200", "message": "Social graph deleted"}
    - attempt a duplicate delete

    """

    # Add your fixtures here
    # fixtures = ['testdata.json']

    def test_create_delete_socialgraph(self):
        """
        Create and Delete socialgraph  test cycle in flangio

        """
        Test_Start()

        showprint = False

        # We need to create a user account
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)


        Test_Msg("Socialgraph - Force a failure - not logged in")

        # No need to be logged in to get the home page.
        usrname = USERNAME_NO_ACCOUNT_TEST
        passwd  = PASSWORD_NO_ACCOUNT_TEST
        # reset output
        output = []

        post_url = "/socialgraph/create"
        post_parameters = {
            "grantor":"me",
            "grantee":"you",
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Unauthorized - Your account credentials were invalid."

        code_return = 401
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_Start("Submit with a GET rather than a POST")

        showprint = False
        # No need to be logged in to get the home page.
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/create"
        post_parameters = {}
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "This method is Not implemented or not allowed. Try a POST"
        # looked_for = ""

        code_return = 405
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint, post_mode="GET" )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        ################################################
        # End of Bad User Info Create Tests
        ################################################
        Test_Start("Now Test for fail with No Grantee")

        showprint = False

        # No need to be logged in to get the home page.
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/create"
        post_parameters = {
                           "grantor": "me",
                          }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "You must supply a grantor and a grantee"

        code_return = 400
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_Start("Now Test for Fail with No Grantor")

        post_parameters = {
                           "grantee": "me",
                          }

        code_return = 400
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_Start("Now test for Grantor Does not exist")

        showprint = False
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/create"
        post_parameters = {
            "grantor":"me",
            "grantee":"you",
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Grantor user does not Exist."

        code_return = 404
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        create_email = "bob@nospam.com"
        create_user  = "REstCat"
        create_pwd   = "87654321"
        Test_Start("Use Grantor: "+create_email)



        post_url = "/accounts/create"
        post_parameters = {"first_name": "Rob",
                       "last_name" : "EstCat",
                       "username"  : create_user,
                       "password1" : create_pwd,
                       "password2" : create_pwd,
                       "email"     : create_email,
                       }
        looked_for = "flangio user created successfully"

        # looked_for = "This field is required."
        code_return = 200

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)


        print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)



        code_return = 404
        post_url = "/socialgraph/create"
        post_parameters = {
            "grantor": create_user,
            "grantee":"you",
            }

        looked_for = "Grantee user does not Exist."

        # We now make the call with the new User and password!
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_Start("Now use new user as Grantee")

        post_parameters = {
                           "grantor": "me",
                           "grantee": create_user,
                          }
        looked_for = "Grantor user does not Exist."

        # Making call with new user and password
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_Start("Now Create a target user")

        create_email_target = "cat@nospam.com"
        create_user_target  = "CatRest"
        create_pwd_target   = "87654321"

        post_url = "/accounts/create"
        post_parameters = {"first_name": "Cat",
                           "last_name" : "Resty",
                           "username"  : create_user_target,
                           "password1" : create_pwd_target,
                           "password2" : create_pwd_target,
                           "email"     : create_email_target,
                           }
        looked_for = "flangio user created successfully"

        # looked_for = "This field is required."
        code_return = 200

        # make call with created user and password
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        # We need a second target user
        # so create one

        Test_Start("Now Create a second target user")

        create_email_target2 = "lion@nospam.com"
        create_user_target2  = "LionRest"
        create_pwd_target2   = "87654321"

        post_url = "/accounts/create"
        post_parameters = {"first_name": "Lion",
                           "last_name" : "Rest",
                           "username"  : create_user_target2,
                           "password1" : create_pwd_target2,
                           "password2" : create_pwd_target2,
                           "email"     : create_email_target2,
                           }
        looked_for = "flangio user created successfully"

        # looked_for = "This field is required."
        code_return = 200

        # make call with created user and password
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)



        check_permission(usrname, showprint=True)
        check_permission(create_user, showprint=True)
        check_permission(create_user_target, showprint=True)
        check_permission(create_user_target2, showprint=True)

        Test_Start("Attempt to create a SocialGraph - Fail with missing permission: "+PERMISSION_NAME)


        showprint = False
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/create"
        post_parameters = {
            "grantor": create_user,
            "grantee":create_user_target,
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Unauthorized - You do not have the right to create this socialgraph."

        code_return = 401
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        # Now test creating a social graph where logged in user = grantor

        post_url = "/socialgraph/create"
        post_parameters = {
            "grantor": create_user,
            "grantee":create_user_target2,
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Social graph created"

        code_return = 200
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        # now give special permission to create any social graph
        # then test graph is created.

        give_permission(usrname,permit_this=PERMISSION_NAME ,showprint=True)


        showprint = False
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/create"
        post_parameters = {
                           "grantor": create_user,
                           "grantee":create_user_target,
                          }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Social graph created"

        code_return = 200
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_Start("Repeat the create step and force an error - Duplicate record")
        output = []

        looked_for = "Conflict. The social graph already exists"
        code_return = 409
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        # Doing this create test again with create_user and password

        Test_Start("Rerunning create step with Account: "+create_user)

        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_Start("Repeat the create step and force an error - Duplicate record")
        output = []

        looked_for = "Conflict. The social graph already exists"
        code_return = 409
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

    # end of additional test

        # clean up permissions ready for delete tests
        remove_permission(usrname, not_permitted=PERMISSION_NAME ,showprint=True)


        Test_End("Emd of Create Sequence")

        ##################################
        ##################################
        # End of Create Tests
        ##################################
        ##################################

        Test_Start("Delete Sequence")


        showprint = False


        Test_Msg("....Logging Out")
        # Let's logout again

        post_url = "/accounts/logout"
        post_parameters = {}
        looked_for = "Logged Out."
        code_return = 200

        # reset output
        output = []

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        print output

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+" - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return)+" : "+ looked_for, success=False)



        # we don't need to create_user_account - this was done earlier
        #user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)


        Test_Msg("Socialgraph - Force a failure - not logged in")


        showprint = False

        # No need to be logged in to get the home page.
        usrname = USERNAME_NO_ACCOUNT_TEST
        passwd  = PASSWORD_NO_ACCOUNT_TEST
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {
            "grantor":"me",
            "grantee":"you",
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Unauthorized - Your account credentials were invalid."

        code_return = 401
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_Start("Submit with a GET rather than a POST")

        showprint = True
        # No need to be logged in to get the home page.
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {}
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "This method is not implemented or not allowed. Try a POST"
        # looked_for = ""

        code_return = 405
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint, post_mode="GET" )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        ################################################
        # End of Bad User Info Delete Tests
        ################################################

        Test_Start("Now Test for fail with No Grantee")

        showprint = False

        # No need to be logged in to get the home page.
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {
            "grantor": "me",
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "You must supply a grantor and a grantee"

        code_return = 400
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_Start("Now Test for Fail with No Grantor")

        post_parameters = {
            "grantee": "me",
            }

        code_return = 400
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_Start("Now test for Grantor Does not exist")

        showprint = False
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {
            "grantor":"me",
            "grantee":"you",
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Grantor user does not Exist."

        code_return = 404
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        # We don't need to create this user they already exist.
        """
        create_email = "bob@nospam.com"
        create_user  = "REstCat"
        create_pwd   = "87654321"
        Test_Start("Use Grantor: "+create_email)



        post_url = "/accounts/create"
        post_parameters = {"first_name": "Rob",
                           "last_name" : "EstCat",
                           "username"  : create_user,
                           "password1" : create_pwd,
                           "password2" : create_pwd,
                           "email"     : create_email,
                           }
        looked_for = "flangio user created successfully"

        # looked_for = "This field is required."
        code_return = 200

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)


        print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        """
        # End of Create User Account (not needed - was created in create test phase earlier


        code_return = 404
        post_url = "/socialgraph/delete"
        post_parameters = {
            "grantor": create_user,
            "grantee":"you",
            }

        looked_for = "Grantee user does not Exist."
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        Test_Start("Now use new user as Grantee")

        post_parameters = {
            "grantor": "me",
            "grantee": create_user,
            }
        looked_for = "Grantor user does not Exist."
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_Start("Now Create a target user")


        # We don't need to create a target user - was created in create test phase earlier
        """
        create_email_target = "cat@nospam.com"
        create_user_target  = "CatRest"
        create_pwd_target   = "87654321"


        post_url = "/accounts/create"
        post_parameters = {"first_name": "Cat",
                           "last_name" : "Resty",
                           "username"  : create_user_target,
                           "password1" : create_pwd_target,
                           "password2" : create_pwd_target,
                           "email"     : create_email_target,
                           }
        looked_for = "flangio user created successfully"

        # looked_for = "This field is required."
        code_return = 200

        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint)


        print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        """

        # Check we have the right permissions
        check_permission(usrname, showprint=True)
        check_permission(create_user, showprint=True)
        check_permission(create_user_target, showprint=True)

        Test_Start("Attempt to delete a SocialGraph - Fail user is not grantor")


        showprint = False
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {
            "grantor": create_user,
            "grantee":create_user_target,
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Unauthorized - You do not have the right to delete this social graph."

        code_return = 401
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        # Give permission to modify social graph then retest delete.
        # give_permission(usrname,permit_this=PERMISSION_NAME ,showprint=True)

        # should still fail because grantor only allowed to remove permission

        showprint = False
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {
            "grantor": create_user,
            "grantee":create_user_target,
            }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Unauthorized - You do not have the right to delete this social graph."

        code_return = 401
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        # Now delete using the grantor account
        showprint = True
        # reset output
        output = []

        post_url = "/socialgraph/delete"
        post_parameters = {
                           "grantor": create_user,
                           "grantee":create_user_target,
                          }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Social graph deleted"

        code_return = 200
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)


        # Now delete again

        Test_Start("Repeat the delete step and force an error - Duplicate record")
        output = []

        looked_for = "Nothing to delete"
        code_return = 200
        result = test_for_post(self, code_return, create_user, create_pwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for,success=False)

        Test_End("Emd of Delete Sequence")


        # clean up permissions
        remove_permission(usrname, not_permitted=PERMISSION_NAME ,showprint=True)


        return
