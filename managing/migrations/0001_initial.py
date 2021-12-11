# Generated by Django 3.2 on 2021-12-04 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0001_initial'),
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
                ('fileid', models.IntegerField(blank=True, null=True)),
                ('last', models.IntegerField(blank=True, default=0, null=True)),
                ('next', models.IntegerField(blank=True, default=0, null=True)),
                ('activityid', models.ForeignKey(db_column='activityid', on_delete=django.db.models.deletion.CASCADE, related_name='chapterid', to='activity.activity')),
            ],
            options={
                'db_table': 'chapter',
                'managed': True,
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
                ('file', models.FileField(upload_to='./')),
                ('activityid', models.ForeignKey(db_column='activityid', on_delete=django.db.models.deletion.CASCADE, to='activity.activity')),
                ('chapterid', models.ForeignKey(db_column='chapterid', on_delete=django.db.models.deletion.DO_NOTHING, to='managing.chapter')),
            ],
            options={
                'db_table': 'chapterfile',
                'ordering': ['chapterid'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Chaptercomment',
            fields=[
                ('commentpk', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=100)),
                ('activityid', models.ForeignKey(db_column='activityid', on_delete=django.db.models.deletion.CASCADE, to='activity.activity')),
                ('chapterid', models.ForeignKey(db_column='chapterid', on_delete=django.db.models.deletion.DO_NOTHING, to='managing.chapter')),
            ],
            options={
                'db_table': 'chaptercomment',
                'managed': True,
            },
        ),
    ]
