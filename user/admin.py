from django.contrib import admin

# Register your models here.

from forum.models import Column
from user.models import User

#admin.site.register(Contest)
admin.site.register(User)
# admin.site.register(Column)
