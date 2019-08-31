from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Users, Statements, Received, Reply

# Register your models here.
class UsersAdmin(ImportExportModelAdmin):
    list_display = ('id', 'channel_id', 'globaltalk', 'mute')
    list_filter = ('globaltalk', 'mute',)
    search_fields = ['channel_id', 'globaltalk', 'mute']
class StatementsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'keyword', 'response', 'create_at', 'channel_id', 'channel_type', 'priority')
    list_filter = ('keyword', 'response', 'create_at', 'channel_id', 'channel_type', 'priority',)
    search_fields = ['keyword', 'response', 'create_at', 'channel_id', 'channel_type', 'priority']
class ReceivedAdmin(ImportExportModelAdmin):
    list_display = ('id', 'type', 'message', 'channel_id', 'create_at')
    list_filter = ('type', 'message', 'channel_id', 'create_at',)
    search_fields = ['type', 'message', 'channel_id', 'create_at']
class ReplyAdmin(ImportExportModelAdmin):
    list_display = ('id', 'type', 'message', 'valid', 'channel_id', 'create_at')
    list_filter = ('type', 'message', 'valid', 'channel_id', 'create_at',)
    search_fields = ['type', 'message', 'valid', 'channel_id', 'create_at']

admin.site.register(Users, UsersAdmin)
admin.site.register(Statements, StatementsAdmin)
admin.site.register(Received, ReceivedAdmin)
admin.site.register(Reply, ReplyAdmin)