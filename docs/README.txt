=============
Django-uocLTI
=============

Django-uocLTI is a simple app for interfacing django apps to LMS platforms, specifically created for use at the Universitat Obert de Catalunya (UOC).  This app turns a django project into an LTI provider, creating a user and an associated profile with fields based on the Consumer-provided LTI fields (`ims-lti <http://www.imsglobal.org/toolsinteroperability2.cfm>`_).

The app is more-or-less just an example of how to set up a django project for processing an LTI request from the consumer, using the `ims-lti-py library <https://pypi.python.org/pypi/ims_lti_py/>`_, along with a simple profile model to save the fields of interest.  


Installation and Setup
======================

Run setup.py to install uocLTI and its dependencies.  Then, add 'uocLTI' to installed apps in your settings and run syncdb to add the profile table.

Add the following line to your main urls.py file::
    
    url(r'^uocLTI/', include('uocLTI.urls')),
    
Settings::

- CONSUMER_URL: This field is not currently being used.
- CONSUMER_KEY: Used for authentication, along with LTI_SECRET
- LTI_SECRET: Used for authentication, along with CONSUMER_KEY   
- VELVET_ROLES: List of roles which are allowed access to the app  
- VELVET_ADMINS: List of roles which are added as administrators (make sure these are rock solid, they set is_staff=True, is_superuser=True thereby giving full access to the app)
- AUTH_PROFILE_MODULE: Set by default to 'uocLTI.LTIProfile', make sure this is not overriden in settings.  If you are going to be using another custom profile model, then you'll need to remove the code related to the profile fields in views.py.  

Usage
=====

The LTI call from the consumer must not be base64 encoded, and the launchurl is http://<domain>/uocLTI/launch_lti/.  The view processes the request and creates a new user and an associated profile if the user does not exist, else the user is logged in and redirected to the LOGIN_REDIRECT_URL url in settings.