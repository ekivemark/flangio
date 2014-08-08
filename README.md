Flang.io - A RESTFul API Toolkit for MongoDB
============================================

Introduction:
-------------

Flangio provides a web interface for MongoDB and simplifies building a RESTFul
APIs in MongoDB. With Flangio you can:


* Perform basic database operations via a web-site including the ability to
easily import CSV and perform searches that return  CSV(.csv), HTML(.html),
and JSON(.json). - No programming experience required. 

* Use flangio's built-in RESTFul API framework or use our examples to quickly
build your own.


Installation
-------------

See README-Installation.md in this project's `docs` folder.  After installed,
login and use the "Web-based API Toolkit Console" to get started.


How you can use flangio for your Projects
-----------------------------------------

Most simply, you can use flangio strictly as a web-based manager for MongoDB.
You can also use flangio as a starting point for your own application or own
customized API.  Many of the features are optional and can be turned of
and on to suit your specific needs by adjusting the `settings.py` file. You can
use flangio as a "backend database" that is accessed primarily by
external systems, via RESTful API, and you can build your own Django application
right inside the flangio project, (therefore accessing MongoDB natively as opposed
through the RESTful API). You simply build out your own Django app (and related urls)
inside `flangio/apps`. If you create an application on flangio you can access
MongoDB natively, via pymongo or another 3rd party MongoDB client.



Components of Flangio
---------------------

There are a handful of core flangio applications.  These are `accounts`,
`mongodb`, `dataimport`, and `search`. Most functions are
accessible via the API Toolkit Console or from a RESTFul API. There project's
core applications' are::

* `mongodb` - Create, Update, Delete, and Index operations for MongoDB database
and collection management.

* `accounts` - Manage users based on Django's traditional `auth.user` with some
enhancements.

* `search` - Read and seeach operations on MongoDBs.  Included in this application
is the ability to create stored searches and convert default JSON output to other
formats including `.csv`, and `.xls`.  

* `dataimport` - Import data into MongoDB from a CSV from a web user interface. For
larger documents it is recommended you use the included command line utility
`csv2mongo`.





    



