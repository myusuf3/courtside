from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField
from register.models import Sport, GENDER_CHOICES


class PlayerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    email = forms.EmailField()
    sports = forms.ModelMultipleChoiceField(queryset=Sport.objects.all(),
                                        widget=forms.CheckboxSelectMultiple(attrs={'class':'input_text'}),
                                        label='Sports')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select,
                                label='Gender', help_text='optional', required=False)
    phone_number = USPhoneNumberField(help_text='optional', required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if len(user) > 0:
            raise forms.ValidationError('Email has been activated')
        return self.cleaned_data['email']

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if len(user) > 0:
            raise forms.ValidationError('username has been already taken')
        return self.cleaned_data['username']


class NewPlayerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text'}), label='Password')
    password2 =  forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text'}), label='Re-type Password')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input_text'}))
    sports = forms.ModelMultipleChoiceField(queryset=Sport.objects.all(),
                                        widget=forms.CheckboxSelectMultiple(attrs={}),
                                        label='Sports')
    gender = forms.ChoiceField(choices=GENDER_CHOICES,
                              widget=forms.Select(attrs={'class':'input_text'}),
                              label='Gender', help_text='optional', required=False)
    phone_number = USPhoneNumberField(widget=forms.TextInput(attrs={'class':'input_text'}), help_text='optional', required=False)

    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password1']:
            raise forms.ValidationError('passwords do not match!')
        return self.cleaned_data['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if len(user) > 0:
            raise forms.ValidationError('Email has been activated')
        return self.cleaned_data['email']
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if len(user) > 0:
            raise forms.ValidationError('username has been already taken')
        return self.cleaned_data['username']



class GameForm(forms.Form):
    sport = forms.ModelChoiceField(queryset=Sport.objects.all(), widget=forms.Select, label='Sports')
    start_date = forms.DateField()
    start_time = forms.TimeField()
    address = forms.CharField(max_length=50)
    minimum_players = forms.IntegerField()
    restrictions = forms.CharField(max_length=200, help_text='eg., 3 on 3, Women Only', required=False)


class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_text'}), max_length=50)
    email = forms.EmailField()
    sports = forms.ModelMultipleChoiceField(queryset=Sport.objects.all(),
                                        widget=forms.CheckboxSelectMultiple,
                                        label='Sports')
    gender = forms.ChoiceField(choices=GENDER_CHOICES,
                              widget=forms.Select,
                              label='Gender', help_text='optional', required=False)
    phone_number = USPhoneNumberField(help_text='optional', required=False)

    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password1']:
            raise forms.ValidationError('passwords do not match!')
        return self.cleaned_data['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if len(user) > 1:
            raise forms.ValidationError('Email has been activated')
        return self.cleaned_data['email']


class PasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text'}), label='Password')
    password2 =  forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text'}), label='Re-type Password')

    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password1']:
            raise forms.ValidationError('passwords do not match!')
        return self.cleaned_data['password2']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input_text', 'placeholder':'Your Email'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text', 'placeholder':'Password'}), label='Password')

    def clean_password(self):
        try:
            email = self.cleaned_data['email']
        except:
            raise forms.ValidationError('Invalid username password combo!')
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(email=email)
        except:
            raise forms.ValidationError('Invalid username password combo!')
        user = authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid username password combo!')
        return self.cleaned_data['password']
