from django.db import models
from student_info.models import student

# Create your models here.

class company(models.Model):
    x = lambda : "Open for all! ";
    name=models.CharField(max_length=40);
    last_date_of_applying=models.DateTimeField();
    students_applied=models.ManyToManyField('student_info.student',blank=True)
    date_of_process=models.DateTimeField();
    email_id=models.EmailField(help_text='Email of the Company contact (will not be displayed to students)');
    phone_number=models.CharField(max_length=20,help_text='Phone number of the Company contact (will not be displayed to students)')
    #comapny_url=models.CharField(max_length=20)
    came_for_group=models.ManyToManyField('ldap_login.group',help_text='Eligible group of students')
    about=models.TextField(help_text='Information about the company to be displayed to students', blank = True, null = True);
#    eligibilty=models.TextField(help_text='Elgibility and other such information to be displayed to students');
    job_description=models.TextField(help_text='Job profiles the company has to offer and the eligibility criteria.', default = x());

    def __str__(self):
        return "%s" % (self.name);

    class Meta:
         verbose_name_plural = "companies"

class placement_in(models.Model):
    jobtype=(('i',"Internship"),('p',"Placement"),('ip','Internship+Placement'))
    
    student= models.ForeignKey('student_info.student');
    company = models.ForeignKey('company');
    profile = models.CharField(max_length=50);
    placementType = models.CharField(choices=jobtype, max_length=2, default = 'i')
    date_of_offer = models.DateField();
    date_of_joining = models.DateField();
    starting_stipen = models.CharField(max_length = 10, null=True, blank = True);
    offered_salary = models.CharField(max_length = 10 ,  default = "0.00");
    place = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return "%s got %s in %s " %(self.student.fullname, self.get_placementType_display(), self.company.name)

    class Meta:
        verbose_name_plural = 'Which Student Got Placements';

full_list=[
{ 'id':0,'name':'student_fullname',"display_name":'Full Name'},
{ 'id':1,"name":'personal_birthdate',"display_name":'birthdate'},
{ "id":2,"name":'marks_Xth_marks',"display_name":'10th Marks'},
{ 'id':3,"name":'marks_XIIth_marks',"display_name":'12th Marks'},
{ 'id':4,"name":'marks_graduation_course',"display_name":'Graduation Course'},
{ 'id':5,"name":'marks_graduation_marks',"display_name":'Graduation Marks'},
{ 'id':6,"name":'workex_function_workex',"display_name":'Years of Workex'}
]

