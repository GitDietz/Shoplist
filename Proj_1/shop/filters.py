from django import forms
from django.contrib.auth.models import User
import django_filters
from .models import ShopGroup

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    member_of = django_filters.ModelMultipleChoiceFilter(queryset=ShopGroup.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]

def groups_for_user(request):
    print('in groups for user')
    if request is None:
        print(f'No request, user = {User}')

        return ShopGroup.objects.filter(members = 5)  # ShopGroup.objects.all()
    print(f'filter is {ShopGroup.objects.filter(members = request.user)}')
    return ShopGroup.objects.filter(members = request.user)

class GroupFilter(django_filters.FilterSet):
    # qs = ShopGroup.objects.all()
    #in_group = django_filters.ModelMultipleChoiceFilter(queryset=ShopGroup.objects.all(), widget=forms.CheckboxSelectMultiple)
    in_group = django_filters.ModelMultipleChoiceFilter(queryset=groups_for_user,
                                                        widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = ShopGroup
        fields = [ ]

