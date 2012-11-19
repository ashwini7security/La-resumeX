from django.shortcuts import redirect
''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH

''' import process helpers '''
import subprocess 
from os import mkdir,chdir,path #for changing directories
from time import sleep

EMAIL_BACKEND = ('django.core.mail.backends.smtp.EmailBackend')

def errorMaker(msg,fatal=False):
    '''displays the given error message nicely and if it's fatal exits'''
    '''I think Apoorva,u can make this better -- i can't find the function u used in change_agent'''
    print msg;
    if fatal:
        exit
    else:
        return;

def debugger(msg):
    '''handles debugging'''
    
    #currently we only print
    print "DEBUG[%s]: %s" % ('Calling function',msg)
    return

def our_redirect(path):
    print ROOT+path
    return redirect(ROOT+path)

def get_done(cmd,path=RESUME_STORE):
    '''handles all panga of executing a command on linux shell'''
    #where do we want to execute this ?
    print "changing path to %s", path
    chdir(path);

    print "Got total --> ", cmd
    cmds = cmd.split(';'); #split multiple commands
    print 'total ',len(cmds);
    for c in cmds:
        try:
           #cmd_with_arguments=c.split();
           print 'Executing ',c

           #connect the pipes in the processes and make the stdin and stdout flow through them properly
           #because Popen doesn't handle pipes properly itself

           sleep(3);
           r = subprocess.Popen(c,shell=True,stdout=None);
           if r is not 0:
               chdir(FULL_PATH); #so that no stupid problem are caused
               return False;    #no need of executing further commands
        except Exception as e:
          print 'Exception was ', e
          chdir(FULL_PATH);
          return False;

    return True;

