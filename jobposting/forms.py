from django.forms import ModelForm
from jobposting.models import posting
from django import forms;

# Create your forms here.

class JobPostingForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    #SECOND THOUGHT: Client side validation is a jimmedar of template. This field is nowhere reflected in the Model's instance except by the value 'This is a walkin' in the how_to_apply field. Hence, we don't handle it in anyway here :)
    ##add this extra field 
    '''walk_in=forms.BooleanField(label="Is this a walk-in?");'''

    class Meta:
      model = posting
      #the list of fields, in the order, that they will be displayed on the form
      fields = ('company_name','company_url','description','how_to_apply'); 
        
  
''' walkin=(('on','yes'),('off','no'));
    company_name=forms.CharField(max_length=50);
    company_url=forms.CharField(max_length=50);
    profile=forms.CharField(widget=forms.Textarea);
    walk_in=forms.ChoiceField(choices=walkin,widget=forms.CheckboxInput(attrs={'onchange':'a(this);'}));
    how_to_apply=forms.CharField(required=False,widget=forms.Textarea) '''
