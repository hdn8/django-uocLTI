from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from ims_lti_py.tool_provider import DjangoToolProvider
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.conf import settings 
from utils import *

@csrf_exempt
def launch_lti(request):
    """ Receives a request from the lti consumer and creates/authenticates user in django """

    """ See post items in log by setting LTI_DEBUG=True in settings """    
    if settings.LTI_DEBUG:
        for item in request.POST:
            print ('%s: %s \r' % (item, request.POST[item]))

    if 'oauth_consumer_key' not in request.POST:
        raise PermissionDenied()  
    
    """ key/secret from settings """
    consumer_key = settings.CONSUMER_KEY 
    secret = settings.LTI_SECRET
    
    tool_provider = DjangoToolProvider(consumer_key, secret, request.POST)
    print "ROLES:  %s " % tool_provider.roles
    
    try: # attempt to validate request, if fails raises 403 Forbidden
        if tool_provider.valid_request(request) == False:
            raise PermissionDenied()
    except:
        raise PermissionDenied() 
    
    """ RETRIEVE username, names, email and roles.  These may be specific to the consumer, 
    in order to change them from the default values:  see README.txt """
    first_name = get_lti_value(settings.LTI_FIRST_NAME, tool_provider)
    last_name = get_lti_value(settings.LTI_LAST_NAME, tool_provider)
    email = get_lti_value(settings.LTI_EMAIL, tool_provider)
#    avatar = tool_provider.custom_params['custom_photo'] 
    roles = get_lti_value(settings.LTI_ROLES, tool_provider)
    user_id = get_lti_value('user_id', tool_provider)
    
    if not email or not user_id:
        print "Email and/or user_id wasn't found in post, return Permission Denied"
        raise PermissionDenied()    
    
    """ CHECK IF USER'S ROLES ALLOW ENTRY, IF RESTRICTION SET BY VELVET_ROLES SETTING """
    if settings.VELVET_ROLES:
        """ Roles allowed for entry into the application.  If these are not set in settings then we allow all roles to enter """
        if not roles:
            """ if roles is None, then setting for LTI_ROLES may be wrong, return 403 for user and print error to log """
            print "VELVET_ROLES is set but the roles for the user were not found.  Check that the setting for LTI_ROLES is correct."
            raise PermissionDenied()
        if not isinstance(roles, list): roles = (roles,) # In the case we are using a custom field for roles, may be a string and needs to be converted to a list
        is_role_allowed = [m for velvet_role in settings.VELVET_ROLES for m in roles if velvet_role.lower()==m.lower()]
        if not is_role_allowed:
            print "User does not have accepted role for entry, roles: %s" % roles
            raise PermissionDenied() 
    
    """ GET OR CREATE NEW USER AND LTI_PROFILE """
    lti_username = '%s:user_%s' % (request.POST['oauth_consumer_key'], user_id) #create username with consumer_key and user_id
    try:
        """ Check if user already exists using email, if not create new """    
        user = User.objects.get(email=email)
        if user.username != lti_username:
            """ If the username is not in the format user_id, change it and save.  This could happen
            if there was a previously populated User table. """
            user.username = lti_username
            user.save()
    except User.DoesNotExist:
        """ first time entry, create new user """
        user = User.objects.create_user(lti_username, email)
        user.set_unusable_password()
        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        user.save()
    except User.MultipleObjectsReturned:
        """ If the application is not requiring unique emails, multiple users may be returned if there was an existing
        User table before implementing this app with multiple users for the same email address.  Could add code to merge them, but for now we return 404 if 
        the user with the lti_username does not exist """    
        user = get_object_or_404(User, username=lti_username)
            
    """ CHECK IF ANY OF USER'S ROLES ARE IN THE VELVET_ADMIN_ROLES SETTING, IF SO MAKE SUPERUSER IF IS NOT ALREADY """
    if not user.is_superuser and settings.VELVET_ADMIN_ROLES:
        if [m for l in settings.VELVET_ADMIN_ROLES for m in roles if l.lower() in m.lower()]:
            user.is_superuser = True
            user.is_staff = True
            user.save()
    
    """ Save extra info to custom profile model (add/remove fields in models.py)""" 
    lti_userprofile = user.get_profile()
    lti_userprofile.roles = roles
#    lti_userprofile.avatar = avatar  #TO BE ADDED:  function to grab user profile image if exists
    lti_userprofile.save()
    
    """ Log in user and redirect to LOGIN_REDIRECT_URL defined in settings (default: accounts/profile) """
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL) 
    