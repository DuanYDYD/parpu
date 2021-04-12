from django.contrib import admin

# Register your models here.

from forum.models import Contest, User, Column

admin.site.register(Contest)
admin.site.register(User)
# admin.site.register(Column)