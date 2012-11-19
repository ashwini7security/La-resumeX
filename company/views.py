#pplu Create your views here

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse;
#from django.shortcuts import render_to_response, redirect;
from company.models import *
from student_info.models import *
from ldap_login.models import *
from datetime import datetime
from student_info.utility import our_redirect,get_done

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH,MEDIA_ROOT

''' import spreadsheet generation module'''
from pyExcelerator import *

#TODO: We have to check the licensing restrictions imposed by it.


###############################################################################################
##################           VIEWS THAT RENDER MENU            ################################
###############################################################################################

# Admin page for a admin. 

def admin_index(request):
     if 'username' not in request.session:
        return our_redirect('/ldap_login/')
     #g = group.objects.get(name='placement committee')
     if request.session['role'] != 'admin':  
         return HttpResponse('page not for u');

     t=loader.get_template('company/admin_index.html');
    
     c=RequestContext(request,{
        
        'ROOT':ROOT,
        'MEDIA_URL':MEDIA_URL,
        
        })
     return HttpResponse(t.render(c))


''' Gives the HTML output of students who have got placed ...'''
def got_placed(request):
    
    
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login/')
        
    #if 'POST' not in request: 
    #    print 'no post'
    
    count = student.objects.all().count(); 
    try:
        placed_id = request.POST['what']
        filter = request.POST['filter']
    except KeyError:
        #return HttpResponse('PLease fill all fields')
        return render_to_response('admin/reportsmenu.html', {'ROOT':ROOT},context_instance = RequestContext(request))
    def mkdict(stu,type):
        lala = []
        for items in stu:
            toreturn = {}
            toreturn['other'] = items;
            if type == 0: # items[0].__class__.__name__ = 'student'
                toreturn['company'] = items.company;
                u = user.objects.get(username = items.student.prn);
            else:
                    print items
                    u = user.objects.get(username = items.prn)
            toreturn['group'] = u.groups.all()[0]
            lala.append(toreturn)
        return lala
        
    #g = group.objects.get(name='placement committee')
    #there might be a case when there would be no role in the session!! -- though we need to correct and avoid such a case actually!
    if (not request.session.has_key('role')) or (request.session['role'] != 'admin'):
        return HttpResponse('not for u');
    placed_stu=placement_in.objects.all(); 
    from operator import itemgetter;
    a = lambda(x): itemgetter(filter)(x).__str__()

    if placed_id == 'placed':
        label = ['placed','unplaced']
        context = {'placed':'yes','PS':sorted(mkdict(placed_stu,0),key = a)};
    elif placed_id == 'unplaced':
        slist=[]
        label = ['unplaced','placed']
        for p in placed_stu:
            slist.append(p.student.prn)
        unplaced_stu=student.objects.exclude(prn__in=slist);
        context = {'placed':'no','UPS':sorted(mkdict(unplaced_stu,1),key = a)};
    try:
        leng = len(context['UPS'])
        print context['UPS'] 
    except:
        leng = len(context['PS'])
        print context['PS']
    context['count']=count;
    context['fil'] = filter; #because flter is a keyword i think 
    context['ROOT'] = ROOT 
    

    c = Context(context);
    t=loader.get_template('company/got_placed.html');
    print "=========",request.get_full_path()
    return HttpResponse(t.render(c))




###############################################################################################
#####################           FETCH STUDENTS           ######################################
###############################################################################################


''' Fetch index gives a UI to delect a company and the crieteria's to be fetched. The backend actually fetches the student and puts in a spreadsheet'''
def get_full_list():
    full = list()
    for f in full_list:
        full.append(f);
    maintable = companySpecific.objects.all().order_by('key');
    i = len(full);
    for mt in maintable:
        tempdict = dict();
        tempdict['id']=i;
        tempdict['name']='companySpecific_'+mt.key
        tempdict['display_name']=mt.displayText;
        full.append(tempdict);
        i = i+1;
    return full;


