from django.db import models
from django.contrib import admin #for special admin things
from datetime import datetime
# Create your models here.

#one group has many users
class group(models.Model):
    name = models.CharField(max_length=20,unique=True);
    created_on = models.DateTimeField(auto_now_add=True);

    def __str__(self):
       if self.name.isdigit() is True:
            Three_yr_courses={ 122:'BBA-IT', 121:'BCA'}
            Two_yr_courses={ 142:'MSc. (CA)', 141:'MBA-IT'}
            course=""
            a=0
            try:
                if int(self.name[5:8]) in Three_yr_courses.keys():
                    a=3
                    course=Three_yr_courses[int(self.name[5:8])]
                elif int(self.name[5:8]) in Two_yr_courses.keys():
                    a=2
                    course=Two_yr_courses[int(self.name[5:8])]   
                yr=course+" 20"+str(self.name[:2]) + '-' + str(a+int(self.name[:2])) 
            except Exception as e:
                yr = self.name
       else:
            yr=self.name
       return yr;

#many user belongs to one group
class user(models.Model): 
    username = models.CharField(max_length=30,primary_key=True); #without the domain suffix
    #password = models.CharField(max_length=255,blank=True,null=True); #we may or many not store the password;
    last_login = models.DateTimeField(blank=True,null=True,default = datetime(2010,12,12,0,0,0));
    created_on = models.DateTimeField(auto_now_add=True);
    groups = models.ManyToManyField(group);
    
    def __str__(self):
	    return self.username;

