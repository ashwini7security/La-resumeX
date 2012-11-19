from django.db import models
from datetime  import datetime, date; #for django
from django.db.models.signals import post_save
from datetime import datetime;

# Create your models here.

class student(models.Model):
    gender=(('m',"Male"),('f',"Female"))
    graduation=['Bsc(H) Computer Science', 'Bsc(IT)']
    prn = models.CharField(max_length=12,unique=True,primary_key=True);
    fullname = models.CharField("First Name", max_length=60, help_text="FULL NAME As on your certificates", blank=False)
    sex=models.CharField(max_length=1,choices=gender);
    email=models.EmailField(max_length=255);
    phone=models.CharField(max_length=12, blank = True, null = True);
    backlogs  = models.CharField(max_length=1);
    yeardrop = models.CharField(max_length=1);
    career_objective=models.TextField(blank=False);
    certification=models.BooleanField();
    project=models.BooleanField();
    academic=models.BooleanField();
    extracurricular=models.BooleanField();
    workex=models.BooleanField();
    Extra_field=models.BooleanField();
    last_update=models.DateTimeField(auto_now=True);
    

    def __str__(self):
        return "%s (%s)" % (self.fullname, self.prn);
 

    def total_workex(self):
        '''returns the total workex in months'''
        duration =0
        workex_objs = workex.objects.filter(primary_table=self);
       
        for w in workex_objs:
            duration +=  ((w.endDate - w.fromDate).days)/12; #will return the number of days;

        return duration; 
 
class marks(models.Model):
    primary_table=models.ForeignKey('student');
    course=models.CharField(max_length=30, null=False);
    uni=models.CharField(max_length=100);
    marks=models.DecimalField(max_digits=10,decimal_places=4, blank=True, null=True);
    markstype=models.CharField(max_length=15)
    outof=models.DecimalField(max_digits=10,decimal_places=4, blank=True, null=True);
    fromDate=models.DateField(null=True, blank=True);
    
    def __str__(self):
        if self.marks is None:
            return "%s in %s at %s" %(self.markstype,self.course,self.uni)
        return "Obtained %d out of %s in %s at %s" % (self.marks,self.outof,self.course,self.uni)


    def get_percentage(self):
        '''returns percentage on good data and returns false on bad data or exceptions'''
        try:
            percentage = (self.marks / self.outof) * 100;
            return round(percentage,2);
        except Exception as e:
            print "Can't get percentage because : ",e;
            return False;

    '''Using syntactic sugar :D ref: http://docs.python.org/library/functions.html#staticmethod 
    SADLY: this staticmethod thingy doesn't work with django. So we can't use it.
    '''
    @staticmethod
    def get_graduation_course(prn):
        '''get all marks objects who are graduation = (not 10,12) AND (not starting with M which is for Masters) and IS belonging to the PRN'''
        ms = marks.objects.filter(course__istartswith='B').filter(primary_table=prn);
        try:
            return ms[0];
        except Exception as e:
            return 'not mentioned';
    class Meta:
        verbose_name_plural = 'Marks of Students';

class personal(models.Model):
     primary_table=models.ForeignKey('student', null=False, unique=True);
     mother_name=models.CharField(max_length=50);
     father_name=models.CharField(max_length=50);
     birthdate=models.DateField(null=True);
     areasofinterest=models.CharField(max_length=100,null=True)
     mother_occupation=models.CharField(max_length=50); 
     father_occupation=models.CharField(max_length=50);
     languages=models.CharField(max_length=200);
     hobbies=models.CharField(max_length=200);
     strength=models.CharField(max_length=200);
     per_address=models.TextField(max_length=200,help_text='Permanent Address');
     corr_address=models.TextField(max_length=200, help_text='Correspondence Address');
     def get_age(self):
        '''returns age'''
        age=date.today()-self.birthdate
        return (age.days /365)
     def __str__(self):
        return "Personal details about %s (%s)" % (self.primary_table.fullname, self.primary_table.prn);

     class Meta:
        verbose_name_plural = 'Personal Info about students';

class swExposure(models.Model):
    primary_table=models.ForeignKey('student', null=False);
    programming = models.CharField(max_length=100);
    databases = models.CharField(max_length=100)
    OS = models.CharField(max_length=100)
    swPackages = models.CharField(max_length=100)
    webTools = models.CharField(max_length=100)
  
    def __str__(self):
        return "Software Exposure of %s(%s)" % (self.primary_table.fullname, self.primary_table.prn);

    class Meta:
        verbose_name_plural = 'Software Exposures';

