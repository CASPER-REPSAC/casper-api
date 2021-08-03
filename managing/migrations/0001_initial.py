# Generated by Django 3.2.5 on 2021-08-01 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activityname', models.CharField(db_column='activityName', max_length=16)),
                ('activitytype', models.IntegerField(db_column='activityType')),
                ('activityid', models.CharField(db_column='activityID', max_length=8, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'activity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapterid', models.CharField(db_column='chapterID', max_length=8, primary_key=True, serialize=False)),
                ('chaptercreated', models.DateTimeField(db_column='chapterCreated')),
            ],
            options={
                'db_table': 'chapter',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Chapterarticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityid', models.CharField(db_column='activityID', max_length=8)),
                ('article', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'chapterArticle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Chaptercomment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityid', models.CharField(db_column='activityID', max_length=8)),
                ('commentcreated', models.DateTimeField(db_column='commentCreated')),
                ('comment', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'chapterComment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Chapterfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityid', models.CharField(db_column='activityID', max_length=8)),
                ('filepath', models.CharField(db_column='filePath', max_length=16)),
                ('filename', models.CharField(db_column='fileName', max_length=8)),
            ],
            options={
                'db_table': 'chapterFile',
                'managed': False,
            },
        ),
    ]