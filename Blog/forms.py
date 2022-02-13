from  django import forms
from .models import blog,blog_catagory


class blog_form(forms.ModelForm):
  class Meta:
    model = blog
    fields = ('title','category','description','image')
    
class blog_cata_form(forms.ModelForm):
 class Meta:
  model =blog_catagory
  fields =('name','slug')
  


