#comment this line when you ARE OUTSIDE SICSR!
from django.http import HttpResponse;
#from django.shortcuts import redirect;
from django.template import RequestContext, loader;
from ldap_login.models import user,group;
from datetime import datetime, timedelta
from django.core.mail import send_mail
from student_info.utility import our_redirect
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect
from laresumex.settings import ROOT
if ROOT == "/laresumex":
    from ldapAuthBackend import ldap_authenticate;
#from django_auth_ldap.config import LDAPSearch
#ldap_login

def login(request):
    #are we processing login attempt ?
    message = None;
    #print request.POST
    if 'username' in request.session:
            if 'redirect' in request.session:
                a = request.session['redirect']
                request.session['redirect'] = ''
                return our_redirect(a);
            else:
                return our_redirect('/home');
    if 'username' in request.POST:# and 'password' in request.POST:
        print "== Got username..!!!!"
        if request.POST['username'] == "":
            print"but its empty"
            status=False;
            message="please enter Username"
        else:    
            print "its Not emply...its",request.POST['username']
            print 'processing login attempt';
            try:
                #comment this line when you ARE OUTSIDE SICSR!
                status = False
                ldap = '';
                if ROOT == "/laresumex":
                    status = ldap_authenticate(request.POST['username'],request.POST['password']);
                    ldap = True
                    print "tried ldap"
   
                if  ldap is not True or status is not True: # if ldap is false, then dont check status as this is primary mode of auth. if ldap is true, then do this only when status is false.
                         print "authenticating via djangi auth"
                         USER = authenticate(username = request.POST['username'], password = request.POST['password'])
                         if USER is not None:
                             print "django login suucess"
                             #request.session['last_login'] = USER.last_login;
                             #login(request,USER);
                             print "Adminuser found, its groups are", user.groups;
                             #ldap = False
                             if USER.is_staff:
                                 request.session['role'] = 'admin'
                             status = True;
                         else:
                             print "django login false"
                             status = False;
                             if ROOT == '':
                                 status = True
                #UNCOMMENT the next line when you are outside SICSR!
                #status = True;
                
                print ldap
                
                print status;
                print 'auth process completed'
            except Exception as e:
                return HttpResponse('Error!!! %s' %  e);
            
        if  status:
                #if successful ldap login
                #update last_login timestamp
                #store encrypted password
                #start session
                request.session.set_expiry(7200);
            
                request.session['username'] = request.POST['username']; 
                userName=request.session['username']
            	#check for user existance... and/or add the use in our feedback database..!!
        
                userexists=user.objects.get_or_create(pk=userName)
                if not userexists[1]:
                    request.session['last_login'] = userexists[0].last_login;
                else:
                    request.session['last_login']=datetime.now();
                print request.session['last_login']
                userexists[0].last_login = datetime.now() + timedelta(minutes = 30);
                userexists[0].save();
		        # this auto gruop assignment takes place by the logic that all students log in from thier PRN's and thier 1st 8 digit of thier PRN represents thier gruop.. to assignm a student to another group we need to do it manually..:) and we need to find out a better way of creating groups..!!! :D
		

		        # to check whether its a student or staff.. :)
                if userName.isdigit() is True:
                    print "its a student"
                    groupid=userName[0:8];
                    request.session['role'] = 'student'
                else:
                    from django.contrib.auth.models import User, Group;
                    try:
                        print userName
                        u_admin = User.objects.get(username = userName)
                        g_admin = Group.objects.get(name = 'placement committee')
                        print "USER == ",u_admin, "GROIUP==", g_admin;
                        if g_admin in u_admin.groups.all():
                            print "admin found";
                            PC_group = group.objects.get_or_create(name= 'placement committee')[0]
                            PC_group.save();

                            userexists[0].groups.add(PC_group);
                            userexists[0].save();
                    except:
                        print "its a staff..!"
                        groupid='staff'
                        print "putting him in group", group;    
                        groupexists=group.objects.get_or_create(name=groupid)[0]
                        groupexists.save();
                        print "groupexists... = ", groupexists
            
                        userexists[0].groups.add(groupexists);
                        userexists[0].save();
   
		
                #our_redirect to the index view!
                if 'redirect' in request.session:
                    a = request.session['redirect']
                    request.session['redirect'] ='' 
                    return our_redirect('/'+a.strip(ROOT));
                else:    
                    return our_redirect('/home');
        else: # if status == False
            message = 'Wrong Username/Password';
            print "because status was", status, "hence message is", message;
            print 'redirecting now...';
            

    else: # when we first enter......
   
    # print request.POST['username']
    # print request.POST['password']
      print "nothing is true hence showing the login teplate again"
    #we aren't either procesing a login attempt OR the user had a failed login attempt!

    t = loader.get_template('ldap_login/login.html');
    c = RequestContext (request,
        {
          'message' : message,
          'ROOT' : ROOT,
        });
         
    return HttpResponse(t.render(c));
          
        
    #unsuccessful ldap login
    #wrong username/password!!!

def logout(request):
    #are we actually logged in ?
    if 'username' in request.session:
        u  = user.objects.get(username = request.session['username'])
        u.last_login = datetime.now();
        print u.last_login
        u.save();
        print 'logging you out';
        request.session.flush();
    else:
		    #no,
            print 'redirecting to login page to tell you to login first :P';
			#then tell me to login first, using the message if possible 
			#message = "Hey, you need to go in before you can go out :P :P";

    return our_redirect('/ldap_login/');	
