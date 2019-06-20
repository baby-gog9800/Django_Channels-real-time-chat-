from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username",required=True,max_length=200)
    username.widget = forms.TextInput(attrs={'class':'form-control'})
    password = forms.CharField(label="Password",required=True,max_length=200)
    password.widget = forms.PasswordInput(attrs={'class':'form-control'})


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email Id',required=True)
    email.widget = forms.TextInput(attrs={'class':'form-control',})
    username = forms.CharField(label="Username",required=True,max_length=200)
    username.widget = forms.TextInput(attrs={'class':'form-control',})
    password = forms.CharField(label="Password",required=True,max_length=200)
    password.widget = forms.PasswordInput(attrs={'class':'form-control',})
    confirm_password = forms.CharField(label="Confirm Password",required=True,max_length=200)
    confirm_password.widget = forms.PasswordInput(attrs={'class':'form-control',})
