from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
import datetime
from django.utils import timezone
from django.views.generic import ListView

#from forum.models import  Column, Comment, Post#,Contest,
from contest.models import Contest
# Create your models here.


class User(AbstractUser):
    '''用户表'''
    # administrater 要继承

    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )

    area = (
        ('co', 'commercial contest'),
        ('sp', 'sports'),
    )

    majorchoice = (
        ('Business', 'Business'),
        ('Quantitative Finance & Risk Management', 'Quantitative Finance & Risk Management'),
        ('Math', 'Math'),
        ('Fintech', 'Fintech'),
        ('Computer Science', 'Computer science'),
        ('Law', 'Law'),
        ('Communication', 'Communication'),
        ('Science', 'Science'),
        ('Language', 'Language'),
    )

    nickname = models.CharField(max_length=128, blank=True, null=True)
    # friends = models.ManyToManyField(
    #     'self', blank=True, null=True, related_name='friends')
    sex = models.CharField(max_length=32, choices=gender, default='male')
    #interestedArea = models.CharField(max_length=128, choices=area, default='sports')
    major = models.CharField(max_length=128, choices=majorchoice)
    motto = models.CharField(max_length=128)
    graduationtime = models.DateField(default=timezone.now)
    interestedContest = models.ManyToManyField('contest.Contest',blank=True, related_name='interestedContest')
    c_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', null=True)
    #成就recording
    #对自己的评级

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    # def checkfriend(self, username):
    #     if username in self.friends.all():
    #         return True
    #     else:
    #         return False

class Friend(models.Model):
    '''friend'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user')
    to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='to')



# class Notice(models.Model):
#     sender = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name='notice_sender',on_delete=models.CASCADE)  # 发送者
#     receiver = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name='notice_receiver',on_delete=models.CASCADE)  # 接收者
#     #event = generic.GenericForeignKey('content_type', 'object_id')
#
#     # status = models.BooleanField(default=False)  # 是否阅读
#     type = models.IntegerField()  # 通知类型 0:评论 1:好友消息 2:好友申请
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'notice'
#         ordering = ['-created_at']
#         verbose_name_plural = u'通知'
#
#     def __unicode__(self):
#         return u"%s的事件: %s" % (self.sender, self.description())

    # def description(self):
    #     if self.event:
    #         return self.event.description()
    #     return "No Event"

class Team(models.Model):
    '''队伍'''

    name = models.CharField(max_length=128)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=1)
    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='team_members')
    announce = models.TextField()  # 验证
    # tresult = models.CharField(max_length=32, choices=resultc)
    contest = models.ForeignKey('contest.Contest',null=True,on_delete=models.CASCADE)
    requirement = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '队伍'
        verbose_name_plural = '队伍'

    # def get_members(self):
    #     return self.team_members

class Application(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()