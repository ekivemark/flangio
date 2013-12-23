"""
run "python manage.py test home>test_results/home_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""

__author__ = 'mark @ekivemark'

from django.test import TestCase
from ..accounts.models import User, UserProfile
from ..tests.test_utils import *
from ..tests.settings_test import *

import inspect

"""
Tests for the flangio.home app.

Run from root of flangio app.
Run with "python manage.py test {app name}"
Example: python manage.py test home >./test_results/home_testresult.txt

Remember: every test definition must begin with "test_"

Generate the test data properly indented for readability
python manage.py dumpdata home --indent=4 >./apps/home/fixtures/testdata.json

"""

# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class Home_Simple_TestCase(TestCase):
    """Background to this test harness
       and prove the test harness works
    """

    # Add your fixtures here
    # fixtures = ['testdata.json']

    def test_basic_addition_Home(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("flangio.apps.home.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("flangio.apps.home.tests.py")

        return

    def test_load_home_page(self):
        """
        Test that we are loading the home page
        """

        Test_Start()

        showprint = False

        Test_Msg("Go to Home Page for flangio")

        # No need to be logged in to get the home page.
        usrname = ""
        passwd = ""
        # reset output
        output = []
        post_url = "/"
        post_parameters = {}
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = HOME_PAGE_TITLE_TEXT

        # set page code expected to be returned
        code_return = 200
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for)


        Test_End()
