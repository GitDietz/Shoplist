from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.functions import Lower
from django.conf import settings


# ## Model Managers ## #

class ItemManager(models.Manager):
    def all(self):
        qs = super(ItemManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        obj_id = instance.id
        qs = super(ItemManager, self).filter(object_id=obj_id)
        return qs

    def to_get(self):
        qs = super(ItemManager,self).filter(purchased=None).filter(cancelled=None).order_by(Lower('description'))
        return qs

    def to_get_by_group(self, group_id):
        qs = super(ItemManager, self).filter(purchased=None).filter(cancelled=None).filter(in_group=group_id).order_by(Lower('description'))
        return qs

    def purchased(self):
        qs = super(ItemManager, self).filter(to_purchase=False)
        return qs


class MerchantManager(models.Manager):
    def all(self):
        qs = super(MerchantManager, self).all()
        return qs


class ShopGroupManager(models.Manager):
    def all(self):
        qs = super(ShopGroupManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        obj_id = instance.id
        qs = super(ShopGroupManager, self).filter(object_id=obj_id)
        return qs

    def managed_by(self, user):
        qs = super(ShopGroupManager, self).filter(manager=user)
        return qs

    def create_group(self, name, manager):
        new_group = self.create(name=name, manager=manager)
        return new_group


# ## Models ## #


class Merchant(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    objects = MerchantManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class ShopGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='manage_by')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='member_of')
    leaders = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='leader_of')
    disabled = models.BooleanField(default=False)
    objects = ShopGroupManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class Item(models.Model):
    requested = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='req_by')
    purchased = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='buy_by')
    cancelled = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='cancel_by')
    description = models.CharField(max_length=100)
    date_requested = models.DateField(auto_now=False, auto_now_add=True)
    date_purchased = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    to_get_from = models.ForeignKey(Merchant, blank=True, null=True, on_delete=None)
    in_group = models.ForeignKey(ShopGroup, blank=True, null=True, on_delete=None)
    objects = ItemManager()

    class Meta:
        ordering = ['description']

    def __str__(self):
        this_merchant = self.to_get_from.name
        if this_merchant:
            label = self.description.title() + ' @ ' + this_merchant
        else:
            label = self.description.title()
        return str(label)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})

    @property
    def to_purchase(self):
        if self.date_purchased is None and self.cancelled is None:
            return True
        else:
            return False


