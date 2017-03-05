from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


# Create your models here.

class UserModel(AbstractUser):
    score = models.IntegerField(blank=True, null=True, default=0)
    # this rank will be used later on
    rank = models.IntegerField(blank=True, null=True, default=0)
    description = models.CharField(max_length=300, null=True, blank=True)
    country = CountryField(max_length=30, blank=True)
    avatar = models.ImageField(blank=True, null=True)

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return '/static/img/defaultAvatar.jpg'
