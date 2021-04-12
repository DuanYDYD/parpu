# Generated by Django 3.1.7 on 2021-04-12 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('con_id', models.IntegerField(primary_key=True, serialize=False)),
                ('contest_name', models.CharField(max_length=80)),
                ('regi_ddl', models.DateField()),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('holder', models.CharField(max_length=80)),
                ('upload', models.FileField(upload_to='uploads/%Y/%m/%d/')),
            ],
        ),
    ]