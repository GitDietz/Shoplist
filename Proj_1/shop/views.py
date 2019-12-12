from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse, redirect
from django.core.urlresolvers import reverse

from .forms import ItemForm, MerchantForm, ShopGroupForm,UsersGroupsForm
from .models import Item, Merchant, ShopGroup
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )
from .filters import UserFilter,GroupFilter

from datetime import date
import re

#  #################################  General Functions #############

def in_post(req_post, find_this):
    '''
    Determines if the post contains one of the required elements to take action on
    :param req_post: request
    :param find_this: string part to look for
    :return: 0 if nothing found or int for the id contained in the post key
    '''
    # print('in_post: running through the post') # the keys
    # print(f'searching for : {find_this}')
    for i in req_post:
        # print(f'dict item is: {i}')
        x = re.search(find_this, i)
        if x is not None:
            y = str(i)
            # print(f'this was found {y}')
            return get_object_id(y)
    return 0


def get_object_id(in_str):
    # print(f'get_object_id: {in_str}')
    x = in_str.split('|')
    return int(x[1])


def get_session_list_choice(request):
    try:
        print('In get_session_list_choice|try')
        list_active = request.session['list']
        if list_active != '':
            return list_active
        else:
            return None
    except KeyError:
        print('In get_session_list_choice|except')
        return None


def get_user_list_property(request):
    list_choices = ShopGroup.objects.filter(members=request.user)
    list_active_no = get_session_list_choice(request)
    active_list_name = ShopGroup.objects.filter(id=list_active_no).first()
    user_list_options = list_choices.count()
    print(f'active list is {active_list_name}')
    return list_choices, user_list_options, list_active_no, active_list_name

# class FilteredListView(ListView):
#     filterset_class = None
#
#     def get_queryset(self):
#         # Get the queryset however you usually would.  For example:
#         queryset = super().get_queryset()
#         # Then use the query parameters and the queryset to
#         # instantiate a filterset and save it as an attribute
#         # on the view instance for later.
#         self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
#         # Return the filtered queryset
#         return self.filterset.qs.distinct()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Pass the filterset to the template - it provides the form.
#         context['filterset'] = self.filterset
#         return context


# class ItemListView(FilteredListView):
#     filterset_class = ItemFilterSet


#  #################################  ITEM / AKA Shop #############
@login_required
def shop_create(request):
    print(f'Shop|Create | user = {request.user.username}')
    form = ItemForm(request.POST or None)
    list_choices, user_list_options, list_active_no, active_list_name = get_user_list_property(request)
    title = 'Add purchase items'
    notice = ''
    if form.is_valid():
        print(f'shop_create|valid form')
        # get the objects still to purchase and check if this new one is among them
        qs_tobuy = Item.objects.to_get()
        item = form.save(commit=False)
        this_found = qs_tobuy.filter(Q(description__iexact=item.description))
        for_group = ShopGroup.objects.filter(id=list_active_no).first()
        if this_found:
            print('already listed')
            notice = 'Already listed ' + item.description
        else:
            print('ok will add to list')
            item.in_group = for_group
            item.description = item.description.title()
            item.requested = request.user
            # vendor_id=request.POST.get('vendor_select') #this returns the relevant ID i selected
            vendor_id = item.to_get_from
            # this_merchant = Merchant.objects.get(pk=vendor_id)
            print(f'Vendor = {vendor_id}')
            item.to_get_from = vendor_id  # this_merchant
            item.date_requested = date.today()
            item.save()
            notice = 'Added ' + item.description

        if 'add_one' in request.POST:
            return redirect('shop:shop_list')
        else:
            form = ItemForm()

    context = {
        'title': title,
        'form': form,
        'notice': notice,
        'selected_list': active_list_name,
        'no_of_lists': user_list_options,
    }
    return render(request, 'item_create.html', context)


