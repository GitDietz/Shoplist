from django.contrib import admin

from .models import Item

class ItemModelAdmin(admin.ModelAdmin):
    list_display = ['description', 'requested','date_requested','purchased','date_purchased']
    class Meta:
        model = Item

admin.site.register(Item,ItemModelAdmin)

