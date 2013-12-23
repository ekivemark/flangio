__author__ = 'Mark @ekivemark'

from settings import *

# Local Django settings for flangio project.

# This is an example for a settings_local.py file.
# Copy this file to the flangio implementation root directory as settings_local.py
#
# Edit the contents to include configuration items for this server instance.
# such as secure access keys for the Amazon cloud or any other secret items
# that you don't want stored back in the git repository.
#
# settings_local.py is excluded from Git.

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin'
ADMIN_MEDIA_PREFIX = 'https://djadminstatic.s3.amazonaws.com/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#           "http://{your_media_store}.s3.amazonws.com/media/"
MEDIA_URL = 'http://flangiomedia.s3.amazonaws.com/media/'
#MEDIA_URL = '/media/'



# If you are using the Amazon cloud you will need a secret_key. Enter it below.
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zz%6w2lqjn1q2vh27kit^n98ppug55pu8pyr4ss$v2hqc^(cav'


#Media Storage options.
BINARY_STORAGE=="AWSS3"


#This must be 'LOCAL', 'AWSS3', or None
BINARY_STORAGE="AWSS3"
# Referenced in settings_local.py to set location of binary storage.

#Set these values to your own AWS S3 credentials.
if BINARY_STORAGE=="AWSS3":
    AWS_BUCKET="flangiomedia"
    AWS_KEY="AKIAI3FSWI4AOSJKO6IA"
    AWS_SECRET="KqZAz0R+VddB0+huVkqXQnV6F3sCFCydOk6Q6TSY"
    AWS_PUBLIC=False
elif BINARY_STORAGE=="LOCAL":
    LOCAL_BINARY_FILE_DIR=os.path.join(BASE_DIR, 'media')
else:
    BINARY_STORAGE=None



#flangio-specific Settings --------------------------------------------------
RESPECT_SOCIAL_GRAPH=True
AUTO_SELF_FOLLOW=True
ALLOW_UPDATE_TX = True
ALLOW_DELETE_TX = True
ENFORCE_TIME_SANITY=False
MAX_TIME_SKEW_MIN=5