@login_required
def shop_list(request):
    print(f'Shop| List | user = {request.user.username}')

    list_choices = ShopGroup.objects.filter(members=request.user)
    list_active_no = get_session_list_choice(request)
    if list_active_no is None:
        redirect('shop:group_select')
    active_list_name = ShopGroup.objects.filter(id=list_active_no).first()
    user_list_options = list_choices.count()
    print(f'active list is {active_list_name}')
    # print(f'list of groups {list_choices}')
    # 2 buttons named can/done with the obj.id
    if request.user.is_authenticated():
        queryset_list = Item.objects.to_get_by_group(list_active_no)
        notice = ''
        if request.POST and request.user.is_staff:
            print(f'this is the post dict {request.POST}')
            cancel_item = in_post(request.POST, 'cancel_item')
            purchased_item = in_post(request.POST, 'got_item')

            if cancel_item != 0 or purchased_item != 0:
                item_to_update = max(cancel_item, purchased_item)
                instance = get_object_or_404(Item, id=item_to_update)
                if cancel_item != 0:
                    print(f'to cancel item {cancel_item}')
                    instance.cancelled = request.user
                elif purchased_item != 0:
                    print(f'to mark as purchased item {purchased_item}')
                    instance.purchased = request.user
                    instance.date_purchased = date.today()
                instance.save()
            else:
                print('No objects to update')
        elif request.POST:
            notice = "You can't update the items"

        context = {
            'title': 'Your shopping list',
            'object_list': queryset_list,
            'active_list': active_list_name,
            'user_lists': user_list_options,
            'notice': notice,
            # 'group_list':list_choices,
            # 'group_form':group_form,
        }
        return render(request, 'item_list.html', context)
    else:
        raise Http404


@login_required
def shop_detail(request, pk):
    print(f'Shop|detail|user = {request.user.username}')
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.requested or request.user.is_staff:
        if request.method == "POST":
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('shop:shop_list'))

        template_name = 'item_detail.html'
        context = {
            'title': 'Update Item',
            'form': ItemForm(instance=item),
            'notice': '',
        }
        return render(request, template_name, context)
    else:
        return redirect('shop:shop_list')


