from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#     birtday = forms.DateField(required=False)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
#
#     def save(self, commit=True):
#         user = super(MyRegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['First name']
#         user.last_name = self.cleaned_data['Last name']
#         user.birthday = self.cleaned_data['Birthday']
#
#         if commit:
#             user.save()
#
#         return user

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

