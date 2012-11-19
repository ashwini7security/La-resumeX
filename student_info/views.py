#Create your views here.
''' impmrt data models '''
from student_info.models import *;
from student_info import tables
''' import generator helpers '''
from django.template import Context, loader
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from datetime import datetime


''' import utility functions '''
from student_info.utility import our_redirect,errorMaker, debugger;
from pprint import pprint
from os import path;
from django.utils.encoding import smart_unicode;

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH,DEBUG

''' import traceback for debugging '''
if DEBUG is True: #do not import when not needed!
    from sys import exc_info; #for getting traceback
    import traceback; #for printing traceback;


##########################################################################
###################### STUDENT FORM ######################################
##########################################################################

def showform(request):
    if 'username' not in request.session:
        print "No session"
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login')
    prn=request.session['username'];    
    
    #the user shoud not get the form if he already has one.
    try:
        s=student.objects.get(pk=request.session['username'])
        print "student Fornd...", s
        return our_redirect('/student_info/%d/edit' % prn);
    except Exception as e:

        print "student does not exist" 
        if prn.isdigit():
            yr=prn[5:7];
        else:
            yr = 'staff'
        print yr
        maintable=list(companySpecific.objects.exclude(fieldType='special').order_by('displayText'));
        print(maintable);       

        t=loader.get_template('student_info/form.html')
        c=RequestContext(request,
            {
                'flag':'form',
                'prn':prn,
                'ROOT':ROOT,
                'mt':maintable,
                'yr':yr
            }
            );
    
        return HttpResponse(t.render(c));


def edit(request,prn):
    if "username" not in request.session:
       print "no session found"
       request.session['redirect'] = request.get_full_path();
       return our_redirect("/ldap_login")
    if prn != request.session['username']:
        print "prn", prn, type(prn)
        print "username", request.session['username'],type(request.session['username'])
        return HttpResponse('Please Edit ur own form :@')
    '''The problem with this view :
            We(I) are doing it the old-fashioned way. 
            We(I) are not using the power of Models which allow automatic server-side validation -- i need to read on that.
    '''
        
    #was prn passed and is it numeric really?
    if prn is not None and prn.isdigit() is True:
        #are we authorized to edit this ?
            #do we hv global edit privileges ?

            #kya ye hamara hi resume hai ?

        #do we hv the record ?
        s = student.objects.filter(pk=prn); #see the way to unzip a tuple that is returned by a func
        if len(s) is 0:
            return HttpResponse('This user doesnt exists');
        else:
            s=s[0]
            debugger("Resume found! Using it");
        
        #get all the records and tell us whether they were creatd or retrieved
        #have moved this to the student_info.models, because all Model info must come from there and tomo if we add a new model, we shouldn't have to come here to provide it's functionality.
        table=tables.get_tables(s)        
        #get company specific required fields
        '''We are segregating the company Specific thigs into 3 sequences... 
        a) the main table, which consists all rows of the main table structurw. Who are neither special kinds, nor are already filled. 
        b) cs are the data filled by this partucular student.
        Main table fetches all the data to be collected per student. CS is the data ctually filled by the students. this is used to prefill the foem while editing.and the maintable is required for the "form" for a new user.
        '''

       
        cs=companySpecificData.objects.filter(primary_table=s).order_by('valueOf')
        maintable=companySpecific.objects.exclude(fieldType='special').exclude(companyspecificdata__in = cs).order_by('displayText');
        print "CS ====",cs
        print "Maintable....",maintable
        
        table['mt']=maintable;
        table['cs']=cs;
        table['flag']='edit';

        c = RequestContext(request,table);
        t = loader.get_template('student_info/form.html');
        
        return HttpResponse(t.render(c));


##########################################################################
#################### STUDENT FORM SUBMIT #################################
##########################################################################