def fetch_index(request):
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login')
        if request.session['role'] !='admin':
             return HttpResponse('page not for u'); 
   
    com=company.objects.all();
    a = ['staff','placement committee']
    g=group.objects.exclude(name__in = a);
    t=loader.get_template('company/fetch_students.html');
    full = get_full_list();
    c=RequestContext(request,{
        'c':com,
        'g':g,
        'ROOT':ROOT,
        'MEDIA_URL':MEDIA_URL,
        'list':full
        })
    return HttpResponse(t.render(c))


''' takes in the post from fetch_students.html . It creates a spreadsheet of all the sudents those who have applied to a particular comapny, with ONLY the information givin tin the post
'''

def get_students_name(request):
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login')
    g = group.objects.get(name='placement committee')

    if user(request.session['username']) not in g.user_set.all():
        return HttpResponse('not for u');
    
    post = request.POST;
    print post.lists();
    for a,v in post.iteritems():
        print a,"======",v,"===",type(v)
    name_list=[]
    if 'company_name' in post:
        com=company.objects.get(name=post['company_name']);
        print "COMPANY ======",com
        name_list=list();
        for g in com.students_applied.all():
            name_list.append(g);
        spreadsheet_name = "SICSR-%s-applicants.xls" % (com.name.replace(' ','-'));
    else:
        p =[]
        for g,v in post.iteritems():
            if g.startswith('groups_'):
                
                s = v.split(',');
                for prn in s:
                    if prn is not "":
                        p.append(prn)
        print p
        s = student.objects.filter(prn__in = p);
        name_list.extend(s);
        spreadsheet_name = "SICSR-students.xls";
    print "List of students is ",name_list;
    if  name_list:
        
        #now we will make a spreadsheet of this data.
        wb = Workbook();
        ws0 = wb.add_sheet('Applicants from SICSR');
        #actually, this is going to come from the person who is selecting the list of students.
        fields_to_get=dict()
        for f,v in request.POST.iteritems():
            if f.startswith('criteria'):
                fields_to_get[int(f[9:])]=v
        print "Fields ro get", fields_to_get
        if len(fields_to_get) is 0:
            return HttpResponse('Check Some Fields to be sent to the company')
        #print headings in the spreadsheet
        full = get_full_list();
        for f in fields_to_get.keys():
            print "title == ", full[f]['display_name'];
            ws0.write(0,f,full[f]['display_name']);

        #print data in the spreadsheet
    
        for x in range(len(name_list)):
            print "X is ...", x, "and s is ...",
            # x is the students name list ka index
            s=name_list[x]
            print "for student", s
            
            for y in fields_to_get.keys(): #hardcoding 4 fields currently
               try:
                # y is the fields ka index
                print "fields to get. ....",fields_to_get[y]            
                si=fields_to_get[y].split('_');
                print "SI ======", si;
                if si[0] == 'student':
                    data = s.__getattribute__(si[1])
                    print "==data===",data    
                elif si[0] == "personal" or si[0] == "swExposure":
                    table= eval(si[0]).objects.get(primary_table=s); 
                    data = str(table.__getattribute__(si[1]))
                elif si[0] == 'workex':
                    data=s.total_workex();
                elif si[0] == 'companySpecific':
                    cs=eval(si[0]).objects.get(key = si[1])
                    csd = companySpecificData.objects.filter(primary_table = s).filter(valueOf = cs)[0];
                    print "CS =====",cs,"CSD =========",csd
                    data = csd.value;
                else:
                    if si[1] == 'graduation':
                        table=marks.get_graduation_course(s)
                        data = str(table)
                    else:    
                        
                            table= eval(si[0]).objects.filter(primary_table=s).filter(course=si[1])[0]; 
                            print "we are using table ", table
                            data = str(table.get_percentage());
               except Exception as e:
                            print "==========HAD GOT and EXCEPTION ;)", e
                            data  = "---"
                            pass;

               #data = eval("name_list[%d].%s" % (x,fields_to_get[y]));
               print "Writing data %s at %d %d" % (data,x,y);
               ws0.write(x+1,y,data);
                                        
        wb.save('/tmp/%s' % (spreadsheet_name));
        copy_spreadsheet_command = "cp -v /tmp/%s %s" % (spreadsheet_name,MEDIA_ROOT);
        get_done(copy_spreadsheet_command);

    t = loader.get_template('company/students_list.html')
    c = Context({
        'students_applied':name_list,
        'spreadsheet_link':MEDIA_URL+'/'+spreadsheet_name,
        'ROOT':ROOT,
        })
    return HttpResponse(t.render(c))   
    #return HttpResponse('f');
    


