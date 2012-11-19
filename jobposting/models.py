from django.db import models
from ldap_login.models import user
from django.db.models.signals import post_save
# Create your models here.

class personalised_posting(models.Model):
    post= models.ForeignKey('posting');
    is_interested = models.BooleanField();
    is_hidden = models.BooleanField();
    prn = models.ForeignKey('ldap_login.user')

    def __str__(self):
        return "job posting of %s for %s" % (self.prn.username , self.post.company_name)
 
class posting(models.Model):
    '''described the Job Posting model.
       WARNING: any changes made to this need to be reflected in the corresponding ModelForm in forms.py too!
    '''
    company_name=models.CharField(max_length=50,blank=False,verbose_name='Organization\'s Name');
    company_url=models.URLField(verify_exists=True,verbose_name='Website address');
    description=models.TextField(blank=False,verbose_name='Description',help_text='Please tell in details about the job profile, eligibility, etc');
    how_to_apply=models.TextField(blank=False,help_text='Please tell how students can apply');
    posted_by=models.CharField(max_length=12,blank=False);
    posted_on=models.DateTimeField(auto_now_add=True,editable=False);
    #tally  = models.IntegerField(default=0, verbose_name = "No of Students that have shown interest in this company", editable = False);
    approved_on = models.DateTimeField(editable = False,null = True , blank =True);
    post_status=(('p','pending'),('a','approved'),('d','disapproved'));
    status=models.CharField(max_length=1,choices=post_status, default = 'p');
    
    def test(self):
        self.company_name = "ha ha ha ";
        self.save();
        return "hooooohooooo"

    def __str__(self):
        return "job posting about %s by %s " % (self.company_name, self.posted_by);

    def tally(self):
        #count = personalised_posting.objects.filter(post = self).aggregate(count = 'is_interested = True')
        count = personalised_posting.objects.filter(post=self).filter(is_interested=True).count();
        return count;

def handle_new_posting(sender, **kwargs):
    '''Signal handler whenever a job posting is created
       Refer: http://localhost/docs/django-docs/ref/signals.html#django.db.models.signals.post_save
    '''
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print "A signal was sent by ", sender
    print 
    print "The instance which forced the signal to sent was ", kwargs['instance']
    print 
    #would be applicable if we would be processing post_save
    print "Was a new job posting created or not ?", kwargs['created']
    print
    #print 'The signal id was',kwargs['dispatch_uid']
    print "++++++++++++++++++++++++++++++++++++++++++++"

#Whenever a posting is saved, signal!
#Refer: http://localhost/docs/django-docs/topics/signals.html#listening-to-signals for syntax of the below and why weak is kept False.
post_save.connect(handle_new_posting,sender=posting,weak=False,dispatch_uid='hamaraSignalwa');   
   
