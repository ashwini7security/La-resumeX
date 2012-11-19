from django.db import models
from student_info.models import student;

# Create your models here.
class resume(models.Model):
    prn = models.ForeignKey('student_info.student',help_text="PRN of the student who's resume was generated",unique=True);
    last_tex_generated = models.DateTimeField(help_text="When was this student's .tex file last generated ?",null=True);
    last_pdf_generated = models.DateTimeField(help_text="When was this student's .pdf file last generated ?",null=True);

    def __str__(self):
        return "resume record of %s " % (self.prn);