def shop_detail_ra(request, pk=None):
    # really over complicated this one

    print(f'Shop|detail|user = {request.user.username}')

    instance = get_object_or_404(Item, id=pk)
    form = ItemForm(instance=instance)
    context = {
        'instance': instance,
        'description': instance.description,
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            updated_desc = form.cleaned_data['description']
            updated_from = form.cleaned_data['to_get_from']
            instance.description = updated_desc
            instance.to_get_from = updated_from
            instance.save()
            return redirect('shop:shop_list')
        else:
            print(f'Error on the form : {form.errors}')

            return render(request, 'item_detail.html', context)
    else:
        if request.user == instance.requested or request.user.is_staff:
            return render(request, 'item_detail.html', context)
        else:
            raise Http404

#  ################################# User's GROUP #############
@login_required
def user_group_select(request):
    print(f'Usr group selection |user = {request.user.username}')
    notice = ''
    list_choices = ShopGroup.objects.filter(members=request.user)
    group_form = UsersGroupsForm(data=ShopGroup.objects.filter(members=request.user))
    print(f'list of groups {list_choices}')
    template_name = 'group_select.html'

    if request.method == 'POST':
        select_item = in_post(request.POST, 'pick_item')
        if select_item != 0:
            request.session['list'] = select_item
            print(f'selected list is {select_item}')
            return redirect('shop:shop_list')
        else:
            notice = 'No list selected'

    context = {
        'title': 'Please select which group you want to view and edit',
        'form': group_form,
        'list_choices': list_choices,
        'notice': notice,
    }
    return render(request, template_name, context)

#  ################################# GROUP #############
@login_required
def group_detail(request, pk=None, shopgroup_obj=None):
    print(f'Shop|group detail|user = {request.user.username}| id = {pk}')
    if pk:
        shopgroup_obj = get_object_or_404(ShopGroup, pk=pk)

    if request.method == "POST" and request.user.is_staff:
        print('In Post section')
        form = ShopGroupForm(request.POST, instance=shopgroup_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shop:group_list'))
        else:
            print(f'Form errors: {form.errors}')
    else:
        form = ShopGroupForm(instance=shopgroup_obj)

    template_name = 'group.html'
    print('Outside Post section')
    context = {
        'title': 'Create or Update Group',
        'form': form,
        'notice': '',
    }
    return render(request, template_name, context)


@login_required
def group_list(request):
    print(f'Group|List | user = {request.user.username}')
    queryset_list = ShopGroup.objects.all()
    notice = ''
    context = {
        'title': 'Group List',
        'object_list': queryset_list,
        'notice': notice,
    }
    return render(request, 'group_list.html', context)


@login_required()
def group_delete(request, pk):
    group = get_object_or_404(ShopGroup, pk=pk)
    if request.method == 'POST' and request.user.is_staff:
        group.delete()
        return HttpResponseRedirect(reverse('shop:group_list'))

    template_name = 'group_delete.html'
    context = {
        'title': 'Delete group',
        'object': group,
        'notice': '',
    }
    return render(request, template_name, context)

# ################################# MERCHANT #############
@login_required
def merchant_list(request):
    print(f'Merchant|List | user = {request.user.username}')
    queryset_list = Merchant.objects.all()
    notice = ''
    context = {
        'title': 'Merchant List',
        'object_list': queryset_list,
        'notice': notice,
    }
    return render(request, 'merchant_list.html', context)


@login_required
def merchant_detail(request, id=None):
    print(f'Merchant|Create or Edit | user = {request.user.username}')
    instance = get_object_or_404(Merchant, id=id)
    form = MerchantForm(request.POST or None)
    title = 'Add or Edit Merchant'
    notice = ''
    if request.method == 'POST' and form.is_valid():
        print(f'merchant |valid form')

        qs = Merchant.objects.all()
        form.save(commit=False)
        this_found = qs.filter(Q(name__iexact=Merchant.name))
        if this_found:
            print('Already in list')
            notice = 'Already listed ' + Merchant.name.title()
        else:
            print(f'ok will add {Merchant.name} to list')
            Merchant.name = Merchant.title()
            Merchant.save()
            notice = 'Added ' + Merchant.name

        return redirect('shop:merchant_list')

    context = {
        'title': title,
        'form': form,
        'notice': notice,
        'instance': instance
    }
    return render(request, 'merchant.html', context)


@login_required
def merchant_create(request):
    if request.method == "POST":
        form = MerchantForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shop:merchant_list'))

    template_name = 'merchant.html'
    context = {
        'title': 'Create Merchant',
        'form': MerchantForm(),
        'notice': '',
    }
    return render(request, template_name, context)


@login_required
def merchant_update(request, pk):
    merchant = get_object_or_404(Merchant, pk=pk)
    if request.method == "POST":
        form = MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shop:merchant_list'))

    template_name = 'merchant.html'
    context = {
        'title': 'Update Merchant',
        'form': MerchantForm(instance=merchant),
        'notice': '',
    }
    return render(request, template_name, context)


@login_required
def merchant_delete(request, pk):
    merchant = get_object_or_404(Merchant, pk=pk)
    if request.method == 'POST' and request.user.is_staff:
        merchant.delete()
        return HttpResponseRedirect(reverse('shop:merchant_list'))

    template_name = 'merchant_delete.html'
    context = {
        'title': 'Delete Merchant',
        'object': merchant,
        'notice': '',
    }
    return render(request, template_name, context)

# ################################# Experimental USER #############


@login_required
def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'user_list.html', {'filter': user_filter})


@login_required
def simple_item_list(request):
    item_list = Item.objects.to_get()
    group_filter = GroupFilter(request.GET,queryset=item_list)
    return render(request, 'filter_list.html', {'filter': group_filter})