from  django import forms
from .models import blog


class blog_form(forms.ModelForm):
  class Meta:
    model = blog
    fields = ('title','description','image')
    

  


