from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
import datetime
from user.models import User, Friend, Team
# Create your models here.
from django.utils import timezone
from django.views.generic import ListView


class Column(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    # manager = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, related_name='column_manager',on_delete=models.CASCADE)  # 版主
    img = models.CharField(
        max_length=200, default='/static/tx/default.jpg', verbose_name=u'图标')
    post_number = models.IntegerField(default=0)  # 主题数
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'column'
        ordering = ['-post_number']
        verbose_name_plural = u'板块'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u'/column=%d/' % self.id

class Post(models.Model):  #文章
    title = models.CharField(max_length=30)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='post_author',on_delete=models.CASCADE)  #作者
    # column = models.ForeignKey(Column)  #所属板块 #################
    # type_name = models.ForeignKey(PostType)  #文章类型 ###################
    content = models.TextField()
    column = models.ForeignKey(Column,related_name='column_belong_to',on_delete=models.CASCADE,null=False)  # 所属板块
    view_times = models.IntegerField(default=0)  #浏览次数
    responce_times = models.IntegerField(default=0)  #回复次数
    like_times = models.IntegerField(default=0) #like次数
    #last_response = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)  #最后回复者

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        ordering = ['-created_at']
        verbose_name_plural = u'主题'

    def __unicode__(self):
        return self.title

    def short(self):
        return u"%s - %s\n%s" % (self.author, self.title, self.created_at.strftime("%Y-%m-%d %H:%M"))

    def get_absolute_url(self):
        return u'/column=%d/post=%d' % (self.column.id, self.id)


'''class Contest(models.Model):
    

    resultc = (
        ('fw', 'first award'),
        ('sw', 'second award'),
        ('tw', 'third award'),
        ('aw', 'award'),
    )

    area = (
        ('co', 'commercial contest'),
        ('sp', 'sports'),
    )

    cname = models.CharField(max_length=128)
    crequirement = models.TextField()
    con_c_time = models.DateTimeField(auto_now_add=True)
    conaward = models.CharField(max_length=32, choices=resultc)
    contestcat = models.CharField(max_length=128, choices=area, default='sports')
    interested_num = models.IntegerField(default=0)'''



class Comment(models.Model):  #评论
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #comment_parent = models.ForeignKey(
    #    'self', blank=True, null=True, related_name='childcomment',on_delete=models.CASCADE)
    content = models.TextField()
    like_num = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'
        ordering = ['created_at']
        verbose_name_plural = u'评论'

    def __unicode__(self):
        return self.content

    def description(self):
        return u'%s 回复了您的帖子(%s) R:《%s》' % (self.author, self.post,
                                           self.content)