##############################################################################################
#########################           SEARCH STUDENTS           ################################
###############################################################################################



''' search  for list of student's acc to thier eligibitliyty'''
def search(request):
    t=loader.get_template('company/search.html')
    c=RequestContext(request,{})
    return HttpResponse(t.render(c))

def getResume(request):
    print str(request.POST)
    print "====Now we'l process the post fields..==="
    final_string=""
    for k,v in request.POST.iteritems():
        if k == 'csrfmiddlewaretoken':
            continue
        s=k.split('_')
        #print "==Table name..", s[0],
        #print "Field name ...",s[1]
        if s[2] == "count":
            final_string+="select primary_table from "+ s[0] +" where "+s[1]+" < "+v+"\n";
        else:
            final_string+="select primary_table from "+s[0]+" where "+s[1]+" like %"+v+"% \n";

    print final_string
    return HttpResponse("Please wait till i fetch the resumes...\n\n"+final_string);




###############################################################################################
######################            STUDENTS CAN APPLY           ################################
###############################################################################################




''' For the student's view, This generated a lists of companies vailable for them to apply for. 
Thisgives the company's information as a tooltip, and a check box for apllying. It also disables thecompanies that have gone.
'''
def company_list(request):
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login/');
    else:
        prn=request.session['username'];
    print prn 
    try:
	       s = student.objects.get(pk=prn)
    except Exception as e:
            output = "<h3>Fill in ur details first</h3>";
            return HttpResponse(output);
    u=user.objects.get(pk=prn)
    companies=list();
    for g in u.groups.all():
        h=company.objects.filter(came_for_group=g)
        for c in h:
            if c not in companies:
                companies.extend(h)

     
    print "companies are ",companies

    today=datetime.today()
    main_list=list()
    for c in companies:
        c_dict=dict()
        print "processing Companies",c
        c_dict['name']=c.name;
        c_dict['date_of_applying']=c.last_date_of_applying
        c_dict['process']=c.date_of_process
        c_dict['info']=c.job_description;
        if c.last_date_of_applying > today:
            c_dict['gone']="";
        else:
            c_dict['gone']="disabled=true";
        m=c.students_applied.all()
        if s in m:
            c_dict['Checked']='Checked=true';
        else:
             c_dict['Checked']="";
        print "the dict", c_dict;
        main_list.append(c_dict)
    print main_list     
    t=loader.get_template('company/company_names')
    c=RequestContext(request,{
                'companies':main_list,
                'ROOT':ROOT
                
            });
    return HttpResponse(t.render(c));


'''  For student's info module, It savs the application by a student, if a person has disselected, it asaves that also ;)'''
def apply(request):
    print request.POST
    #check for the session and our_redirect
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login/')   
       
    prn=request.session['username']

    # check for only three entries in POST except for csrfmiddlewaretoken
    if len(request.POST) >4: # onr extra for csrf...
        return HttpResponse('More than Three companies :)')
    # fetch student of ths prn
    
    try:
	       s = student.objects.get(pk=prn)
    except Exception as e:
            output = "<h3>Fill in ur details first</h3>";
            return HttpResponse(output);
    
    # make a list f the companies ths student had applied to pehle
    c=company.objects.filter(students_applied=s)
    #take each company from POST

    for k in request.POST.keys():
         if k == 'csrfmiddlewaretoken':
            continue;
         applied_company=company.objects.get(name=k)
         # if already applied
         if applied_company in c:
             continue;
         else:
            applied_company.students_applied.add(s);
            applied_company.save();           
            #add this student to the list of applied_students
            #save
    # if unchecked.. then remove.
    for k in c:
        if k.name in request.POST.keys():
            continue
        else:
            k.students_applied.remove(s)
            k.save();
        
    return our_redirect('/common/company/done');
