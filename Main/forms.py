from  django import forms
from Acounnt.models import Acount
from .models import House,Building,extras,galary,aria,Contact
from django.contrib.auth.forms import UserCreationForm ,authenticate


class register_form(UserCreationForm):
 email = forms.EmailField(max_length=50, help_text='User must have email')

 class Meta:
  model = Acount
  fields = ('email', 'username', 'password1', 'password2',)

class AuthenticationForm(forms.ModelForm):
 password = forms.CharField(label='password', widget=forms.PasswordInput)

 class Meta:
  model = Acount
  fields = ('email', 'password')

 def clean(self):
  if self.is_valid():
   email = self.cleaned_data['email']
   password = self.cleaned_data['password']
   if not authenticate(email=email, password=password):
    raise forms.ValidationError('Invalid login')

class UserUpdateForm(forms.ModelForm):
  
  class Meta:
    model = Acount
    fields = ('email', 'username', 'image','phone_number','first_name','last_name','gender')

    def clean_email(self):
      if self.is_valid():
        email = self.cleaned_data['email']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(email='email')
      except Acount.DoesNotExist:
        return email
      raise forms.ValidationError(f'{email} is alredy in use')
    
class house_form(forms.ModelForm):
  class Meta:
    model = House
    fields = '__all__'

class glary_form(forms.ModelForm):
  class Meta:
    model = galary
    fields =('image','proper')
    
class extra_form(forms.ModelForm):
  class Meta:
    model = extras
    fields =('name','proper')
    
class contact_form(forms.ModelForm):
  class Meta:
    model = Contact
    fields =('name','email','subject','messaage')


class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = Acount
    fields = ('email', 'username', 'image', 'phone_number',
              'first_name', 'last_name', 'gender')

  def clean_email(self):
    if self.is_valid():
      email = self.cleaned_data['email']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(email='email')
      except Acount.DoesNotExist:
        return email
      raise forms.ValidationError(f'{email} is alredy in use')

  def clean_username(self):
    if self.is_valid():
      username = self.cleaned_data['username']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(username='username')
      except Acount.DoesNotExist:
        return username
      raise forms.ValidationError(f'{username} is alredy in use')

  def clean_username(self):
    if self.is_valid():
      username = self.cleaned_data['username']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(username='username')
      except Acount.DoesNotExist:
        return username
      raise forms.ValidationError(f'{username} is alredy in use')
