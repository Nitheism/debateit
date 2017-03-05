from django.db import models

# Create your models here.

CHOICES = (
    ('player', 'Report player'),
    ('issue', 'Report issue'),

)


class Report(models.Model):
    message = models.CharField(max_length=200, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    type = models.CharField(choices=CHOICES, max_length=100, blank=False, null=False)
