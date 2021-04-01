from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import signals
import datetime



class User(AbstractUser):
    '''用户表'''
    # administrater 要继承

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    area = (
        ('co','commercial contest'),
        ('sp', 'sports'),
    )

    majorchoice = (
        ('bs','business'),
        ('math','math'),
        ('ft','fintech'),
        ('cs','computer science')
    )

    nickname = models.CharField(max_length=128, blank=True, null=True)
    friends = models.ManyToManyField(
        'self', blank=True, null=True, related_name='friends')
    sex = models.CharField(max_length=32, choices=gender, default='男')
    intestedarea = models.CharField(max_length=128, choices=area, default='sports')
    major = models.CharField(max_length=128, choices=majorchoice)
    motto = models.CharField(max_length=128)
    graduationyear = models.DateField()
    c_time = models.DateTimeField(auto_now_add=True)
    #成就recording
    #对自己的评级

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def checkfriend(self, username):
        if username in self.friends.all():
            return True
        else:
            return False

class Team(models.Model):
    '''队伍'''
    resultc=(
        ('fw','first award')
        ('sw','second award')
        ('tw','third award')
        ('aw','award')
    )

    area = (
        ('co', 'commercial contest'),
        ('sp', 'sports'),
    )

    tname = models.CharField(max_length=128)
    tid = models.AutoField(primary_key=True)
    leader = models.ForeignKey('User', on_delete=models.CASCADE)
    #teamembers = models.  #队友
    teamembers = models.ManyToManyField(
        'self', blank=True, null=True, related_name='teamembers')
    tannounce = models.TextField() #验证
    tresult = models.CharField(max_length=32, choices=resultc)
    contestbelonging = models.CharField(max_length=128, choices=area, default='sports')
    teamrequirement = models.TextField()

    def __str__(self):
        return self.tname

    class Meta:
        verbose_name = '队伍'
        verbose_name_plural = '队伍'

class community(models.Model):
    '''社区'''

    area = (
        ('co', 'commercial contest'),
        ('sp', 'sports'),
    )

    commarea = models.CharField(max_length=128, choices=area, default='sports')
    topic = models.CharField(max_length=128)
    commid = models.AutoField(primary_key=True)
    #list

    def __str__(self):
        return self.name###################

    class Meta:
        verbose_name = '社区'
        verbose_name_plural = '社区'

class post(models.Model):
    '''帖子'''

    pid = models.AutoField(primary_key=True)
    content = models.TextField()
    comment = models.TextField() #要做多个
    postlikenum = models.IntegerField(default=0)
    commentlikenum = models.IntegerField(default=0)
    binfo = models.TextField()

    def __str__(self):
        return self.name#######

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'



class Post(models.Model):  #文章
    title = models.CharField(max_length=30)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='post_author')  #作者
    column = models.ForeignKey(Column)  #所属板块 #################
    type_name = models.ForeignKey(PostType)  #文章类型 ###################
    content = models.TextField()

    view_times = models.IntegerField(default=0)  #浏览次数
    responce_times = models.IntegerField(default=0)  #回复次数
    last_response = models.ForeignKey(settings.AUTH_USER_MODEL)  #最后回复者

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        ordering = ['-created_at']
        verbose_name_plural = u'主题'

    def __unicode__(self):
        return self.title

    def description(self):
        return u'%s 发表了主题《%s》' % (self.author, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {'post_pk': self.pk})

class contest(models.Model):
    '''比赛'''

    resultc = (
        ('fw', 'first award')
        ('sw', 'second award')
        ('tw', 'third award')
        ('aw', 'award')
    )

    area = (
        ('co', 'commercial contest'),
        ('sp', 'sports'),
    )

    cname = models.CharField(max_length=128)
    cid = models.AutoField(primary_key=True)
    crequirement = models.TextField()
    con_c_time = models.DateTimeField(auto_now_add=True)
    conaward = models.CharField(max_length=32, choices=resultc)
    contestcat = models.CharField(max_length=128, choices=area, default='sports')



class Comment(models.Model):  #评论
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment_parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='childcomment')
    content = models.TextField()

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

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {'post_pk': self.post.pk})