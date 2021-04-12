from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
import datetime
from django.utils import timezone
from django.views.generic import ListView

#from forum.models import Contest, Column, Comment, Post
# Create your models here.


class User(AbstractUser):
    '''用户表'''
    # administrater 要继承

    gender = (
        ('male', 'male'),
        ('female', 'female'),
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
    # friends = models.ManyToManyField(
    #     'self', blank=True, null=True, related_name='friends')
    sex = models.CharField(max_length=32, choices=gender, default='male')
    intestedarea = models.CharField(max_length=128, choices=area, default='sports')
    major = models.CharField(max_length=128, choices=majorchoice)
    motto = models.CharField(max_length=128)
    graduationyear = models.DateField(default=timezone.now)
    c_time = models.DateTimeField(auto_now_add=True)
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

class Team(models.Model):
    '''队伍'''
    resultc=(
        ('fw','first award'),
        ('sw','second award'),
        ('tw','third award'),
        ('aw','award'),
    )

    area = (
        ('co', 'commercial contest'),
        ('sp', 'sports'),
    )

    tname = models.CharField(max_length=128)
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
