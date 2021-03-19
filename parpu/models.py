from django.db import models


class User(models.Model):
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

    name = models.CharField(max_length=128)
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    intestedarea = models.CharField(max_length=128, choices=area, default='sports')
    major = models.CharField(max_length=128, choices=majorchoice)
    motto = models.CharField(max_length=128)
    graduationyear = models.DateField()
    c_time = models.DateTimeField(auto_now_add=True)
    #成就recording
    #对自己的评级

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

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
    tannounce = models.TextField() #验证
    tresult = models.CharField(max_length=32, choices=resultc)
    contestbelonging = models.CharField(max_length=128, choices=area, default='sports')
    teamrequirement = models.TextField()

    def __str__(self):
        return self.name

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
        return self.name

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
        return self.name

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'

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