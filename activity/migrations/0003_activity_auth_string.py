# Generated by Django 3.2 on 2022-01-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_alter_activity_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='auth_string',
            field=models.CharField(db_column='auth_string', default='pbkdf2_sha256$260000$j9olt89iQqM4IUMLv2KslY$ULBaVPAH6MjZlKFvhDJ4YpqBUtNI7ItL5Ui2FDL0u+Y=', max_length=128),
        ),
    ]
