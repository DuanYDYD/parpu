from django import forms
from django.conf import settings
from captcha.fields import CaptchaField
from captcha.fields import CaptchaTextInput
from forum.models import Post #,Message,
from user.models import User, Friend, Team, Application


class UserForm(forms.ModelForm):
    #错误信息
    error_messages = {
        'duplicate_username': "Existing user!.",
        'password_mismatch': "You need to enter two identical passwords.",
        'duplicate_email': 'existing email.'
    }

    username = forms.RegexField(
        max_length=40,
        regex=r'^[\w.@+-]+$',
        #错误信息 invalid 表示username不合法的错误信息, required 表示没填的错误信息
        error_messages={
            'invalid': "Can only content digits, letters and the characters including @/./+/-/_",
            'required': "Username is need"
        },
        widget=forms.TextInput(attrs={'class': 'input--style'}))
    email = forms.EmailField(error_messages={
        'invalid': "wrong email format",
        'required': 'email is needed'
    })

    motto = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input--style'})
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'input--style'})
    )

    graduationtime = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'input--style'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input--style'}), error_messages={'required': "password is needed"})
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input--style'}), error_messages={'required': "confirmed password is needed"})

    captcha = CaptchaField(
        widget=CaptchaTextInput(attrs={'class': 'input--style'}),
        error_messages={'invalid': 'wrong validation code'})

    class Meta:
        model = User
        fields = ("username", "email","sex","major",'graduationtime','motto')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages["duplicate_username"])

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"])
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data["email"]

        #判断是这个email 用户是否存在
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ForgetForm(forms.Form):
    email = forms.EmailField()
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

class TeamForm(forms.ModelForm):
    captcha = CaptchaField(error_messages={'invalid': 'wrong validation code'})
    class Meta:
        model = Team
        fields = ('name', 'capacity','announce','requirement')

class ApplicationForm(forms.ModelForm):
    captcha = CaptchaField(error_messages={'invalid': 'wrong validation code'})
    class Meta:
        model = Application
        fields = ('content',)