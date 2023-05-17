from django import forms
from .models import Complaint,Student,Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Complaint_form(forms.ModelForm):
    complaint_details = forms.CharField(widget=forms.Textarea(attrs={'rows':'10','cols':'50','class':'input'}), label=False)
    class Meta:
        model = Complaint
        fields = ['complaint_details' , 'branch' , 'category',]

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input'}))
    class Meta:
        model = User
        fields = ['username' , 'password1' , 'password2', 'email']

class Student_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('birth_date','branch',)

class Feedback_form(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows':'10','cols':'80','class':'input'}), label=False)
    class Meta:
        model = Feedback
        fields = ('feedback',)

