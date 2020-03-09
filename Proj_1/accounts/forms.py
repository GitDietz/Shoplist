from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.db.models import Q

from shop.models import ShopGroup

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
    email = forms.EmailField(label='Email Address', required=True) # overrides the default
    email2 = forms.EmailField(label='Confirm Email')
    first_name = forms.CharField(label='First Name (will display for others)', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    joining = forms.CharField(label='Group to create', max_length=100)
    purpose = forms.CharField(label='What is this group for?', max_length=200)

    class Meta:
        model = User
        fields = [
            # 'username',
            'email',
            'email2',
            'first_name',
            'last_name',
            'password',
            'joining',
            'purpose'
        ]
        # widgets = {'username': forms.HiddenInput()}
        # initial = {'username': 'user1'}
    #possible to use a form level clean similar to the class above - validation will then show on the form itself and not the field

    def clean_email2(self): #this is 2 so it runs off the email2 field
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        print(f'first is {email}, second is {email2}')
        if email != email2:
            raise ValidationError('Emails are not the same')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise ValidationError('Emails already exists for a user, please enter another one')

        # return super(UserRegisterForm, self).clean()
        return email2


    def clean_joining(self):
        target_group = self.cleaned_data.get('joining')
        # now check that the group does not exists and create it, rather do this in the form
        qs_shop_group = ShopGroup.objects.all()
        this_found = qs_shop_group.filter(Q(name__iexact=target_group))
        if this_found.exists():
            raise ValidationError('That group already exists, please enter another name')

        # return super(UserRegisterForm, self).clean()
        return target_group


    # def clean_username(self):
    #     uname = self.cleaned_data.get('username')
    #     print('in the username clean')
    #     last_name = self.cleaned_data.get('first_name')
    #     new_username = self.cleaned_data.get('first_name') + min(last_name[:2],'')
    #     this_user = User.objects.all().filter(Q(username__iexact=new_username))
    #     i=1
    #     while this_user.exists():
    #         this_user + str(i)
    #         i+=1
    #     return new_username