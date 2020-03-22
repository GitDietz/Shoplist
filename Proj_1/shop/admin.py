from django.contrib import admin

from .models import Item, Merchant, ShopGroup


class ItemModelAdmin(admin.ModelAdmin):
    list_display = ['description', 'requested', 'date_requested', 'purchased', 'date_purchased', 'in_group', 'to_get_from']

    class Meta:
        model = Item


admin.site.register(Item, ItemModelAdmin)


class MerchantModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'for_group', 'date_added']

    class Meta:
        model = Merchant


admin.site.register(Merchant, MerchantModelAdmin)


class ShopGroupModelAdmin(admin.ModelAdmin):
    list_display = ['name']

    class Meta:
        model = ShopGroup


admin.site.register(ShopGroup, ShopGroupModelAdmin)
