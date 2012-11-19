# Create your views here.
#import gdata.gauth;
import gdata;
import time
from django.http import HttpResponse;

def GetAuthSubUrl():
  domain = 'sicsr.ac.in'
  next = 'http://localhost:8000/calendar/event'
  scopes = ['https://www.google.com/calendar/feeds/']
  secure = False  # set secure=True to request a secure AuthSub token
  session = True
  return gdata.gauth.generate_auth_sub_url(next, scopes, secure=secure, session=session, domain=domain)

def InsertSingleEvent(calendar_client, title='Some Company is coming',
                      content='For taking all students for a free lunch!', where='In college',
                      start_time=None, end_time=None):
    event = gdata.calendar.data.CalendarEventEntry()
    event.title = atom.data.Title(text=title)
    event.content = atom.data.Content(text=content)
    event.where.append(gdata.calendar.data.CalendarWhere(value=where))

    if start_time is None:
      # Use current time for the start_time and have the event last 1 hour
      start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
      end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
    event.when.append(gdata.calendar.data.When(start=start_time, end=end_time))

    new_event = calendar_client.InsertEvent(event)

    print 'New single event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)

    return new_event

def login(request):
    txt = "<a href='%s'>Login!</a>" % (GetAuthSubUrl());
    return HttpResponse(txt);

    #authenticate to calendar
    #if first login (get db token)
        #ask for username and password 
        #store the token
    #else
        #retrieve the token
        #authenticate

def event(request):
	calendar_client = gdata.calendar.client.CalendarClient()
	InsertSingleEvent(calendar_client);
    current_url = request.get_full_path();
    # Unlike the other calls, extract_auth_sub_token_from_url() will create an AuthSubToken or SecureAuthSubToken object.
    # Use str(single_use_token) to return the token's string value.
    single_use_token = gdata.auth.extract_auth_sub_token_from_url(current_url);


    
