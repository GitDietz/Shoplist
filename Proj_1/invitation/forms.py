from django import forms
from django.contrib.auth import get_user_model
from .models import InvitationKey
from shop.models import ShopGroup
# from django.contrib.auth import



class InvitationKeyForm(forms.ModelForm):
    email = forms.EmailField()
    # invite_to_group = forms.ModelChoiceField(queryset=ShopGroup.objects.all()) # managed_by(request.user))

    class Meta:
        model = InvitationKey
        fields = [
            'email',
            'invite_to_group',
            # 'to_get_from',
            # 'date_requested',
            # 'purchased',
            # 'requested',
            # 'date_purchased'
        ]

    def __init__(self, user, *args, **kwargs):
        """ this limits the selection options to only the lists managed by the user"""
        super(InvitationKeyForm, self).__init__(*args, **kwargs)
        managed_groups = ShopGroup.objects.managed_by(user)
        self.fields['invite_to_group'].queryset = managed_groups

    def clean_email(self):
        return self.cleaned_data['email']

    def clean_invite_to_group(self):
        return self.cleaned_data['invite_to_group']

