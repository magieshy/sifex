from django.db import models
from django.contrib.auth.models import AbstractUser
# from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.dispatch import receiver


class User(AbstractUser):
    wharehouse = models.BooleanField(default=False, verbose_name='wharehouse')
    acceptance = models.BooleanField(default=False, verbose_name='acceptance')
    importer = models.BooleanField(default=False, verbose_name='import')
    accountance = models.BooleanField(default=False, verbose_name='accountance')
    management = models.BooleanField(default=False, verbose_name='management')
    profile_pic = models.ImageField(upload_to="user/profile/", null=True, blank=True)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
