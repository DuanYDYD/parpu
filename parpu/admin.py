from django.contrib import admin

# Register your models here.

from user.models import User, Friend, Team, Application
from forum.models import  Column, Post, PostLike, Comment, CommentLike
from contest.models import Contest

admin.site.register(Contest)
admin.site.register(User)
admin.site.register(Friend)
admin.site.register(Column)
admin.site.register(Team)
admin.site.register(Application)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)