from django import forms
from .models import Item, Merchant,ShopGroup
from pagedown.widgets import PagedownWidget


class ItemForm(forms.ModelForm):
    description = forms.CharField()  # widget=PagedownWidget)
    #  vendor_select = forms.ModelChoiceField(queryset=Merchant.objects.all()) - this type should work for other lookup operations
    #  date_requested = forms.DateField(widget=forms.SelectDateWidget)
    #  used 2 methods either the model choice field above or adding the actual model field to the list below

    class Meta:
        model = Item
        fields = [
            'description',
            # 'vendor_select',
            'to_get_from',
            # 'date_requested',
            # 'purchased',
            # 'requested',
            # 'date_purchased'
        ]

    def clean_description(self):
        return self.cleaned_data['description'].title()

    # def clean_vendor_select(self):
    #     return self.cleaned_data['vendor_select']

    def clean_to_get_from(self):
        return self.cleaned_data['to_get_from']


class ItemListForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'description',
            'date_purchased',
        ]


class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['name']


class ShopGroupForm(forms.ModelForm):
    class Meta:
        model = ShopGroup
        fields = ['name', 'manager','members']