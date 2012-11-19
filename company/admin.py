from company.models import *
from django.contrib import admin
from student_info.models import student; #for mailing the student on his personal mail address.
from django.core.mail import EmailMessage,get_connection #because this one actually let's use BCC and all.
from django.template import Context, loader
from laresumex.settings import MANAGERS;
'''
class membershipInline(admin.TabularInline):
    model = student_info.placement_in.set; #a reference to the intermediary modeli
    extra = 1
#    fk_name = 'placement_in'
'''

class companyAdmin(admin.ModelAdmin):
    __name__='CompanyAdmin';
    readonly_fields = ['students_applied']; #will display this field as a link rather than editable box
    
    #for list display
    list_display = ('name','date_of_process','last_date_of_applying')
    list_filter = ['came_for_group'];
    #inlines = [
    #    membershipInline,
    #    ]
    
    #add a set of actions
    actions = ['informStudents'];

    def informStudents(self, request, selectedCompanies):
        print "Informing students about ",selectedCompanies;

        t = loader.get_template('company/informStudents_mail.html');
        conn = get_connection(); #for mailing
        
        
        for c in selectedCompanies:
            ppltoInform = c.came_for_group.get_query_set()[0].user_set.all() 
            context = Context(
                {
                    'company' : c,
                })

            body = t.render(context)

            to = [];
            for p in ppltoInform:
                to += ["%s@sicsr.ac.in" % str(p.username)]; #for primary sicsrwala address
        
            #send mail actually.
            email = EmailMessage();
            email.from_email = '"Ashwini Narayan" <placements@sicsr.ac.in>';
            email.subject = '[Placements] %s coming to campus' % c.name;
            #email.from = 'root@sdrcserver.sdrc'; #left for automatic putting
            email.connection = conn;
            email.body = body;
            
            cc = [];
            # Getting the From/ CC from the placement Committee group.
            from django.contrib.auth.models import Group;
            g = Group.objects.get(name = 'placement committee')
            
            for u in g.user_set.all():
               cc.append(u.email)
            
            bcc = []
            for m in MANAGERS:
                bcc.append(list(m)[1])
            
            email.to = to + cc;
            email.bcc = bcc;
            print "to is ",email.to;
            print "bcc is ",email.bcc;
            print "body is ",email.body
            email.content_subtype='html';
            email.send();
            dir(email)
            print "Done with %s" % (c);

        self.message_user(request,"Successfully informd students");    
    informStudents.short_description = "Inform students about companies"

class placement_inAdmin(admin.ModelAdmin):
    list_filter = ['company']

admin.site.register(company,companyAdmin);
admin.site.register(placement_in,placement_inAdmin);

