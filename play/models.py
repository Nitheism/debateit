from django.db import models


# This is the model for waiting users
class OnlineUsers(models.Model):
    username = models.CharField(max_length=150, blank=False, null=False)
    reply_channel_name = models.CharField(max_length=255, blank=False, null=False)


# This is the model for currently existing rooms
class PairUsers(models.Model):
    username_a = models.CharField(max_length=150, blank=False, null=False)
    username_b = models.CharField(max_length=150, blank=False, null=False)
    reply_channel_a = models.CharField(max_length=255, blank=False, null=False)
    reply_channel_b = models.CharField(max_length=255, blank=False, null=False)
    score_a = models.FloatField(blank=True, null=True, default=0)
    score_b = models.FloatField(blank=True, null=True, default=0)
    args_count_a = models.IntegerField(blank=True, null=True, default=0)
    args_count_b = models.IntegerField(blank=True, null=True, default=0)


# This is a model for all themes it is editable in the admin panel
class ThemesForDebate(models.Model):
    theme = models.CharField(max_length=150, blank=False, null=False)
