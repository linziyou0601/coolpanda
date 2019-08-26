from django.db import models

# Create your models here.
class users(models.Model):
    id = models.AutoField(primary_key=True)
    channel_id = models.TextField(null=False)
    globaltalk = models.IntegerField(null=False, default=0)
    mute = models.IntegerField(null=False, default=0)
    
class statements(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.TextField(null=False)
    response = models.TextField(null=False)
    create_at = models.TextField(null=False)
    channel_id = models.TextField(null=False)
    channel_type = models.TextField(null=False)
    mute = models.IntegerField(null=False, default=5)

class received(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(null=False)
    channel_id = models.TextField(null=False)
    create_at = models.TextField(null=False)

class reply(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(null=False)
    valid = models.IntegerField(default=0)
    channel_id = models.TextField(null=False)
    create_at = models.TextField(null=False)