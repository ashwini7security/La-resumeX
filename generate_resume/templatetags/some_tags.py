from django import template
from datetime import datetime

register = template.Library()

@register.filter
def split(s,splitter):
    #print "We got %s and the type is %s" % (s,type(s))
    
    if s is None or s == '' or s.strip() == '': 
        #print "Returning a blank list"
        return None
    else:
        #print "returning a split thingy", s.split(splitter);
        return s.split(splitter)

split.is_safe=True;
