Flang.io - A RESTFul API Toolkit for MongoDB
============================================

Introduction:
-------------

Flangio was designed for data collection in a healthcare and research setting,
but it is a general MongoDB management tool that adds a number of additional
features.

With Flangio you can:


* Perform basic database operations via a web-site including the ability to
easily import CSV and perform searches that return Microsoft Excel(.xls),
CSV(.csv), HTML(.html), and JSON(.json). - No programming experience required. 

* Use flangio's built-in RESTFul API framework or use our examples to quickly
build your own.  - No programming experience required. 

* Use Django "users" and manage a directed graph (i.e. follow-like relationship)
between users.

* Selectively return documents (i.e.  filter "row-level") results based on the
directed user graph.


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
`mongodj`, `dataimport`, and `search`. Most fucntions are
accessiable via web site or a RESTFul API. There project's applications' key
functions are as follows:


* `accounts` - Manages users based on Django's traditional `auth.user` with some
enhancements.

* `mongodb` - Create, Upddate, Delete and Index operations for MongoDB Database
and Collectionmanagement.

* `search` - Read and seeach operations on MongoDBs.  Included in this application
is the ability to create stored searches and convert default JSON output to other
formats including `.csv`, and `.xls`.  

* `dataimport` - Import data form other sources such as CSV into MongoDB. For
larger documents it is reccomended you use the included command line utility
`csv2mongo`





    



