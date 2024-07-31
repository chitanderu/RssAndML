from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import MyUser
from .models import UserFeedInfo

class MyLoginForm(AuthenticationForm):
    username = forms.CharField(label='username', max_length=255)
    password = forms.CharField(label='password', max_length=255)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if email and password:
            user = MyUser.objects.filter(email=email).first()
            print("yes!")
            if not user:
                print("no!!~!")
                raise forms.ValidationError('Invalid email or password')
        return cleaned_data





class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=255)
    name = forms.CharField(max_length=255)
    password=forms.CharField(max_length=255)


    class Meta:
        model = MyUser
        fields = ('email', 'name','password1', 'password2')




class RSSFeedForm(forms.ModelForm):
    class Meta:
        model = UserFeedInfo
        fields = ('url',)
        labels = {
            'url': 'RSS URL',
        }
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }