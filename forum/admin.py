from django.contrib import admin

# Register your models here.
from user.models import User, Friend, Team
from forum.models import User, Column

#admin.site.register(User)
admin.site.register(Column)
admin.site.register(Friend)
