from django.db import models


class User(models.Model):
    '''用户表'''

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
    intestedarea = models.CharField(max_length=128, choices=area, default='shangsai')
    major = models.CharField(max_length=128, choices=majorchoice)
    motto = models.CharField(max_length=128)
    graduationyear = models.DateField()
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Team(models.Model):
    '''队伍'''


    tname = models.CharField(max_length=128)
    tid = models.AutoField(primary_key=True)
    leader = models.ForeignKey('User', on_delete=models.CASCADE)
    teaMem =