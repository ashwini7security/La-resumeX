from django import forms

# Create your Forms here.

class ContactForm(forms.Form):
    types = (('f','Feature Request'),('b','Bug Report'),('s','Suggestion'),('p','Praise! :)'))
 
    subject=forms.CharField(max_length=100,required=True)
    messageType=forms.ChoiceField(label="Message Type",choices=types)
    message=forms.CharField(required=True,widget=forms.Textarea);
    url=forms.URLField(label='URL',help_text="URL of the page where you found the bug or need a feature.",required=True,verify_exists=True);
    screenshot=forms.FileField(help_text="Screenshot for reference, if any",required=False);


