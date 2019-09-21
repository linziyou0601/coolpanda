# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Received(models.Model):
    type = models.TextField()
    message = models.TextField()
    channel_id = models.TextField()
    create_at = models.TextField()

    class Meta:
        managed = False
        db_table = 'received'
        app_label = 'chatbot'


class Reply(models.Model):
    type = models.TextField()
    message = models.TextField()
    valid = models.IntegerField(blank=True, null=True)
    channel_id = models.TextField()
    create_at = models.TextField()

    class Meta:
        managed = False
        db_table = 'reply'
        app_label = 'chatbot'


class Statements(models.Model):
    keyword = models.TextField()
    response = models.TextField()
    create_at = models.TextField()
    channel_id = models.TextField()
    channel_type = models.TextField()
    priority = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statements'
        app_label = 'chatbot'


class Users(models.Model):
    channel_id = models.TextField()
    globaltalk = models.IntegerField()
    mute = models.IntegerField()
    allowpush = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'chatbot'

class PushMessages(models.Model):
    message_type = models.TextField()
    message_title = models.TextField()
    message_content = models.TextField()
    create_at = models.TextField()

    class Meta:
        managed = False
        db_table = 'pushMessages'
        app_label = 'chatbot'
