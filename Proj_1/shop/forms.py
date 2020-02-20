from django import forms
from django.utils.safestring import mark_safe
from .models import Item, Merchant,ShopGroup
from pagedown.widgets import PagedownWidget

#
# class SpanWidget(forms.Widget):
#     """
#     Renders a value wrapped in a <span> tag.
#     Requires use of specific form support. (see ReadonlyForm
#     or ReadonlyModelForm)
#     """
#
#     def render(self, name, value, attrs=None):
#         final_attrs = self.build_attrs(attrs, name=name)
#         return mark_safe(u'<span%s >%s</span>' % (
#             forms.util.flatatt(final_attrs), self.original_value))
#
#     def value_from_datadict(self, data, files, name):
#         return self.original_value
#
#
# class SpanField(forms.Field):
#     '''A field which renders a value wrapped in a <span> tag.
#
#     Requires use of specific form support. (see ReadonlyForm
#     or ReadonlyModelForm)
#     '''
#
#     def __init__(self, *args, **kwargs):
#         kwargs['widget'] = kwargs.get('widget', SpanWidget)
#         super(SpanField, self).__init__(*args, **kwargs)
#
#
# class Readonly(object):
#     """Base class for ReadonlyForm and ReadonlyModelForm which provides
#     the meat of the features described in the docstings for those classes.
#     """
#     class NewMeta:
#         readonly = tuple()
#
#     def __init__(self, *args, **kwargs):
#         super(Readonly, self).__init__(*args, **kwargs)
#         readonly = self.NewMeta.readonly
#         if not readonly:
#             return
#         for name, field in self.fields.items():
#             if name in readonly:
#                 field.widget = SpanWidget()
#             elif not isinstance(field, SpanField):
#                 continue
#             field.widget.original_value = str(getattr(self.instance, name))
#

class ItemForm(forms.ModelForm):
    description = forms.CharField()  # widget=PagedownWidget)
    #  vendor_select = forms.ModelChoiceField(queryset=Merchant.objects.all()) - this type should work for other lookup operations
    #  date_requested = forms.DateField(widget=forms.SelectDateWidget)
    #  used 2 methods either the model choice field above or adding the actual model field to the list below

    class Meta:
        model = Item
        fields = [
            'description',
            'quantity',
            # 'vendor_select',
            'to_get_from',
            # 'date_requested',
            # 'purchased',
            # 'requested', not going to change requested
            # 'date_purchased'
        ]

    def __init__(self, *args, **kwargs):
        """ this limits the selection options to only the active list for the user"""
        list = kwargs.pop('list')
        active_list = Merchant.objects.filter(for_group_id=list)

        # super(ItemForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.fields['to_get_from'].queryset = active_list
        # not used part of the readonly
        # self.fields['requested'].widget.attrs['readonly'] = True

    def clean_description(self):
        return self.cleaned_data['description'].title()

    def clean_to_get_from(self):
        return self.cleaned_data['to_get_from']

    def clean_quantity(self):
        return self.cleaned_data['quantity']

    # below is a method to effectively ignore any changes to the field making it read only,
    # the form still responds to changes, so there may be an inactive setting to add
    # def clean_requested(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         return instance.requested
    #     else:
    #         return self.cleaned_data['requested']


class UsersGroupsForm(forms.ModelForm):
    groups_for_user = forms.ModelChoiceField(queryset=ShopGroup.objects.all())

    class Meta:
        model = ShopGroup
        fields = ['groups_for_user']


class ItemListForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'date_purchased']


class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['name', 'for_group']

    def __init__(self, *args, **kwargs):
        """ this limits the selection options to only the active list for the user"""
        list = kwargs.pop('list')
        initial_value = kwargs.pop('default')
        active_list = ShopGroup.objects.filter(id=list)

        super(MerchantForm, self).__init__(*args, **kwargs)

        self.fields['for_group'].queryset = active_list
        self.fields['for_group'].initial = initial_value
        # self.fields['for_group'].disabled = True
        # this method works but the side effect is no value being returned for the field
        # attempts to make the clean function replace the value
        # self.fields['for_group'].required = False
    #     # self.fields['for_group'] = forms.ChoiceField(
    #     #     required=True,
    #     #     choices=active_list,
    #     #     initial=initial_value,
    #     # )
    #
    # def clean_name(self):
    #     return self.cleaned_data['name'].title()
    #
    # def clean_for_group(self):
    #     if self.cleaned_data['for_group'] == "":
    #         self.cleaned_data['for_group'] = self.fields['for_group'].initial
    #     return self.cleaned_data['for_group']


class MerchantForm_RA(forms.ModelForm):
    # the original form
    class Meta:
        model = Merchant
        fields = ['name']


class ShopGroupForm(forms.ModelForm):
    class Meta:
        model = ShopGroup
        fields = ['name', 'manager', 'members', 'leaders']

    def clean_leaders(self):
        l_leaders = self.cleaned_data['leaders']
        print(l_leaders)
        l_members = self.cleaned_data['members']
        print(l_members)
        if all(elem in l_members for elem in l_leaders):
            return self.cleaned_data['leaders']
        else:
            raise forms.ValidationError('Only listed members can be leaders')

