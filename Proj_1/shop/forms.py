from django import forms
from .models import Item
from pagedown.widgets import PagedownWidget

class ItemForm(forms.ModelForm):
    description = forms.CharField() # widget=PagedownWidget)
    #date_requested = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Item
        fields = [
            'description',
            #'date_requested',
            # 'purchased',
            # 'requested',
            #'date_purchased',
        ]

    def clean_description(self):
        return self.cleaned_data['description'].title()


class ItemListForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'description',
            'date_purchased',
        ]