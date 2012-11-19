from jobposting.models import *
from django.contrib import admin
from ldap_login.models import * #currently weak because we don't have fullnams yet :(
from student_info.models import student #for getting d fullname when it's there.
from django.template import Context, loader
from django.http import HttpResponse

class personalizedPostingAdmin(admin.ModelAdmin):
    list_filter = ['post','is_interested'];

class postingAdmin(admin.ModelAdmin):
    list_display= ['__str__','status', 'tally'];
    list_filter = ['status']
    search_fields = ['company_name']
    
    def getStudents(self, request, selected_jobpostings):
        jpStudentsDict = {}
        for jp in selected_jobpostings:
            students_list = []
            for pp in personalised_posting.objects.filter(post=jp).filter(is_interested=True):
                '''try:
                    s = student.objects.get(prn=str(pp.prn));
                    students_list.append("%d - %s" % (str(pp.prn),s.fullname));
                except student.DoesNotExist:'''
                students_list.append(pp.prn);
                '''except Exception as e:
                    print "Unexpected exception in admin %s " % e;'''

            jpStudentsDict['%s : %d students' % (str(jp.company_name),len(students_list))] = students_list;
        print jpStudentsDict;

        t = loader.get_template("jobposting/studentsList.html");
        c = Context ({ 'jpStudents' : jpStudentsDict });
        return HttpResponse(t.render(c));
    getStudents.short_description="List interested students!";

    def approve(self, request, queryset):
        r = queryset.update(status='a');
        if r == 1:
            message_bit = "1 posting was approved"
        else:
            message_bit = "%s postings are now approved" %r;
        self.message_user(request,message_bit);    
    approve.short_description="Approve selected";

    actions = ['approve','getStudents'];

    
admin.site.register(posting,postingAdmin);
admin.site.register(personalised_posting,personalizedPostingAdmin);

