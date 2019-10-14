from django.contrib import admin

from .models import Item, Merchant

class ItemModelAdmin(admin.ModelAdmin):
    list_display = ['description', 'requested','date_requested','purchased','date_purchased']
    class Meta:
        model = Item

admin.site.register(Item,ItemModelAdmin)

class MerchantModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_added']
    class Meta:
        model = Merchant


admin.site.register(Merchant,MerchantModelAdmin)