# Generated by Django 3.2.7 on 2021-11-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapterid', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=16)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('article', models.CharField(max_length=500)),
                ('filepath', models.CharField(blank=True, max_length=32, null=True)),
                ('filesize', models.IntegerField(blank=True, null=True)),
                ('last', models.IntegerField(blank=True, default=0, null=True)),
                ('next', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'chapter',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Chaptercomment',
            fields=[
                ('commentpk', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'chaptercomment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Chapterfile',
            fields=[
                ('filepk', models.AutoField(primary_key=True, serialize=False)),
                ('filepath', models.CharField(max_length=64)),
                ('filename', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('fileext', models.CharField(max_length=5)),
                ('file', models.FileField(upload_to='./files/')),
            ],
            options={
                'db_table': 'chapterfile',
                'ordering': ['chapterid'],
                'managed': False,
            },
        ),
    ]
