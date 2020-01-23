from django import forms
from .models import *
from django.contrib.auth.models import User   # do i need this ?? 

class ClassroomForm(forms.ModelForm):
	class Meta:
		model = Classroom
		fields = ['name','subject','year']
		#exclude = ['owner',]

class Studentform(forms.ModelForm):
	class Meta:
		model = Student
		exclude = ['classroom',]


class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email' ,'password']

		widgets={
		'password': forms.PasswordInput(),
		}

class SigninForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

