# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    activityname = models.CharField(db_column='activityName', max_length=16)  # Field name made lowercase.
    activitytype = models.IntegerField(db_column='activityType')  # Field name made lowercase.
    activityid = models.CharField(db_column='activityID', primary_key=True, max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'activity'


class Chapter(models.Model):
    activityid = models.ForeignKey(Activity, models.DO_NOTHING, db_column='activityID')  # Field name made lowercase.
    chapterid = models.CharField(db_column='chapterID', primary_key=True, max_length=8)  # Field name made lowercase.
    chaptercreated = models.DateTimeField(db_column='chapterCreated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chapter'


class Chapterarticle(models.Model):
    activityid = models.CharField(db_column='activityID', max_length=8)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='chapterID')  # Field name made lowercase.
    article = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'chapterArticle'


class Chaptercomment(models.Model):
    activityid = models.CharField(db_column='activityID', max_length=8)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='chapterID')  # Field name made lowercase.
    commentcreated = models.DateTimeField(db_column='commentCreated')  # Field name made lowercase.
    comment = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chapterComment'


class Chapterfile(models.Model):
    activityid = models.CharField(db_column='activityID', max_length=8)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='chapterID')  # Field name made lowercase.
    filepath = models.CharField(db_column='filePath', max_length=16)  # Field name made lowercase.
    filename = models.CharField(db_column='fileName', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chapterFile'
