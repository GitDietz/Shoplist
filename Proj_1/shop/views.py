from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse, redirect

from .forms import ItemForm
from .models import Item
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )
from datetime import date
import re


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
        x = re.search(find_this,i)
        if x != None:
            y = str(i)
            # print(f'this was found {y}')
            return get_object_id(y)
    return 0

def get_object_id(in_str):
    # print(f'get_object_id: {in_str}')
    x = in_str.split('|')
    return int(x[1])


@login_required
def shop_create(request):
    form = ItemForm(request.POST or None)
    title = 'Add purchase items'
    notice = ''
    if form.is_valid():
        print(f'shop_create|valid form')
        ### get the objects still to purchase and check if this new one is among them
        qs_tobuy = Item.objects.to_get()
        has_it = False
        item = form.save(commit=False)
        this_found = qs_tobuy.filter(Q(description__iexact=item.description))
        if this_found:
            print('already listed')
            has_it = True
            notice = 'Already listed ' + item.description
        else:
            print('ok will add to list')
            item.description = item.description.title()
            item.requested = request.user
            item.date_requested = date.today()
            item.save()
            notice = 'Added ' + item.description

        if 'add_one' in request.POST:
            return redirect('shop:shop_list')
        else:
            form = ItemForm()


    context = {
        'title':title,
        'form':form,
        'notice':notice,
    }
    return render(request, 'item_create.html', context)

@login_required
def shop_list(request):
    print(f'Shop|List | user = {request.user.username}')
    # 2 buttons named can/done with the obj.id
    if request.user.is_authenticated():
        queryset_list = Item.objects.to_get()

        # print(f'Query set is : {queryset_list}') essages.success(request, 'Successfully deleted')
        notice = ''
        if request.POST and request.user.is_staff:
            # print(f'this is the post dict {request.POST}')
            cancel_item = in_post(request.POST,'cancel_item')
            purchased_item = in_post(request.POST,'got_item')

            if cancel_item !=0 or purchased_item !=0:
                item_to_update = max(cancel_item, purchased_item)
                instance = get_object_or_404(Item, id=item_to_update)
                if cancel_item !=0:
                    instance.cancelled = request.user
                elif purchased_item !=0 :
                    instance.purchased = request.user
                    instance.date_purchased = date.today()
                instance.save()
            else:
                print('No objects to update')
        elif request.POST:
            notice = "You can't update the items"

        context = {
            'title': 'List of all items',
            'object_list':queryset_list,
            'notice':notice,
        }
        return render(request, 'item_list.html', context)
    else:
        raise Http404

@login_required
def shop_detail(request, id=None):
    print(f'Shop|detail|user = {request.user.username}')
    instance = get_object_or_404(Item, id=id)
    context = {
        'instance': instance,
        'description': instance.description,
    }
    return render(request, 'item_detail.html', context)
