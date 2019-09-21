from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Users, Statements, Received, Reply, PushMessages

# Register your models here.

# import-export resource book model
class UsersResource(resources.ModelResource):
    class Meta:
        model = Users
class StatementsResource(resources.ModelResource):
    class Meta:
        model = Statements
class ReceivedResource(resources.ModelResource):
    class Meta:
        model = Received
class ReplyResource(resources.ModelResource):
    class Meta:
        model = Reply
class PushMessagesResource(resources.ModelResource):
    class Meta:
        model = PushMessages

# ImportExportModelAdmin
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
class PushMessagesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'message_type', 'message_title', 'message_content', 'create_at')
    list_filter = ('message_type', 'message_title',)
    search_fields = ['message_type', 'message_title']

admin.site.register(Users, UsersAdmin)
admin.site.register(Statements, StatementsAdmin)
admin.site.register(Received, ReceivedAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(PushMessages, PushMessagesAdmin)