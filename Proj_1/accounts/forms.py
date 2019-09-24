from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        print(f'Attempt to login {username}')
        # possible to use
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count ==1:
        #     user = user_qs.first()
        if username and password:
            qs = User.objects.filter(username=username)
            if qs.count() == 1:
                known_user = True
            else:
                known_user = False

            if not known_user:
                print('unknown user')
                raise ValidationError("This user does not exist")
            else:
                user = authenticate(username=username, password=password)
                if not user:
                    print('passw fault')
                    raise ValidationError("The password is very incorrect")
                else:
                    print('knwon user')
                    if not user.is_active:
                        raise ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args,**kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address') # overrides the default
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
    #possible to use a form level clean similar to the class above - validation will then show on the form itself and not the field

    def clean_email2(self): #this is 2 so it runs off the email2 field
        print(self.cleaned_data)
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        print(f'first is {email}, second is {email2}')
        if email != email2:
            raise ValidationError('Emails are not the same')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise ValidationError('Emails already exists, please enter another one')

        return super(UserRegisterForm, self).clean()
