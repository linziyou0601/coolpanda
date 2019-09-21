from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import PushMessages

# Register your models here.

# import-export resource book model
class PushMessagesResource(resources.ModelResource):
    class Meta:
        model = PushMessages

# ImportExportModelAdmin
class PushMessagesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'message_type', 'message_title', 'message_content', 'create_at')
    list_filter = ('message_type', 'message_title',)
    search_fields = ['message_type', 'message_title']

admin.site.register(PushMessages, PushMessagesAdmin)