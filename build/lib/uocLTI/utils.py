

def get_lti_value(key, tool_provider):
    """ Searches for the given key in the tool_provider and its custom and external params.  
        If not found returns None """
    
    lti_value = None
    
    if "custom" in key:
        lti_value = tool_provider.custom_params[key]
    if "ext" in key:
        lti_value = tool_provider.ext_params[key]
    if not lti_value:
        try:
            lti_value = getattr(tool_provider,key)
        except AttributeError:
            print "Attribute: %s not found in LTI tool_provider" % key

    return lti_value
        
