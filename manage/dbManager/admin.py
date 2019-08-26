from django.contrib import admin
from .models import users, statements, received, reply

# Register your models here.
admin.site.register(users)
admin.site.register(statements)
admin.site.register(received)
admin.site.register(reply)