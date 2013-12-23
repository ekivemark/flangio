__author__ = 'mark @ekivemark'
"""
Unit Test Framework Standard Variables used across modules

Author: Mark Scrimshire @ekivemark

Add
{from ..test.settings_test import * }
to top of {app name}/tests.py in order to be able to use variables without the {settings_test.} prefix

Run tests from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py test {app name} >./test_results/{app name}_testresult.txt

Generate the test data
python manage.py dumpdata {app name} --indent=4 >./apps/{app name}/fixtures/{app name}_testdata.json

Copy this file from config/settings_test.py to same location as settings.py
(usually the root of the hive app)

This avoids setting variable values in multiple locations.
"""
import pymongo

# Point to a new Mongo History Database

MONGO_DB_NAME="test"


# Edit this number to your cellphone number for testing purposes.
TESTER_CELL_NUMBER = "7036232789"

# Create a Master Account
MASTER_USER_NAME = "alpha"
MASTER_PASSWORD = "password"
MASTER_EMAIL = "mark+master@healthca.mp"

# User full name = Mark Simple
USER_FIRST_NAME="Mark"
USER_LAST_NAME="Simple"
USER_PIN="4321"
USER_PHONE="999-999-9999"
USERNAME_FOR_TEST='mark'
PASSWORD_FOR_TEST='123456789'
EMAIL_FOR_TEST="spam1@nospam.org"

SMSCODE_FOR_TEST='9999'

VALID_LASTNAME="First"
VALID_FIRSTNAME="Arthur"

USERNAME_NOT_TEST='nottester'
PASSWORD_NOT_TEST='password'

SMSCODE_NOT_TEST='9999'

INVALID_LASTNAME="Wrong"
INVALID_FIRSTNAME="Al"

PERMISSION_DENIED="Permission Denied.  Your account credentials                             are valid but you do not have the permission                             required to access this function."

USER_CREATED_SUCCESS = "flangio user created successfully"

SSN_NUM_VALIDATION_ERROR="You must supply exactly 4 digits."
SSN_ALPHA_VALIDATION_ERROR="Enter a whole number."

VALID_TEST_FIRSTNAME="Ian"
VALID_TEST_LASTNAME="Nitial"


# Home Page look_for_this text
HOME_PAGE_TITLE_TEXT = "Welcome to flangio."

# locsetup
USERNAME_NO_ACCOUNT_TEST = "badusername"
PASSWORD_NO_ACCOUNT_TEST = 'password'

SMSCODE_NO_ACCOUNT_TEST = '9999'

MASTER_PERMISSIONS = {"create-other-users",
                      "create-any-socialgraph",
                      "assign-points",
                      "edit-transactions",
                      "delete-transactions",
                      "delete-any-socialgraph"
                      }
