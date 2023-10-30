from django.contrib.auth.forms import  UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Comment


class Signup(UserCreationForm):
    username = forms.CharField(label='Username',max_length=10,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UserName'}))
    first_name = forms.CharField(label='First Name',max_length=10,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Enter password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
      email=self.cleaned_data['email']
      if User.objects.filter(email= email).exists():
        raise forms.ValidationError("Email already exists")
      return email
    

class EmailBlogForm(forms.Form):
    name = forms.CharField(label='Name',max_length=10,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    from_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),label='Your Email')
    to_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),label='Recipient Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),label='Message')





class CommentForm(forms.ModelForm):
    name = forms.CharField(label='Name',max_length=10,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

   