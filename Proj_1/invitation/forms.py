from django import forms
from django.contrib.auth import get_user_model
from .models import InvitationKey
from Proj_1.shop.models import ShopGroup


class InvitationKeyForm(forms.ModelForm):
    email = forms.EmailField()
    invite_name = forms.CharField(label="Your friend's name", required=True)
    # invite_to_group = forms.ModelChoiceField(queryset=ShopGroup.objects.all()) # managed_by(request.user))

    class Meta:
        model = InvitationKey
        fields = [
            'email',
            'invite_name',
            'invite_to_group',
        ]

    def __init__(self, user, *args, **kwargs):
        """ this limits the selection options to only the lists managed by the user"""
        super(InvitationKeyForm, self).__init__(*args, **kwargs)
        managed_groups = ShopGroup.objects.managed_by(user)
        self.fields['invite_to_group'].queryset = managed_groups
        # self.fields['invite_to_group'].initial = 'FIRST_OPTION' no solution for this yet

    def clean_email(self):
        return self.cleaned_data['email']

    def clean_invite_to_group(self):
        return self.cleaned_data['invite_to_group']

    def clean_invite_name(self):
        return self.cleaned_data['invite_name']


class InvitationSelectForm(forms.ModelForm):
    # invite_choices = [('1', 'Accept'), ('2', 'Decline')]
    # choice = forms.ChoiceField(widget=forms.RadioSelect, choices=invite_choices)

    class Meta:
        model = InvitationKey
        fields = ['invite_to_group']

    # def __init__(self, user, *args, **kwargs):
    #     """ this limits the selection options to only the lists managed by the user"""
    #     super(InvitationSelectForm, self).__init__(*args, **kwargs)
    #     open_invites = InvitationKey.objects.filter(invite_used=False).filter(invited_email=user.email)
    #     self.fields['invite_to_group'].queryset = open_invites


# class InvitationAcceptForm(forms.ModelForm):
#     first_name = forms.CharField(label='Your first Name - other members will see this', required=True)
#     last_name = forms.CharField(label='Your last Name', required=True)
#     password = forms.PasswordInput()
#
#     class Meta:
#         model = InvitationKey
#         fields = ['first_name',
#                   'last_name,'
#                   'password']



