""" 
This file contains the default settings, the project 
settings file will override them 
""" 

from django.conf import settings


def setconf(name, default_value):
    """set default value to django.conf.settings"""
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setconf('LTI_DEBUG', False)
setconf('AUTH_PROFILE_MODULE', 'uocLTI.LTIProfile')
setconf('CONSUMER_URL', 'consumer url')
setconf('CONSUMER_KEY', 'the consumer key')
setconf('LTI_SECRET', 'the secret key')
setconf('LTI_FIRST_NAME','lis_person_name_given')
setconf('LTI_LAST_NAME','lis_person_name_family')
setconf('LTI_EMAIL','lis_person_contact_email_primary')
setconf('LTI_ROLES', 'roles')


""" There are two settings used to determine who we allow in the site, and who are admins of the site.
    VELVET_ROLES = Roles allowed for entry into the site, if the user's role is not in this list they will get a 403 Forbidden response 
    VELVET_ADMINS = Roles considered to be site admins; the users with these roles will be admins with access to django admin 
    
    The admin roles need to be in both settings, first they get entry into the site, then they are made admins/staff. 
"""

setconf('VELVET_ROLES', False)
setconf('VELVET_ADMIN_ROLES', False)



