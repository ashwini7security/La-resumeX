import ldap;
#class ldapAuthBackend:
def ldap_authenticate(username=None, password=None):
    
    if username is None or password is None:
       return False;
    if username =="" or password =="":
       return False;
    #try ldap login
                #If cannot locate ldap server,
                        #try local login
                #else
                        #do ldap login


    if not username.endswith("@sicsr.edu"):
           username += "@sicsr.edu";
           server = "10.10.21.3"; #jupiter
           try:
               l = ldap.open(server);
               print 'Connecting using %s ******* ' % (username);
               status = l.simple_bind_s(username,password);
               print 'Connect successfully!';
               return True;
           except ldap.LDAPError, error_message:
               print "Couldn't authenticate %s" % (error_message);