def submit(request, prn):
    '''processes submissions of NEW forms and also EDIT forms!'''

    if 'username' not in request.session:
        print "no session found"
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login')
    
   #was javascript enabled and everything ok on the client side ???
    if not ('allok' in request.POST and request.POST['allok'] == '1'):
       return HttpResponse("<h2 align='center' style='color: red;'>  Hey, This is Server, you need to enable JavaScript if you want us to help you! </h2>");

    #what is submitted ?
    print "I have got files called ", request.FILES;

    photo_file=RESUME_STORE+"/photos/"+prn+".png";
    
    if path.exists(photo_file):
        photo_exists = True;  
        print "Photo already existed";
    else:
        photo_exists = False;
        print "Photo doesn't exist already";
    
    if len(request.FILES) is 0:
        print "No photo was submitted!";
    else:
        print "A photo was submitted!";

    #let's make photo file non-mandatory.
    #if not photo_exists and len(request.FILES) is 0:
    #    return our_redirect('/form')

    #TODO: check whether the photo is a photo or something else ?
    for f in request.FILES.values():
            dest=RESUME_STORE+"/photos/"+prn+".png" #so that things remain soft-coded :P
            print "files to be saved in", dest;
            destination = open(dest, 'wb+')
            print "i got the file handle as ",destination
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    
    
    post=request.POST;
    print "========>>>POST<<<========"
    for p,v in post.lists():
        print p,"..........",v
    # pprint(post);

    # check for the validity of the prn etc...
    s=student.objects.filter(pk=prn)
    print s, len(s)
    if len(s) is 1:
        print " ======>>> editing original <<<======="
        s[0].delete() #delete to create a new one.
    
    try:

        s = student.objects.create(
            pk=prn,
            fullname=post['fullname'],
            career_objective=post['career_objective'],
            )
    
        s.save(); #will also update the timestamp;
        p = personal.objects.get_or_create(primary_table=s)[0];
        table_dict=dict();
        mvsd=dict();
        extra_fields = dict()
        l = ['marks', 'extracurricular','academic','certification','project','workex','ExtraField'] #list of model names other than personal.


        for field,data in post.lists(): #it will be a list
            #we are using this long branch of IF and ELIFs because Python doesn't have switch case!!!
            if field == 'csrfmiddlewaretoken':
                continue;
            field_name=field.split('_');
            print "type(field)", type(field), field
            if len(field_name) is 1: # for student model
                #print "=====>Setting ", field_name[0] , "of student with ",data[0]
                s.__setattr__(field_name[0],data[0])
                continue;
            if field_name[0] == 'personal':  
                if field_name[2].isdigit() is False:
                    index=field_name[1]+'_'+field_name[2];
                    #print "=====> adding", data , "to attribute", index, "of Personal";
                    p.__setattr__(index,data[0]);     
            if field_name[0]=="birthdate" and field_name[1] == 'monthyear':
                date=data[0].split(',')
                print "=====>DATE<=====",date
                print datetime(int(date[2]),int(date[1]),int(date[0]))
                p.__setattr__("birthdate",datetime(int(date[2]),int(date[1]),int(date[0])));
                #if it's an ExtraField
            '''elif 'ExtraField' in field_name[0]:
                print "found ExtraFile"
                field_name=field.split('_');
                column_dict=dict();
                column_dict[field_name[1]]=data;
                index=field_name[0]+'_'+field_name[2];
                if field_name[0].lstrip('ExtraField') == '':
                    continue             
                if index not in table_dict:
                   i='ExtraField_title_'+field_name[0].lstrip('ExtraField');
                   table_dict[index]={'title':post[i]}
                table_dict[index].update(column_dict);'''

            if (field_name[0] == 'companySpecific'):
                try:
                    cs=companySpecific.objects.get(key=field_name[1])    
                    print "\n\nCOMPANY SPECIFIC....!!!!!!...."
                    #print "\n\n\nCOMPANY SPECIFIC...!!!!!!...", data, type(data);
                    a = str(data[0]);
                    for d in data[1:]:
                        a += ',' + d
                    csd=companySpecificData(
                    primary_table=s,
                    valueOf=cs,
                    value=a                
                    );
                    csd.save();
                except:
                    pass;
            if str(field_name[0]) in l:
                column_dict=dict();
                column_dict[field_name[1]]=data[0];
           
                if "title" not in column_dict:
                    if field_name[0]=="ExtraField":
                        column_dict['title']=post.get('ExtraField_title_1','') #if it's not found return a default value -- because it was raising exceptions...done using django-docs/ref/request-response.html#querydict-objects
                    else:    
                        column_dict['title']=field_name[0]
           
                index=field_name[0]+'_'+field_name[2];
           
                if index not in table_dict:
                    table_dict[index]=dict()
           
                table_dict[index].update(column_dict)
           
            '''row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=s);
            row[field_name[1]] = data;'''
            if len(field_name) is 3 and field_name[0] not in l: # for multi-valued single Display
              print "!!!!!!!!inside mvsd processing";
              if field_name[2].isdigit() is False:
                field_name[1]=field_name[1]+'_'+field_name[2]  
              else:
                index=field_name[0]+'_'+field_name[1];
                if index not in mvsd:
                    mvsd[index]=data[0];
                else:
                   mvsd[index]+=','+data[0];
                   
 

            #if we are retrieving the data
            '''row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=prn);
             row[field_name[1]] = data;
             row.save();'''
             
        p.save();
        print "P saved"
    
        print "=========>>>> The Main list : <=============="    
        pprint(table_dict)
        #print "======> s/w Exposure====="
        #print sw_exposure 
        print "=====>MVSD<======"
        print mvsd
    except Exception as e:
        print "======EXCEPTION....while submitting============", e,;
        print 
        print "=====Traceback====="
        #exception_info = exc_info();
        #traceback.print_tb(exception_info[2]);
        return our_redirect('/form')
    
    # ============>>> MVSD <<<====================
    for table_row, value in mvsd.iteritems():
        if table_row.startswith('Extra'):
            continue;
            print "FO"

        tablerow=table_row.split('_');
        if tablerow[0] == "personal":
            table=p;
        else:
            table=eval(tablerow[0]).objects.get_or_create(primary_table=s);
            table=table[0];
        
        print "table-->",table;
        print "we have a column called __%s__" % (tablerow[1]);
        print "value--> Can't be printed here you stiupid!"
        #print "value--->",value;
        table.__setattr__(tablerow[1], value);
        table.save();
        #print "table value====>>>", table.__getattribute__(tablerow[1])
        #print table,".",tablerow[1]," value set to ", table.__getattribute__(tablerow[1]);

    #===========>>> Table Dict <<<=================
    for table, row_values in table_dict.iteritems():
        r=table.split('_')
        print "=======> table ", r[0];
        t=eval(r[0])();
        t.primary_table=s
        print "Creating new row for ", r[0];
        if "desc" in row_values and row_values["desc"] == "":
            print "======>>FALTU FIELD<<======" # for field that just comes in the POST.. will need to fix in the form later.
            continue;
        s.__setattr__(r[0],True);
        for c,d in row_values.iteritems():
            if "monthyear" in c:
                date=d.split(',');
                d=datetime(int(date[2]), int(date[1]), int(date[0]))
                if "end" in c:
                    c="endDate"
                else:
                    c="fromDate"
            t.__setattr__(c,d);
            #UNCOMENT BELOW ONLY IN DEV ENVIRONMENT NOT PRODUCTION - YOU HAVE BEEN WARNED
            #print r[0],".",c,"======>",d;    
        t.save();    
        print "Saved"
    s.save();
    print "S,saved"
    p.save();
    print "P saved"
    return our_redirect('/common/Submitted/done');



########################################################################
######################   OTHER FIELDS    ###############################
########################################################################

def ajaxRequest(request):
    '''for processing any ajax request for a field data'''
    '''will accept data in XML (ok?) and return data in XML '''
    pass;

    return our_redirect('/student_info/%d/edit' %(int(request.session['username'])))
    return HttpResponse('you arent supposed to see this page. if u see this please contact apoorva')



