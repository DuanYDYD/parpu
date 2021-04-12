from django.db import models
from django.utils import timezone

class Contest(models.Model):
    '''竞赛类'''
    # administrater 要继承
    area = (
        ('B', 'business contest'),
        ('T', 'technology contest'),
        ('S', 'sports'),
        ('D', 'debate competition'),
    )

    con_id = models.IntegerField(primary_key=True)
    contest_name = models.CharField(max_length= 80)
    area = models.CharField(max_length=80, choices=area, default='B')
    regi_ddl = models.DateField(default=timezone.now)
    startdate = models.DateField(default=timezone.now)
    enddate = models.DateField(default=timezone.now) #注册截止日期，开始日期，结束日期
    holder = models.CharField(max_length=80) #主办方

    upload = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)

# Create your models here.
