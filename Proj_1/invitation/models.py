import os
import random
import datetime
import re
import uuid

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.http import int_to_base36
# from django.utils.hashcompat import sha_constructor
from hashlib import sha1 as sha_constructor
from django.utils.translation import ugettext_lazy as _

# from shop.models import ShopGroup


class InvitationKeyManager(models.Manager):
    def get_key(self, invitation_key):
        """
        Return InvitationKey, or None if it doesn't (or shouldn't) exist.
        """
        # Don't bother hitting database if invitation_key doesn't match pattern.
        # [0-9a-f]{40}
        if not re.search(r'[0-9a-f]{40}', invitation_key):
            return None
        try:
            key = self.get(key=invitation_key)
        except self.model.DoesNotExist:
            return None
        return key

    def is_key_valid(self, invitation_key):
        """
        Check if an ``InvitationKey`` is valid or not, returning a boolean,
        ``True`` if the key is valid.
        """
        invitation_key = self.get_key(invitation_key)
        return invitation_key and invitation_key.is_usable()

    def key_for_email(self,email):
        keys = InvitationKey.objects.filter(invited_email=email).filter(invite_used=False)
        if keys.exists():
            return True
        else:
            return False

    def delete_expired_keys(self):
        for key in self.all():
            if key.key_expired():
                key.delete()


class InvitationKey(models.Model):
    key = models.CharField(_('invitation key'), max_length=40)
    date_invited = models.DateField(_('date invited'), default=datetime.date.today)
    from_user = models.ForeignKey(User, related_name='invitations_sent', on_delete=models.CASCADE)
    registrant = models.ForeignKey(User, null=True, blank=True, related_name='invitations_used', on_delete=models.CASCADE)
    invite_to_group = models.ForeignKey('shop.ShopGroup', on_delete=models.CASCADE)
    invited_email = models.EmailField(null=False, blank=False)
    invite_used = models.BooleanField(null=False, default=False)
    objects = InvitationKeyManager()

    class Meta:
        app_label = 'invitation'

    def __unicode__(self):
        return u"Invitation from %s on %s" % (self.from_user.username, self.date_invited)

    def is_usable(self):
        """
        Return whether this key is still valid for registering a new user.
        """
        return self.registrant is None and not self.key_expired()

    def key_expired(self):
        """
        Determine whether this ``InvitationKey`` has expired, returning
        a boolean -- ``True`` if the key has expired.

        The date the key has been created is incremented by the number of days
        specified in the setting ``ACCOUNT_INVITATION_DAYS`` (which should be
        the number of days after invite during which a user is allowed to
        create their account); if the result is less than or equal to the
        current date, the key has expired and this method returns ``True``.

        """
        expiration_date = self.date_invited + datetime.timedelta(days=settings.ACCOUNT_INVITATION_DAYS)
        if expiration_date > datetime.date.today():
            return False
        else:
            return True
            # self.date_invited + expiration_date <= datetime.datetime.now()

    key_expired.boolean = True

    def mark_used(self, registrant):
        """
        Note that this key has been used to register a new user.
        """
        self.registrant = registrant
        self.invite_used = True
        self.save()



# models.signals.post_save.connect(user_post_save, sender=User)

#
# def invitation_key_post_save(sender, instance, created, **kwargs):
#     """Decrement invitations_remaining when InvitationKey is created."""
#     if created:
#         invitation_user = InvitationUser.objects.get(inviter=instance.from_user)
#         remaining = invitation_user.invitations_remaining
#         invitation_user.invitations_remaining = remaining - 1
#         invitation_user.save()
#
#
# models.signals.post_save.connect(invitation_key_post_save, sender=InvitationKey)

