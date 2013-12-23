"""
run "python manage.py test accounts>test_results/accounts_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""

__author__ = 'mark @ekivemark'

from django.test import TestCase
from models import User, UserProfile
from ..tests.test_utils import *
from ..tests.settings_test import *

import inspect

"""
Tests for the flangio.accounts app.

Run from root of flangio app.
Run with "python manage.py test {app name}"
Example: python manage.py test accounts >./test_results/accounts_testresult.txt

Remember: every test definition must begin with "test_"

Generate the test data properly indented for readability
python manage.py dumpdata accounts --indent=4 >./apps/accounts/fixtures/testdata.json

"""

# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class Accounts_Simple_TestCase(TestCase):
    """Background to this test harness
       and prove the test harness works
    """

    # Add your fixtures here
    # fixtures = ['testdata.json']

    def test_basic_addition_Accounts(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("flangio.apps.accounts.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("flangio.apps.accounts.tests.py")

        return



class Accounts_User_Cycle_TestCase(TestCase):
    """
    Create, view and delete a user account

    # fields to deal with in create_user:
    first_name  = forms.CharField(max_length=30, label="First Name")
    last_name   = forms.CharField(max_length=60, label="Last Name")
    username    = forms.CharField(max_length=30, label="Username")
    password1   = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label="Password")
    password2   = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label="Password (again)")
    pin         = forms.IntegerField( label="PIN", required=False)
    email       = forms.EmailField(max_length=75, label="Email")
    mobile_phone_number = forms.CharField(max_length=15,
                                          label="Mobile Phone Number",
                                          required=False)
    """

    # fixtures = ['testdata.json']

    def test_login_user(self):
        """ Attempt to login as a user
        """

        Test_Start()

        showprint = False

        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)


        if showprint != False:
            print "User Info:"
            print user_info

        Test_Msg("User Account: "+ str(user_info))

        Test_End()


    def test_create_user(self):
        """
        create a user
        """
        Test_Start()

        showprint = True

        Test_Msg("Creating initial account")
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)

        Test_Msg("Now Test with incomplete credentials")

        usrname = USERNAME_FOR_TEST
        passwd = ""

        # reset output
        output = []
        post_url = "/accounts/create"
        post_parameters = {"first_name": "billy",
                           "last_name" : "tester",
                           "username"  : "billytester",
                           "password1" : "987654321",
                           "password2" : "",
                           "pin"       : "1234",
                           "email"     : "nospam+billy@healthca.mp",
                           "mobile_phone_number" : "999-999-9999"
                          }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Unauthorized - Your account credentials were invalid"

        # set page code expected to be returned
        code_return = 401
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - Not Authorized")
        else:
            Test_Msg("Test Failed for "+str(code_return), success=False)


        Test_Msg("Test with Correct User/Password but invalid data")

        showprint = False

        output = []
        passwd = PASSWORD_FOR_TEST
        looked_for = "This field is required"
        code_return = 500

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        if showprint != False:
            print "Result returned:"
            print result
            print "Output:"
            print output
            print ""

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+" - Errors in the input")
        else:
            Test_Msg("Test Failed for "+str(code_return), success=False)

        Test_Msg("Test with good data")

        showprint = False
        output = []
        looked_for = USER_CREATED_SUCCESS

        post_parameters = {"first_name": "billy",
                           "last_name" : "tester",
                           "username"  : "billytester",
                           "password1" : "987654321",
                           "password2" : "987654321",
                           "pin"       : "1234",
                           "email"     : "nospam+billy@healthca.mp",
                           "mobile_phone_number" : "999-999-9999"
                          }

        code_return = 200
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        if showprint != False:
            print "Result returned:"
            print result
            print "Output:"
            print output
            print ""

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+" - Good Result - User Created")
        else:
            Test_Msg("Test Failed for "+str(code_return), success=False)


        Test_End()


    def test_create_user_fail_required_fields(self):
        """
        check we get error for required fields when creating user
        """

        Test_Start()

        showprint = False
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST

        # First create the initial user
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)


        showprint = False

        # reset output
        output = []

        # Setup Post
        post_url = "/accounts/create"
        post_parameters = {"first_name": "",
                           "last_name" : "",
                           "username"  : "",
                           "password1" : "",
                           "password2" : "",
                           "email"     : "",
                           }
        looked_for = "This field is required."
        code_return = 500

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        if showprint != False:
            print "Result returned:"
            print result
            print "Output:"
        check_error(output[0],post_parameters, looked_for , showprint )
        if showprint != False:
            print post_parameters
            print ""




        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+" - Fields Required")
        else:
            Test_Msg("Test Failed for "+str(code_return), success=False)


        Test_End()

        return


class Accounts_Password_Problems(TestCase):
    """
    Password Fail
    """

    # fixtures = ['testdata.json']


    def test_password_match_fail(self):
        """
        check we get error for required fields when creating user
        """

        Test_Start()

        showprint = False
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST

        # First create the initial user
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)


        showprint = True

        # reset output
        output = []

        # Setup Post
        post_url = "/accounts/create"
        post_parameters = {"first_name": "Rob",
                           "last_name" : "EstCat",
                           "username"  : "REstCat",
                           "password1" : "87654321",
                           "password2" : "87654322",
                           "email"     : "bob@nospam.com",
                           }
        looked_for = "The two password fields didn't match."
        # looked_for = "This field is required."
        code_return = 500

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        if showprint != False:
            print "Result returned:"
            print result
            print "Output:"

        dict_to_check = {'password2':""}
        error_result = check_error(output[0],dict_to_check , looked_for , showprint )

        if showprint != False:
            print "Results from CheckError:"
            print dict_to_check
            print "Error Result:", error_result


        if result == None and error_result == True:
            Test_Msg("Successful Test for "+str(code_return)+" - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return)+" : "+ looked_for, success=False)


        Test_End()

        return

    def test_duplicate_email_fail(self):
        """
        check we get error for required fields when creating user
        """

        Test_Start()

        showprint = False
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST

        # First create the initial user
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)

        check_permission(usrname, True)
        give_permission(usrname,permit_this="can add user profile")
        give_permission(usrname,permit_this="can change user profile")
        give_permission(usrname,permit_this="can delete user profile")
        give_permission(usrname,permit_this="can add user")
        give_permission(usrname,permit_this="can change user")
        give_permission(usrname,permit_this="can delete user")

        check_permission(usrname, True)

        showprint = True

        # reset output
        output = []

        # Setup Post
        post_url = "/accounts/create"
        post_parameters = {"first_name": "Rob",
                           "last_name" : "EstCat",
                           "username"  : "REstCat",
                           "password1" : "87654321",
                           "password2" : "87654321",
                           "email"     : "bob@nospam.com",
                           }
        looked_for = USER_CREATED_SUCCESS

        # looked_for = "This field is required."
        code_return = 200

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)

        if showprint != False:
            print "Result returned:"
            print result
            print "Output:"

        """
        We should have the following output:
        {
    "message": "User creation failed due to errors.",
    "code": 500,
    "errors": [
        {
            "field": "username",
            "description": [
                "This username is already taken."
            ]
        },
        {
            "field": "email",
            "description": [
                "This email address is already registered."
            ]
        }
    ]
}

        """
        # repeat input to force duplicate email error
        code_return = 500
        looked_for = "User creation failed due to errors."
        # reset output
        output = []

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)


        Test_Msg("Checking duplicate username")

        dict_to_check = {'username':""}
        looked_for = "This username is already taken."
        error_result = check_error(output[0],dict_to_check , looked_for , showprint )

        if showprint != False:
            print "Results from CheckError:"
            print dict_to_check
            print "Error Result:", error_result


        if result == None and error_result == True:
            Test_Msg("Successful Test for "+str(code_return)+" - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return)+" : "+ looked_for, success=False)

        Test_Msg("Checking duplicate email")

        dict_to_check = {'email':""}
        looked_for = "This email address is already registered."
        error_result = check_error(output[0],dict_to_check , looked_for , showprint )

        if showprint != False:
            print "Results from CheckError:"
            print dict_to_check
            print "Error Result:", error_result


        if result == None and error_result == True:
            Test_Msg("Successful Test for "+str(code_return)+" - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return)+" : "+ looked_for, success=False)


        Test_End()

        return

    def test_login_logout(self):
        """
        Login and Logout
        """

        Test_Start()

        showprint = False
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST

        # First create the initial user
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)


        showprint = True

        # reset output
        output = []

        # Setup Post
        post_url = "/accounts/login"
        post_parameters = {
                           "username"  : USERNAME_FOR_TEST,
                           "password"  : PASSWORD_NOT_TEST,
                           }
        looked_for = "Login Failed."
        # looked_for = "Invalid username or password."
        code_return = 401

        # reset output
        output = []

        result = test_for_post(self, code_return, usrname, PASSWORD_NOT_TEST, output, post_url,post_parameters, looked_for, called_by, showprint)


        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+" - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return)+" : "+ looked_for, success=False)

        Test_Msg("Now Login properly")

        """
        {
    "message": "OK. User logged in.",
    "code": 200
}
        """


        # reset output
        output = []

        # Setup Post
        post_url = "/accounts/login"
        post_parameters = {
            "username"  : USERNAME_FOR_TEST,
            "password"  : PASSWORD_FOR_TEST,
            }
        looked_for = "OK. User logged in."
        code_return = 200

        # reset output
        output = []

        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint)


        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+" - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return)+" : "+ looked_for, success=False)

        Test_Msg("Now Test Logout")

        """
        {
    "message": "Logged Out.",
    "code": 200
}
        """

        showprint = True

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



        return