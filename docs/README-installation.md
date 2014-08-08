Installation and Configuration
==============================

This document contains information on setting up flangio for development or
production. These were graciously written by Mark Scrimisre @ekivemark.

Installation on Ubuntu 14.04:
-----------------------------


flangio is built atop Django and MongoDB so these need to be setup first.

These instructions are for Ubuntu 13.04, but can be modified to support other
non-debian Linux sources. Install some prerequisites.

    sudo apt-get update
    sudo apt-get upgrade
    sudo-apt-get install python-pip build-essential python-virtualenv apache2 libapache2-mod-wsgi python-pymongo python-bson python-dev nmap git-core

    sudo apt-get install python-setuptools
    sudo pip install virtualenvwrapper

Now install MongoDB. See
(http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/) for more
information.

    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    sudo apt-get update
    sudo apt-get install mongodb-10gen
    sudo apt-get update
    
    
Create a working directory to hold our Django projects, then change into that
directory.
    
    mkidir django-projects
    cd django-projects

Download most recent flangio using Git:
    
    git clone https://github.com/videntity/flangio.git
    cd flangio
    
Install other python requirements from a requirements file (Django, etc.)

     sudo pip install -r flangio/config/requirements.txt
     

Using Django's `manage.py` command, create the project's relational database
(i.e. not MongoDB).  

    python manage.py syncdb


These tables manage users, accounts, and other information. Some tables are
created as part of Django and 3rd party packaes.
By Default flangio uses SQLite. This is SQLite by default and is stored
in a directory called `db` in the project's root directory.

Create a file to hold our sinceid index counter.

    echo "0" > db/since.id
   
Change the permissions on the entire folder so Apache can use it. (SQLite specific)

    chmod -R 777 db   
    
Flangio also needs to have permission to use the uploads folder. 

    chmod -R 777 uploads
    
Add a couple lines to the file `/etc/apache2/sites-available/000-default.conf` inside the
`<VirtualHosts></VirtualHosts>` tags.

    WSGIScriptAlias / /home/ubuntu/django-projects/flangio/flangio/config/apache/django.wsgi
    WSGIPassAuthorization off

Add the following lines to the same file, inside the same <VirtualHosts></VirtualHosts> section. 
This is needed to allow Apache to access the WSGI file used by Flangio

    <Directory /home/ubuntu/django-projects/flangio/flangio/config/apache>
      <IfVersion < 2.3 >
       Order allow,deny
       Allow from all
      </IfVersion>
      <IfVersion >= 2.3>
       Require all granted
      </IfVersion>
    </Directory>



Restart Apache

    sudo service apache2 restart
    
    
If you haven't started MongoDB do that now:

    sudo /etc/init.d/mongod start
    
or using the command:

    sudo start mongod
    
For more information on configuring Django with apache or other Web servers
such as NGINX, see https://docs.djangoproject.com/en/1.3/howto/deployment/modwsgi/.
For performance, static content should not be served via Django.


Advanced Configuration Options
------------------------------


flangio extends Django's `settings.py` file for its custom settings parameters.
You can override things by defining a file called `settings_local.py` and place it
in the same folder as `settings.py`.  


    # Django default settings for Flangio------------------------------------
    # Anything in this file can overridden by creating a
    # settings_local.py file and placing additional settngs there.
    .
    .
    # flangio Default Settings -------------------------------------------------
    
    # The next 2 settings ensure that the transaction time is no more off +/-
    # MAX_TIME_SKEW_MIN
    
    
    ENFORCE_TIME_SANITY  = False
    
    # Maximum time in minutes the transaction time submitted by the client can be
    # off from UTC.
    
    MAX_TIME_SKEW_MIN    = 5   
    
    #Deprecated
    OTHER_LABELS         = False # If True, use label value from DataLabelMeta instead of default.



    # If following MUSLEI format, then users related must exist before DB IO can
    # This goes for all three actors; `sender`, `receiver` and `subject`. 
    USERS_MUST_EXIST     = True
    
    
    # If set to False it creates an "admin party" arrangement amongst all
    # registered users.
    RESPECT_SOCIAL_GRAPH = False
    
    
    #When an account is created, then create a self follow social graph.
    AUTO_SELF_FOLLOW     = True
    
    # Deprecated
    ALLOW_UPDATE_TX      = True
    
    
    # Deprecated
    ALLOW_DELETE_TX      = True
    
    
    
    # Change this to change how files uploaded are stored. It can be stored on
    the same server  LOCAL means save it to this server, AWSS3 means use S3.
    # You must have your AWS keys defined in settings for this to work.
    # Allowable values are 'LOCAL' (default), 'AWSS3'.
    
    BINARY_STORAGE = "LOCAL"
    

    # On the master database/collection sort the resulting columns by these names.
    # If a blank tuple (default), no sorting will occur.
    
    SORTCOLUMNS= ()
    
    
    
    #Mongo DB settings
    
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DB_NAME = "flangio"
    MONGO_MASTER_COLLECTION = "quantified-clan"
    #MONGO_HISTORYDB_NAME = "history"
    
    # Default limit for search queries. This can be overridden by user.
    MONGO_LIMIT = 200
    
    
    # This file creates an ever incrementing integer ID for every MUESLI-compliant
    # transaction. This is basicly identical to Twitter's sinceid field.
    # In production on high-vaulme systems place this on its own filesystem or
    replace this with a database.
    
    SINCE_ID_FILE = os.path.join(BASE_DIR, 'db/since.id')
    
    
    # Defaulted to MUESLI See http://code.google.com/p/muesli for more information.
    # MUESLI = Mobile Universal Encapsulated Serialized Longitudinal Information
    
    
    ALLOWABLE_TRANSACTION_TYPES = ("text","tweet", "omhe")
    
    
    ALLOWABLE_HEALTH_TRANSACTION_TYPES = "text","omhe", "indivo", "hdata", "pdf",
                                  "png", "jpg", "bmp", "tiff", "jpeg200",
                                   "ms_word_doc", "ms_word_docx","ms_excel_xls",
                                   "ms_excel_xlsx", "tweet", "snomedct", "hl7v2",
                                   "cda-c32", "ccda", "ccr", "ccd", "unk", "icd9",
                                   "icd10", "cpt", "script", "hicpcs", "loinc",
                                   "lab", "rx", "cd-iso", "dvd-iso", "zip",
                                   "tar.gz", "rxnorm", "dicom_image",
                                   "dicom_structured_report", "x10", "idc",
                                   "edi", )