class ExtraField(models.Model):
    primary_table=models.ForeignKey('student');
    title=models.CharField(blank=False,max_length=20);
    desc = models.TextField(blank=False);
    fromDate = models.DateField(null=True,blank=True);
    endDate = models.DateField(null=True,blank=True);
    def __str__(self):
        return "Details about %s  of %s" % (self.title,self.primary_table.fullname);

    class Meta:
        verbose_name_plural = 'ExtraField info about students';

class workex(ExtraField):
    pass;
        
class certification(ExtraField):
    pass;

class project(ExtraField):
    heading=models.CharField(max_length=40 ,blank=True);
    
class academic(ExtraField):
    pass;

class extracurricular(ExtraField):
    pass;


    
 
# strores company specific details that shd not be stored in the resume
class companySpecific(models.Model):
    Types=(('text','Simple Text'),('radio','Simple yes/No type'),('textarea','a large area'),('special','Type, to render speciallyy -> for experts ;)'))
    datatypes = (('none','none'),('numeric','numbers greater than  0'),('string','Only alphabets and spaces.'));
    
    fieldType=models.CharField(max_length=50,default='text',choices=Types)
    key = models.CharField(max_length=100, help_text="enter a key for internal purposes, WITHOUT SPACES or UNDERSCORE(_)")
    displayText=models.CharField(max_length=100,help_text="The text you want to appear on the form");
    is_mandatory = models.BooleanField(help_text= 'Should this field be mandatory' );
    dataType = models.CharField(max_length = 10, help_text = 'What kinds of imput are allowed???', default = 'none' , choices = datatypes)
    createdOn = models.DateTimeField(auto_now_add = True);

    def __str__(self):
        return self.displayText;


class companySpecificData(models.Model):
    primary_table=models.ForeignKey('student')
    valueOf=models.ForeignKey('companySpecific');
    value=models.CharField(max_length=100,blank=True);
    def __str__(self):
        return "value of %s by %s " %(self.valueOf.displayText, self.primary_table.prn)
   



#for references inside various views
tables = {'p':'personal', 'c':'certification','sw':'swExposure','m':'marks','pro':'project','a':'academic','w':'workex','ex':'ExtraField', 'e':'extracurricular'}

def handle_student_updates(sender, **kwargs):
    '''Signal handler whenever any of a student related data is modified and saved
       Refer: http://localhost/docs/django-docs/ref/signals.html#django.db.models.signals.post_save
    '''
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print "A signal was sent by ", sender
    print 
    print "The instance which forced the signal to sent was ", kwargs['instance']
    print 
    #would be applicable if we would be processing post_save
    print "Was a new job instance created ?", kwargs['created']
    try:
       if kwargs['instance'].primary_table:
           s = kwargs['instance'].primary_table;
           print 'Found the student whose data was last modified on %s ' % (s.last_update)
           s.last_update = datetime.now();
           s.save();
           print 'Changed last modified to %s ' % (s.last_update)
       else:
           print "Can't get prn";
    except Exception as e:
        print "Exception %s occured" % e;
    print "++++++++++++++++++++++++++++++++++++++++++++"

#Whenever a posting is saved, signal!
#Refer: http://localhost/docs/django-docs/topics/signals.html#listening-to-signals for syntax of the below and why weak is kept False.
for k,model in tables.items():
    post_save.connect(handle_student_updates,sender=eval(model),weak=False,dispatch_uid='studentUpdateSignal');


#In sabko ume actually use karna hai jab hum version treat karenge au
"""
class ExtraTable(models.Model):
    tables = (('p','personal'),('sw','software_exposure'),('ex','extraField'),('m','marks'),('s','student'))
    Column_Type = (('MVOLD','Multi-valued one line display'),
                   ('MVMLD','Multi-valued multiple line display'),
                   ('SVOLD','Single-valued one line display')
                   );

    column_name = models.CharField(max_length=50);
    column_type = models.CharField(max_length=5,choices=Column_Type);
    column_length = models.PositiveIntegerField();
    column_title = models.CharField(max_length=2,choices=tables);

class ExtraTableKaData(models.Model):
    field = models.ForeignKey('ExtraTable');
    data = models.TextField();"""



