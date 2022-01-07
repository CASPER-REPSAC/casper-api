# Generated by Django 3.2 on 2022-01-07 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('extra_data', models.TextField()),
            ],
            options={
                'db_table': 'socialaccount_socialaccount',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
