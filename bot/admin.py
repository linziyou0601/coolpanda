from django.contrib import admin
from .models import Users, Statements, Received, Reply

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_id', 'globaltalk', 'mute')
    list_filter = ('globaltalk', 'mute',)
    search_fields = ['channel_id', 'globaltalk', 'mute']
class StatementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', 'response', 'create_at', 'channel_id', 'channel_type', 'priority')
    list_filter = ('keyword', 'response', 'create_at', 'channel_id', 'channel_type', 'priority',)
    search_fields = ['keyword', 'response', 'create_at', 'channel_id', 'channel_type', 'priority']
class ReceivedAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'channel_id', 'create_at')
    list_filter = ('message', 'channel_id', 'create_at',)
    search_fields = ['message', 'channel_id', 'create_at']
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'valid', 'channel_id', 'create_at')
    list_filter = ('message', 'valid', 'channel_id', 'create_at',)
    search_fields = ['message', 'valid', 'channel_id', 'create_at']

admin.site.register(Users, UsersAdmin)
admin.site.register(Statements, StatementsAdmin)
admin.site.register(Received, ReceivedAdmin)
admin.site.register(Reply)