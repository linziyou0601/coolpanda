from django.contrib import admin
from .models import Users, Statements, Received, Reply

# Register your models here.
admin.site.register(Users)
admin.site.register(Statements)
admin.site.register(Received)
admin.site.register(Reply)
